import streamlit as st
from streamlit_extras.let_it_rain import rain

# Page config
st.set_page_config(page_title="Will You Be My Valentine? 💖", page_icon="❤️")

# Initialize session state
if "step" not in st.session_state:
    st.session_state.step = 1

if "yes_size" not in st.session_state:
    st.session_state.yes_size = 20

# Background
st.markdown("""
<style>
body {
    background-color: #ffe6ea;
}
</style>
""", unsafe_allow_html=True)

# YES CLICKED → FINAL PAGE
if st.session_state.step == "yes":
    rain(emoji="❤️", font_size=54, falling_speed=5, animation_length=4)
    st.markdown(
        "<h1 style='text-align:center; color:#e6005c;'>YAYYY 💖💖💖</h1>",
        unsafe_allow_html=True
    )
    st.success("I knew you’d say yes 😄❤️")
    st.balloons()
    st.stop()

# Normal pages
st.markdown(
    "<h1 style='text-align:center; color:#e6005c;'>Alexandria stone, Will you be my Valentine? 💌</h1>",
    unsafe_allow_html=True
)

messages = {
    1: "Think about it again 🥺",
    2: "Are you sureee? 😭",
    3: "This is getting painful 💔",
    4: "I am on my knees now 🧎‍♂️",
    5: "why are you like this? 😢",
    6: "I thought you loved me? 😞",
    7: "This is just sad now 😭",
    8: "I am crying 😢😭",
    9: "Last chance! 😩",
    10: "Okay this YES button is unavoidable 😌"
}

st.markdown(
    f"<h3 style='text-align:center;'>{messages.get(st.session_state.step, 'Just say yes already 😭❤️')}</h3>",
    unsafe_allow_html=True
)

#  STYLE ONLY THE YES BUTTON (stable selector)
st.markdown(f"""
<style>
button[data-testid="baseButton-primary"][id*="yes_btn"] {{
    font-size: {st.session_state.yes_size}px !important;
    padding: 15px 40px !important;
    background-color: #e6005c !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
}}
</style>
""", unsafe_allow_html=True)

# Buttons
col1, col2 = st.columns(2)

with col1:
    if st.button("YES 💖", key="yes_btn"):
        st.session_state.step = "yes"
        st.rerun()

with col2:
    if st.button("No 🙈", key="no_btn"):
        st.session_state.step += 1
        st.session_state.yes_size += 10
        st.rerun()

st.caption("There is no escape 😌❤️")
