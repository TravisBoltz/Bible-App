import numpy as np
import io
import base64
import wave
import torch

class AudioProcessor:
    @staticmethod
    def process_base64_audio(base64_audio):
        """Convert base64 audio data to format compatible with Whisper"""
        try:
            # Decode base64 audio data
            audio_data = base64.b64decode(base64_audio.split(',')[1])
            
            # Create in-memory wave file
            wav_file = io.BytesIO()
            with wave.open(wav_file, 'wb') as wav:
                wav.setnchannels(1)  # Mono
                wav.setsampwidth(2)  # 16-bit
                wav.setframerate(16000)  # 16kHz
                wav.writeframes(audio_data)
            
            # Convert to numpy array
            wav_file.seek(0)
            with wave.open(wav_file, 'rb') as wav:
                audio = np.frombuffer(wav.readframes(wav.getnframes()), dtype=np.int16)
                # Normalize to float32 range [-1, 1]
                audio = audio.astype(np.float32) / 32768.0
            
            # Return numpy array for CPU processing
            # The calling function will convert to tensor if GPU is available
            return audio

        except Exception as e:
            print(f"Error processing audio: {e}")
            return None

    @staticmethod
    def create_temp_wav(audio_data):
        """Create a temporary WAV file from audio data"""
        temp_wav = io.BytesIO()
        with wave.open(temp_wav, 'wb') as wav:
            wav.setnchannels(1)
            wav.setsampwidth(2)
            wav.setframerate(16000)
            wav.writeframes(audio_data)
        return temp_wav.getvalue()