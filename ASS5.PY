import streamlit as st
import requests
import random
from PIL import Image
from io import BytesIO

st.set_page_config(page_title="AI Image Studio", page_icon="🎨", layout="wide")

st.title("🎨 AI Image Studio")
st.write("Generate stunning AI images with customizable settings!")


if "messages" not in st.session_state:
    st.session_state.messages = []


st.sidebar.header("⚙️ Image Settings")

art_style = st.sidebar.selectbox(
    "Choose Art Style",
    [
        "Realistic",
        "Anime",
        "Fantasy",
        "Cyberpunk",
        "Oil Painting",
        "Pixel Art",
        "Watercolor",
        "Digital Art"
    ]
)

width = st.sidebar.slider(
    "Image Width",
    min_value=256,
    max_value=1024,
    value=512,
    step=64
)

height = st.sidebar.slider(
    "Image Height",
    min_value=256,
    max_value=1024,
    value=512,
    step=64
)

magic_enhance = st.sidebar.checkbox("✨ Enable Magic Enhance")

# -----------------------------
# Surprise Prompts
# -----------------------------
surprise_prompts = [
    "An astronaut riding a horse on Mars",
    "A cyberpunk street food vendor in Tokyo",
    "A dragon drinking coffee in New York",
    "A medieval knight using a laptop",
    "A floating castle above the clouds"
]


for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg.get("image") is not None:
            st.image(msg["image"], caption=msg.get("caption", ""))
        else:
            st.markdown(msg["content"])


def generate_image(prompt):

    full_prompt = f"{prompt}, {art_style}"

    if magic_enhance:
        full_prompt += ", masterpiece, 8k resolution, highly detailed, trending on artstation, unreal engine 5 render"

    url = (
        f"https://image.pollinations.ai/prompt/{full_prompt}"
        f"?width={width}&height={height}"
    )

    with st.spinner("🎨 Generating your masterpiece..."):

        response = requests.get(url)

        if response.status_code == 200:

            image = Image.open(BytesIO(response.content))

            with st.chat_message("assistant"):

                st.image(
                    image,
                    caption=f"{prompt} ({art_style})",
                    use_container_width=True
                )

                st.success("Image generated successfully!")

                st.download_button(
                    label="📥 Download Image",
                    data=response.content,
                    file_name=f"{art_style.lower().replace(' ','_')}_image.png",
                    mime="image/png"
                )

                st.code(full_prompt, language="text")

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": f"Generated image for **{prompt}**",
                    "image": image,
                    "caption": prompt
                }
            )

        else:

            with st.chat_message("assistant"):
                st.error("❌ Failed to generate image.")

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": "Failed to generate image."
                }
            )



if st.button("🎲 Surprise Me!"):

    prompt = random.choice(surprise_prompts)

    with st.chat_message("user"):
        st.markdown(prompt)

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    generate_image(prompt)



user_prompt = st.chat_input("Describe an image...")

if user_prompt:

    with st.chat_message("user"):
        st.markdown(user_prompt)

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_prompt
        }
    )

    generate_image(user_prompt)
