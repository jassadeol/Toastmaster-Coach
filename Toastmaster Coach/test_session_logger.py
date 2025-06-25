import os
import json
from datetime import date
from pathlib import Path

# --- Import your function (assuming it's saved in a module called session_logger.py)
from session_logger import create_session_folder

def generate_mock_session(focus, session_type, session_number=None):
    today = date.today().strftime("%Y-%m-%d")
    folder_path = create_session_folder(focus, session_type, today, session_number)

    # Write a mock summary.txt
    with open(Path(folder_path) / "summary.txt", "w") as f:
        f.write(f"Session Type: {session_type.capitalize()}\nFocus: {focus}\nDate: {today}\nNotes: Placeholder summary.")

    # Create a feedback.json template
    feedback = {
        "focus": focus,
        "session_type": session_type,
        "date": today,
        "duration_minutes": 25,
        "feedback": {
            "score": 8,
            "comments": "Solid clarity and structure.",
            "recommendations": ["Slow down pacing", "Add variety to tone"]
        },
        "audio_file": "audio.wav"
    }
    with open(Path(folder_path) / "feedback.json", "w") as f:
        json.dump(feedback, f, indent=4)

    # Create a dummy audio.wav (empty placeholder for now)
    Path(folder_path, "audio.wav").touch()

    print(f"✓ Mock session created at: {folder_path}")

# ---- Run mock sessions ----
if __name__ == "__main__":
    generate_mock_session("ReduceFillerWords", "preliminary")
    generate_mock_session("EnhanceVocalVariety", "practice", session_number=1)
    generate_mock_session("MasterTransitions", "practice", session_number=2)
    generate_mock_session("PresentWithPersuasiveClarity", "midterm")
