# 🔐 Password Security Analyzer

A comprehensive password security tool built with Python and CustomTkinter. Analyze password strength, check for breaches against the Have I Been Pwned database, and generate strong secure passwords.

## Features

✅ **Password Strength Analysis**
- Calculates password entropy (in bits)
- Rates passwords as Weak, Medium, or Strong
- Provides actionable suggestions for improvement
- Real-time visual strength meter

✅ **Breach Detection**
- Checks passwords against Have I Been Pwned (HIBP) API
- Detects if password appeared in known data breaches
- Counts breach occurrences
- Uses secure k-anonymity model (only sends first 5 SHA-1 characters)

✅ **Password Generator**
- Generates cryptographically secure random passwords
- Customizable length (12, 16, 20 characters)
- Includes uppercase, lowercase, numbers, and symbols
- One-click clipboard copy

## Requirements

- Python 3.8+
- Windows/Mac/Linux

## Installation

### Option 1: Download Executable (Easiest)
Download the latest `.exe` file from [Releases](https://github.com/yourusername/SecurityTool/releases) and run it directly—no Python installation needed!

### Option 2: Run from Source
1. Clone the repository:
```bash
git clone https://github.com/yourusername/SecurityTool.git
cd SecurityTool
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python main.py
```

## Usage

1. **Analyze a Password:**
   - Enter any password in the text field
   - Click "Analyze" button
   - View strength rating, entropy, suggestions, and breach status

2. **Generate a Strong Password:**
   - Select desired length (12, 16, or 20 characters)
   - Click "Generate Strong Password"
   - Click "Copy to Clipboard" to copy the generated password

3. **Interpret Results:**
   - **Weak**: Password fails multiple strength criteria
   - **Medium**: Password meets some criteria
   - **Strong**: Password meets all security criteria
   - **Red/Yellow/Blue** progress bar indicates strength level

## Security Notes

- ✅ Passwords are **never sent** to any server during analysis
- ✅ HIBP API uses k-anonymity (only SHA-1 prefix is transmitted)
- ✅ Generated passwords use cryptographically secure `secrets` module
- ✅ All processing happens locally on your machine

## Building from Source

To build your own executable:

```bash
pip install pyinstaller
pyinstaller main.spec
```

The executable will be in the `dist/` folder.

## Requirements

- `customtkinter` - Modern GUI framework
- `pyperclip` - Clipboard management
- `requests` - API requests for breach checking

## License

MIT License - feel free to use and modify

## Disclaimer

This tool is for educational purposes. Always use unique, complex passwords for important accounts. Consider using password managers for storing credentials.

## Contributing

Found a bug or have a feature suggestion? Open an issue or submit a pull request!
