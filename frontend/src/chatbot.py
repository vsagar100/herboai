import streamlit as st
from PIL import Image
from datetime import datetime
import random

# Dummy data for demonstration
herbal_plants = [
    {
        "name": "Ashwagandha",
        "image": "https://upload.wikimedia.org/wikipedia/commons/6/6d/Withania_somnifera_-_K%C3%B6hler%E2%80%93s_Medizinal-Pflanzen-283.jpg",
        "used_for": ["Stress relief", "Immunity booster", "Energy enhancement"],
        "ayush_system": "Ayurveda",
        "remedies": ["Prepare Ashwagandha tea for daily consumption", "Use with warm milk before bed"]
    },
    {
        "name": "Tulsi",
        "image": "https://upload.wikimedia.org/wikipedia/commons/3/3a/Ocimum_tenuiflorum2.jpg",
        "used_for": ["Cough and cold", "Respiratory health", "Immunity"],
        "ayush_system": "Ayurveda",
        "remedies": ["Add Tulsi leaves to boiling water and inhale steam", "Drink Tulsi-infused herbal tea"]
    }
    # Add more plants here
]

st.set_page_config(page_title="HerboAI - Virtual Herbal Garden", layout="wide")

st.markdown("""
    <style>
    .big-font {
        font-size:32px !important;
        font-weight: 700;
        color: #2c3e50;
    }
    .herbal-box {
        border: 1px solid #dee2e6;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 2px 2px 8px rgba(0,0,0,0.05);
        background-color: #f8f9fa;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🌿 HerboAI – Virtual Herbal Garden")
st.markdown("""<p class="big-font">Discover AYUSH-based remedies and medicinal plants, guided by AI.</p>""", unsafe_allow_html=True)

with st.expander("🔍 Search Herbal Plants and Remedies"):
    search_term = st.text_input("Enter plant name or symptom (e.g., 'cough', 'stress', 'Ashwagandha')")

    if search_term:
        results = [plant for plant in herbal_plants if search_term.lower() in plant['name'].lower() or any(search_term.lower() in u.lower() for u in plant['used_for'])]

        if results:
            for plant in results:
                st.markdown(f"<div class='herbal-box'>", unsafe_allow_html=True)
                st.image(plant['image'], width=200)
                st.markdown(f"### 🌱 {plant['name']}")
                st.markdown(f"**AYUSH System**: {plant['ayush_system']}")
                st.markdown(f"**Uses**: {', '.join(plant['used_for'])}")
                st.markdown(f"**Remedies**:")
                for rem in plant['remedies']:
                    st.markdown(f"- {rem}")
                st.markdown("</div>", unsafe_allow_html=True)
                st.markdown("---")
        else:
            st.warning("No herbal remedies found for your query. Try another keyword.")

st.markdown("---")

st.subheader("🌿 Featured Herbal Remedy of the Day")
featured = random.choice(herbal_plants)
st.image(featured['image'], width=300)
st.markdown(f"### 🌱 {featured['name']}")
st.markdown(f"**Used for**: {', '.join(featured['used_for'])}")
st.markdown(f"**Recommended Remedy**: {random.choice(featured['remedies'])}")

st.markdown("---")

st.info("🔧 Admin Panel coming soon — add/edit plant details to improve AI suggestions.")
