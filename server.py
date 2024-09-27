import asyncio
import json
import logging
import time
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID
from aioquic.asyncio import QuicConnectionProtocol, serve
from aioquic.h3.connection import H3_ALPN, H3Connection
from aioquic.h3.events import HeadersReceived, DatagramReceived
from aioquic.h3.exceptions import NoAvailablePushIDError
from aioquic.quic.configuration import QuicConfiguration
from aioquic.quic.events import DatagramFrameReceived, ProtocolNegotiated
from aiortc import RTCPeerConnection, RTCSessionDescription
from aiortc.contrib.media import MediaRecorder
from datetime import datetime, timedelta

# WebRTC Handling
pcs = set()

async def handle_webrtc_offer(offer_sdp: str):
    offer = RTCSessionDescription(sdp=offer_sdp, type="offer")
    pc = RTCPeerConnection()

    pcs.add(pc)

    # Handle incoming tracks
    @pc.on("track")
    async def on_track(track):
        print(f"Track {track.kind} received")

        # Relay media to an RTMP stream using aiortc's MediaRecorder
        recorder = MediaRecorder("rtmp://your.rtmp.url/stream")

        await recorder.addTrack(track)
        await recorder.start()

        @track.on("ended")
        async def on_ended():
            print(f"Track {track.kind} ended")
            await recorder.stop()

    await pc.setRemoteDescription(offer)
    answer = await pc.createAnswer()
    await pc.setLocalDescription(answer)

    return pc.localDescription.sdp


class WebTransportHandler:
    def __init__(self, *, connection: H3Connection, stream_id: int, transmit) -> None:
        self.connection = connection
        self.queue = asyncio.Queue()
        self.stream_id = stream_id
        self.transmit = transmit
        self.accepted = False
        self.closed = False
        self.http_event_queue = deque()

    async def handle_webtransport_connect(self):
        self.queue.put_nowait({"type": "webtransport.connect"})

    async def receive(self):
        return await self.queue.get()

    async def send(self, message: Dict):
        if message["type"] == "webtransport.accept":
            self.accepted = True
            headers = [
                (b":status", b"200"),
                (b"sec-webtransport-http3-draft", b"draft02"),
                (b"server", b"aioquic"),
                (b"date", formatdate(time.time(), usegmt=True).encode()),
            ]
            self.connection.send_headers(stream_id=self.stream_id, headers=headers)

            # Consume backlog
            while self.http_event_queue:
                event = self.http_event_queue.popleft()
                self.http_event_received(event)

        elif message["type"] == "webtransport.datagram.send":
            self.connection.send_datagram(stream_id=self.stream_id, data=message["data"])

        if message.get("end_stream"):
            self.closed = True
        self.transmit()

    def http_event_received(self, event):
        if not self.closed:
            if self.accepted:
                if isinstance(event, DatagramReceived):
                    data = event.data.decode("utf-8")
                    print(f"Received Datagram: {data}")
                    # Assume this is the WebRTC offer
                    offer_sdp = json.loads(data)["offer"]
                    asyncio.ensure_future(self.process_webrtc_offer(offer_sdp))

    async def process_webrtc_offer(self, offer_sdp: str):
        answer_sdp = await handle_webrtc_offer(offer_sdp)
        # Send WebRTC answer back to the client via datagram
        await self.send({
            "type": "webtransport.datagram.send",
            "data": json.dumps({"answer": answer_sdp}).encode("utf-8")
        })


class HttpServerProtocol(QuicConnectionProtocol):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._http = None
        self._handlers: Dict[int, WebTransportHandler] = {}

    def http_event_received(self, event):
        if isinstance(event, HeadersReceived) and event.stream_id not in self._handlers:
            self._handlers[event.stream_id] = WebTransportHandler(
                connection=self._http, stream_id=event.stream_id, transmit=self.transmit
            )
            asyncio.ensure_future(self._handlers[event.stream_id].handle_webtransport_connect())
        elif isinstance(event, DatagramReceived):
            handler = self._handlers.get(event.stream_id)
            if handler:
                handler.http_event_received(event)

    def quic_event_received(self, event):
        if isinstance(event, ProtocolNegotiated):
            if event.alpn_protocol in H3_ALPN:
                self._http = H3Connection(self._quic, enable_webtransport=True)
        elif isinstance(event, DatagramFrameReceived):
            handler = self._handlers.get(event.stream_id)
            if handler:
                handler.http_event_received(DatagramReceived(data=event.data))

        if self._http is not None:
            for http_event in self._http.handle_event(event):
                self.http_event_received(http_event)


def generate_self_signed_cert():
    # Generate RSA private key
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048, backend=default_backend())

    # Generate self-signed certificate
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, u"US"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"California"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, u"San Francisco"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"Example, Inc."),
        x509.NameAttribute(NameOID.COMMON_NAME, u"example.com"),
    ])
    cert = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(issuer)
        .public_key(private_key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(datetime.utcnow())
        .not_valid_after(datetime.utcnow() + timedelta(days=365))
        .add_extension(
            x509.SubjectAlternativeName([x509.DNSName(u"example.com")]),
            critical=False,
        )
        .sign(private_key, hashes.SHA256(), default_backend())
    )

    # Serialize certificate and private key
    cert_pem = cert.public_bytes(encoding=serialization.Encoding.PEM)
    key_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption(),
    )

    return cert_pem, key_pem


# QUIC Server Entry
async def main():
    # Generate dynamic self-signed cert and key
    cert_pem, key_pem = generate_self_signed_cert()

    # Set up QUIC configuration with the generated cert and key
    configuration = QuicConfiguration(is_client=False)
    configuration.load_cert_chain(certfile=cert_pem, keyfile=key_pem)

    # Start the QUIC server
    await serve(
        host="0.0.0.0",
        port=4433,
        configuration=configuration,
        create_protocol=HttpServerProtocol,
    )

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())

