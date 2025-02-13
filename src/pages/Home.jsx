import { useState, useEffect } from "react";
import Layout from "../components/Layout";
import VerseCard from "../components/VerseCard";

const initialState = {
  currentVerse: null,
  isListening: false,
};

const verses = [
  {
    reference: "James 1:2-3",
    translation: "AMPC",
    text: "Consider it wholly joyful, my brethren, whenever you are enveloped in or encounter trials of any sort or fall into various temptations. Be assured and understand that the trial and proving of your faith bring out endurance and steadfastness and patience.",
  },
  {
    reference: "Romans 8:28",
    translation: "NIV",
    text: "And we know that in all things God works for the good of those who love him, who have been called according to his purpose.",
  },
];

const Home = () => {
  const [state, setState] = useState(initialState);
  const [recognition, setRecognition] = useState(null);

  useEffect(() => {
    if (window.webkitSpeechRecognition) {
      const recognition = new window.webkitSpeechRecognition();
      recognition.continuous = true;
      recognition.interimResults = true;

      recognition.onresult = (event) => {
        const transcript = Array.from(event.results)
          .map((result) => result[0].transcript)
          .join("");

        verses.forEach((verse) => {
          if (
            transcript
              .toLowerCase()
              .includes(verse.text.toLowerCase().substring(0, 20))
          ) {
            setState({
              currentVerse: verse.reference,
              isListening: true,
            });
          }
        });
      };

      recognition.onerror = (event) => {
        console.error("Speech recognition error:", event.error);
        setState(initialState);
      };

      setRecognition(recognition);
    } else {
      console.error("Speech recognition not supported");
    }

    return () => {
      if (recognition) {
        recognition.stop();
      }
    };
  }, []);

  const handleListenClick = () => {
    if (state.isListening) {
      recognition?.stop();
      setState(initialState);
    } else {
      recognition?.start();
      setState({ ...state, isListening: true });
    }
  };

  return (
    <Layout>
      <div className="flex-1 flex flex-col">
        <div className="flex-1 flex items-center justify-center px-4">
          <div className="text-center">
            <h2 className="text-xl font-medium text-gray-900 mb-4">
              {state.currentVerse
                ? `${
                    verses.find((v) => v.reference === state.currentVerse)
                      ?.reference
                  } (${
                    verses.find((v) => v.reference === state.currentVerse)
                      ?.translation
                  })`
                : "Speak a Bible verse"}
            </h2>
            <p className="text-gray-700 text-lg leading-relaxed max-w-2xl">
              {state.currentVerse
                ? verses.find((v) => v.reference === state.currentVerse)?.text
                : "Try speaking Romans 8:28 or James 1:2-3"}
            </p>
          </div>
        </div>
        <div className="px-4 pb-8">
          <VerseCard
            isListening={state.isListening}
            onListenClick={handleListenClick}
          />
        </div>
      </div>
    </Layout>
  );
};

export default Home;
