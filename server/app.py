from flask import Flask, request
from flask_cors import CORS
import eventlet
import socketio
import os
from dotenv import load_dotenv
import whisper
import google.generativeai as genai
import json
from audio_processor import AudioProcessor
from bible_service import bible_service
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

load_dotenv()

app = Flask(__name__)
CORS(app)
sio = socketio.Server(cors_allowed_origins='*')
app = socketio.WSGIApp(sio, app)

# Initialize Whisper model (we'll load it only once)
logger.info("Loading Whisper model...")
whisper_model = whisper.load_model("large")
logger.info("Whisper model loaded successfully")

# Configure Gemini
genai.configure(api_key=os.getenv('GOOGLE_AI_KEY'))
model = genai.GenerativeModel('gemini-pro')

def process_audio_chunk(audio_data):
    logger.debug("Processing audio chunk...")
    processed_audio = AudioProcessor.process_base64_audio(audio_data)
    if processed_audio is not None:
        try:
            logger.debug("Running Whisper transcription...")
            result = whisper_model.transcribe(processed_audio)
            logger.info(f"Transcription result: {result['text']}")
            return result["text"]
        except Exception as e:
            logger.error(f"Error transcribing audio: {e}")
    else:
        logger.error("Failed to process audio data")
    return None

def extract_bible_references(text):
    try:
        logger.debug(f"Extracting Bible references from: {text}")
        prompt = f"""Extract all Bible references from the text. Return ONLY valid Bible references in JSON format.
        Text: {text}
        Return format:
        {{"references": [
            {{"book": "BookName", "chapter": Number, "verse": Number}}
        ]}}
        Rules:
        1. Handle both formal ("John 3:16") and informal ("John chapter 3 verse 16") formats
        2. Convert ordinal words to numbers ("First John" → "1 John")
        3. Handle chapter and verse mentioned separately ("reading from Genesis chapter one verse one")
        4. Use proper book name format ("1 John" not "First John" or "1st John")
        
        Examples:
        - "John 3:16" → {{"references": [{{"book": "John", "chapter": 3, "verse": 16}}]}}
        - "First John chapter 2 verse 15" → {{"references": [{{"book": "1 John", "chapter": 2, "verse": 15}}]}}
        - "reading from Genesis chapter one verse one" → {{"references": [{{"book": "Genesis", "chapter": 1, "verse": 1}}]}}
        - "Second Chronicles 7:14" → {{"references": [{{"book": "2 Chronicles", "chapter": 7, "verse": 14}}]}}
        - "Third John verse 4" → {{"references": [{{"book": "3 John", "chapter": 1, "verse": 4}}]}}
        
        Note: If no valid Bible reference is found, return an empty references array.
        """
        response = model.generate_content(prompt)
        try:
            result = json.loads(response.text)
            logger.info(f"Extracted references: {result}")
            return result
        except json.JSONDecodeError:
            # If the response isn't valid JSON, try to extract just the JSON part
            import re
            json_match = re.search(r'\{.*\}', response.text, re.DOTALL)
            if json_match:
                result = json.loads(json_match.group())
                logger.info(f"Extracted references (after cleanup): {result}")
                return result
            logger.warning("No valid references found in text")
            return {"references": []}
    except Exception as e:
        logger.error(f"Error extracting references: {e}")
        return {"references": []}

def get_bible_verses(references):
    verses = []
    translations = ['kjv', 'asv', 'web', 'ylt', 'bbe']  # Try multiple translations
    
    for ref in references:
        logger.debug(f"Looking up verse: {ref}")
        verse = None
        # Try each translation until we find the verse
        for translation in translations:
            verse = bible_service.get_verse(
                book=ref['book'],
                chapter=ref['chapter'],
                verse=ref['verse'],
                translation=translation
            )
            if verse:
                logger.info(f"Found verse in {translation}: {verse}")
                verses.append(verse)
                break
        
        if not verse:
            logger.warning(f"No exact match found for {ref}, trying text search")
            # If no exact match found, try searching
            search_results = bible_service.search_text(ref['book'])
            if search_results:
                verses.extend(search_results[:1])  # Add the first matching verse
                logger.info(f"Found similar verse: {search_results[0]}")
    
    return verses

@sio.on('connect')
def connect(sid, environ):
    logger.info(f'Client connected: {sid}')

@sio.on('disconnect')
def disconnect(sid):
    logger.info(f'Client disconnected: {sid}')

@sio.on('audio_data')
def handle_audio_data(sid, data):
    logger.debug(f'Received audio data from {sid}')
    # Process incoming audio data
    transcript = process_audio_chunk(data)
    if transcript:
        logger.info(f"Transcript: {transcript}")
        # Extract references
        result = extract_bible_references(transcript)
        logger.info(f"Extracted references: {result}")
        # Fetch actual verses
        verses = get_bible_verses(result['references'])
        logger.info(f"Found verses: {verses}")
        # Send back transcript and verses
        response_data = {
            'text': transcript, 
            'verses': verses
        }
        logger.debug(f"Sending response to client: {response_data}")
        sio.emit('transcription', response_data, room=sid)
    else:
        logger.warning("No transcript generated from audio")

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5001))
    logger.info(f"Starting server on port {port}")
    eventlet.wsgi.server(eventlet.listen(('', port)), app)