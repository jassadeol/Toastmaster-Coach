

""" Jasleen Deol
    Date: June 24, 2025
    Description: core logic that runs the coaching session, prompts, processes and analyzes speech
    Future: further metrics, further customization of lesson plan, users have accounts and progress is monitored
    grab information from articles or online to create lessons of own 
"""


#import for audio processing, speech transcription, logging and GPT API Calls, time and system
import pyaudio, wave, whisper, nltk, openai
import os, time, sys, random, json
from openai import OpenAI
from datetime import datetime
from lesson_plan import get_today_focus, get_random_prompt
from focus_modules import focus_library
from dotenv import load_dotenv
from session_logger import create_session_folder, log_session
from user_profile import load_user_profile, update_focus_after_session


#download natural language toolkit assets for speech analysis
#i.e stopwords, filler words
nltk.download('stopwords')

#assigned OpenAI Api key for GPT integration
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# core functionality
SESSION_DURATION = 30

# -- Card Display Helpers --
# -------- Sample Data -------- #
daily_focuses = [
    "Reduce filler words",
    "Enhance vocal variety",
    "Practice impromptu speaking",
    "Master transitions between ideas",
    "Present with persuasive clarity"
]

lesson_plan = {
    focus: {
        "description": f"This is a sample lesson description for '{focus}'.",
        "example_prompt": f"Example prompt for '{focus}'."
    } for focus in daily_focuses
}
# Simulated past performance
"""user_profile = {
    "user": "Jasleen",
    "focus_progress": {
        "Present with persuasive clarity": {
            "preliminary_done": True,
            "practice_sessions": 2,
            "midterm_done": False,
            "last_feedback": "Try closing with a stronger call-to-action."
        }
    },
    "next_session": {
        "focus": "Present with persuasive clarity",
        "session_type": "practice",
        "feedback_recall": None
    }
}
"""
# ----- ^ above to be deleted --------
def display_start_card(profile):
    focus = profile["next_session"]["focus"]
    session_type = profile["next_session"]["session_type"]
    stats = profile["focus_progress"].get(focus, {
        "preliminary_done": False,
        "practice_sessions": 0, 
        "midterm_done": False, 
        "last_feedback": ""
        })
    prompt = lesson_plan[focus]["example_prompt"]

    print(f"""
    Toastmaster Coach: Session Preview

    > User: {profile['user']}
    > Focus Area: {focus}
    > Prompt: {prompt}
    > Last WPM: 132 | Filler Words: 5 | Session #{stats['practice_sessions'] + 1}
    
    Type 'listen' to hear the lesson overview (simulated)
    Type 'feedback' to read previous feedback for this focus 
    Type 'start' when ready to begin
    """)

def display_post_session_card(focus, session_num, retry_num, wpm, filler_count, disfluencies, tip):
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print (f"""
    Session Feedback Summary - Attempt #{session_num +1} # Attempt {retry_num+1}

    > Time: {time_now}
    > Focus Area: {focus}
    > WPM: {wpm} | Fillers: {filler_count} | disfluencies: {', '.join(disfluencies)}
    
    What You Did Well
    - Opened strong wih a confident one
    - Maintained steady pacing
    
    Suggested Improvement
    {tip} 
    Click (simulated audio feedback available)
    Type 'retry' to do another attempt
    Type 'progress' to view updated stats
    Type 'continue' for the next session""")


#Function: Live audio recording into .wav file
def record_audio(filename, session_number, duration):
    #initialize mic input using PyAudio
    RATE = 16000
    CHUNK = 1024
    #filename = os.path.join(folder, f"speech_{str(session_number).zfill(2)}.wav")

    p = pyaudio.PyAudio()

    stream = p.open(format=pyaudio.paInt16, channels=1, rate=RATE, input=True, frames_per_buffer=CHUNK)
    print("Recording... start speaking (CTRL+C to cancel)\n")
    frames = []

    start_time = time.time()
    end_time = start_time + duration
    
    #collect audio in small chunks for the duration set
    while time.time() < end_time:
        data = stream.read(CHUNK)
        frames.append(data)

        remaining = int(end_time - time.time())
        mins, secs = divmod(remaining, 60)
        timer_display = f"\r Time left: {mins:02d} : {secs:02d}"
        sys.stdout.write(timer_display)
        sys.stdout.flush()
    
    
    #clean up audio stream 
    stream.stop_stream(); stream.close(); p.terminate()
    
    #write to WAV file
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))

    print("\nRecording complete.\n")

