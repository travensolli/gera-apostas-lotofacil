import React, { useState } from 'react';
import axios from 'axios';

const GenerateBets = () => {
  const [inputs, setInputs] = useState({});
  const [results, setResults] = useState([]);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setInputs((prevInputs) => ({
      ...prevInputs,
      [name]: value,
    }));
  };

  const handleGenerate = async () => {
    try {
      const response = await axios.post('http://localhost:5000/generate-combinations', inputs);
      setResults(response.data.combinations || []); // Ensure combinations exist and fallback to an empty array
    } catch (error) {
      console.error('Error generating bets:', error);
    }
  };

  return (
    <div>
      <h1>Gerar apostas</h1>
      <form>
        <label>
          Número de Concursos:
          <input
            type="number"
            name="num_concursos"
            value={inputs.num_concursos || ''}
            onChange={handleInputChange}
          />
        </label>
        <br />
        <label>
          Quantidade:
          <input
            type="number"
            name="quantidade"
            value={inputs.quantidade || ''}
            onChange={handleInputChange}
          />
        </label>
      </form>
      <button onClick={handleGenerate}>Gerar</button>
      <table>
        <thead>
          <tr>
            <th>Aposta</th>
          </tr>
        </thead>
        <tbody>
          {results.map((result, index) => (
            <tr key={index}>
              <td>{result}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default GenerateBets;
