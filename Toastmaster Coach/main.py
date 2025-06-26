
""" Jasleen Deol
    Date: June 24, 2025
    Description: core logic that runs the coaching session, prompts, processes and analyzes speech
    Future: further metrics, further customization of lesson plan, users have accounts and progress is monitored
    grab information from articles or online to create lessons of own 
"""

#import for audio processing, speech transcription, logging and GPT API Calls, time and system
import pyaudio, wave, whisper, nltk, openai
import os, time, sys
from openai import OpenAI
from datetime import datetime
from lesson_plan import get_today_focus, get_random_prompt
from focus_modules import focus_library
from dotenv import load_dotenv
from session_logger import create_session_folder
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

#Function: core logic, step by step process from start to end of Coach
def run_coaching_loop():
     #session_type = input("Session type (practice/prelim/midterm/final): ").strip().lower()
     profile = load_user_profile()
     focus, session_type, prompt = get_today_focus(profile=profile)
     #prompt = get_random_prompt()
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