#Function: transcribe audio file to text for analysis
def transcribe_audio(filename):
    model=whisper.load_model("base")
    result = model.transcribe(filename)
    return result["text"]

#Function: detect filler words from speech and print basic metrics
def analyze_speech(text, cheatsheet):
    words = text.split()

    filler_count = sum(1 for word in words if word.lower() in cheatsheet)

    new_fillers = {word for word in words if word.lower() not in cheatsheet and word.lower() in ['uhh', 'err', 'hmm']}

    wpm = len(words)/3

    print("Basic Metrics:")
    print(f"Total words: {len(words)}")
    print(f"Filler words detected: {filler_count}")
    print(f"Other disfluencies: {', '.join(new_fillers) if new_fillers else 'None'}")
    print(f"Estimated words per minute: {wpm:.2f}")

    return filler_count, list(new_fillers), wpm

#Function: return feedback on speech using from gpt
def gpt_feedback(text, focus):
    system_msg = f"You are a speech coach. Give helpful, constructive feedback for the following speech. Focus especially on '{focus}'. Keep your tone encouraging but specific. "

    response = client.chat.completions.create(
        model="gpt-4.1-nano",
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": text}
            ]
        )

    feedback = response.choices[0].message.content

    print ("\nCoach GPT Feedback: \n ", feedback)
    return feedback


#Function: keep journal of each session to monitor progress with time and focus type
def log_session(folder, session_number, session_type, focus, prompt, transcript, feedback, filler_count, extras, wpm):
    os.makedirs("logs", exist_ok=True)
    #filename = f"logs/{session_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    filename = os.path.join(folder, f"{focus}_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{session_type}_{str(session_number).zfill(2)}.txt")
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"Date: {datetime.now()} \nFocus: {focus} \nPrompt: {prompt} \n\n --- Transcript --- \n{transcript}\n")
        f.write(f"\n -- Metrics --\n Filler Words: {filler_count}\nNew Disfluencies: {extras}\n\nWords per Minute: {wpm}\n\n")
        f.write(f"\n -- GPT Feedback --\n{feedback}\n")

#Function: explain the lesson, along with examples for speech preparation 
def display_focus_material(focus):
    mat = focus_library.get(focus)
    if mat:
        print(f"""
        {mat['description']}
        Filler/Flaws to avoid: {', '.join(mat['cheatsheet'])}
        Bad Example: {mat['examples']['bad']}
        Better Version: {mat['examples']['good']} """)
    return mat['cheatsheet'] if mat else []
def run_pre_session_intro():
    display_start_card(user_profile)
    while True:
        ready = input(">> ").strip().lower()
        if ready == "listen":
            print("\nPlaying audio ...\n")
            time.sleep(2)
        elif ready == "feedback":
            print("\nPrevious feedback:")
            print (user_profile["focus_progress"][user_profile["next_session"]["focus"]]["last_feedback"]+ "\n")
        elif ready == "start":
            break
def run_attempt(retry_count, session, focus, attempts):
    print(f"\nRecording: Session {session + 1}, Attempt {retry_count+1} ...")
    time.sleep(3)

    #simulate output
    wpm = random.randint(50, 120)
    filler_count = random.randint(0, 6)
    disfluencies = random.sample(["uh", "um", "like", "you know"], k=2)
    tip = random.choice([
        "Try to conclude with clearer call-to-action", 
        "Watch for fillers mid-paragraph - they dilute momentum", 
        "Your transitions need tightening between points",
        ])
                
    #post session logic
    display_post_session_card(
        focus=user_profile["next_session"]["focus"],
        session_num = session,
        retry_num = retry_count,
        wpm=wpm, 
        filler_count=filler_count, 
        disfluencies=disfluencies, 
        tip=tip)

    attempts.append({
        "attempt_num" : retry_count+1, 
        "wpm": wpm, 
        "fillers": filler_count, 
        "disfluencies": disfluencies, 
        "tip": tip,
        "timestamp": datetime.now().isoformat()

    })

