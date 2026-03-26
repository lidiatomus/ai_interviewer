function TranscriptCard({ transcript }) {
  return (
    <div className="card">
      <h2>Transcript</h2>

      {transcript?.map((item) => (
        <div key={item.question_index} className="transcript-item">
          <p>
            <strong>Q{item.question_index + 1}:</strong> {item.question_text}
          </p>
          <p>
            <strong>A:</strong> {item.answer_text || "No answer provided."}
          </p>
        </div>
      ))}
    </div>
  );
}

export default TranscriptCard;