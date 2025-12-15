import React, { useEffect, useRef, useState } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { chapters } from '../data/chapters';
import { MarkdownContent } from '../utils/markdown';
import { storage } from '../utils/storage';
import AchievementVideoModal from '../components/AchievementVideoModal';
import './Chapter.css';

const Chapter: React.FC = () => {
  const { chapterId, sectionId } = useParams<{ chapterId: string; sectionId: string }>();
  const navigate = useNavigate();
  const [progress, setProgress] = useState(0);
  const [markdownContent, setMarkdownContent] = useState<string>('');
  const [loading, setLoading] = useState(true);
  const [pendingNext, setPendingNext] = useState<{ to: string; label: string } | null>(null);
  const contentRef = useRef<HTMLDivElement>(null);
  const bodyRef = useRef<HTMLDivElement>(null);
  const progressRef = useRef<HTMLDivElement>(null);

  const chapter = chapters.find((c) => c.id === chapterId);
  const section = chapter?.sections.find((s) => s.id === sectionId);

  // Загружаем markdown файл
  useEffect(() => {
    if (!section?.markdownFile) {
      setLoading(false);
      return;
    }

    setLoading(true);
    // Используем fetch для загрузки markdown файлов из public директории
    // Файлы должны быть в public/content/chapters/
    const fetchPath = `/content/${section.markdownFile}`;
    
    fetch(fetchPath)
      .then((response) => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.text();
      })
      .then((text) => {
        setMarkdownContent(text);
        setLoading(false);
      })
      .catch((error) => {
        console.error('Ошибка загрузки markdown файла:', error, fetchPath);
        setMarkdownContent('# Ошибка загрузки контента\n\nФайл не найден или не может быть загружен.\n\nПуть: ' + fetchPath);
        setLoading(false);
      });
  }, [section?.markdownFile]);

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
      if (!contentRef.current || !bodyRef.current) return;

      // Find the scrolling container (layout-content)
      const scrollContainer = contentRef.current.closest('.layout-content') as HTMLElement;
      if (!scrollContainer) return;

      const containerScrollTop = scrollContainer.scrollTop;
      const containerHeight = scrollContainer.clientHeight;

      // Compute section content progress (only markdown area) relative to the scroll container.
      const containerRect = scrollContainer.getBoundingClientRect();
      const bodyRect = bodyRef.current.getBoundingClientRect();

      // Top of the markdown body within scrollContainer's scroll coordinates
      const bodyTopInContainer = containerScrollTop + (bodyRect.top - containerRect.top);
      const bodyHeight = bodyRef.current.offsetHeight;

      // If everything fits, consider it fully read.
      const scrollable = bodyHeight - containerHeight;
      const raw =
        scrollable <= 0 ? 1 : (containerScrollTop - bodyTopInContainer) / scrollable;

      const newProgress = Math.max(0, Math.min(100, Math.round(raw * 100)));

      setProgress(newProgress);
      if (chapterId && sectionId) {
        storage.saveProgress(chapterId, sectionId, newProgress);
      }
    };

    const scrollContainer = contentRef.current?.closest('.layout-content') as HTMLElement;
    if (scrollContainer) {
      scrollContainer.addEventListener('scroll', handleScroll);
      // Also check on mount and resize
      // Run after layout settles (markdown + images may change height)
      requestAnimationFrame(handleScroll);
      window.addEventListener('resize', handleScroll);

      const ro =
        typeof ResizeObserver !== 'undefined'
          ? new ResizeObserver(() => {
              requestAnimationFrame(handleScroll);
            })
          : null;
      if (ro && bodyRef.current) {
        ro.observe(bodyRef.current);
      }

      return () => {
        scrollContainer.removeEventListener('scroll', handleScroll);
        window.removeEventListener('resize', handleScroll);
        ro?.disconnect();
      };
    }
  }, [chapterId, sectionId, loading, markdownContent]);

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

  const handleNextClick = (e: React.MouseEvent, to: string, label: string) => {
    e.preventDefault();
    setPendingNext({ to, label });
  };

  const closeModal = () => setPendingNext(null);

  const completeAndNavigate = () => {
    if (!pendingNext) return;
    const dest = pendingNext.to;
    setPendingNext(null);
    navigate(dest);
  };

  return (
    <div className="chapter" ref={contentRef}>
      <AchievementVideoModal
        open={Boolean(pendingNext)}
        title="Достижение получено!"
        description={
          chapter && section
            ? `Раздел «${section.title}» прочитан. Отличная работа — идём дальше!`
            : 'Раздел прочитан. Отличная работа — идём дальше!'
        }
        videoSrc="/video/Ach.mp4"
        onClose={closeModal}
        onDone={completeAndNavigate}
      />
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

        <div className="chapter-body" ref={bodyRef}>
          {loading ? (
            <div>Загрузка...</div>
          ) : (
            <MarkdownContent content={markdownContent} />
          )}
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
              onClick={(e) =>
                handleNextClick(e, `/chapter/${chapterId}/section/${nextSection.id}`, nextSection.title)
              }
            >
              {nextSection.title} →
            </Link>
          ) : nextChapter && nextChapter.sections.length > 0 ? (
            <Link
              to={`/chapter/${nextChapter.id}/section/${nextChapter.sections[0].id}`}
              className="chapter-nav-link next"
              onClick={(e) =>
                handleNextClick(
                  e,
                  `/chapter/${nextChapter.id}/section/${nextChapter.sections[0].id}`,
                  nextChapter.title
                )
              }
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

