import json, random
from pathlib import Path
from datetime import date
from lesson_plan import daily_focuses

PROFILE_PATH = Path("user_profile.json")

def load_user_profile():
    if PROFILE_PATH.exists():
        with open(PROFILE_PATH, "r") as f:
            return json.load(f)

    else:
        profile = {
                "user": "jasleen",
                "focus_progress": {},
                "last_session": {},
                "next_session": {}
            }
        
        # Inject first session plan
        focus, session_type = determine_next_session(profile)
        profile["next_session"] = {
            "focus": focus,
            "session_type": session_type,
            "feedback_recall": None
        }
    return profile

def save_user_profile(profile):
    with open(PROFILE_PATH, "w") as f:
        json.dump(profile, f, indent=4)

def update_focus_after_session(profile, focus, session_type, feedback_summary, duration):
    progress = profile["focus_progress"].setdefault(focus, {
        "preliminary_done": False, 
        "practice_session": 0, 
        "midterm_done": False,
        "last_feedback": ""
        })
        
    if session_type == "preliminary":
        progress["preliminary_done"] = True
    elif session_type == "practice":
        progress["practice_sessions"] +=1
    elif session_type == "midterm":
        progress["midterm_done"] = True

    progress["last_feedback"] = feedback_summary

    #record session history
    next_focus, next_type = determine_next_session(profile)
    profile["next_session"] = {
        "focus": next_focus,
        "session_type": next_type, 
        "feedback_recall": focus
        }

    save_user_profile(profile)

def determine_next_session(profile):
    progress = profile["focus_progress"]

    #randomize focus
    #focus_list = list(lesson_plan.keys)
    random.shuffle(daily_focuses)

    for focus in daily_focuses:
        stats = progress.setdefault(focus, {
        "preliminary_done": False, 
        "practice_sessions": 0, 
        "midterm_done": False,
        "last_feedback": ""
        })
        if not stats ["preliminary_done"]:
            return focus, "preliminary"
        elif stats["practice_sessions"] < 10:
            return focus, "practice"
        elif not stats ["midterm_done"]:
            return focus, "midterm"

    #if all focuses are complete, default to review/practice
    fallback_focus = sorted(progress.items(), key=lambda x: x[1]["practice_sessions"])[0][0]
    return fallback_focus, "practice"
