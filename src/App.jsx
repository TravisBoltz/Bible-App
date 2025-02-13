import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { StrictMode } from "react";
import Home from "./pages/Home";

// Configure future flags for React Router v7
const routerFutureConfig = {
  v7_startTransition: true,
  v7_relativeSplatPath: true,
};

function App() {
  return (
    <StrictMode>
      <Router future={routerFutureConfig}>
        <Routes>
          <Route path="/" element={<Home />} />
        </Routes>
      </Router>
    </StrictMode>
  );
}

export default App;
