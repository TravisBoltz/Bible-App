import { Card } from "./ui/card";
import { Button } from "./ui/button";

const VerseCard = ({ isListening, onListenClick }) => {
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
          Transcribing and detecting
          <br />
          Bible quotations in real time.
        </p>

        <Button
          variant={isListening ? "destructive" : "default"}
          className={`w-[197px] h-[48px] rounded-full ${
            isListening
              ? "bg-red-100 text-red-600 hover:bg-red-200"
              : "bg-black text-white hover:bg-gray-800"
          }`}
          onClick={onListenClick}
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
