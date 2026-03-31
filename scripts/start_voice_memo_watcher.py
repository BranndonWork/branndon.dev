#!/usr/bin/env python3
"""Start the voice memo transcription watcher in the background"""
import subprocess
import sys
import os
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
WATCHER_SCRIPT = SCRIPT_DIR / "voice_memo_transcription_watcher.py"
PID_FILE = SCRIPT_DIR / "voice_memo_transcription_watcher.pid"
LOG_FILE = SCRIPT_DIR.parent / "data" / "voice_memo_watcher.log"

def main():
    # Check if already running
    if PID_FILE.exists():
        pid = PID_FILE.read_text().strip()
        try:
            # Check if process is actually running
            subprocess.run(["ps", "-p", pid], check=True, capture_output=True)
            print(f"❌ Voice memo watcher already running (PID: {pid})")
            print("   Run stop_voice_memo_watcher.py first to stop it")
            sys.exit(1)
        except subprocess.CalledProcessError:
            # Process not running, remove stale PID file
            PID_FILE.unlink()

    # Ensure log directory exists
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

    # Start the watcher
    print("🚀 Starting voice memo transcription watcher...")

    with open(LOG_FILE, 'w') as log:
        process = subprocess.Popen(
            ["poetry", "run", "python", "-u", str(WATCHER_SCRIPT)],
            stdout=log,
            stderr=subprocess.STDOUT,
            cwd=SCRIPT_DIR.parent,
            start_new_session=True,
            preexec_fn=os.setpgrp
        )

    # Save PID
    PID_FILE.write_text(str(process.pid))

    print(f"✅ Voice memo watcher started (PID: {process.pid})")
    print(f"📁 Transcripts will be saved to: data/responses/")
    print(f"📝 Logs: {LOG_FILE}")
    print(f"🛑 To stop: poetry run python scripts/stop_voice_memo_watcher.py")

if __name__ == "__main__":
    main()
