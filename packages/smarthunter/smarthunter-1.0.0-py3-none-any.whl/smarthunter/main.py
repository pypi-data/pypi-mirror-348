#!/usr/bin/env python3
"""
SmartHunter - A tool to find encoded strings in binary files.
"""
import sys
import argparse
import base64
import re
import binascii
import json
import string
from pathlib import Path
from urllib.parse import unquote_to_bytes

try:
    from rich import print
    from rich.table import Table
    from rich.console import Console
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

# Morse code mapping
MORSE_CODE = {
    '.-': 'A', '-...': 'B', '-.-.': 'C', '-..': 'D', '.': 'E', '..-.': 'F', '--.': 'G',
    '....': 'H', '..': 'I', '.---': 'J', '-.-': 'K', '.-..': 'L', '--': 'M', '-.': 'N',
    '---': 'O', '.--.': 'P', '--.-': 'Q', '.-.': 'R', '...': 'S', '-': 'T', '..-': 'U',
    '...-': 'V', '.--': 'W', '-..-': 'X', '-.--': 'Y', '--..': 'Z', 
    '-----': '0', '.----': '1', '..---': '2', '...--': '3', '....-': '4', 
    '.....': '5', '-....': '6', '--...': '7', '---..': '8', '----.': '9',
    '/': ' '
}

# Braille mapping (simplified - maps braille pattern to alphanumeric)
BRAILLE_OFFSET = 0x2800
BRAILLE_MAP = {i: chr(0x30 + i) for i in range(64)}  # Maps to '0'-'9', 'A'-'Z', etc.

def printable_ratio(bs):
    """Return ratio of printable ASCII characters."""
    printable_set = set(string.printable.encode())
    return sum(b in printable_set for b in bs) / len(bs) if bs else 0

def is_valid_ascii(text, threshold=0.8):
    """Check if a string is mostly ASCII printable."""
    if isinstance(text, bytes):
        try:
            text = text.decode('utf-8', errors='ignore')
        except UnicodeDecodeError:
            return False
    
    # Reject strings that are too short
    if len(text) < 3:
        return False
        
    # Reject strings with mostly control characters or non-printable sequences
    return printable_ratio(text.encode()) > threshold

def deduplicate_results(results):
    """Remove duplicate items based on the decoded text."""
    seen_texts = set()
    unique_results = []
    
    for item in results:
        # Only include items with non-empty text
        if not item['text'].strip():
            continue
            
        # Normalize text for comparison (lowercase, strip spaces)
        norm_text = item['text'].lower().strip()
        
        # Skip already seen texts
        if norm_text in seen_texts:
            continue
            
        seen_texts.add(norm_text)
        unique_results.append(item)
    
    return unique_results

def looks_like_flag(text):
    """Check if text looks like a flag."""
    # Common flag formats: flag{...}, CTF{...}, KEY{...}, etc.
    flag_patterns = [
        r'flag\{[^}]+\}',
        r'ctf\{[^}]+\}', 
        r'key\{[^}]+\}',
        r'\{[^}]{5,}\}'  # Generic {content} pattern with at least 5 chars
    ]
    
    for pattern in flag_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return True
    
    return False

