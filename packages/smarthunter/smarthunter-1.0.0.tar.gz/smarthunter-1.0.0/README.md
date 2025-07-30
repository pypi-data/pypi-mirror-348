# SmartHunter 🔍

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI version](https://img.shields.io/badge/pypi-v1.0.0-blue.svg)](https://pypi.org/project/smarthunter/)
[![Python Versions](https://img.shields.io/badge/python-3.9%20|%203.10%20|%203.11-blue)](https://pypi.org/project/smarthunter/)

**SmartHunter** is a high-performance tool designed to scan binaries, firmware, and any byte source for hidden strings and flags in multiple encoding formats. Built with CTF competitions and security research in mind, it features intelligent string detection, automatic flag pattern recognition, and scoring mechanisms.

```
00002345 [base64] (score: 0.95) 'flag{h1dd3n_1n_pl41n_s1ght}'
000047A9 [hex] (score: 0.85) 'secret_key_found_in_binary'
0000F5C8 [base32] (score: 0.80) 'CTF{d3c0d3_m3_1f_y0u_c4n}'
```

## ✨ Features

- **Multi-Encoding Support**: Detect strings in 13 different encoding formats:

  - Base64 (Standard and URL-safe)
  - Base32
  - Base85
  - Hexadecimal
  - URL encoding (%XX)
  - Octal
  - Decimal
  - UTF-16 (both endianness)
  - Morse code
  - Braille
  - BaseXX (hidden flags in text)
  - Cleartext (ASCII)

- **Smart Detection**:

  - Confidence scoring algorithm
  - Automatic flag pattern boosting (`flag{}`, `CTF{}`, etc.)
  - Deduplication of results
  - Configurable thresholds

- **Performance Optimized**:

  - Efficient regular expressions
  - Fast byte manipulation
  - Memory-mapped file access for large binaries

- **Flexible Output**:
  - Clean mode for high-confidence results only
  - Adjustable confidence threshold
  - Customizable min/max length filtering
  - JSON export for further analysis

## 🚀 Installation

### From PyPI

```bash
pip install smarthunter
```

### From Source

```bash
git clone https://github.com/yourname/smarthunter.git
cd smarthunter
pip install -e .
```

## 📋 Usage

### Basic Usage

```bash
# Scan a file and display all found strings
smarthunter sample.bin

# Use clean mode to show only high-confidence results (score >= 0.8)
smarthunter sample.bin --clean

# Set a custom confidence threshold (0.0-1.0)
smarthunter sample.bin --threshold 0.7

# Control string length filtering
smarthunter sample.bin --min 6 --max 120

# Export results to JSON for further analysis
smarthunter sample.bin --out results.json
```

### Command-Line Options

| Option              | Description                                      |
| ------------------- | ------------------------------------------------ |
| `--clean`           | Show only high-confidence results (score >= 0.8) |
| `--threshold FLOAT` | Set minimum confidence score (0.0-1.0)           |
| `--min INT`         | Minimum length of decoded string (default: 4)    |
| `--max INT`         | Maximum length of decoded string (default: 120)  |
| `--out FILE`        | Save results to JSON file                        |

## 💻 Python API

SmartHunter can be easily integrated into your Python projects:

```python
from smarthunter import scan_file

# Scan a file and process results
results = scan_file("firmware.bin")

# Results are sorted by confidence score
for result in results:
    print(f"Found at 0x{result['offset']:08x}: {result['text']}")
    print(f"  Encoding: {result['codec']}")
    print(f"  Confidence: {result['score']:.2f}")

# Filter by confidence score
high_confidence = [r for r in results if r['score'] >= 0.8]

# Find likely flags
flags = [r for r in results if 'flag{' in r['text'].lower()]
```

## 🔍 Examples

### Finding Hidden Flags in CTF Challenges

SmartHunter excels at finding hidden flags in CTF challenges:

```bash
# Scan a CTF binary and output high-confidence results
smarthunter challenge.bin --clean
```

### Analyzing Firmware for Secrets

```bash
# Search for secrets in firmware with minimum length of 8 characters
smarthunter firmware.bin --min 8 --threshold 0.6 --out firmware_secrets.json
```

### Scanning Text Files for Steganography

```bash
# Check if a text file contains hidden messages
smarthunter steg_message.txt --threshold 0.7
```

## 🔧 How It Works

SmartHunter works by:

1. Memory-mapping the target file for efficient access
2. Applying optimized detection algorithms for each encoding format
3. Scoring detected strings based on multiple factors:
   - Printable character ratio
   - Pattern matches (flags, keys, etc.)
   - String length
4. Filtering and deduplicating results
5. Ranking findings by confidence score

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Feel free to:

- Report bugs
- Suggest features
- Add new decoders
- Improve performance
- Submit pull requests

## 📚 Acknowledgments

- Inspired by CTF challenges and the need for better binary string extraction tools
- Special thanks to the security and CTF community

---

Made with ❤️ for security researchers and CTF players
