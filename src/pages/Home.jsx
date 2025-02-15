import { useState } from "react";
import Layout from "../components/Layout";
import VerseCard from "../components/VerseCard";

const Home = () => {
  const [currentVerse, setCurrentVerse] = useState(null);
  const [transcript, setTranscript] = useState("");

  const handleTranscriptionData = (data) => {
    if (data.text) {
      setTranscript(data.text);
    }
    if (data.verses && data.verses.length > 0) {
      setCurrentVerse(data.verses[0]);
    }
  };

  return (
    <Layout>
      <div className="flex-1 flex flex-col">
        <div className="flex-1 flex items-center justify-center px-4">
          <div className="text-center">
            {transcript && (
              <div className="mb-8 p-4 bg-gray-50 rounded-lg">
                <h3 className="text-lg font-medium text-gray-700 mb-2">Transcript</h3>
                <p className="text-gray-600">{transcript}</p>
              </div>
            )}
            <h2 className="text-xl font-medium text-gray-900 mb-4">
              {currentVerse
                ? `${currentVerse.reference} (${currentVerse.translation})`
                : "Speak a Bible verse"}
            </h2>
            <p className="text-gray-700 text-lg leading-relaxed max-w-2xl">
              {currentVerse
                ? currentVerse.text
                : "Try speaking phrases like 'John chapter 3 verse 16' or 'Psalm 23'"}
            </p>
          </div>
        </div>
        <div className="px-4 pb-8">
          <VerseCard onTranscriptionData={handleTranscriptionData} />
        </div>
      </div>
    </Layout>
  );
};

export default Home;
