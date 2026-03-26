import { useState } from "react";
import { useNavigate } from "react-router-dom";
import TopicForm from "../components/TopicForm";
import { startInterview } from "../api/interviewApi.js";

function HomePage() {
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleStart = async (topic) => {
    try {
      setLoading(true);
      const data = await startInterview(topic);

      navigate(`/interview/${data.interview_id}`, {
        state: {
          questionIndex: data.question_index,
          questionText: data.question_text,
        },
      });
    } catch (error) {
      console.error(error);
      alert("Failed to start interview.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page-container">
      <TopicForm onStart={handleStart} loading={loading} />
    </div>
  );
}

export default HomePage;