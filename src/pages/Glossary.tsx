import React, { useState, useMemo } from 'react';
import { glossary } from '../data/glossary';
import './Glossary.css';

const Glossary: React.FC = () => {
  const [searchQuery, setSearchQuery] = useState('');

  const filteredGlossary = useMemo(() => {
    if (!searchQuery.trim()) return glossary;
    
    const query = searchQuery.toLowerCase();
    return glossary.filter(
      (item) =>
        item.term.toLowerCase().includes(query) ||
        item.definition.toLowerCase().includes(query)
    );
  }, [searchQuery]);

  return (
    <div className="glossary">
      <h1>Глоссарий</h1>
      <p className="glossary-intro">
        Справочник основных терминов и понятий, используемых в пособии
      </p>

      <div className="glossary-search">
        <input
          type="text"
          placeholder="Поиск по глоссарию..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
        />
      </div>

      <div className="glossary-list">
        {filteredGlossary.map((item, index) => (
          <div key={index} className="glossary-item">
            <h3 className="glossary-term">{item.term}</h3>
            <p className="glossary-definition">{item.definition}</p>
          </div>
        ))}
      </div>

      {filteredGlossary.length === 0 && (
        <div className="glossary-empty">
          <p>Ничего не найдено. Попробуйте изменить запрос.</p>
        </div>
      )}
    </div>
  );
};

export default Glossary;

