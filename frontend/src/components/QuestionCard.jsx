import { useState } from "react";

function QuestionCard({ questionIndex, questionText, onSubmit, loading }) {
  const [answer, setAnswer] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!answer.trim()) return;
    onSubmit(answer.trim(), () => setAnswer(""));
  };

  return (
    <form onSubmit={handleSubmit} className="card">
      <p className="question-number">Question {questionIndex + 1} of 5</p>
      <h2>{questionText}</h2>

      <textarea
        className="text-area"
        rows="6"
        placeholder="Write your answer here..."
        value={answer}
        onChange={(e) => setAnswer(e.target.value)}
      />

      <button
        type="submit"
        className="primary-btn"
        disabled={loading || !answer.trim()}
      >
        {loading ? "Submitting..." : "Next"}
      </button>
    </form>
  );
}

export default QuestionCard;