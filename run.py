import streamlit as st
import requests
import os
from typing import Dict, List, Optional
from dataclasses import dataclass
import time
import logging
from pathlib import Path

class StreamlitUI:
    def __init__(self):
        self.generator = ContentGenerator()
        self.setup_page()

    def setup_page(self):
        """Configure Streamlit page settings."""
        st.set_page_config(
            page_title="AI Learning Content Generator",
            page_icon="🎓",
            layout="wide"
        )
        
    def show_sidebar(self):
        """Display sidebar with customization options."""
        with st.sidebar:
            st.header("Customization Options")
            style = st.selectbox(
                "Learning Style",
                ["Fictional", "Study"]
            )
            return {"style": style}

    def show_progress(self, message: str) -> None:
        """Display progress bar with message."""
        progress_bar = st.progress(0)
        for i in range(100):
            time.sleep(0.01)
            progress_bar.progress(i + 1, text=message)

    def run(self):
        """Main UI logic."""
        st.title("🎓 AI-Powered Learning Content Generator")
        st.subheader("Create engaging educational videos with AI")

        # Get customization options
        options = self.show_sidebar()

        # Input section
        col1, col2 = st.columns([2, 1])
        with col1:
            topic = st.text_input("What would you like to learn about?")
            additional_notes = st.text_area(
                "Any specific aspects you'd like to focus on?",
                height=100
            )

        with col2:
            st.info(
                "💡 **Tips for best results:**\n"
                "- Be specific with your topic\n"
                "- Add key points you want to cover\n"
                "- Consider your target audience"
            )

        # Generation process
        if st.button("Generate Learning Content", type="primary"):
            if topic:
                try:
                    # Create content with progress tracking
                    with st.spinner("🎯 Planning your learning journey..."):
                        storyline = self.generator.generate_storyline(
                            topic,
                            options["style"]
                        )
                        st.success("✅ Learning path created!")
                        st.text_area("Storyline Preview:", storyline, height=150)

                    with st.spinner("🎨 Creating visual elements..."):
                        prompts = storyline.split("\n\n")
                        images = self.generator.generate_images(prompts)
                        st.success("✅ Visuals generated!")
                        
                        # Display image previews
                        cols = st.columns(len(images))
                        for col, img in zip(cols, images):
                            with col:
                                st.image("https://via.placeholder.com/150", 
                                        caption=f"Scene {images.index(img) + 1}")

                    with st.spinner("🎵 Generating narration..."):
                        audio = self.generator.generate_audio(storyline)
                        st.success("✅ Audio narration ready!")

                    with st.spinner("🎬 Composing final video..."):
                        content = VideoContent(
                            topic=topic,
                            storyline=storyline,
                            images=images,
                            audio_path=audio
                        )
                        video_path = self.generator.create_video(content)
                        st.success("✅ Your learning video is ready!")

                    # Final video display
                    st.markdown("### 📺 Your Personalized Learning Video")
                    st.video("https://via.placeholder.com/640x360")
                    
                    # Download button
                    st.download_button(
                        label="Download Video",
                        data=b"video_data",  # Replace with actual video data
                        file_name="learning_video.mp4",
                        mime="video/mp4"
                    )

                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
                    logger.error(f"Generation failed: {e}")
            else:
                st.warning("⚠️ Please enter a topic to proceed.")

if __name__ == "__main__":
    app = StreamlitUI()
    app.run()
