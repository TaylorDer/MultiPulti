import React, { useState, useMemo } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { chapters } from '../data/chapters';
import './Sidebar.css';

interface SidebarProps {
  isOpen: boolean;
  onClose: () => void;
  fontSize: number;
  onFontSizeChange: (delta: number) => void;
}

const Sidebar: React.FC<SidebarProps> = ({ isOpen, onClose, fontSize, onFontSizeChange }) => {
  const [searchQuery, setSearchQuery] = useState('');
  const location = useLocation();

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

  const isActive = (chapterId: string, sectionId: string) => {
    return location.pathname === `/chapter/${chapterId}/section/${sectionId}`;
  };

  return (
    <>
      {isOpen && <div className="sidebar-overlay" onClick={onClose} />}
      <aside className={`sidebar ${isOpen ? 'sidebar-open' : ''}`}>
        <div className="sidebar-header">
          <h2>Содержание</h2>
          <button className="sidebar-close" onClick={onClose} aria-label="Закрыть">
            ×
          </button>
        </div>
        
        <div className="sidebar-search">
          <input
            type="text"
            placeholder="Поиск..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
        </div>

        <div className="sidebar-controls">
          <button
            onClick={() => onFontSizeChange(-0.1)}
            className="font-size-btn"
            aria-label="Уменьшить шрифт"
          >
            A−
          </button>
          <span className="font-size-value">{Math.round(fontSize * 100)}%</span>
          <button
            onClick={() => onFontSizeChange(0.1)}
            className="font-size-btn"
            aria-label="Увеличить шрифт"
          >
            A+
          </button>
        </div>

        <nav className="sidebar-nav">
          {filteredChapters.map((chapter) => (
            <div key={chapter.id} className="sidebar-chapter">
              <div className="sidebar-chapter-title">{chapter.title}</div>
              <ul className="sidebar-sections">
                {chapter.sections.map((section) => (
                  <li key={section.id}>
                    <Link
                      to={`/chapter/${chapter.id}/section/${section.id}`}
                      className={`sidebar-link ${isActive(chapter.id, section.id) ? 'active' : ''}`}
                      onClick={onClose}
                    >
                      {section.title}
                    </Link>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </nav>
      </aside>
    </>
  );
};

export default Sidebar;


