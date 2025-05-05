import { useState } from "react";
import UpdateDatabase from "./components/UpdateDatabase";
import DatabaseView from "./components/DatabaseView";
import GenerateCombinations from "./components/GenerateCombinations";
import Navbar from './components/Navbar';
import "./App.css";

function App() {
  const [activeTab, setActiveTab] = useState("database");

  return (
    <div className="App">
      <Navbar />
      <main>
        <div className="tabs">
          <button
            className={activeTab === "database" ? "active" : ""}
            onClick={() => setActiveTab("database")}
          >
            Dados dos Concursos
          </button>
          <button
            className={activeTab === "generator" ? "active" : ""}
            onClick={() => setActiveTab("generator")}
          >
            Gerador de Apostas
          </button>
        </div>

        {activeTab === "database" && (
          <section className="database-view">
            <h2>Exibição da Base de Dados</h2>
            <DatabaseView />
          </section>
        )}

        {activeTab === "generator" && (
          <section className="generate-combinations">
            <h2>Sugestões de Apostas</h2>
            <GenerateCombinations />
          </section>
        )}
      </main>

    </div>
  );
}

export default App;
