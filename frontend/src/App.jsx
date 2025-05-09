import { BrowserRouter as Router, Route, Routes, Link, Navigate } from 'react-router-dom';
import PreviousDraws from './pages/PreviousDraws';
import GenerateBets from './pages/GenerateBets';

function App() {
  return (
    <Router>
      <div className="flex h-screen">
        {/* Sidebar */}
        <div className="w-64 bg-gray-800 text-white flex flex-col">
          <div className="p-4 text-lg font-bold border-b border-gray-700">Menu</div>
          <nav className="flex-1 p-4">
            <ul>
              <li className="mb-2">
                <Link to="/" className="block p-2 rounded hover:bg-gray-700">Ver sorteios anteriores</Link>
              </li>
              <li>
                <Link to="/generate-bets" className="block p-2 rounded hover:bg-gray-700">Gerar apostas</Link>
              </li>
            </ul>
          </nav>
        </div>

        {/* Main Content */}
        <div className="flex-1 bg-gray-100 p-4">
          <Routes>
            <Route path="/" element={<PreviousDraws />} />
            <Route path="/generate-bets" element={<GenerateBets />} />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;
