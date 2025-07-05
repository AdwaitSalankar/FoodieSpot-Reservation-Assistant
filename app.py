import streamlit as st
from agent import ReservationAgent
import json
import time
import os
from utils import load_env

# Set page config
st.set_page_config(
    page_title="FoodieSpot",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load environment and initialize agent
@st.cache_resource
def get_agent():
    load_env()
    return ReservationAgent()

agent = get_agent()


# ---------- CSS Styling ----------
def local_css():
    st.markdown("""
    <style>
    html, body, [class*="css"] {
        font-family: 'Segoe UI', sans-serif;
        background: linear-gradient(to bottom, #ffffff 0%, #dbeafe 100%);
        height: 100%;
        margin: 0;
        padding: 0;
    }

    .hero {
        text-align: center;
        padding-top: 5vh;
        padding-bottom: 8vh;
    }

    .hero-label {
        display: inline-block;
        background: #f3f4f6;
        color: #111827;
        font-size: 0.85rem;
        padding: 0.5rem 1rem;
        border-radius: 999px;
        margin-bottom: 1rem;
        box-shadow: 0 1px 4px rgba(0,0,0,0.1);
    }

    .hero-title {
        font-size: 3.5rem;
        font-weight: 800;
        color: #ffffff;
        margin-bottom: 1rem;
        line-height: 1.2;
    }

    .highlight {
        color: #6aa0f7;
    }

    .hero-subtitle {
        font-size: 1.2rem;
        color: #98a2b5;
        max-width: 600px;
        margin-left: auto;
        margin-right: auto;
    }

    .cta-button {
        background-color: #3b82f6;
        color: white;
        font-size: 1rem;
        padding: 0.75rem 2rem;
        border-radius: 999px;
        border: none;
        cursor: pointer;
        transition: all 0.3s ease;
    }

    .cta-button:hover {
        background-color: #2563eb;
    }

    .cta-subtext {
        text-align: center;
        font-size: 0.9rem;
        color: #98a2b5;
    }
                
    .top-header {
        text-align: left;
        font-size: 1.5rem;
        font-weight: 800;
        color: #ffffff;
        line-height: 1.2;
    }
    .top-right {
        text-align: right;
    }

    </style>
    """, unsafe_allow_html=True)


# ---------- Main Chat App ----------
def main_app():
    st.title("🍽️ FoodieSpot Reservation Assistant")
    st.write("How can I help with your dining plans today?")

    st.sidebar.title("FoodieSpot")
    st.sidebar.markdown("Your personal dining assistant")

    if "messages" not in st.session_state:
        st.session_state.messages = [{
            "role": "assistant",
            "content": (
                "Welcome to FoodieSpot! What would you like to do today? Here are some options:\n\n"
                "- Get list of available restaurants\n"
                "- Make / Modify / Cancel a reservation\n\n"
                "Our Locations:\n"
                "- Downtown\n"
                "- Midtown\n"
                "- Uptown\n"
                "- Outskirts\n\n"
                "Our Cuisines:\n"
                "- North Indian\n"
                "- South Indian\n"
                "- Multicuisine\n\n"
                "You can begin by asking about available restaurants in an area."
            )
        }]

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat disabled toggle
    chat_enabled = False  # Toggle this to True to enable chat again

    if chat_enabled:
        # Chat input
        if prompt := st.chat_input("Type your message here..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                full_response = ""
                
                # Displaying
                for chunk in agent.process_message(prompt):
                    full_response += chunk
                    time.sleep(0.02)
                    message_placeholder.markdown(full_response + "▌")
                
                message_placeholder.markdown(full_response)

            st.session_state.messages.append({"role": "assistant", "content": full_response})
    
    else:
        # fake input box
        st.markdown("""
        <style>
        .chat-disabled {
            width: 100%;
            padding: 0.75rem 1rem;
            font-size: 1rem;
            border: 1px solid #ccc;
            border-radius: 25px;
            background-color: #3b404a;
            color: #9ca3af;
            pointer-events: none;
            opacity: 0.7;
            margin-top: 1rem;
            margin-bottom: 1rem;
        }
        </style>
        <input class="chat-disabled" type="text" value="Type you message here..." disabled>
        """, unsafe_allow_html=True)

        st.info("⚠️ Chat is currently disabled to prevent unnecessary usage of API credits.")

    # sidebar
    st.sidebar.subheader("📋 Your Reservations")

    try:
        json_path = os.path.join(os.path.dirname(__file__), "reservations.json")
        
        if not os.path.exists(json_path):
            st.sidebar.info("No reservations made yet")
        else:
            with open(json_path, "r") as f:
                reservations = json.load(f)
            
            if not reservations:
                st.sidebar.info("No reservations made yet")
            else:
                # toggle
                show_all = st.sidebar.checkbox("Show All Reservations", value=False)
                
                if show_all:
                    for i, res in enumerate(reservations, 1):
                        restaurant_name = next(
                            (r.name for r in agent.db.restaurants if r.id == res["restaurant_id"]),
                            f"Restaurant ID {res['restaurant_id']}"
                        )
                        st.sidebar.markdown(f"""
    **Reservation {i}**  
    **Reservation ID:** {res.get('id', 'N/A')}  
    **Restaurant Name:** {(restaurant_name)}  
    **Name:** {res.get('name', 'N/A')}  
    **Party Size:** {res.get('party_size', 'N/A')}  
    **Date:** {res.get('date', 'N/A')}  
    **Time:** {res.get('time', 'N/A')}  
    **Special Requests:** {res.get('special_requests', 'N/A') if res.get('special_requests') else 'N/A'}
                        """)
                        st.sidebar.markdown("---")
                else:
                    latest_res = reservations[-1]
                    restaurant_name = next(
                        (r.name for r in agent.db.restaurants if r.id == latest_res["restaurant_id"]),
                        f"Restaurant ID {latest_res['restaurant_id']}"
                        )
                    st.sidebar.markdown(f"""
    **Latest Reservation:**  
    **Reservation_id:** {latest_res.get('id', 'N/A')}  
    **Restaurant Name:** {(restaurant_name)}  
    **Name:** {latest_res.get('name', 'N/A')}  
    **Party Size:** {latest_res.get('party_size', 'N/A')}  
    **Date:** {latest_res.get('date', 'N/A')}  
    **Time:** {latest_res.get('time', 'N/A')}  
    **Special Requests:** {latest_res.get('special_requests', 'N/A') if latest_res.get('special_requests') else 'N/A'}
                    """)

    except json.JSONDecodeError:
        st.sidebar.error("Error reading reservation data")
    except Exception as e:
        st.sidebar.error(f"Couldn't load reservation: {str(e)}")

    st.sidebar.markdown("---")
    st.sidebar.subheader("Need Help?")

    with st.sidebar.expander("💡 Prompt Suggestions"):
        st.markdown("""
        **To find restaurants at a location:**
        - "Give me restaurants available in Downtown"
        - "Recommend restaurants in Midtown"
                    
        **Try these prompts to book a reservation:**
        - "Make a reservation at Boat House, 28th May, 8pm, for 15 people, under name Adwait, with a window seat"
        
        **Other useful prompts:**
        - "Change time to 9pm instead of 8pm in RES-40238"
        - "Cancel RES-40238"
        """)

    st.sidebar.markdown("---")

    st.sidebar.markdown("\n**About Me**\n")
    st.sidebar.markdown("👤 Made by [Adwait](https://github.com/AdwaitSalankar) ")

# ---------- Landing Page ----------
def landing_page():
    local_css()

    st.markdown("""
    <style>
    .navbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: transparent;  /* You can add background-color if needed */
        font-family: 'Segoe UI', sans-serif;
        font-size: 1.2rem;
        font-weight: 600;
    }

    .navbar-left {
        color: #ffffff;
    }

    .navbar-right {
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 0.95rem;
        color: #fffff;
        border-radius: 8px;
        box-shadow: 0 1px 4px rgba(0, 0, 0, 0.05);
    }
    .navbar-right img {
        vertical-align: middle;
        width: 32px;
    }
    </style>

    <div class="navbar">
        <div class="navbar-left">🍽️ FOODIESPOT</div>
        <div class="navbar-right">
            MADE USING 
            <img src="https://streamlit.io/images/brand/streamlit-mark-color.png" alt="Streamlit">
        </div>
    </div>
    """, unsafe_allow_html=True)

    if "start_chat" not in st.session_state:
        st.session_state.start_chat = False

    st.markdown("""
    <div class="hero">
        <div class="hero-label">✨ Your AI Dining Assistant</div>
        <div class="hero-title">
            The Conversational AI assistant<br>
            <span class="highlight">for your reservations.</span>
        </div>
        <div class="hero-subtitle">
            FoodieSpot helps you explore restaurants, book tables, and manage dining plans effortlessly with an intelligent assistant.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Centered button using columns
    col1, col2, col3 = st.columns([4, 2, 4])
    with col2:
        if st.button("Start Chatting →", use_container_width=True):
            st.session_state.start_chat = True
            st.rerun()

    # Subtext below the button
    st.markdown("<div class='cta-subtext'>Chat with the AI assistant to Make / Modify / Cancel a reservation</div>", unsafe_allow_html=True)

# ---------- Page Routing ----------
if st.session_state.get("start_chat", False):
    main_app()
else:
    landing_page()
