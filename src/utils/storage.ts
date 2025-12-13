import { AppSettings, ReadingProgress } from '../types';

const SETTINGS_KEY = 'app_settings';
const PROGRESS_KEY = 'reading_progress';

export const storage = {
  getSettings(): AppSettings {
    const stored = localStorage.getItem(SETTINGS_KEY);
    if (stored) {
      return JSON.parse(stored);
    }
    return { fontSize: 1 };
  },

  saveSettings(settings: AppSettings): void {
    localStorage.setItem(SETTINGS_KEY, JSON.stringify(settings));
  },

  getProgress(): Record<string, ReadingProgress> {
    const stored = localStorage.getItem(PROGRESS_KEY);
    if (stored) {
      return JSON.parse(stored);
    }
    return {};
  },

  saveProgress(chapterId: string, sectionId: string, progress: number): void {
    const allProgress = this.getProgress();
    const key = `${chapterId}:${sectionId}`;
    allProgress[key] = { chapterId, sectionId, progress };
    localStorage.setItem(PROGRESS_KEY, JSON.stringify(allProgress));
  },

  getSectionProgress(chapterId: string, sectionId: string): number {
    const allProgress = this.getProgress();
    const key = `${chapterId}:${sectionId}`;
    return allProgress[key]?.progress || 0;
  },
};


