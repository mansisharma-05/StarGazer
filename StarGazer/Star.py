import streamlit as st
import numpy as np
import pandas as pd
import pickle
import random
from datetime import date,time
import pytz
import math

# CSS for highlighted content box with glowing bullet points
highlight_box = """
<style>
.content-box {
    background: rgba(15, 15, 15, 0.4);
    padding: 32px;
    border-radius: 17px;
    color: white;
}
</style>
"""

st.markdown(highlight_box, unsafe_allow_html=True)

# Wrap content inside the box
st.markdown("""
    <div style="text-align: center; padding: 40px; 
                background-color:rgba(15, 15, 15, 0.6);; border-radius: 20px;">
        <h1 style="color: #ffd300; font-size: 5rem; font-weight: 800; 
                   letter-spacing: 2px; 
                   text-shadow: 0 0 10px rgba(255, 211, 0, 0.5);">
            🔮 StarGazer
        </h1>
        <p style="color: #ffd300; font-size: 1.3rem; opacity: 0.9;">
            Because the stars know your story.
        </p>
        </div>
""", unsafe_allow_html=True)
    


st.image('https://cdn.discovermagazine.com/assets/image/46516/shutterstock_1506783812-x.jpg')

with open('StarGazer.pkl','rb') as f:
    chatgpt = pickle.load(f)

page_bg = """
<style>
[data-testid="stAppViewContainer"] {
    background:
        linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)),
        url("https://sprinklesofstyle.co.uk/wp-content/uploads/2020/11/original-astrology.gif");
    background-size: 270px 270px;
    background-repeat: repeat;
    background-attachment: fixed;
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# Try to import high-precision astrology libs (optional)
HAS_KERYKEION = False
HAS_SWISS = False
try:
    import kerykeion as ky  # optional: nicer high-level natal chart tool
    HAS_KERYKEION = True
except Exception:
    try:
        import swisseph as swe  # Python wrapper for Swiss Ephemeris
        HAS_SWISS = True
    except Exception:
        # fallbacks will be used (approximate positions)
        pass

# ---------- CONFIG ----------
HOROSCOPE_API_KEY = ""  # <- put your API key here (optional). e.g., API-Ninjas or AstrologyAPI key.
HOROSCOPE_PROVIDER = "api_ninjas"  # options: "api_ninjas", "astrologyapi", "local"
# -------------------------

# --- Header ---
st.markdown("""
<p style='
    font-size: 24px; 
    font-weight: 600; 
    text-align: center; 
    color: #FFD700;
    text-shadow: 0 0 10px #FFD700, 0 0 20px #ffdd55;
'>
Every soul begins it's journey with a single breath under a specific sky. Let's decode the stellar signature of that exact moment.
</p>
""", unsafe_allow_html=True)
# --- Input Box ---
st.write("### Enter your details")
name = st.text_input("Your name")
dob = st.date_input(
    "Date of Birth", 
    min_value=date(1950,1,1), 
    max_value=date(2025,12,31)
)

# Zodiac Sign Calculation
def get_zodiac(month, day):
    signs = [
        ("Capricorn", (12, 22), (1, 19)),
        ("Aquarius", (1, 20), (2, 18)),
        ("Pisces", (2, 19), (3, 20)),
        ("Aries", (3, 21), (4, 19)),
        ("Taurus", (4, 20), (5, 20)),
        ("Gemini", (5, 21), (6, 20)),
        ("Cancer", (6, 21), (7, 22)),
        ("Leo", (7, 23), (8, 22)),
        ("Virgo", (8, 23), (9, 22)),
        ("Libra", (9, 23), (10, 22)),
        ("Scorpio", (10, 23), (11, 21)),
        ("Sagittarius", (11, 22), (12, 21)),
    ]
    for sign, start, end in signs:
        if (month == start[0] and day >= start[1]) or (month == end[0] and day <= end[1]):
            return sign

# Personality Traits (simple dictionary)
traits = {
    "Aries": "Bold, energetic, and unstoppable.",
    "Taurus": "Strong-willed, stable, deeply loving.",
    "Gemini": "Curious, witty, and expressive.",
    "Cancer": "Emotional, intuitive, nurturing.",
    "Leo": "Confident, radiant, natural leader.",
    "Virgo": "Analytical, calm, perfection-seeking.",
    "Libra": "Balanced, charming, harmony-seeking.",
    "Scorpio": "Mysterious, powerful, deeply emotional.",
    "Sagittarius": "Adventurous, philosophical, free-spirited.",
    "Capricorn": "Ambitious, disciplined, hardworking.",
    "Aquarius": "Innovative, humanitarian, visionary.",
    "Pisces": "Dreamy, empathetic, artistic."
}

lucky_color = {
    "Aries": "Red", "Taurus": "Green", "Gemini": "Yellow", "Cancer": "White",
    "Leo": "Gold", "Virgo": "Blue", "Libra": "Pink", "Scorpio": "Black",
    "Sagittarius": "Purple", "Capricorn": "Brown", "Aquarius": "Silver", "Pisces": "Sea Blue"
}

lucky_stone = {
    "Aries": "Diamond", "Taurus": "Emerald", "Gemini": "Agate", "Cancer": "Pearl",
    "Leo": "Ruby", "Virgo": "Sapphire", "Libra": "Opal", "Scorpio": "Topaz",
    "Sagittarius": "Turquoise", "Capricorn": "Garnet", "Aquarius": "Amethyst", "Pisces": "Moonstone"
}

lucky_day = {
    "Aries": "Tuesday", "Taurus": "Friday", "Gemini": "Wednesday", "Cancer": "Monday",
    "Leo": "Sunday", "Virgo": "Wednesday", "Libra": "Friday", "Scorpio": "Tuesday",
    "Sagittarius": "Thursday", "Capricorn": "Saturday", "Aquarius": "Saturday", "Pisces": "Thursday"
}

messages = [
    "The universe is aligning a new beginning for you.",
    "Trust the timing of your life.",
    "Your energy will attract miracles today.",
    "Let go of what you can’t control. Peace follows.",
    "Something beautiful is on its way to you.",
]

import random

# --- Predict ---
if name and dob:
    zodiac = get_zodiac(dob.month, dob.day)
    
    st.markdown("<hr style='border:1px solid #FFD700;'>", unsafe_allow_html=True)
    st.markdown(f"""
    <h2 style='color:#FFD700;'>✨ Hello {name}, here is your cosmic guide:</h2>
    <p style='font-size:20px;'><b>Zodiac Sign:</b> {zodiac}</p>
    <p style='font-size:20px;'><b>Personality:</b> {traits[zodiac]}</p>
    <p style='font-size:20px;'><b>Lucky Color:</b> {lucky_color[zodiac]}</p>
    <p style='font-size:20px;'><b>Lucky Stone:</b> {lucky_stone[zodiac]}</p>
    <p style='font-size:20px;'><b>Lucky Day:</b> {lucky_day[zodiac]}</p>
    <p style='font-size:22px; color:#C084FC; margin-top:20px;'>
        🌌 <i>Message from the Universe:</i><br>{random.choice(messages)}
    </p>
    """, unsafe_allow_html=True)


st.markdown("---")
st.markdown("Developed by **Mansi Sharma & Ashmeet Singh**")
    