import { useEffect, useState } from "react";
import { useLocation, useNavigate, useParams } from "react-router-dom";
import QuestionCard from "../components/QuestionCard";
import {
  submitAnswer,
  finishInterview,
  getInterview,
} from "../api/interviewApi.js";

function InterviewPage() {
  const { interviewId } = useParams();
  const location = useLocation();
  const navigate = useNavigate();

  const [questionIndex, setQuestionIndex] = useState(
    location.state?.questionIndex ?? 0
  );
  const [questionText, setQuestionText] = useState(
    location.state?.questionText ?? ""
  );
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const loadInterview = async () => {
      if (questionText) return;

      try {
        const data = await getInterview(interviewId);
        const firstUnanswered = data.transcript.find((item) => !item.answer_text);

        if (firstUnanswered) {
          setQuestionIndex(firstUnanswered.question_index);
          setQuestionText(firstUnanswered.question_text);
        } else {
          navigate(`/results/${interviewId}`);
        }
      } catch (error) {
        console.error("Load interview error:", error);
        alert("Failed to load interview.");
      }
    };

    loadInterview();
  }, [interviewId, questionText, navigate]);

  const handleSubmit = async (answerText, resetAnswer) => {
    try {
      setLoading(true);

      const response = await submitAnswer(interviewId, questionIndex, answerText);
      resetAnswer();

      if (response.done) {
        await finishInterview(interviewId);
        navigate(`/results/${interviewId}`);
      } else {
        setQuestionIndex(response.next_question_index);
        setQuestionText(response.next_question_text);
      }
    } catch (error) {
      console.error("Submit answer error:", error);
      console.error("Response data:", error?.response?.data);
      alert(error?.response?.data?.detail || "Failed to submit answer.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page-container">
      <QuestionCard
        questionIndex={questionIndex}
        questionText={questionText}
        onSubmit={handleSubmit}
        loading={loading}
      />
    </div>
  );
}

export default InterviewPage;