def run_terminal_coaching():
    #change to a do..while loop so that display_start_card is called after session ends
    #session = 0
    session_count = input("How many sessions would you like to do today? ")
    try:
        session_count = int(session_count)
    except:
        print("Invalid input. Defaulting to one session.")
        session_count = 1

    focus, session_type, prompt = get_today_focus(profile=user_profile)
    
    #pre-session logic 
    for session in range(session_count):
        retry_count = 0
        retry_limit = 2
        attempts = []
        focus = user_profile["next_session"]["focus"]
        
        run_pre_session_intro()
        run_attempt(retry_count, session, focus, attempts)
        
        #start_signal = input("Press enter when ready to begin recording:  ")
        #if start_signal == "":

        #for session in range(1, session_count+1):
        while retry_count < retry_limit:
            #cmd = input("Type 'retry' to try this exercise again or 'continue''progress', or press Enter to continue: ").strip().lower()
            if retry_count >= retry_limit:
                print("You have reached the max retry attempts. Moving on")
                break
            cmd = input(">> ")
            if cmd == "retry":
                retry_count +=1 
                run_attempt(retry_count, session, focus, attempts)
            elif cmd == "progress":
                print("\n Updated stats")
                print (user_profile["focus_progress"][user_profile["next_session"]["focus"]]["last_feedback"]+ "\n")
                continue
            elif cmd == "continue":
                break
            else:
                print("Invalid input. Continue to next session please.")
                break
                
            # TODO: log_session(focus, session_number + s, attempts)
        
        print(f"\n Session {session + 1} complete.\n")
        log_session(
            base_folder="logs", 
            focus=focus, 
            session_type=session_type,
            session_number=session, 
            attempts=attempts)
        #display_start_card(user_profile)
     
#turns feedback data into valid Adaptive Card JSON
def build_feedback_card(session_num, attempt_num, metrics, strengths, feedback):
    return {
        "type": "AdaptiveCard",
        "version": "1.5",
        "body": [
            {"type": "TextBlock", "text": f"Feedback - Session {session_num}, Attempt {attempt_num}", "weight": "Bolder", "size": "Large"},
            {"type": "FactSet", "facts": [
                {"title": "WPM", "value": str(metrics["wpm"])},
                {"title": "Fillers", "value": str(metrics["fillers"])},
                {"title": "Disfluencies", "value": ", ".join(metrics["disfluencies"])}
            ]},
            {"type": "TextBlock", "text": "What You Did Well", "weight": "Bolder", "spacing": "Medium"},
            {"type": "TextBlock", "text": "\n".join(f"- {s}" for s in strengths), "wrap": True},
            {"type": "TextBlock", "text": "Suggested Improvement", "weight": "Bolder", "spacing": "Medium"},
            {"type": "TextBlock", "text": feedback, "wrap": True}
        ],
        "actions": [
            {"type": "Action.Submit", "title": "Retry", "data": {"action": "retry"}},
            {"type": "Action.Submit", "title": "View Progress", "data": {"action": "progress"}},
            {"type": "Action.Submit", "title": "Continue", "data": {"action": "continue"}}
        ]
    }        

#if __name__ == "__main__":
#    run_terminal_coaching()
        
#Function: core logic, step by step process from start to end of Coach
def run_coaching_loop():
     
     profile = load_user_profile()
     focus, session_type, prompt = get_today_focus(profile=profile)
     if 0 < profile["focus_progress"][focus]["practice_sessions"] < 10:
         session_number = profile["focus_progress"][focus]["practice_sessions"]
     else:
        session_number = 0


     print(f"\nToday's Focus: {focus} ({session_type})")
     cheatsheet = display_focus_material(focus)

     input(f"\nPrompt: {prompt} \nPress Enter when ready to begin your {(SESSION_DURATION/60):.1f} min(s) speech...")

     #grab file name and file path
     date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
     session_folder = create_session_folder(focus=focus, session_type=session_type, date=date, session_number=session_number)
     filename = os.path.join(
         session_folder, 
         f"speech_{str(session_number).zfill(2)}.wav"
         )

     #main meat
     record_audio(filename, session_number, duration=SESSION_DURATION)
     transcript = transcribe_audio(filename)

     #grab feedback and log it
     filler_count, extras, wpm = analyze_speech(transcript, cheatsheet)
     feedback = gpt_feedback(transcript, focus)
     log_session(session_folder, session_number, session_type, focus, prompt, transcript, feedback, filler_count, extras, wpm)

     update_focus_after_session(profile, focus=focus, session_type=session_type, feedback_summary=feedback,duration=SESSION_DURATION)

     print("\n Session complete and profile saved.")

#Function: entry point to program, prompt user for # of sessions
if __name__ == "__main__":
    print("Welcome to your Personal Toastmaster Coach")

    rounds = int(input(f"How many rounds would you like in today's session (i.e. 2 or 3)?\n"))

    for i in range(rounds):
        print(f"\nRound {i+1} of {rounds}")
        run_coaching_loop()
        

 #run server locally
"""if __name__ == "__main__":
    mode = input("Run as (1) terminal coach or (2) website\n")
    if mode =="1":
        run_coaching_loop()
    elif mode == "2":
        pass
"""