def scan_file(path, min_len=4, max_len=120):
    """Scan a file for encoded strings."""
    results = []
    
    # Load the file
    with open(path, 'rb') as f:
        content = f.read()
    
    # 1. Cleartext - ASCII strings
    ascii_pattern = re.compile(rb'[ -~]{6,}')  # 6+ printable ASCII chars
    for match in re.finditer(ascii_pattern, content):
        try:
            text = match.group(0).decode('ascii', errors='ignore')
            if min_len <= len(text) <= max_len and printable_ratio(match.group(0)) > 0.95:
                results.append({
                    'offset': match.start(),
                    'length': len(match.group(0)),
                    'codec': 'ascii',
                    'text': text,
                    'score': 0.5 + (0.3 if looks_like_flag(text) else 0)  # Boost flags
                })
        except Exception:
            pass
    
    # 2. Base64 Standard
    base64_pattern = rb'(?:[A-Za-z0-9+/]{4}\s*){3,}(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?'
    for match in re.finditer(base64_pattern, content):
        try:
            raw = b''.join(match.group(0).split())  # Remove whitespace
            decoded = base64.b64decode(raw)
            if min_len <= len(decoded) <= max_len and is_valid_ascii(decoded, 0.8):
                text = decoded.decode(errors='ignore')
                results.append({
                    'offset': match.start(),
                    'length': len(match.group(0)),
                    'codec': 'base64',
                    'text': text,
                    'score': 0.9 + (0.1 if looks_like_flag(text) else 0)
                })
        except Exception:
            pass
    
    # 3. Base64 URL-safe
    base64url_pattern = rb'(?:[A-Za-z0-9\-_]{4}\s*){3,}(?:[A-Za-z0-9\-_]{2}==|[A-Za-z0-9\-_]{3}=)?'
    for match in re.finditer(base64url_pattern, content):
        try:
            raw = b''.join(match.group(0).split())  # Remove whitespace
            decoded = base64.urlsafe_b64decode(raw)
            if min_len <= len(decoded) <= max_len and is_valid_ascii(decoded, 0.8):
                text = decoded.decode(errors='ignore')
                results.append({
                    'offset': match.start(),
                    'length': len(match.group(0)),
                    'codec': 'base64url',
                    'text': text,
                    'score': 0.9 + (0.1 if looks_like_flag(text) else 0)
                })
        except Exception:
            pass
    
    # 4. Base32
    base32_pattern = rb'(?:[A-Z2-7]{8}\s*){2,}=?=?=?=?'
    for match in re.finditer(base32_pattern, content):
        try:
            raw = b''.join(match.group(0).split())  # Remove whitespace
            decoded = base64.b32decode(raw)
            if min_len <= len(decoded) <= max_len and is_valid_ascii(decoded, 0.8):
                text = decoded.decode(errors='ignore')
                results.append({
                    'offset': match.start(),
                    'length': len(match.group(0)),
                    'codec': 'base32',
                    'text': text,
                    'score': 0.8 + (0.2 if looks_like_flag(text) else 0)
                })
        except Exception:
            pass
    
    # 5. Base85
    base85_pattern = rb'(?:[!-u]{5}\s*){4,}'
    for match in re.finditer(base85_pattern, content):
        try:
            raw = b''.join(match.group(0).split()) 
            decoded = base64.a85decode(raw)
            if min_len <= len(decoded) <= max_len and is_valid_ascii(decoded, 0.8):
                text = decoded.decode(errors='ignore')
                results.append({
                    'offset': match.start(),
                    'length': len(match.group(0)),
                    'codec': 'base85',
                    'text': text,
                    'score': 0.85 + (0.15 if looks_like_flag(text) else 0)
                })
        except Exception:
            pass
    
    # 6. Hexadecimal
    hex_pattern = rb'(?:[0-9A-Fa-f]{2}\s*){4,}'
    for match in re.finditer(hex_pattern, content):
        try:
            raw = b''.join(match.group(0).split())  # Remove whitespace
            # Only process if it's valid hex (even number of digits)
            if len(raw) % 2 == 0:
                decoded = binascii.unhexlify(raw)
                if min_len <= len(decoded) <= max_len and is_valid_ascii(decoded, 0.8):
                    text = decoded.decode(errors='ignore')
                    results.append({
                        'offset': match.start(),
                        'length': len(match.group(0)),
                        'codec': 'hex',
                        'text': text,
                        'score': 0.7 + (0.2 if looks_like_flag(text) else 0)
                    })
        except Exception:
            pass
    
    # 7. URL encoded
    url_pattern = rb'(?:%[0-9A-Fa-f]{2}){2,}'
    for match in re.finditer(url_pattern, content):
        try:
            raw = match.group(0)
            decoded = unquote_to_bytes(raw)
            if min_len <= len(decoded) <= max_len and is_valid_ascii(decoded, 0.8):
                text = decoded.decode(errors='ignore')
                results.append({
                    'offset': match.start(),
                    'length': len(match.group(0)),
                    'codec': 'url',
                    'text': text,
                    'score': 0.8 + (0.2 if looks_like_flag(text) else 0)
                })
        except Exception:
            pass
    
    # 8. Octal
    octal_pattern = re.compile(rb'(?:[0-7]{3}\s*){4,}')
    for match in re.finditer(octal_pattern, content):
        try:
            parts = re.findall(rb'[0-7]{3}', match.group(0))
            decoded = bytes([int(part, 8) for part in parts])
            if min_len <= len(decoded) <= max_len and is_valid_ascii(decoded, 0.8):
                text = decoded.decode(errors='ignore')
                results.append({
                    'offset': match.start(),
                    'length': len(match.group(0)),
                    'codec': 'octal',
                    'text': text,
                    'score': 0.65 + (0.2 if looks_like_flag(text) else 0)
                })
        except Exception:
            pass
    
    # 9. Decimal
    decimal_pattern = re.compile(rb'(?:\d{1,3}\s+){4,}')
    for match in re.finditer(decimal_pattern, content):
        try:
            nums = [int(x) for x in match.group(0).split()]
            # Check if values are in valid ASCII range
            if all(0 <= n <= 255 for n in nums):
                decoded = bytes(nums)
                if min_len <= len(decoded) <= max_len and is_valid_ascii(decoded, 0.8):
                    text = decoded.decode(errors='ignore')
                    results.append({
                        'offset': match.start(),
                        'length': len(match.group(0)),
                        'codec': 'decimal',
                        'text': text,
                        'score': 0.65 + (0.2 if looks_like_flag(text) else 0)
                    })
        except Exception:
            pass
    
    # 10. UTF-16
    utf16_markers = [b'\x00\x00', b'\xFE\xFF', b'\xFF\xFE']
    for marker in utf16_markers:
        for match in re.finditer(marker, content):
            try:
                # Extract a chunk of reasonable size
                pos = match.start()
                chunk = content[pos:pos+max_len*2]
                
                # Try both endianness
                for encoding in ['utf-16le', 'utf-16be']:
                    try:
                        text = chunk.decode(encoding, errors='strict')
                        if min_len <= len(text) <= max_len and is_valid_ascii(text, 0.7):
                            results.append({
                                'offset': pos,
                                'length': len(chunk),
                                'codec': encoding,
                                'text': text,
                                'score': 0.7 + (0.2 if looks_like_flag(text) else 0)
                            })
                            break
                    except UnicodeDecodeError:
                        continue
            except Exception:
                pass
    
    # 11. Morse Code
    morse_pattern = rb'[.-]{1,5}(?:\s+[.-]{1,5}){3,}'
    for match in re.finditer(morse_pattern, content):
        try:
            morse_text = match.group(0).decode('ascii', errors='ignore')
            decoded = ''
            for symbol in morse_text.split():
                if symbol in MORSE_CODE:
                    decoded += MORSE_CODE[symbol]
            
            if decoded and min_len <= len(decoded) <= max_len and is_valid_ascii(decoded, 0.7):
                results.append({
                    'offset': match.start(),
                    'length': len(match.group(0)),
                    'codec': 'morse',
                    'text': decoded,
                    'score': 0.6 + (0.3 if looks_like_flag(decoded) else 0)
                })
        except Exception:
            pass
    
    # 12. Braille (UTF-8 encoded)
    braille_pattern = rb'\xe2\xa0[\x80-\xbf]'  # UTF-8 lead bytes for Braille block
    for match in re.finditer(braille_pattern, content):
        try:
            pos = match.start()
            chunk_size = min(200, len(content) - pos)  # Get a reasonable chunk to analyze
            chunk = content[pos:pos+chunk_size]
            
            try:
                braille_chars = chunk.decode('utf-8')
                decoded = ''
                for c in braille_chars:
                    if 0x2800 <= ord(c) <= 0x28FF:  # Braille unicode range
                        braille_value = ord(c) - BRAILLE_OFFSET
                        decoded += BRAILLE_MAP.get(braille_value & 0x3F, '?')
                
                if decoded and min_len <= len(decoded) <= max_len and is_valid_ascii(decoded, 0.7):
                    results.append({
                        'offset': pos,
                        'length': len(chunk),
                        'codec': 'braille',
                        'text': decoded,
                        'score': 0.6 + (0.3 if looks_like_flag(decoded) else 0)
                    })
            except UnicodeDecodeError:
                pass
        except Exception:
            pass
    
    # 13. BaseXX (hidden flag in text - every Nth character) 
    # Examine larger chunks for potential flags
    chunk_size = 200
    for i in range(0, len(content) - chunk_size, chunk_size // 2):  # Overlapping chunks
        chunk = content[i:i+chunk_size]
        
        # Check if readable text with ascii
        try:
            text = chunk.decode('ascii', errors='ignore')
            
            # Try extracting every Nth character
            for n in range(2, 6):  # Try common spacings (every 2nd, 3rd, 4th, 5th)
                extracted = text[::n]
                
                # Check if it looks like a flag 
                if (('flag{' in extracted.lower()) or 
                    ('ctf{' in extracted.lower()) or 
                    (extracted.lower().startswith('flag') or extracted.lower().startswith('key'))):
                    
                    if min_len <= len(extracted) <= max_len:
                        results.append({
                            'offset': i,
                            'length': len(chunk),
                            'codec': f'basexx-{n}',
                            'text': extracted,
                            'score': 0.75 + 0.2  # Always high score for flag patterns
                        })
        except Exception:
            pass
    
    # Sort by score and offset
    results.sort(key=lambda x: (-x['score'], x['offset']))
    
    # Deduplicate results
    results = deduplicate_results(results)
    
    return results

def print_results(results, threshold=0):
    """Print results in a simple format."""
    if not results:
        print("No results matching the threshold criteria.")
        return
    
    # Simple console output that works everywhere
    for result in results:
        if result['score'] >= threshold:
            print(f"{result['offset']:08x} [{result['codec']}] (score: {result['score']:.2f}) {result['text']!r}")

def main():
    parser = argparse.ArgumentParser(description="SmartHunter - Find encoded strings in binary files")
    parser.add_argument("file", type=str, help="File to scan")
    parser.add_argument("--min", type=int, default=4, help="Minimum length of decoded string (default: 4)")
    parser.add_argument("--max", type=int, default=120, help="Maximum length of decoded string (default: 120)")
    parser.add_argument("--out", type=str, help="Output file for JSON results")
    parser.add_argument("--clean", action="store_true", help="Clean output mode (only high-confidence strings)")
    parser.add_argument("--threshold", type=float, default=0.0, help="Minimum confidence score (0.0-1.0)")
    
    args = parser.parse_args()
    
    file_path = Path(args.file)
    if not file_path.exists():
        print(f"Error: File '{args.file}' not found")
        return 1
    
    print(f"Scanning {file_path}...")
    results = scan_file(file_path, min_len=args.min, max_len=args.max)
    
    # Print raw number of detected strings before filtering
    print(f"Total detected strings: {len(results)}")
    
    # Apply clean mode or threshold filtering
    threshold = 0.8 if args.clean else args.threshold
    filtered_results = [r for r in results if r['score'] >= threshold]
    
    if not filtered_results:
        print(f"No encoded strings found with confidence threshold >= {threshold:.2f}!")
        print("Try lowering the threshold with --threshold or remove the --clean flag")
    else:
        print(f"Found {len(filtered_results)} encoded strings after filtering:")
        print_results(filtered_results, threshold)
    
    if args.out:
        out_path = Path(args.out)
        out_path.write_text(json.dumps(results, indent=2))
        if RICH_AVAILABLE:
            print(f"[bold cyan]Saved → {out_path}[/]")
        else:
            print(f"Saved → {out_path}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 