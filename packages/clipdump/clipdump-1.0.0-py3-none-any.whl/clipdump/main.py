import pyperclip
from datetime import datetime
import os
import sys

now = datetime.now()

def auto():
    home = os.path.expanduser("~")
    dir = os.path.join(home, "Documents", "Clipdump")
    os.makedirs(dir, exist_ok=True)
    filename = os.path.join(dir, now.strftime("%Y-%m-%d %H-%M-%S") + ".txt")
    text = pyperclip.paste()
    if not text:
        print("Clipboard empty; nothing saved")
    with open(filename, "w") as f:
        f.write(text)
    print(f"Clipboard contents saved to {filename}")

def strip_text():
    text = pyperclip.paste()
    if not text:
        "Clipboard empty"
        return
    new_text = text.strip()
    pyperclip.copy(new_text)

def help():
    print("Clipdump usage:")
    print("• --append: appends clipboard contents to a specified pre-existing file. Usage: clipdump --append <file>")
    print("• --auto: automatically saves clipboard contents to an new timestamped text file in C:\\users\\<username>\\Documents\\Clipdump. Usage: clipdump --auto")
    print("• --strip: removes trailing whitespace from clipboard contents. Usage: clipdump --strip")
    print("• --help: displays this help menu. Usage: clipdump --help")

def append(file):
    try:
        text = pyperclip.paste()
        if not text:
            "Clipboard empty; nothing saved"
            return
        with open(file, "a") as f:
            f.write("\n" + text)
    except FileNotFoundError:
        print("File not found; unable to append. Enter clipdump --help for usage")
        return
    print(f"Clipboard contents appended to {file}")

def cli():
    if len(sys.argv) < 2:
        print("Unknown command. Usage: clipdump -a | --append | --strip <file>.  Enter clipdump --help for usage")
        return
    command = sys.argv[1].lower()
    if command == "-a":
        auto()
    elif command == "--append":
        if len(sys.argv) < 3:
            print("Missing file for append; unable to append.  Enter clipdump --help for usage")
            return
        filename = sys.argv[2]
        append(filename)
    elif command == "--strip":
        strip_text()
    elif command == "--help":
        help()
if __name__ == "__main__":
    cli()