import axios from "axios";

const api = axios.create({
  baseURL: "http://127.0.0.1:8000",
});

export const startInterview = async (topic) => {
  const response = await api.post("/interviews/start", { topic });
  return response.data;
};

export const submitAnswer = async (interviewId, questionIndex, answerText) => {
  const response = await api.post(`/interviews/${interviewId}/answer`, {
    question_index: questionIndex,
    answer_text: answerText,
  });
  return response.data;
};

export const finishInterview = async (interviewId) => {
  const response = await api.post(`/interviews/${interviewId}/finish`);
  return response.data;
};

export const getInterview = async (interviewId) => {
  const response = await api.get(`/interviews/${interviewId}`);
  return response.data;
};