
# QUIC WebTransport Server with WebRTC 🚀

A Python-based server using **aioquic** and **aiortc** to handle QUIC WebTransport connections and WebRTC media streaming. The server allows for low-latency, real-time communication over WebTransport and can relay media tracks to an RTMP server or save them locally using the AIORTC `MediaRecorder`.

## 🚀 Features

- **WebTransport over QUIC**: Supports WebTransport sessions for low-latency communication.
- **WebRTC Media Relay**: Relays incoming WebRTC media streams to RTMP or saves them locally.
- **Dynamic Certificate Management**: Generates self-signed certificates for development or uses specified certificates for production.
- **Fallback HTTP POST for WebRTC Offer**: Supports WebRTC signaling via HTTP POST if WebTransport is unavailable.

## 🛠️ Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/mastashake08/quic-stream.git
   cd your-repo
   ```

2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

   Ensure the following dependencies are installed:
   - `aioquic`
   - `aiortc`
   - `cryptography`
   - `starlette`
   - `uvicorn`

## ⚙️ Usage

1. **Run the QUIC WebTransport server in development mode** with a self-signed certificate:

   ```bash
   python your_script.py --dev --media-recorder-path "rtmp://your.rtmp.url/stream"
   ```

   In this mode, the server will dynamically generate a self-signed certificate and relay WebRTC media to an RTMP URL or local file specified by the `--media-recorder-path` flag.

2. **Run the QUIC WebTransport server in production mode** with specified SSL certificates:

   ```bash
   python your_script.py --cert path/to/cert.pem --key path/to/key.pem --media-recorder-path "output.mp4"
   ```

   In production mode, you need to specify the certificate and key files using the `--cert` and `--key` flags. The media recorder path can either be an RTMP URL or a local file path for saving the media.

### Command-Line Options:

- `--dev`: Run in development mode with a self-signed certificate.
- `--cert`: Path to the SSL certificate (for production mode).
- `--key`: Path to the SSL private key (for production mode).
- `--media-recorder-path`: **(Required)** The path for the media recorder, which can be an RTMP URL or a local file (e.g., `output.mp4`).

## Endpoints

1. **WebRTC Offer via HTTP POST**:
   - The client sends a WebRTC offer in JSON format to the `/offer` endpoint via HTTP POST.
   
   Example request body:
   ```json
   {
       "sdp": "v=0...",
       "type": "offer"
   }
   ```

   Example `curl` request:
   ```bash
   curl -X POST http://localhost:8080/offer \
        -H "Content-Type: application/json" \
        -d '{"sdp": "v=0...","type":"offer"}'
   ```

2. **WebTransport Initialization**:
   - The client can initialize a WebTransport session by sending a GET request to `/wt`.
   
   Example `curl` request:
   ```bash
   curl -X GET http://localhost:8080/wt
   ```

## 🧩 How It Works

- The server handles QUIC WebTransport sessions using `aioquic`. WebRTC offers can be sent via QUIC datagrams, and the media streams are relayed to an RTMP server or saved locally.
- If WebTransport is not available, clients can send WebRTC offers using a POST request to the `/offer` endpoint.
- WebRTC media is handled by `aiortc` and can be relayed to an RTMP stream or saved locally using the `MediaRecorder`.

## Example WebRTC Flow

- **Client sends WebRTC offer** as a QUIC datagram or HTTP POST request.
- **Server responds** with a WebRTC answer via QUIC or HTTP POST response.
- **Media Tracks** are received and forwarded to an RTMP server or saved locally.

### Development Mode:

- In development mode, the server dynamically generates a self-signed TLS certificate. This is useful for local testing without needing to provide SSL certificates.

### Production Mode:

- In production mode, you need to provide the SSL certificate and key paths for secure communication over QUIC.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check out the [issues page](https://github.com/your-username/your-repo/issues).

1. Fork the project.
2. Create your feature branch (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Open a pull request.

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

> Made with ❤️ using Python, aioquic, and aiortc.
```

### Customizations and Explanations:

1. **`--media-recorder-path`**:
   - The usage of the `--media-recorder-path` argument is highlighted. This can be used to relay WebRTC media streams to an RTMP URL or save them to a local file.

2. **Command-line usage**:
   - The command-line examples show how to run the server in both development and production modes.
   - The required arguments `--media-recorder-path` and the optional `--dev`, `--cert`, and `--key` arguments are explained.

3. **Endpoints**:
   - I’ve documented the `/offer` and `/wt` endpoints and provided example `curl` requests to test them.

4. **Contribution**:
   - Added contribution guidelines to encourage collaborative improvements.

