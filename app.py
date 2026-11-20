import streamlit as st
from groq import Groq
from urllib.parse import quote_plus
import os

st.set_page_config(
    page_title="Karnataka AI Tourist Guide",
    page_icon="🌍",
    layout="wide"
)

st.title(" Karnataka AI Tourist Guide")
st.subheader("Explore Karnataka with Artificial Intelligence")

st.write(
    "Ask anything about Karnataka tourist places, "
    "historical locations, temples, waterfalls and hill stations."
)

api_key = os.getenv("GROQ_API_KEY")

try:
    if not api_key:
        api_key = st.secrets["GROQ_API_KEY"]
except Exception:
    pass


places = {
    "Bagalkote": [
        "Badami Cave Temples",
        "Aihole",
        "Pattadakal",
        "Kudala Sangama"
    ],

    "Ballari": [
        "Ballari Fort",
        "Sandur"
    ],

    "Belagavi": [
        "Belagavi Fort",
        "Gokak Falls",
        "Kittur Fort",
        "Saundatti"
    ],

    "Bengaluru Rural": [
        "Devanahalli Fort",
        "Ghati Subramanya Temple"
    ],

    "Bengaluru Urban": [
        "Lalbagh Botanical Garden",
        "Cubbon Park",
        "Bangalore Palace",
        "Vidhana Soudha"
    ],

    "Bidar": [
        "Bidar Fort",
        "Bahmani Tombs",
        "Basavakalyan"
    ],

    "Chamarajanagar": [
        "Bandipur National Park",
        "BRT Tiger Reserve",
        "Male Mahadeshwara Hills"
    ],

    "Chikkaballapur": [
        "Nandi Hills",
        "Skandagiri",
        "Muddenahalli"
    ],

    "Chikkamagaluru": [
        "Mullayanagiri",
        "Baba Budangiri",
        "Kudremukh",
        "Kemmanagundi"
    ],

    "Chitradurga": [
        "Chitradurga Fort",
        "Vani Vilas Sagar"
    ],

    "Dakshina Kannada": [
        "Mangaluru",
        "Panambur Beach",
        "Dharmasthala",
        "Kukke Subramanya"
    ],

    "Davanagere": [
        "Kunduvada Lake",
        "Santhebennur"
    ],

    "Dharwad": [
        "Dharwad",
        "Hubballi",
        "Unkal Lake"
    ],

    "Gadag": [
        "Lakkundi",
        "Trikuteshwara Temple",
        "Dambal"
    ],

    "Hassan": [
        "Belur",
        "Halebidu",
        "Shravanabelagola"
    ],

    "Haveri": [
        "Ranebennur Blackbuck Sanctuary",
        "Bankapura"
    ],

    "Kalaburagi": [
        "Gulbarga Fort",
        "Sharana Basaveshwara Temple",
        "Sannati"
    ],

    "Kodagu": [
        "Madikeri",
        "Abbey Falls",
        "Dubare Elephant Camp",
        "Talacauvery",
        "Raja Seat"
    ],

    "Kolar": [
        "Kolaramma Temple",
        "Avani",
        "Kolar Gold Fields"
    ],

    "Koppal": [
        "Anegundi",
        "Itagi Mahadeva Temple",
        "Munirabad"
    ],

    "Mandya": [
        "Srirangapatna",
        "Shivanasamudra Falls",
        "Melukote",
        "Kokkarebellur"
    ],

    "Mysuru": [
        "Mysore Palace",
        "Chamundi Hills",
        "Somanathapura Temple",
        "Brindavan Gardens"
    ],

    "Raichur": [
        "Raichur Fort",
        "Hatti Gold Mines"
    ],

    "Ramanagara": [
        "Ramanagara Hills",
        "Kanakapura"
    ],

    "Shivamogga": [
        "Jog Falls",
        "Agumbe",
        "Kodachadri",
        "Sakrebailu",
        "Keladi"
    ],

    "Tumakuru": [
        "Devarayanadurga",
        "Madhugiri Fort",
        "Siddaganga"
    ],

    "Udupi": [
        "Sri Krishna Matha",
        "Malpe Beach",
        "St Mary's Island",
        "Kaup Lighthouse",
        "Maravanthe Beach"
    ],

    "Uttara Kannada": [
        "Gokarna",
        "Murudeshwar",
        "Yana",
        "Dandeli",
        "Karwar"
    ],

    "Vijayanagara": [
        "Hampi",
        "Virupaksha Temple",
        "Vijaya Vittala Temple"
    ],

    "Vijayapura": [
        "Gol Gumbaz",
        "Ibrahim Rauza",
        "Almatti Dam"
    ],

    "Yadgir": [
        "Yadgir Fort",
        "Shorapur"
    ]
}

def google_maps_link(place):

    query = quote_plus(place + ", Karnataka, India")

    return (
        "https://www.google.com/maps/search/?api=1&query="
        + query
    )

def ask_ai(question):

    client = Groq(api_key=api_key)

    prompt = f"""
    You are a knowledgeable Karnataka tourism assistant.

    Answer the user's questions about Karnataka, India.

    Your responsibilities:
    1. Explain tourist places in simple English.
    2. Mention the district of the place when known.
    3. Explain historical and cultural importance.
    4. Suggest other nearby attractions when relevant.
    5. Give useful travel information.
    6. Do not invent locations or facts.
    7. If you are unsure, clearly mention that.
    8. Keep the answer well structured.

    User question: {question}
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "You are a Karnataka tourism expert."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.4,
        max_tokens=1200
    )

    return response.choices[0].message.content

st.sidebar.title("📍 Explore Districts")

selected_district = st.sidebar.selectbox(
    "Select Karnataka District",
    ["All Districts"] + list(places.keys())
  

st.header(" Explore Tourist Places")

if selected_district == "All Districts":

    for district, locations in places.items():

        with st.expander(district):

            for place in locations:

                link = google_maps_link(place)

                st.markdown(
                    f"- **{place}** | "
                    f"[📍 View on Google Maps]({link})"
                )

else:

    st.subheader(selected_district)

    for place in places[selected_district]:

        link = google_maps_link(place)

        st.markdown(
            f"📍 **{place}** "
            f"[Open Google Maps]({link})"
        )


st.divider()

st.header(" Ask Karnataka AI")

question = st.text_area(
    "Enter your question:",
    placeholder="Example: What are the best places to visit in Coorg?"
)

if st.button("Generate AI Answer"):

    if not api_key:

        st.error(
            "Groq API key is missing. "
            "Please configure GROQ_API_KEY."
        )

    elif not question.strip():

        st.warning("Please enter a question.")

    else:

        with st.spinner("AI is preparing your answer..."):

            try:

                answer = ask_ai(question)

                st.success("AI Answer")

                st.markdown(answer)

                st.markdown(
                    "[🔗 Search this question on Google Maps]("
                    + google_maps_link(question)
                    + ")"
                )

            except Exception as e:

                st.error(f"Error: {e}")



st.divider()

st.caption(
    "Karnataka AI Tourist Guide | "
    "Powered by Python, Streamlit and Groq AI"
)

st.caption(
    "Explore Karnataka – One Place at a Time "
)
