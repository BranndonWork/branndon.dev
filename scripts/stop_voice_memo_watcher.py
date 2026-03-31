#!/usr/bin/env python3
"""Stop the voice memo transcription watcher"""
import subprocess
import sys
import signal
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
PID_FILE = SCRIPT_DIR / "voice_memo_transcription_watcher.pid"

def main():
    # Check if PID file exists
    if not PID_FILE.exists():
        print("❌ Watcher not running (no PID file found)")

        # Try to find process anyway
        print("🔍 Searching for running watcher processes...")
        try:
            result = subprocess.run(
                ["pgrep", "-f", "voice_memo_transcription_watcher.py"],
                capture_output=True,
                text=True
            )
            if result.stdout.strip():
                pids = result.stdout.strip().split('\n')
                print(f"⚠️  Found orphaned process(es): {', '.join(pids)}")
                for pid in pids:
                    try:
                        subprocess.run(["kill", pid], check=True)
                        print(f"✅ Killed process {pid}")
                    except subprocess.CalledProcessError:
                        print(f"❌ Failed to kill process {pid}")
            else:
                print("✅ No watcher processes found")
        except FileNotFoundError:
            print("✅ No watcher processes found")

        sys.exit(0)

    # Read PID
    pid = PID_FILE.read_text().strip()

    # Check if process is running
    try:
        subprocess.run(["ps", "-p", pid], check=True, capture_output=True)
    except subprocess.CalledProcessError:
        print(f"❌ Process {pid} not running (stale PID file)")
        PID_FILE.unlink()
        sys.exit(0)

    # Kill the process
    print(f"🛑 Stopping watcher (PID: {pid})...")
    try:
        subprocess.run(["kill", pid], check=True)
        print(f"✅ Watcher stopped")
        PID_FILE.unlink()
    except subprocess.CalledProcessError:
        print(f"❌ Failed to stop process {pid}")
        print("   Try manually: kill {pid}")
        sys.exit(1)

if __name__ == "__main__":
    main()
