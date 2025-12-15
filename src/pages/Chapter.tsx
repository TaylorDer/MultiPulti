import React, { useEffect, useMemo, useRef, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { chapters } from '../data/chapters';
import { MarkdownContent } from '../utils/markdown';
import { storage } from '../utils/storage';
import AchievementToast from '../components/AchievementToast';
import './Chapter.css';

const Chapter: React.FC = () => {
  const { chapterId, sectionId } = useParams<{ chapterId: string; sectionId: string }>();
  const [progress, setProgress] = useState(0);
  const [markdownContent, setMarkdownContent] = useState<string>('');
  const [loading, setLoading] = useState(true);
  const [achievement, setAchievement] = useState<{ title: string; description?: string } | null>(null);
  const contentRef = useRef<HTMLDivElement>(null);
  const bodyRef = useRef<HTMLDivElement>(null);
  const progressRef = useRef<HTMLDivElement>(null);

  const chapter = chapters.find((c) => c.id === chapterId);
  const section = chapter?.sections.find((s) => s.id === sectionId);

  const soundUrl = useMemo(() => '/sounds/chapter-complete.mp3', []);

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

  // Achievement: chapter completed (all sections 100%)
  useEffect(() => {
    if (!chapterId || !sectionId || !chapter) return;

    // Only evaluate when current section is fully read.
    if (progress < 100) return;

    // Already earned?
    if (storage.hasChapterCompletedAchievement(chapterId)) return;

    const isCompleted = chapter.sections.every((s) => {
      if (s.id === sectionId) return progress >= 100;
      return storage.getSectionProgress(chapterId, s.id) >= 100;
    });

    if (!isCompleted) return;

    storage.markChapterCompletedAchievement(chapterId);

    setAchievement({
      title: 'Достижение получено!',
      description: `Глава «${chapter.title}» прочитана.`,
    });

    try {
      const audio = new Audio(soundUrl);
      audio.volume = 0.5;
      void audio.play();
    } catch {
      // ignore audio errors (autoplay restrictions etc.)
    }
  }, [chapter, chapterId, progress, sectionId, soundUrl]);

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

  return (
    <div className="chapter" ref={contentRef}>
      {achievement && (
        <AchievementToast
          title={achievement.title}
          description={achievement.description}
          onClose={() => setAchievement(null)}
        />
      )}
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

