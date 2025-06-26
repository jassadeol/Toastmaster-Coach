"""Jasleen Deol
   Date: June 23, 2025
   Purpose: file to store daily topics and prompt
   Future: automate prompts and curriculum; 
            ensure focuses match user's progress
"""
import random
from datetime import datetime

daily_focuses = [
    "Reduce filler words",
    "Enhance vocal variety", 
    "Practice impromptu speaking", 
    "Master transitions between ideas", 
    "Present with persuasive clarity"
    ]

#currently hardcoded but will be a themed list
prompts = [
    "Should failure be celebrated?",
    "What's a small habit that changed your life?", 
    "Pitch a fictional invention to investors", 
    "Describe your ideal utopia"
    "Explain something complex like you're taking to a 5 year old"

    ]

def get_today_focus(profile):
    next_session = profile.get("next_session", {})
    return next_session.get("focus"), next_session.get("session_type"), random.choice(prompts)

#    return daily_focuses[datetime.now().day % len(daily_focuses)]

def get_random_prompt():
    return random.choice(prompts)
