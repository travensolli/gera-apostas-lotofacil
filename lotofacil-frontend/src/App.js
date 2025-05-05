import UpdateDatabase from "./components/UpdateDatabase";
import DatabaseView from "./components/DatabaseView";
import GenerateCombinations from "./components/GenerateCombinations";
import "./App.css";

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Lotofácil</h1>
      </header>
      <main>
        <section className="update-database">
          <h2>Atualizar Base de Dados</h2>
          <UpdateDatabase />
        </section>

        <section className="database-view">
          <h2>Exibição da Base de Dados</h2>
          <DatabaseView />
        </section>

        <section className="generate-combinations">
          <h2>Sugestões de Apostas</h2>
          <GenerateCombinations />
        </section>
      </main>
    </div>
  );
}

export default App;
