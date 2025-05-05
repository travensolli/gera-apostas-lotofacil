import axios from "axios";

function UpdateDatabase() {
  const updateDatabase = async () => {
    try {
      const response = await axios.post("http://localhost:8000/update-database");
      alert(response.data.message);
    } catch (error) {
      alert("Erro ao atualizar a base de dados");
    }
  };

  return <button onClick={updateDatabase}>Atualizar Base de Dados</button>;
}

export default UpdateDatabase;