import streamlit as st
import requests
from PIL import Image
from io import BytesIO

st.title("🖼️ AI Image Generator")


if "messages" not in st.session_state:
    st.session_state.messages = []


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["role"] == "assistant" and message.get("image"):
            st.image(message["image"])
        else:
            st.markdown(message["content"])


if user_prompt := st.chat_input("Describe an image..."):

    # Display and save user message
    with st.chat_message("user"):
        st.markdown(user_prompt)

    st.session_state.messages.append({
        "role": "user",
        "content": user_prompt
    })

    
    url = f"https://image.pollinations.ai/prompt/{user_prompt}"
    response = requests.get(url)

    with st.chat_message("assistant"):
        if response.status_code == 200:
            image = Image.open(BytesIO(response.content))
            st.image(image, caption=user_prompt)

        
            st.session_state.messages.append({
                "role": "assistant",
                "content": f"Generated image for: **{user_prompt}**",
                "image": image
            })
        else:
            st.error("Failed to generate image.")
            st.session_state.messages.append({
                "role": "assistant",
                "content": "Failed to generate image."
            })
