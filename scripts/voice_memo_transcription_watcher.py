import time
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import speech_recognition as sr
from pydub import AudioSegment
import tempfile
import shutil

VOICE_MEMOS_DIR = Path.home() / "Library/Group Containers/group.com.apple.VoiceMemos.shared/Recordings"
RESPONSES_DIR = Path("/Volumes/Storage/Dropbox/workspace/projects/branndon.dev/data/responses")

class NewRecordingHandler(FileSystemEventHandler):
    def __init__(self):
        self.recognizer = sr.Recognizer()
        print("Ready to detect and transcribe new recordings.\n")

    def on_created(self, event):
        if event.is_directory or not event.src_path.endswith('.m4a'):
            return

        print(f"\n🎤 New recording detected: {Path(event.src_path).name}")
        time.sleep(3)  # Wait for file to finish writing

        # Convert m4a to wav for speech recognition
        print("Converting audio format...")
        try:
            audio = AudioSegment.from_file(event.src_path, format="m4a")

            # Create temp wav file
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_wav:
                audio.export(temp_wav.name, format="wav")
                temp_wav_path = temp_wav.name

            # Transcribe
            print("Transcribing...")
            with sr.AudioFile(temp_wav_path) as source:
                audio_data = self.recognizer.record(source)
                transcript = self.recognizer.recognize_google(audio_data)

            # Clean up temp file
            Path(temp_wav_path).unlink()

            print("\nTranscript:")
            print(transcript)
            print("\n" + "="*50 + "\n")

            # Save transcript next to audio file
            txt_file = Path(event.src_path).with_suffix('.txt')
            txt_file.write_text(transcript)

            # Move both files to responses directory
            audio_dest = RESPONSES_DIR / Path(event.src_path).name
            txt_dest = RESPONSES_DIR / txt_file.name

            shutil.move(event.src_path, audio_dest)
            shutil.move(txt_file, txt_dest)

            print(f"📁 Moved to: {RESPONSES_DIR}/")
            print(f"   🎤 {audio_dest.name}")
            print(f"   📝 {txt_dest.name}\n")

        except Exception as e:
            print(f"❌ Error transcribing: {e}\n")
            txt_file = Path(event.src_path).with_suffix('.txt')
            txt_file.write_text(f"Transcription failed: {e}")

if __name__ == "__main__":
    print("Watching for new Voice Memos...")
    print(f"Directory: {VOICE_MEMOS_DIR}")
    print(f"Responses saved to: {RESPONSES_DIR}")
    print("Start recording now. Press Ctrl+C to stop.\n")

    event_handler = NewRecordingHandler()
    observer = Observer()
    observer.schedule(event_handler, str(VOICE_MEMOS_DIR), recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping watcher...")
        observer.stop()
    observer.join()
    print("Watcher stopped.")
