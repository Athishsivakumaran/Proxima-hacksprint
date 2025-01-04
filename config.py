import os
from datasets import load_dataset 
from diffusers import FluxPipeline
import ast,google.generativeai as genai,torch,soundfile as sf,os
from transformers import SpeechT5Processor, SpeechT5ForTextToSpeech, SpeechT5HifiGan
# genai.configure(api_key=os.environ["GEMINI_API_KEY"])


class Config:

    def __init__(self):
        self.speech_to_text={"processor":None,"model":None,"vocoder":None}
        self.image_generate_pipe=None
        self.text_generator=None
        
    def initialize_models(self):
        # Initialize the SpeechT5 models
        self.speech_to_text["processor"]=SpeechT5Processor.from_pretrained("microsoft/speecht5_tts")
        self.speech_to_text["model"] = SpeechT5ForTextToSpeech.from_pretrained("microsoft/speecht5_tts")
        self.speech_to_text["vocoder"] = SpeechT5HifiGan.from_pretrained("microsoft/speecht5_hifigan")
        
        
        self.image_generate_pipe = FluxPipeline.from_pretrained("black-forest-labs/FLUX.1-schnell", torch_dtype=torch.bfloat16)
        self.image_generate_pipe.to("cuda")

