import React, { useEffect, useRef, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { chapters } from '../data/chapters';
import { MarkdownContent } from '../utils/markdown';
import { storage } from '../utils/storage';
import './Chapter.css';

const Chapter: React.FC = () => {
  const { chapterId, sectionId } = useParams<{ chapterId: string; sectionId: string }>();
  const [progress, setProgress] = useState(0);
  const contentRef = useRef<HTMLDivElement>(null);
  const progressRef = useRef<HTMLDivElement>(null);

  const chapter = chapters.find((c) => c.id === chapterId);
  const section = chapter?.sections.find((s) => s.id === sectionId);

  useEffect(() => {
    if (!chapterId || !sectionId) return;

    const savedProgress = storage.getSectionProgress(chapterId, sectionId);
    setProgress(savedProgress);

    // Save last viewed section
    storage.saveSettings({
      ...storage.getSettings(),
      lastChapter: chapterId,
      lastSection: sectionId,
    });
  }, [chapterId, sectionId]);

  useEffect(() => {
    const handleScroll = () => {
      if (!contentRef.current) return;

      // Find the scrolling container (layout-content)
      const scrollContainer = contentRef.current.closest('.layout-content') as HTMLElement;
      if (!scrollContainer) return;

      const contentTop = contentRef.current.offsetTop;
      const contentHeight = contentRef.current.offsetHeight;
      const containerScrollTop = scrollContainer.scrollTop;
      const containerHeight = scrollContainer.clientHeight;

      // Calculate how much of the content is visible
      const visibleTop = Math.max(0, containerScrollTop - contentTop);
      const visibleBottom = Math.min(contentHeight, containerScrollTop + containerHeight - contentTop);
      const visibleHeight = Math.max(0, visibleBottom - visibleTop);
      
      const newProgress = contentHeight > 0 
        ? Math.min(100, Math.round((visibleTop + visibleHeight) / contentHeight * 100))
        : 0;

      setProgress(newProgress);
      if (chapterId && sectionId) {
        storage.saveProgress(chapterId, sectionId, newProgress);
      }
    };

    const scrollContainer = contentRef.current?.closest('.layout-content') as HTMLElement;
    if (scrollContainer) {
      scrollContainer.addEventListener('scroll', handleScroll);
      // Also check on mount and resize
      handleScroll();
      window.addEventListener('resize', handleScroll);
      return () => {
        scrollContainer.removeEventListener('scroll', handleScroll);
        window.removeEventListener('resize', handleScroll);
      };
    }
  }, [chapterId, sectionId]);

  if (!chapter || !section) {
    return (
      <div className="chapter-error">
        <h2>Раздел не найден</h2>
        <Link to="/toc">Вернуться к содержанию</Link>
      </div>
    );
  }

  const currentSectionIndex = chapter.sections.findIndex((s) => s.id === sectionId);
  const prevSection = currentSectionIndex > 0 ? chapter.sections[currentSectionIndex - 1] : null;
  const nextSection =
    currentSectionIndex < chapter.sections.length - 1
      ? chapter.sections[currentSectionIndex + 1]
      : null;

  const prevChapterIndex = chapters.findIndex((c) => c.id === chapterId);
  const nextChapter =
    !nextSection && prevChapterIndex < chapters.length - 1
      ? chapters[prevChapterIndex + 1]
      : null;

  return (
    <div className="chapter" ref={contentRef}>
      <div className="chapter-progress-container" ref={progressRef}>
        <div className="chapter-progress-bar" style={{ width: `${progress}%` }} />
        <span className="chapter-progress-text">{progress}%</span>
      </div>

      <div className="chapter-content">
        <nav className="chapter-breadcrumb">
          <Link to="/toc">Содержание</Link>
          <span> / </span>
          <span>{chapter.title}</span>
          <span> / </span>
          <span>{section.title}</span>
        </nav>

        <h1 className="chapter-title">{section.title}</h1>

        <div className="chapter-body">
          <MarkdownContent content={section.content} />
        </div>

        <div className="chapter-navigation">
          {prevSection ? (
            <Link
              to={`/chapter/${chapterId}/section/${prevSection.id}`}
              className="chapter-nav-link prev"
            >
              ← {prevSection.title}
            </Link>
          ) : (
            <div></div>
          )}

          {nextSection ? (
            <Link
              to={`/chapter/${chapterId}/section/${nextSection.id}`}
              className="chapter-nav-link next"
            >
              {nextSection.title} →
            </Link>
          ) : nextChapter && nextChapter.sections.length > 0 ? (
            <Link
              to={`/chapter/${nextChapter.id}/section/${nextChapter.sections[0].id}`}
              className="chapter-nav-link next"
            >
              {nextChapter.title} →
            </Link>
          ) : (
            <div></div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Chapter;

