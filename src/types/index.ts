export interface Chapter {
  id: string;
  title: string;
  sections: Section[];
}

export interface Section {
  id: string;
  title: string;
  content: string; // Markdown content
  images?: ImageData[];
}

export interface ImageData {
  src: string;
  alt: string;
  caption?: string;
}

export interface GlossaryItem {
  term: string;
  definition: string;
}

export interface ReadingProgress {
  chapterId: string;
  sectionId: string;
  progress: number; // 0-100
}

export interface AppSettings {
  fontSize: number; // base font size multiplier
  lastChapter?: string;
  lastSection?: string;
}

