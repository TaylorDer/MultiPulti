import React, { useEffect, useRef } from 'react';
import './AchievementVideoModal.css';

type AchievementVideoModalProps = {
  open: boolean;
  title: string;
  description?: string;
  videoSrc: string;
  onDone: () => void;
  onClose: () => void;
};

const AchievementVideoModal: React.FC<AchievementVideoModalProps> = ({
  open,
  title,
  description,
  videoSrc,
  onDone,
  onClose,
}) => {
  const videoRef = useRef<HTMLVideoElement>(null);

  useEffect(() => {
    if (!open) return;
    const v = videoRef.current;
    if (!v) return;

    try {
      v.currentTime = 0;
      const p = v.play();
      // If autoplay is blocked, user can press Play (controls are enabled).
      void p;
    } catch {
      // ignore
    }
  }, [open]);

  if (!open) return null;

  return (
    <div className="achv-modal-backdrop" role="dialog" aria-modal="true" aria-label="Достижение">
      <div className="achv-modal">
        <button className="achv-modal-close" type="button" onClick={onClose} aria-label="Закрыть">
          ×
        </button>

        <div className="achv-modal-header">
          <div className="achv-badge" aria-hidden="true">
            ✓
          </div>
          <div>
            <div className="achv-title">{title}</div>
            {description && <div className="achv-description">{description}</div>}
          </div>
        </div>

        <div className="achv-video-wrap">
          <video
            ref={videoRef}
            className="achv-video"
            src={videoSrc}
            controls
            playsInline
            onEnded={onDone}
          />
        </div>

        <div className="achv-actions">
          <button className="achv-btn secondary" type="button" onClick={onClose}>
            Закрыть
          </button>
          <button className="achv-btn primary" type="button" onClick={onDone}>
            Продолжить →
          </button>
        </div>
      </div>
    </div>
  );
};

export default AchievementVideoModal;


