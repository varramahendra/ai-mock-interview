import { useState } from "react";
import axios from "axios";
import "./App.css";

// Voice recognition
const SpeechRecognition =
  window.SpeechRecognition || window.webkitSpeechRecognition;

const recognition = SpeechRecognition
  ? new SpeechRecognition()
  : null;

function App() {

  const [answer, setAnswer] = useState("");
  const [chat, setChat] = useState([]);
  const [loading, setLoading] = useState(false);
  const [history, setHistory] = useState([]);


  // Start voice input
  function startVoice() {

    if (!recognition) {
      alert("Voice not supported");
      return;
    }

    recognition.start();

    recognition.onresult = (event) => {
      const text = event.results[0][0].transcript;
      setAnswer(text);
    };
  }


  // Speak AI response
  function speak(text) {

    const speech = new SpeechSynthesisUtterance(text);

    window.speechSynthesis.speak(speech);
  }


  // Send answer
  async function send() {

    if (!answer.trim()) return;

    setLoading(true);

    try {

      const res = await axios.post(
        "http://127.0.0.1:8000/interview",
        { answer }
      );

      const aiReply = res.data.reply;

      setChat(prev => [
        ...prev,
        { type: "user", text: answer },
        { type: "ai", text: aiReply }
      ]);

      speak(aiReply);

      setAnswer("");

    } catch (err) {
      alert("Backend error");
    }

    setLoading(false);
  }


  // Load history
  async function loadHistory() {

    try {

      const res = await axios.get(
        "http://127.0.0.1:8000/history"
      );

      setHistory(res.data);

    } catch {
      alert("Cannot load history");
    }
  }


  return (
    <div className="container">

      <h2>🎯 AI Mock Interview</h2>

      <button className="history-btn" onClick={loadHistory}>
        📊 View History
      </button>


      <div className="chat-box">

        {chat.map((msg, i) => (
          <div
            key={i}
            className={msg.type === "user" ? "user" : "ai"}
          >
            {msg.text}
          </div>
        ))}


        {history.map((item) => (
          <div key={item[0]} className="ai">
            <b>You:</b> {item[1]} <br />
            <b>AI:</b> {item[2]}
          </div>
        ))}


        {loading && (
          <p className="loader">🤖 Interviewer is thinking...</p>
        )}

      </div>


      <div className="input-box">

        <button onClick={startVoice}>🎤</button>

        <input
          value={answer}
          onChange={(e) => setAnswer(e.target.value)}
          placeholder="Type or speak..."
        />

        <button onClick={send}>Send</button>

      </div>

    </div>
  );
}

export default App;
