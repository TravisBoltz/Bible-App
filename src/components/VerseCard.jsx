import { Card } from "./ui/card";
import { Button } from "./ui/button";
import { useEffect, useRef, useState } from "react";
import { io } from "socket.io-client";

const VerseCard = ({ onTranscriptionData }) => {
  const [isListening, setIsListening] = useState(false);
  const socketRef = useRef(null);
  const mediaRecorderRef = useRef(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Connect to WebSocket server
    socketRef.current = io('http://localhost:5001');

    socketRef.current.on('connect', () => {
      console.log('Connected to server');
      setError(null);
    });

    socketRef.current.on('connect_error', (error) => {
      console.error('Connection error:', error);
      setError('Failed to connect to server');
    });

    socketRef.current.on('transcription', (data) => {
      console.log('Received transcription:', data);
      onTranscriptionData(data);  // Pass both transcript and verses to parent
    });

    return () => {
      if (socketRef.current) {
        socketRef.current.disconnect();
      }
    };
  }, [onTranscriptionData]);

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaRecorderRef.current = new MediaRecorder(stream, {
        mimeType: 'audio/webm;codecs=opus'
      });

      mediaRecorderRef.current.ondataavailable = (event) => {
        if (event.data.size > 0) {
          const reader = new FileReader();
          reader.onloadend = () => {
            if (socketRef.current && socketRef.current.connected) {
              socketRef.current.emit('audio_data', reader.result);
            }
          };
          reader.readAsDataURL(event.data);
        }
      };

      mediaRecorderRef.current.start(1000); // Send chunks every second
      setIsListening(true);
      setError(null);
    } catch (err) {
      console.error("Error accessing microphone:", err);
      setError("Error accessing microphone. Please make sure you have granted microphone permissions.");
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && mediaRecorderRef.current.state === 'recording') {
      mediaRecorderRef.current.stop();
      mediaRecorderRef.current.stream.getTracks().forEach(track => track.stop());
    }
    setIsListening(false);
  };

  const handleListenClick = () => {
    if (isListening) {
      stopRecording();
    } else {
      startRecording();
    }
  };

  return (
    <Card className="w-full sm:w-[700px] mx-auto bg-white rounded-[32px] sm:rounded-[24px] p-8 sm:py-[26px] sm:px-[20px] min-h-[400px] sm:min-h-0 flex flex-col justify-between">
      <div className="flex flex-col items-center gap-[24px]">
        <div className="rounded-full bg-gray-200 p-4">
          <img
            alt={isListening ? "Recording" : "Muted"}
            className="w-4 h-4 text-gray-600"
            src={isListening ? "/recording.svg" : "/recorder.svg"}
          />
        </div>

        <p className="text-md font-semibold text-center">
          {isListening ? "Listening..." : "Tap to start listening"}
          <br />
          Bible quotations will appear in real-time.
        </p>

        {error && (
          <p className="text-red-500 text-sm text-center">
            {error}
          </p>
        )}

        <Button
          variant={isListening ? "destructive" : "default"}
          className={`w-[197px] h-[48px] rounded-full ${
            isListening
              ? "bg-red-100 text-red-600 hover:bg-red-200"
              : "bg-black text-white hover:bg-gray-800"
          }`}
          onClick={handleListenClick}
        >
          <img
            className="w-4 h-5 mt-0.5"
            src={isListening ? "/mute_microphone.svg" : "/microphone.svg"}
            alt={isListening ? "mute" : "Microphone"}
          />
          {isListening ? "Stop Listening" : "Start Listening"}
        </Button>
      </div>
    </Card>
  );
};

export default VerseCard;
