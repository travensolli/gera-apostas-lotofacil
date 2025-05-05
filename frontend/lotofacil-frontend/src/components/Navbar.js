import React from 'react';
import './Navbar.css';

function Navbar() {
  return (
    <nav className="navbar">
      <h1>Lotofácil</h1>
      <ul>
        <li><a href="#update">Atualizar Base</a></li>
        <li><a href="#view">Exibir Dados</a></li>
        <li><a href="#generate">Gerar Apostas</a></li>
      </ul>
    </nav>
  );
}

export default Navbar;