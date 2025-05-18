# Aegiscan CLI

Aegiscan is a simple Static Application Security Testing (SAST) tool written in Python.  
It scans Python code via the command line and detects potential security vulnerabilities based on customizable rules.

---

## Features

- Scan Python code from a remote Git repository or local directory  
- Detect potential security issues using rule files in YAML or JSON format  
- Output results in JSON, YAML, or plain text format  
- Filter results by severity level (LOW, MEDIUM, HIGH, CRITICAL)  
- Easy to extend with custom rules

---

## Installation

```bash
git clone https://github.com/BaranTeyin1/Aegiscan-cli
cd aegiscan-cli
pip install -r requirements.txt
```

## Usage
```bash
python main.py --git-url <git-repo-url> --rules <rules-folder> --output results.json --severity HIGH
```
## Example
```bash
python main.py --local-file ./myproject --rules ./rules --output results.txt
```

## Contributing

This project is open source. Feel free to submit issues or pull requests!
