# Text-to-Speech (TTS) Integration

This office assistant now includes HuggingFace Text-to-Speech functionality using VITS models for audio responses.

## Features

- **HuggingFace VITS Models**: Uses state-of-the-art VITS (Variational Inference with adversarial learning for end-to-end Text-to-Speech) models
- **Conditional Audio Generation**: Only generates audio when users explicitly request it
- **Smart Audio Detection**: Automatically detects audio requests using natural language keywords
- **Cross-platform Audio Playback**: Works on macOS, Linux, and Windows
- **Configurable**: Can be enabled/disabled via command line arguments
- **Error Handling**: Graceful fallback to text-only responses if TTS fails

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. The TTS module will automatically download the HuggingFace model on first use.

## Usage

### Basic Usage

Run the office assistant with TTS enabled (default):
```bash
python main.py
```

Run with TTS explicitly enabled:
```bash
python main.py --tts
```

Run with TTS disabled:
```bash
python main.py --no-tts
```

### Requesting Audio Responses

The assistant will only generate audio when you explicitly request it. Use these keywords in your requests:

**Keywords that trigger audio:**
- `audio`, `voice`, `speak`, `sound`, `hear`, `listen`
- `with audio`, `in audio`, `as audio`, `audio please`
- `voice please`, `speak please`, `voice response`, `audio response`
- `speak it`, `say it`, `read it`, `read aloud`
- `speak the`, `say the`, `tell me with`, `tell me in`

**Examples:**
- ✅ "I want to request a day off **with audio**"
- ✅ "Can you **speak** the vacation policy?"
- ✅ "**Tell me** about work from home **in voice**"
- ✅ "**Read aloud** the meeting room booking process"
- ❌ "I want to request a day off" (no audio)
- ❌ "What's the vacation policy?" (no audio)

### Testing TTS Functionality

Test the TTS system:
```bash
python test_tts.py
```

### Direct TTS Usage

You can also use the TTS module directly in your code:

```python
from tts_module import text_to_speech, get_tts_instance

# Simple usage
audio_path = text_to_speech("Hello, this is a test message.", play_audio=True)

# Advanced usage with custom model
tts = get_tts_instance("facebook/mms-tts-eng")
audio_path = tts.speak("Your request has been processed.", play_audio=True)
```

## Configuration

### Model Selection

The default model is `facebook/mms-tts-eng`. You can change this by modifying the model name in the TTS module:

```python
# In tts_module.py or your code
tts = TTSManager("your-preferred-model-name")
```

### Audio Settings

- **Sample Rate**: 16kHz (configurable in TTSManager)
- **Audio Format**: WAV files
- **Temporary Files**: Audio files are saved to system temp directory by default

## Troubleshooting

### Common Issues

1. **Model Download Fails**
   - Ensure you have internet connection
   - Check HuggingFace model availability
   - Try a different model name

2. **Audio Playback Issues**
   - On Linux: Install `alsa-utils` for audio playback
   - On macOS: Audio should work out of the box
   - On Windows: Ensure audio drivers are installed

3. **Memory Issues**
   - VITS models require significant memory
   - Consider using CPU if GPU memory is limited
   - Close other applications if needed

4. **Performance Issues**
   - First run will be slower due to model download
   - Subsequent runs should be faster
   - Consider using smaller models for better performance

### Error Messages

- `TTS model not available`: Model failed to load
- `TTS generation failed`: Audio generation failed
- `Audio playback not supported`: System doesn't support audio playback

## Technical Details

### Model Architecture

The TTS system uses HuggingFace VITS models which provide:
- High-quality speech synthesis
- Fast inference
- Good prosody and naturalness
- Support for multiple languages

### Audio Processing

- Text preprocessing removes markdown formatting
- Audio is generated at 16kHz sample rate
- WAV format for maximum compatibility
- Automatic cleanup of temporary files

### Performance

- Model loading: ~2-5 seconds (first time)
- Audio generation: ~1-3 seconds per response
- Memory usage: ~1-2GB for model
- Disk usage: ~500MB for model files

## Future Enhancements

- Support for multiple voices
- Voice cloning capabilities
- Real-time streaming audio
- Custom voice training
- Multi-language support
- Audio quality settings

## Dependencies

- `torch>=2.0.0`: PyTorch for model inference
- `torchaudio>=2.0.0`: Audio processing
- `transformers>=4.30.0`: HuggingFace transformers
- `accelerate>=0.20.0`: Model acceleration
- `librosa>=0.10.0`: Audio analysis
- `soundfile>=0.12.0`: Audio file I/O
- `scipy>=1.10.0`: Scientific computing

## License

This TTS integration follows the same license as the parent project. The HuggingFace models may have their own licensing terms - please check the model pages for details.
