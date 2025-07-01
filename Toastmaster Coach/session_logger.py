import os, time, json
from datetime import datetime

#Function: Create folders for each session type/focus/date
def create_session_folder(focus, session_type, date, session_number=None):
    base_path = "logs"
    os.makedirs(base_path, exist_ok=True)

    #session type folder
    session_type_path = os.path.join(base_path, session_type)
    os.makedirs(session_type_path, exist_ok=True)

    #session-specific folder name
    if session_type != "practice":
        folder_name = f"{focus}_{date}_{session_type}"
    else:
        folder_name = f"{focus}_{date}_practice_{str(session_number).zfill(2)}"

    session_folder = os.path.join(session_type_path, folder_name)
    os.makedirs(session_folder, exist_ok=True)
    return session_folder


    #os.makedirs("logs", exist_ok=True)
    #filename = f"logs/{session_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

def consolidate_feedback(feedback_list):
    if not feedback_list:
        return "No feedback recorded"

    if len(feedback_list) == 1:
        return feedback_list[0]

    #echos first and last for now - can use AI to summarize it better
    return f"Start with: '{feedback_list[0]}', ended with: {feedback_list[-1]}. Notable growth across {len(feedback_list)} attempts."

def log_session(base_folder, focus, session_type, session_number, attempts):
    os.makedirs(base_folder, exist_ok=True)
    safe_focus = focus.replace(" ", "_").lower()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    filename = f"{safe_focus}_{session_type}_{str(session_number).zfill(2)}_{timestamp}.json"
    filepath = os.path.join(base_folder, filename)

    # Build log structure
    log = {
        "focus": focus,
        "session_type": session_type,
        "session_number": session_number,
        "timestamp": timestamp,
        "total_attempts": len(attempts),
        "consolidated_feedback": consolidate_feedback([["feedback"] for a in attempts]),
        "attempts": attempts
    }

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(log, f, indent=2)