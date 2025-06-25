import os, time

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
