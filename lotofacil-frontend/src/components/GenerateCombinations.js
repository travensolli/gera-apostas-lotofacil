import { useState } from "react";
import axios from "axios";
import "./GenerateCombinations.css"; // Importar estilos

function GenerateCombinations() {
  const [numConcursos, setNumConcursos] = useState(10);
  const [quantidade, setQuantidade] = useState(5);
  const [combinations, setCombinations] = useState([]);

  const generate = async () => {
    try {
      const response = await axios.post("http://localhost:8000/generate-combinations", {
        num_concursos: numConcursos,
        quantidade: quantidade,
      });
      // Ajustar para acessar combinations.apostas
      setCombinations(response.data.combinations.apostas || []);
    } catch (error) {
      alert("Erro ao gerar combinações");
    }
  };

  return (
    <div className="generate-combinations">
      <h2>Gerar Apostas Sugeridas</h2>
      <div className="form">
        <input
          type="number"
          value={numConcursos}
          onChange={(e) => setNumConcursos(e.target.value)}
          placeholder="Número de Concursos"
        />
        <input
          type="number"
          value={quantidade}
          onChange={(e) => setQuantidade(e.target.value)}
          placeholder="Quantidade de Combinações"
        />
        <button onClick={generate}>Gerar Combinações</button>
      </div>
      {combinations.length > 0 && (
        <div className="results">
          <h3>Apostas Sugeridas</h3>
          <table>
            <thead>
              <tr>
                <th>#</th>
                <th>Dezenas</th>
              </tr>
            </thead>
            <tbody>
              {combinations.map((combo, index) => (
                <tr key={index}>
                  <td>{index + 1}</td>
                  <td>{combo.dezenas.join(", ")}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export default GenerateCombinations;