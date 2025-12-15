import React from 'react';
import { Link } from 'react-router-dom';
import './Header.css';

interface HeaderProps {
  onMenuClick: () => void;
}

const Header: React.FC<HeaderProps> = ({ onMenuClick }) => {
  return (
    <header className="header">
      <div className="header-content">
        <button className="menu-button" onClick={onMenuClick} aria-label="Меню">
          <span></span>
          <span></span>
          <span></span>
        </button>
        <Link to="/" className="header-title">
          Проектирование программных систем
        </Link>
        <nav className="header-nav">
          <Link to="/toc">Содержание</Link>
          <Link to="/tests">Тесты</Link>
          <Link to="/glossary">Глоссарий</Link>
          <Link to="/about">О пособии</Link>
        </nav>
      </div>
    </header>
  );
};

export default Header;

