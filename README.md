# AI Bible Quotation App

## Overview
A real-time Bible verse detection application that listens to live speech, transcribes it using OpenAI Whisper, and displays detected Bible quotations. The app uses a SQLite Bible database with multiple translations (KJV, ASV, WEB, YLT, BBE) for verse lookups.

## Features
- Real-time speech-to-text using OpenAI Whisper (supports GPU acceleration)
- Smart Bible reference detection using Google Gemini AI
- Multiple Bible translations support
- WebSocket-based real-time communication
- User-friendly interface with live transcription display

## Technical Stack
- Frontend: React + Vite, TailwindCSS, Socket.IO Client
- Backend: Flask, Python-SocketIO, SQLAlchemy
- AI Models: OpenAI Whisper (speech recognition), Google Gemini (reference extraction)
- Database: SQLite with multiple Bible translations

## Prerequisites
- Python 3.10 or higher
- Node.js 18 or higher
- CUDA-compatible GPU (optional, for faster transcription)

## Installation

### Backend Setup
1. Navigate to the server directory:
   ```bash
   cd server
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a .env file with your configuration:
   ```
   PORT=5001
   HOST=localhost
   GOOGLE_AI_KEY=your_gemini_api_key
   DATABASE_URL=sqlite:///bible-sqlite.db
   ```

### Frontend Setup
1. Install Node.js dependencies:
   ```bash
   npm install
   ```

2. Start the development server:
   ```bash
   npm run dev
   ```

## Usage

1. Start the backend server:
   ```bash
   cd server
   python app.py
   ```

2. In a separate terminal, start the frontend:
   ```bash
   npm run dev
   ```

3. Open your browser to http://localhost:5173 (or the URL shown in the terminal)

4. Click "Start Listening" and speak. The app will:
   - Show real-time transcription of your speech
   - Detect and display any Bible references mentioned
   - Show the full verse text from the database

## Configuration Options

### Whisper Model Selection
You can change the Whisper model in `app.py`. Available options:
- "tiny": Fastest, least accurate
- "base": Good balance for CPU
- "small": Recommended for GPU
- "medium": More accurate, requires more GPU memory
- "large": Most accurate, requires significant GPU memory

### Translation Preferences
The system tries multiple translations in this order:
1. KJV (King James Version)
2. ASV (American Standard Version)
3. WEB (World English Bible)
4. YLT (Young's Literal Translation)
5. BBE (Bible in Basic English)

## Known Issues and Solutions

### 1. GPU Memory Issues
**Problem**: "CUDA out of memory" error when using larger Whisper models
**Solution**: 
- Switch to a smaller model size
- Reduce batch size in audio processing
- Use CPU if GPU memory is limited

### 2. Audio Processing Issues
**Problem**: No transcription appearing
**Solutions**:
- Check microphone permissions in browser
- Verify WebSocket connection in browser console
- Ensure audio format is compatible (WebM with Opus codec)

### 3. Bible Reference Detection
**Problem**: Some references not being detected
**Solutions**:
- Use standard reference formats (e.g., "John 3:16")
- For old/new testament books, use number prefix (e.g., "1 John" instead of "First John")
- Check logs for reference parsing errors

### 4. Database Connection
**Problem**: "no such table" errors
**Solution**: Ensure bible-sqlite.db is in the server directory and has proper permissions

## Troubleshooting

1. **WebSocket Connection Failed**:
   - Verify backend server is running on port 5001
   - Check CORS settings in backend
   - Look for connection errors in browser console

2. **No Audio Transcription**:
   - Check microphone permissions
   - Verify audio input is working
   - Check backend logs for Whisper errors

3. **Missing Bible Verses**:
   - Verify bible-sqlite.db file is present
   - Check database permissions
   - Use correct book name format

4. **Performance Issues**:
   - Monitor GPU memory usage
   - Adjust Whisper model size
   - Consider reducing audio chunk size

## Contributing
1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments
- Bible database from [bible_databases](https://github.com/scrollmapper/bible_databases)
- OpenAI Whisper for speech recognition
- Google Gemini for natural language processing
