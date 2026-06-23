import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from overlay import OverlayApp

def main():
    print("=" * 50)
    print(" Game Overlay System ")
    print("=" * 50)
    print("Controls:")
    print(" F10 - Toggle overlay visibility")
    print(" ESC - Close overlay")
    print("=" * 50)
    print("Reading status from: status.txt")
    print("States: normal, critical")
    print("=" * 50)
    app = OverlayApp()
    sys.exit(app.run())

if __name__ == "__main__":
    main()