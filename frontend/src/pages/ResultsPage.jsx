import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import { getInterview } from "../api/interviewApi.js";
import SummaryCard from "../components/SummaryCard";
import TranscriptCard from "../components/TranscriptCard";

function ResultsPage() {
  const { interviewId } = useParams();
  const [interview, setInterview] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadResults = async () => {
      try {
        const data = await getInterview(interviewId);
        setInterview(data);
      } catch (error) {
        console.error("Load results error:", error);
        console.error("Response data:", error?.response?.data);
        alert(error?.response?.data?.detail || "Failed to load results.");
      } finally {
        setLoading(false);
      }
    };

    loadResults();
  }, [interviewId]);

  if (loading) {
    return <div className="page-container">Loading results...</div>;
  }

  if (!interview) {
    return <div className="page-container">No interview found.</div>;
  }

  return (
    <div className="page-container results-layout">
      <SummaryCard
        summary={interview.summary}
        sentiment={interview.sentiment}
        keywords={interview.keywords}
      />

      <TranscriptCard transcript={interview.transcript} />

      <div className="card results-actions">
        <Link to="/" className="secondary-btn">
          Start New Interview
        </Link>
      </div>
    </div>
  );
}

export default ResultsPage;