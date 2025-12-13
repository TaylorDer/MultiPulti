import React, { useState, useMemo } from 'react';
import { Link } from 'react-router-dom';
import { chapters } from '../data/chapters';
import './TOC.css';

const TOC: React.FC = () => {
  const [searchQuery, setSearchQuery] = useState('');

  const filteredChapters = useMemo(() => {
    if (!searchQuery.trim()) return chapters;
    
    const query = searchQuery.toLowerCase();
    return chapters.filter(chapter =>
      chapter.title.toLowerCase().includes(query) ||
      chapter.sections.some(section =>
        section.title.toLowerCase().includes(query) ||
        section.content.toLowerCase().includes(query)
      )
    );
  }, [searchQuery]);

  return (
    <div className="toc">
      <h1>Содержание</h1>
      
      <div className="toc-search">
        <input
          type="text"
          placeholder="Поиск по содержанию..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
        />
      </div>

      <div className="toc-chapters">
        {filteredChapters.map((chapter, chapterIndex) => (
          <div key={chapter.id} className="toc-chapter">
            <h2>
              <span className="chapter-number">{chapterIndex + 1}.</span>
              {chapter.title}
            </h2>
            <ul className="toc-sections">
              {chapter.sections.map((section, sectionIndex) => (
                <li key={section.id}>
                  <Link to={`/chapter/${chapter.id}/section/${section.id}`}>
                    <span className="section-number">
                      {chapterIndex + 1}.{sectionIndex + 1}
                    </span>
                    {section.title}
                  </Link>
                </li>
              ))}
            </ul>
          </div>
        ))}
      </div>

      {filteredChapters.length === 0 && (
        <div className="toc-empty">
          <p>Ничего не найдено. Попробуйте изменить запрос.</p>
        </div>
      )}
    </div>
  );
};

export default TOC;

