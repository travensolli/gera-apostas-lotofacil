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
      if (response.data && response.data.combinations && response.data.combinations.apostas) {
        setResults(response.data.combinations.apostas);
      } else {
        console.error('Unexpected API response format:', response.data);
        setResults([]);
      }
    } catch (error) {
      console.error('Error generating bets:', error);
      setResults([]); // Clear results in case of error
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
      <table style={{ borderCollapse: 'collapse', width: '100%' }}>
        <thead>
          <tr>
            <th style={{ border: '1px solid black', padding: '8px', textAlign: 'left' }}>#</th>
            <th style={{ border: '1px solid black', padding: '8px', textAlign: 'left' }}>Dezenas</th>
          </tr>
        </thead>
        <tbody>
          {results.map((result, index) => (
            <tr key={index}>
              <td style={{ border: '1px solid black', padding: '8px' }}>{index + 1}</td>
              <td style={{ border: '1px solid black', padding: '8px' }}>{result.dezenas.join(', ')}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default GenerateBets;
