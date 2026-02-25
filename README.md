FileScout 🕵️‍♂️

FileScout is a lightweight, fast utility written in Python that verifies the true identity of a file. It cross-references the file's declared extension with its actual inner content (Magic Numbers / File Signatures) to detect spoofed, corrupted, or empty files.

This tool is especially useful for cybersecurity, digital forensics, and system administration, ensuring that a file is exactly what it claims to be before you interact with it.

🧠 How It Works

Operating systems often rely on file extensions (like .jpg, .pdf, or .exe) to determine how to handle a file. However, malicious actors can easily rename a .exe malware to .txt to bypass basic filters and trick users.

FileScout ignores the extension. Instead, it reads the Magic Bytes (the first few bytes of a file's raw data/header) to identify its true format. It checks these hexadecimal signatures and their specific offsets against a customizable database (magic_bytes.json) to confirm if the file's content matches its name.

🚀 Installation: Making it a Terminal Command

To use FileScout globally (so you can just type scout from any directory in your terminal), you need to make it an executable command. Follow these steps for Linux:

Clone or download the repository:

git clone [https://github.com/felipebehling/FileScout.git](https://github.com/felipe/FileScout.git)
cd FileScout

Make the Python script executable:
By default, text files aren't executable. You need to grant execution permissions:

chmod +x FileScout.py

Move the files to your system's binaries path:
Move the script (renaming it to scout for convenience) and the JSON database to /usr/local/bin, a folder your terminal monitors for commands:

sudo cp FileScout.py /usr/local/bin/scout
sudo cp magic_bytes.json /usr/local/bin/

Note: Ensure your FileScout.py file starts with the shebang line #!/usr/bin/env python3 so the system knows how to run it.

🛠️ Usage

Once installed, simply call scout followed by the target file:

scout filename.ext

Example:

scout secret_document.pdf

📊 Interpreting Results

FileScout uses visual color-coded outputs to quickly inform you about the file's status. Here is what each result means:

 ✓ Match with type declared: .[ext]

Meaning: The file is authentic.

Details: The internal magic bytes match the extension present in the file name. A description of the identified format will be provided below it.

✗ Does not match with type declared: .[ext]

Meaning: The file is spoofed, renamed, or corrupted.

Details: The extension says one thing (e.g., .pdf), but the raw data inside the file indicates it is something else entirely (e.g., an executable). Treat this file with extreme caution.

 ⚠ File '[filename]' is empty (0 bytes).

Meaning: The file contains absolutely no data.

Details: Empty files do not have headers or magic bytes, so FileScout cannot verify them. This usually happens when a file is newly created via commands like touch.

Extension '[ext]' was not found in database

Meaning: Unknown extension.

Details: The file's extension is not currently mapped in the magic_bytes.json file. The tool aborted the scan because it doesn't know what signature to look for. You can manually add new signatures to the JSON file to support more formats.

🤝 Contributing

Contributions, issues, and feature requests are welcome!
If you want to add new file signatures, simply update the magic_bytes.json file and submit a Pull Request.

📝 License

Distributed under the GNU General Public License. See LICENSE for more information.
