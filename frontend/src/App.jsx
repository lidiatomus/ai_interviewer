import { Routes, Route } from "react-router-dom";
import HomePage from "./pages/HomePage";
import InterviewPage from "./pages/InterviewPage";
import ResultsPage from "./pages/ResultsPage";

function App() {
  return (
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route path="/interview/:interviewId" element={<InterviewPage />} />
      <Route path="/results/:interviewId" element={<ResultsPage />} />
    </Routes>
  );
}

export default App;