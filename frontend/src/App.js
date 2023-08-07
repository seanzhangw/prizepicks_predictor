import './App.css';
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import OvrUnder from './pages/OvrUnder';
import WinLoss from './pages/WinLoss';
import NavBar from './components/NavBar';

function App() {
  return (
    <div>
      <Router>
      <div>
        <NavBar />
        <Routes>
          <Route exact path="/home" component={Home} />
          <Route path="/ovr-under" component={OvrUnder} />
          <Route path="/w-l" component={WinLoss} />
          {/* You can add more routes for other pages */}
        </Routes>
      </div>
    </Router>
    </div>
  );
}

export default App;
