import streamlit as st
import requests
from datetime import datetime
from dotenv import load_dotenv
import os
from PIL import Image
import base64
from io import BytesIO

# Load API key
load_dotenv()
API_KEY = os.getenv("NASA_API_KEY", "DEMO_KEY")
BASE_URL = "https://api.nasa.gov/planetary/apod"

st.set_page_config(page_title="NASA APOD Explorer", page_icon="🌌", layout="centered")

st.title("🌌 NASA Astronomy Picture of the Day")
st.markdown("**Explore the universe, one picture at a time.**")

# Sidebar date picker
with st.sidebar:
    st.header("Search by Date")
    selected_date = st.date_input("Pick a date", datetime.today())
    search_btn = st.button("Search APOD")

# Fetch APOD
@st.cache_data(ttl=3600)
def get_apod(date=None):
    params = {"api_key": API_KEY}
    if date:
        params["date"] = date.strftime("%Y-%m-%d")
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("API Error. Check your key or try DEMO_KEY.")
        return None

# Main logic
date_str = selected_date.strftime("%Y-%m-%d") if search_btn else None
data = get_apod(date_str)

if data:
    st.subheader(f"📅 {data['date']}")
    st.markdown(f"### **{data['title']}**")

    # Image
    if data['media_type'] == 'image':
        img_response = requests.get(data['hdurl'])
        img = Image.open(BytesIO(img_response.content))
        st.image(img, use_column_width=True)

        # Download button
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        st.download_button(
            label="Download HD Image",
            data=img_str,
            file_name=f"apod_{data['date']}.png",
            mime="image/png"
        )
    else:
        st.video(data['url'])

    # Explanation
    with st.expander("Explanation"):
        st.write(data['explanation'])

    # Copyright
    if 'copyright' in data:
        st.caption(f"© {data['copyright']}")

else:
    st.info("Select a date and click 'Search APOD' or wait for today's picture.")

# Footer
st.markdown("---")
st.markdown("**Built with ❤️ for DTU Space MSc Application** | [GitHub](#)")
