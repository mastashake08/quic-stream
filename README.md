


# QUIC WebTransport Server with WebRTC 🚀

<p align="center">
  <img src="https://raw.githubusercontent.com/mastashake08/quic-stream/main/logo.svg" alt="Project Logo" width="200"/>
</p>

A Python-based QUIC and WebTransport server, leveraging the power of **aioquic** and **aiortc** for low-latency, secure communication. This project dynamically generates TLS certificates and supports WebRTC for real-time media streaming to an RTMP server.

## 🚀 Features

- **WebTransport over QUIC**: Fast, reliable, low-latency communication using QUIC and HTTP/3.
- **WebRTC Integration**: Real-time peer-to-peer communication via WebRTC for audio/video streaming.
- **Dynamic TLS Certificates**: No need to store or manage certificates, they are generated on the fly.
- **Media Relaying**: Seamless forwarding of WebRTC media tracks to an RTMP server using `aiortc`.

## 🛠️ Installation

To install the project and its dependencies:

1. Clone the repository:

   ```bash
   git clone https://github.com/username/repository.git
   cd repository
   ```

2. Install dependencies via `requirements.txt`:

   ```bash
   pip install -r requirements.txt
   ```

## ⚙️ Usage

1. Run the QUIC WebTransport server with dynamically generated certificates:

   ```bash
   python your_script.py
   ```

   The server will run on port `4433` by default.

2. Test the server by connecting a WebTransport or WebRTC client.

### Example WebRTC Flow:

- **Client sends WebRTC offer** as a QUIC datagram.
- **Server responds** with a WebRTC answer via QUIC datagram.
- **Media Tracks** are received and forwarded to an RTMP server for live streaming.

## 🧩 How It Works

- The server dynamically generates a self-signed TLS certificate using `cryptography`.
- QUIC is used as the transport layer for WebTransport sessions, enabling low-latency datagram and stream communication.
- WebRTC signaling (offer/answer) is handled via QUIC datagrams, avoiding traditional HTTP POST signaling.
- `aiortc` manages the WebRTC connections and relays media streams to an RTMP server using `MediaRecorder`.

## 💡 Example SVG Logo (You can customize this)

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="200" height="200">
  <circle cx="50" cy="50" r="48" fill="#61DAFB" stroke="#000" stroke-width="4"/>
  <text x="50%" y="50%" fill="#000" font-size="12" text-anchor="middle" alignment-baseline="central" font-family="Arial, Helvetica, sans-serif">
    QUIC + WebRTC
  </text>
</svg>
```

Save this SVG code as `logo.svg` in your project directory or in an appropriate folder in your GitHub repository.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check out the [issues page](https://github.com/username/repository/issues) if you want to contribute.

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

### Customization Details

1. **SVG Logo**:
   - You can customize the SVG logo to fit your branding or project needs. The current logo is a basic circular graphic with text, which you can modify or replace with a more sophisticated design.

2. **Repository URLs**:
   - Be sure to replace all instances of `https://github.com/username/repository` with your actual GitHub username and repository name.

3. **Installation and Usage**:
   - Make sure the instructions match your actual project structure and script names (replace `your_script.py` with your actual script file if necessary).

4. **Contributing**:
   - The contributing section is a basic guideline. You can expand it to include code style guidelines, testing instructions, or any specific requirements for contributors.

### How to Add the SVG Logo

1. Save the SVG logo code into a file called `logo.svg` in your repository. For example, you can create a directory named `assets` and save the logo there (`assets/logo.svg`).
   
2. Update the image link in the markdown to point to that file:
   ```html
   <img src="https://raw.githubusercontent.com/username/repository/main/assets/logo.svg" alt="Project Logo" width="200"/>
   ```

3. Push the changes to your GitHub repository, and the logo will be displayed directly in your README file.

### How to Use This

1. **Create `README.md`**: Save the markdown content above into a file called `README.md`.
   
2. **Push to GitHub**: Commit the changes and push to your GitHub repository.
   
3. **View on GitHub**: The `README.md` will be displayed automatically on the repository homepage, complete with the embedded SVG logo.