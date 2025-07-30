import sys
from pipfixer.core import pipfixer

def main():
    if len(sys.argv) < 2:
        print("⚠️  Usage: pipfixer <your_script.py>")
        return
    filepath = sys.argv[1]
    pipfixer(filepath)

if __name__ == "__main__":
    main()
