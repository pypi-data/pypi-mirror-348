# 🔐 Recursive Archive Extractor

```
 ▄▄▄ ▗▞▀▚▖▗▞▀▘█  ▐▌ ▄▄▄ ▄▄▄ ▄ ▄   ▄ ▗▖  ▗▖
█    ▐▛▀▀▘▝▚▄▖▀▄▄▞▘█   ▀▄▄  ▄ █   █  ▝▚▞▘ 
█    ▝▚▄▄▖         █   ▄▄▄▀ █  ▀▄▀    ▐▌  
                            █       ▗▞▘▝▚▖
```

> A powerful Python tool that **recursively extracts nested archive files**, logs password-protected ZIPs, and handles multiple compression formats with style.

---

## 📦 Supported Formats

- `.zip` (with password detection)
- `.xz`
- `.bz2`
- `.gz`
- `.tar`

---

## 🚀 Features

- 📂 Recursively unpacks deeply nested archive layers.
- 🧠 Auto-detects archive types based on file headers.
- 🛡️ Detects and logs password-protected ZIPs.
- 🪵 Writes extraction logs per layer.
- 📁 Copies final locked ZIP layer for further analysis.
- 🖼️ Clean structure and modular design.

---

## 🛠️ Installation

```bash
git clone https://github.com/Paul00/recursivX.git
cd recursivX
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt  # Currently, no third-party modules required
```

---

## 🧪 Usage

```bash
python recursivX.py input_archive.ext -o output_folder
```

### Example:

```bash
python recursivX.py sample.zip -o unpacked_layers
```

---

## 📁 Output Structure

```
extracted/
├── layer_1/
│   └── ...
├── layer_2/
│   └── ...
├── final_locked_layer.zip  ← If password-protected
└── extraction_log.txt      ← Full extraction log
```

---

## 📓 Log Format

Each extraction layer is logged with detected archive type and filename. If password protection is found, you'll see:

```
[Layer 3] sample_protected.zip requires password
  → Encapsulated files: secret.txt, data.json
```

---

## 🙏 Credits

Crafted with care by [Paul00](https://github.com/Paul00)

---

## 📜 License

MIT License – do whatever you want, just don’t claim you wrote it 😉
