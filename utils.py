from config import Config
import torch,os,shutil
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips, TextClip, CompositeVideoClip

class ContentGenerator():
    def __init__(self):
        self.config=Config
        self.config.initialize_models()
    
    def generate_prompts(self,topic,style):
        model = genai.GenerativeModel('gemini-pro')
        prompt = f"""
        Create a  engaging story that explains {topic} using superheroes or other fictional characters. The story should be educational and easy for students to understand. Break down the story into frames. Each frame should be a dictionary with two keys: 'image_prompt' for the image description and 'narrator' for the accompanying text. Return the response as a list of dictionaries, like this: 
        [
            {{'image_prompt': 'description of image 1', 'narrator': 'text for image 1'}},
            {{'image_prompt': 'description of image 2', 'narrator': 'text for image 2'}}
        ]
        At the end, make a strong connection to the actual concept of {topic} and conclude the story effectively.Also make scientific and theoretical explanations where needed and make narrations very detailed. No additional text or commentary is needed.
        """    
        response = model.generate_content(prompt)

        
        story_and_prompts = ast.literal_eval(response.text)
    
        image_prompts = [frame['image_prompt'] for frame in story_and_prompts]
        narrators = [frame['narrator'] for frame in story_and_prompts]

        return image_prompts, narrators

    def generate_images(self,prompts):
        folder_name = "images"

        # Clear or create the folder
        if os.path.exists(folder_name):
            shutil.rmtree(folder_name)
        os.makedirs(folder_name)
        for i in  range(len(prompts)):
            image = self.config.image_generate_pipe(
                prompts[i],
                guidance_scale=0.0,
                num_inference_steps=4,
                max_sequence_length=128,
                generator=torch.Generator("cuda").manual_seed(0)
            ).images[0]
            image.save(os.path.join(folder_name, f"flux-schnell_{i}.png"),f"flux-schnell_{i}.png")
    def generate_audio(self,storyline):
        for i in  range(len(storyline)):
            inputs = processor(text=storyline[i], return_tensors="pt")
            embeddings_dataset = load_dataset("Matthijs/cmu-arctic-xvectors", split="validation")
            speaker_embeddings = torch.tensor(embeddings_dataset[7306]["xvector"]).unsqueeze(0)
            speech = model.generate_speech(inputs["input_ids"], speaker_embeddings, vocoder=vocoder)
            sf.write(f"speech{i}.wav", speech.numpy(), samplerate=16000)
    
    
    def create_video(self,storyline,images,audio):
        clips = []
    
        for i in range(length):
            # Create the image and audio clips
            image_clip = ImageClip(f"flux-schnell_{i}.png").resize(0.5).set_duration(AudioFileClip(f"speech{i}.wav").duration).set_fps(fps)
            audio_clip = AudioFileClip(f"speech{i}.wav")
            
            # Combine image and audio
            image_clip = image_clip.set_audio(audio_clip)
            clips.append(image_clip)
        
        # Concatenate all video clips
        final_video = concatenate_videoclips(clips, method="compose")
        
        # Write the final video
        final_video.write_videofile("final_video_no_subtitles.mp4", fps=fps, codec='libx264', preset="ultrafast")

        
