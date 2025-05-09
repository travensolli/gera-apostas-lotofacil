import React, { useState, useEffect } from 'react';
import axios from 'axios';

const PreviousDraws = () => {
  const [draws, setDraws] = useState([]);
  const [page, setPage] = useState(1);
  const [pageSize, setPageSize] = useState(10);
  const [orderBy, setOrderBy] = useState('concurso');
  const [filterDate, setFilterDate] = useState('');

  const handleFilterChange = (e) => {
    setFilterDate(e.target.value);
  };

  const handlePageChange = (newPage) => {
    setPage(newPage);
  };

  const handleOrderChange = (e) => {
    setOrderBy(e.target.value);
  };

  useEffect(() => {
    const fetchDraws = async () => {
      try {
        const response = await axios.get('http://localhost:5000/get-database-data', {
          params: { page, page_size: pageSize, order_by: orderBy, filter_date: filterDate },
        });
        setDraws(response.data.data);
      } catch (error) {
        console.error('Error fetching previous draws:', error);
      }
    };

    fetchDraws();
  }, [page, pageSize, orderBy, filterDate]);

  return (
    <div>
      <h1>Ver sorteios anteriores</h1>
      <div>
        <label>
          Filtrar por data:
          <input type="date" value={filterDate} onChange={handleFilterChange} />
        </label>
        <label>
          Ordenar por:
          <select value={orderBy} onChange={handleOrderChange}>
            <option value="concurso">Concurso</option>
            <option value="data">Data</option>
          </select>
        </label>
      </div>
      <table>
        <thead>
          <tr>
            {draws.length > 0 &&
              Object.keys(draws[0]).map((column) => (
                <th key={column}>{column}</th>
              ))}
          </tr>
        </thead>
        <tbody>
          {draws.map((draw, index) => (
            <tr key={index}>
              {Object.values(draw).map((value, idx) => (
                <td key={idx}>{value}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
      <div>
        <button onClick={() => handlePageChange(page - 1)} disabled={page === 1}>
          Anterior
        </button>
        <span>Página {page}</span>
        <button onClick={() => handlePageChange(page + 1)}>
          Próxima
        </button>
      </div>
    </div>
  );
};

export default PreviousDraws;
