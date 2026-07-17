import streamlit as st
from moviepy import VideoFileClip, CompositeVideoClip, TextClip, ImageClip
import tempfile
import os

st.set_page_config(page_title="AI Watermark Studio", layout="wide")

st.title("🎥 AI Watermark Studio")
st.write("Add Text or Logo Watermarks to Videos")

os.makedirs("outputs", exist_ok=True)

video = st.file_uploader(
    "Upload Video",
    type=["mp4", "avi", "mov"]
)

if video:

    st.video(video)

    watermark_type = st.radio(
        "Watermark Type",
        ["Text", "Logo"]
    )

    if watermark_type == "Text":

        watermark_text = st.text_input(
            "Enter Watermark",
            "AI Watermark Studio"
        )

        text_color = st.color_picker(
            "Text Color",
            "#FFFFFF"
        )

        font_size = st.slider(
            "Font Size",
            20,
            100,
            40
        )

    else:

        logo = st.file_uploader(
            "Upload PNG Logo",
            type=["png"]
        )

        logo_size = st.slider(
            "Logo Width",
            50,
            300,
            120
        )

    position = st.selectbox(
        "Position",
        [
            "Top Left",
            "Top Right",
            "Center",
            "Bottom Left",
            "Bottom Right"
        ]
    )

    if st.button("Generate Watermarked Video"):

        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_video:

            temp_video.write(video.read())

            video_path = temp_video.name

        clip = VideoFileClip(video_path)

        positions = {
            "Top Left": ("left", "top"),
            "Top Right": ("right", "top"),
            "Center": ("center", "center"),
            "Bottom Left": ("left", "bottom"),
            "Bottom Right": ("right", "bottom")
        }

        layers = [clip]

        if watermark_type == "Text":

            txt = (
                TextClip(
                    text=watermark_text,
                    font_size=font_size,
                    color=text_color,
                    stroke_color="black",
                    stroke_width=2
                )
                .with_duration(clip.duration)
                .with_position(positions[position])
            )

            layers.append(txt)

        else:

            if logo is None:
                st.error("Upload Logo")
                st.stop()

            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_logo:

                temp_logo.write(logo.read())

                logo_path = temp_logo.name

            img = (
                ImageClip(logo_path)
                .resized(width=logo_size)
                .with_duration(clip.duration)
                .with_position(positions[position])
            )

            layers.append(img)

        final = CompositeVideoClip(layers)

        output = "outputs/watermarked_video.mp4"

        with st.spinner("Processing..."):

            final.write_videofile(
                output,
                codec="libx264",
                audio_codec="aac",
                fps=clip.fps
            )

        st.success("Watermark Added Successfully!")

        st.video(output)

        with open(output, "rb") as file:

            st.download_button(
                "Download Video",
                file,
                file_name="watermarked_video.mp4",
                mime="video/mp4"
            )
