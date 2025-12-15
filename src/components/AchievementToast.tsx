import React, { useEffect } from 'react';
import './AchievementToast.css';

type AchievementToastProps = {
  title: string;
  description?: string;
  durationMs?: number;
  onClose: () => void;
};

const AchievementToast: React.FC<AchievementToastProps> = ({
  title,
  description,
  durationMs = 4500,
  onClose,
}) => {
  useEffect(() => {
    const t = window.setTimeout(onClose, durationMs);
    return () => window.clearTimeout(t);
  }, [durationMs, onClose]);

  return (
    <div className="achievement-toast" role="status" aria-live="polite">
      <div className="achievement-badge" aria-hidden="true">
        ✓
      </div>
      <div className="achievement-content">
        <div className="achievement-title">{title}</div>
        {description && <div className="achievement-description">{description}</div>}
      </div>
      <button className="achievement-close" type="button" onClick={onClose} aria-label="Закрыть">
        ×
      </button>
    </div>
  );
};

export default AchievementToast;


