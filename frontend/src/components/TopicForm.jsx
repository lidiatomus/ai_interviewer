import { useState } from "react";

function TopicForm({ onStart, loading }) {
  const [topic, setTopic] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!topic.trim()) return;
    onStart(topic.trim());
  };

  return (
    <form onSubmit={handleSubmit} className="card form-card">
      <h1>AI Interviewer</h1>
      <p>Choose a topic and start a short AI-powered interview.</p>

      <input
        type="text"
        placeholder="Enter a topic, e.g. AI in the workplace"
        value={topic}
        onChange={(e) => setTopic(e.target.value)}
        className="text-input"
      />

      <button
        type="submit"
        className="primary-btn"
        disabled={loading || !topic.trim()}
      >
        {loading ? "Starting..." : "Start Interview"}
      </button>
    </form>
  );
}

export default TopicForm;