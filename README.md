# Code2Image ✨📄→🖼️

A Flask-based web application that converts code snippets into beautifully formatted images with syntax highlighting.

## :dart: Features

- 📝 Code editor with syntax highlighting
- 🎨 Multiple theme options (Dark/Light/Solarized/Monokai)
- 🔢 Line numbers support
- 🖋️ Custom font support (Fira Code)
- 📁 File upload capability
- 🖼️ Real-time preview
- 📥 Image download (PNG format)

## :hammer_and_wrench: Installation

### Prerequisites
- Python 3.9+
- pip
- Fontconfig (for system font management)

### 1. Clone the repository
```bash
git clone https://github.com/thealper2/code2image.git
cd code2image
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Install Fira Code font (Required for proper rendering)

```bash
# Download and install Fira Code
wget https://github.com/tonsky/FiraCode/releases/download/6.2/Fira_Code_v6.2.zip
unzip Fira_Code_v6.2.zip -d ~/.fonts/

# Update font cache
fc-cache -fv

# Verify installation
fc-list | grep "Fira Code"
```

### 4. Run the application

```bash
python3 run.py
```

The application will be available at http://localhost:5000

## :handshake: Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a new branch for your feature (git checkout -b feature/your-feature)
3. Commit your changes (git commit -am 'Add some feature')
4. Push to the branch (git push origin feature/your-feature)
5. Create a new Pull Request

## :scroll: License

This project is licensed under the MIT License - see the LICENSE file for details.