function SummaryCard({ summary, sentiment, keywords }) {
  return (
    <div className="card">
      <h2>Interview Summary</h2>
      <p>
        <strong>Sentiment:</strong> {sentiment || "N/A"}
      </p>
      <p>{summary || "No summary available."}</p>

      <div className="keywords">
        {keywords?.map((keyword, index) => (
          <span key={index} className="keyword-chip">
            {keyword}
          </span>
        ))}
      </div>
    </div>
  );
}

export default SummaryCard;