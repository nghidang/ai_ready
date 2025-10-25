"""
Text-to-Speech module using HuggingFace VITS models
"""
import os
import torch
import torchaudio
from transformers import VitsModel, AutoTokenizer
import soundfile as sf
import tempfile
from typing import Optional, Union
import warnings

# Suppress warnings for cleaner output
warnings.filterwarnings("ignore")

# Fix tokenizers parallelism warning
os.environ["TOKENIZERS_PARALLELISM"] = "false"

class TTSManager:
    """Text-to-Speech manager using HuggingFace VITS models"""
    
    def __init__(self, model_name: str = "facebook/mms-tts-eng", device: Optional[str] = None):
        """
        Initialize TTS manager with a VITS model
        
        Args:
            model_name: HuggingFace model name for TTS
            device: Device to run the model on ('cpu', 'cuda', or None for auto)
        """
        self.model_name = model_name
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.model = None
        self.tokenizer = None
        self.sample_rate = 16000  # Default sample rate for most VITS models
        
        print(f"Initializing TTS with model: {model_name}")
        print(f"Using device: {self.device}")
        
        self._load_model()
    
    def _load_model(self):
        """Load the VITS model and tokenizer"""
        try:
            print("Loading VITS model...")
            self.model = VitsModel.from_pretrained(self.model_name)
            self.model.to(self.device)
            
            # Try to get tokenizer, fallback to basic if not available
            try:
                self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            except:
                print("No tokenizer found, using basic text processing")
                self.tokenizer = None
            
            print("TTS model loaded successfully!")
            
        except Exception as e:
            print(f"Error loading TTS model: {e}")
            print("Falling back to basic TTS functionality")
            self.model = None
            self.tokenizer = None
    
    def text_to_speech(self, text: str, output_path: Optional[str] = None) -> Union[str, None]:
        """
        Convert text to speech and save as audio file
        
        Args:
            text: Text to convert to speech
            output_path: Path to save audio file (optional)
            
        Returns:
            Path to generated audio file or None if failed
        """
        if not self.model:
            print("TTS model not available")
            return None
        
        try:
            # Clean and prepare text
            text = self._clean_text(text)
            if not text.strip():
                print("Empty text provided")
                return None
            
            print(f"Generating speech for: {text[:50]}...")
            
            # Tokenize text if tokenizer is available
            if self.tokenizer:
                inputs = self.tokenizer(text, return_tensors="pt")
                input_ids = inputs["input_ids"].to(self.device)
            else:
                # Basic text processing
                input_ids = torch.tensor([[ord(c) for c in text[:100]]]).to(self.device)
            
            # Generate audio
            with torch.no_grad():
                outputs = self.model(input_ids)
                waveform = outputs.waveform
            
            # Convert to numpy and ensure correct format
            audio_np = waveform.squeeze().cpu().numpy()
            
            # Generate output path if not provided
            if not output_path:
                temp_dir = tempfile.gettempdir()
                output_path = os.path.join(temp_dir, f"tts_output_{hash(text) % 10000}.wav")
            
            # Save audio file
            sf.write(output_path, audio_np, self.sample_rate)
            print(f"Audio saved to: {output_path}")
            
            return output_path
            
        except Exception as e:
            print(f"Error generating speech: {e}")
            return None
    
    def _clean_text(self, text: str) -> str:
        """Clean and prepare text for TTS"""
        # Remove or replace problematic characters
        text = text.replace('\n', ' ')
        text = text.replace('\r', ' ')
        text = text.replace('\t', ' ')
        
        # Remove multiple spaces
        while '  ' in text:
            text = text.replace('  ', ' ')
        
        # Remove special characters that might cause issues
        text = ''.join(c for c in text if c.isprintable() or c.isspace())
        
        return text.strip()
    
    def play_audio(self, audio_path: str) -> bool:
        """
        Play audio file using system audio player
        
        Args:
            audio_path: Path to audio file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            import subprocess
            import platform
            
            system = platform.system()
            
            if system == "Darwin":  # macOS
                subprocess.run(["afplay", audio_path], check=True)
            elif system == "Linux":
                subprocess.run(["aplay", audio_path], check=True)
            elif system == "Windows":
                subprocess.run(["powershell", "-c", f"(New-Object Media.SoundPlayer '{audio_path}').PlaySync()"], check=True)
            else:
                print(f"Audio playback not supported on {system}")
                return False
            
            return True
            
        except Exception as e:
            print(f"Error playing audio: {e}")
            return False
    
    def speak(self, text: str, play_audio: bool = True) -> Optional[str]:
        """
        Convert text to speech and optionally play it
        
        Args:
            text: Text to convert to speech
            play_audio: Whether to play the audio after generation
            
        Returns:
            Path to generated audio file or None if failed
        """
        audio_path = self.text_to_speech(text)
        
        if audio_path and play_audio:
            self.play_audio(audio_path)
        
        return audio_path
    
    def cleanup_temp_files(self, audio_path: str):
        """Clean up temporary audio files"""
        try:
            if os.path.exists(audio_path):
                os.remove(audio_path)
                print(f"Cleaned up temporary file: {audio_path}")
        except Exception as e:
            print(f"Error cleaning up file {audio_path}: {e}")


# Global TTS instance
_tts_instance = None

def get_tts_instance(model_name: str = "facebook/mms-tts-eng") -> TTSManager:
    """Get or create a global TTS instance"""
    global _tts_instance
    if _tts_instance is None:
        _tts_instance = TTSManager(model_name)
    return _tts_instance

def text_to_speech(text: str, model_name: str = "facebook/mms-tts-eng", play_audio: bool = True) -> Optional[str]:
    """
    Convenience function to convert text to speech
    
    Args:
        text: Text to convert to speech
        model_name: HuggingFace model name for TTS
        play_audio: Whether to play the audio after generation
        
    Returns:
        Path to generated audio file or None if failed
    """
    tts = get_tts_instance(model_name)
    return tts.speak(text, play_audio)

# Example usage and testing
if __name__ == "__main__":
    # Test the TTS functionality
    test_text = "Hello! I'm your office assistant. How can I help you today?"
    
    print("Testing TTS functionality...")
    audio_path = text_to_speech(test_text, play_audio=True)
    
    if audio_path:
        print(f"TTS test successful! Audio saved to: {audio_path}")
    else:
        print("TTS test failed!")
