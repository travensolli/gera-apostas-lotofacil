import React, { useEffect, useState } from "react";
import axios from "axios";
import "./DatabaseView.css";

function DatabaseView() {
  const [data, setData] = useState([]);
  const [error, setError] = useState(null);
  const [page, setPage] = useState(1);
  const [pageSize, setPageSize] = useState(10);
  const [orderBy, setOrderBy] = useState("concurso");
  const [filterDate, setFilterDate] = useState("");
  const [sortDirection, setSortDirection] = useState("asc");

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get("http://localhost:8000/get-database-data", {
          params: {
            page,
            page_size: pageSize,
            order_by: orderBy,
            sort_direction: sortDirection,
            filter_date: filterDate || undefined,
          },
        });
        setData(response.data.data);
      } catch (err) {
        setError("Erro ao carregar os dados da base de dados");
      }
    };

    fetchData();
  }, [page, pageSize, orderBy, sortDirection, filterDate]);

  const handlePageChange = (newPage) => {
    setPage(newPage);
  };

  const handlePageSizeChange = (event) => {
    setPageSize(Number(event.target.value));
    setPage(1); // Reset to first page
  };

  const handleOrderByChange = (event) => {
    setOrderBy(event.target.value);
  };

  const handleFilterDateChange = (event) => {
    setFilterDate(event.target.value);
    setPage(1); // Reset to first page
  };

  const handleColumnClick = (column) => {
    if (orderBy === column) {
      setSortDirection(sortDirection === "asc" ? "desc" : "asc");
    } else {
      setOrderBy(column);
      setSortDirection("asc");
    }
  };

  const handleFilterDateRangeChange = (start, end) => {
    setFilterDate({ start, end });
    setPage(1); // Reset to first page
  };

  if (error) {
    return <div className="error">{error}</div>;
  }

  return (
    <div className="database-view">
      <h1>Dados da Base de Dados</h1>

      <div className="controls">
        <label>
          Itens por página:
          <select value={pageSize} onChange={handlePageSizeChange}>
            <option value={5}>5</option>
            <option value={10}>10</option>
            <option value={20}>20</option>
          </select>
        </label>

        <label>
          Ordenar por:
          <select value={orderBy} onChange={handleOrderByChange}>
            <option value="concurso">Número do Concurso</option>
            <option value="data">Data</option>
          </select>
        </label>

        <label>
          Filtrar por data:
          <input
            type="date"
            value={filterDate}
            onChange={handleFilterDateChange}
          />
        </label>

        <label>
          Data Inicial:
          <input
            type="date"
            value={filterDate.start || ""}
            onChange={(e) => handleFilterDateRangeChange(e.target.value, filterDate.end)}
          />
        </label>

        <label>
          Data Final:
          <input
            type="date"
            value={filterDate.end || ""}
            onChange={(e) => handleFilterDateRangeChange(filterDate.start, e.target.value)}
          />
        </label>
      </div>

      <table>
        <thead>
          <tr>
            {data.length > 0 && Object.keys(data[0]).map((key) => (
              <th key={key} onClick={() => handleColumnClick(key)}>
                {key}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {data.map((row, index) => (
            <tr key={index}>
              {Object.values(row).map((value, i) => (
                <td key={i}>{value}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>

      <div className="pagination"></div>
        <button onClick={() => handlePageChange(page - 1)} disabled={page === 1}>
          Anterior
        </button>
        <span>Página {page}</span>
        <button onClick={() => handlePageChange(page + 1)}>
          Próxima
        </button>
    </div>
  );
}

export default DatabaseView;