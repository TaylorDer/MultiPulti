import { Chapter } from '../types';

export const chapters: Chapter[] = [
  {
    id: 'introduction',
    title: 'Введение',
    sections: [
      {
        id: 'introduction-1',
        title: 'Введение',
        markdownFile: 'chapters/introduction-1.md',
      },
    ],
  },
  {
    id: 'chapter-1',
    title: 'ОСНОВЫ ПРОЕКТИРОВАНИЯ  ПРОГРАММНЫХ СИСТЕМ',
    sections: [
      {
        id: 'chapter-1-особенности-процесса-синтеза-программных-систем',
        title: 'ОСОБЕННОСТИ ПРОЦЕССА СИНТЕЗА  ПРОГРАММНЫХ СИСТЕМ',
        markdownFile: 'chapters/chapter-1-особенности-процесса-синтеза-программных-систем.md',
      },
      {
        id: 'chapter-1-особенности-этапа-проектирования',
        title: 'ОСОБЕННОСТИ ЭТАПА ПРОЕКТИРОВАНИЯ',
        markdownFile: 'chapters/chapter-1-особенности-этапа-проектирования.md',
      },
      {
        id: 'chapter-1-структурирование-системы',
        title: 'СТРУКТУРИРОВАНИЕ СИСТЕМЫ',
        markdownFile: 'chapters/chapter-1-структурирование-системы.md',
      },
      {
        id: 'chapter-1-моделирование-управления',
        title: 'МОДЕЛИРОВАНИЕ УПРАВЛЕНИЯ',
        markdownFile: 'chapters/chapter-1-моделирование-управления.md',
      },
      {
        id: 'chapter-1-декомпозиция-подсистем-на-модули',
        title: 'ДЕКОМПОЗИЦИЯ ПОДСИСТЕМ НА МОДУЛИ',
        markdownFile: 'chapters/chapter-1-декомпозиция-подсистем-на-модули.md',
      },
      {
        id: 'chapter-1-информационная-закрытость',
        title: 'ИНФОРМАЦИОННАЯ ЗАКРЫТОСТЬ',
        markdownFile: 'chapters/chapter-1-информационная-закрытость.md',
      },
      {
        id: 'chapter-1-связность-модуля',
        title: 'СВЯЗНОСТЬ МОДУЛЯ',
        markdownFile: 'chapters/chapter-1-связность-модуля.md',
      },
      {
        id: 'chapter-1-функциональная-связность',
        title: 'ФУНКЦИОНАЛЬНАЯ СВЯЗНОСТЬ',
        markdownFile: 'chapters/chapter-1-функциональная-связность.md',
      },
      {
        id: 'chapter-1-информационная-связность',
        title: 'ИНФОРМАЦИОННАЯ СВЯЗНОСТЬ',
        markdownFile: 'chapters/chapter-1-информационная-связность.md',
      },
      {
        id: 'chapter-1-коммуникативная-связность',
        title: 'КОММУНИКАТИВНАЯ СВЯЗНОСТЬ',
        markdownFile: 'chapters/chapter-1-коммуникативная-связность.md',
      },
      {
        id: 'chapter-1-процедурная-связность',
        title: 'ПРОЦЕДУРНАЯ СВЯЗНОСТЬ',
        markdownFile: 'chapters/chapter-1-процедурная-связность.md',
      },
      {
        id: 'chapter-1-временная-связность',
        title: 'ВРЕМЕННАЯ СВЯЗНОСТЬ',
        markdownFile: 'chapters/chapter-1-временная-связность.md',
      },
      {
        id: 'chapter-1-логическая-связность',
        title: 'ЛОГИЧЕСКАЯ СВЯЗНОСТЬ',
        markdownFile: 'chapters/chapter-1-логическая-связность.md',
      },
      {
        id: 'chapter-1-связность-по-совпадению',
        title: 'СВЯЗНОСТЬ ПО СОВПАДЕНИЮ',
        markdownFile: 'chapters/chapter-1-связность-по-совпадению.md',
      },
      {
        id: 'chapter-1-определение-связности-модуля',
        title: 'ОПРЕДЕЛЕНИЕ СВЯЗНОСТИ МОДУЛЯ',
        markdownFile: 'chapters/chapter-1-определение-связности-модуля.md',
      },
      {
        id: 'chapter-1-сцепление-модулей',
        title: 'СЦЕПЛЕНИЕ МОДУЛЕЙ',
        markdownFile: 'chapters/chapter-1-сцепление-модулей.md',
      },
      {
        id: 'chapter-1-сложность-программной-системы',
        title: 'СЛОЖНОСТЬ ПРОГРАММНОЙ СИСТЕМЫ',
        markdownFile: 'chapters/chapter-1-сложность-программной-системы.md',
      },
      {
        id: 'chapter-1-характеристики-иерархической-структуры-программной-системы',
        title: 'ХАРАКТЕРИСТИКИ ИЕРАРХИЧЕСКОЙ СТРУКТУРЫ  ПРОГРАММНОЙ СИСТЕМЫ',
        markdownFile: 'chapters/chapter-1-характеристики-иерархической-структуры-программной-системы.md',
      },
      {
        id: 'chapter-1-контрольные-вопросы',
        title: 'Контрольные вопросы',
        markdownFile: 'chapters/chapter-1-контрольные-вопросы.md',
      },
    ],
  },
  {
    id: 'chapter-2',
    title: 'ОСНОВЫ ОБЪЕКТНО-ОРИЕНТИРОВАННОГО',
    sections: [
      {
        id: 'chapter-2-представления-программных-систем',
        title: 'ПРЕДСТАВЛЕНИЯ ПРОГРАММНЫХ СИСТЕМ',
        markdownFile: 'chapters/chapter-2-представления-программных-систем.md',
      },
      {
        id: 'chapter-2-иерархическая-организация',
        title: 'ИЕРАРХИЧЕСКАЯ ОРГАНИЗАЦИЯ',
        markdownFile: 'chapters/chapter-2-иерархическая-организация.md',
      },
      {
        id: 'chapter-2-общая-характеристика-объектов',
        title: 'ОБЩАЯ ХАРАКТЕРИСТИКА ОБЪЕКТОВ',
        markdownFile: 'chapters/chapter-2-общая-характеристика-объектов.md',
      },
      {
        id: 'chapter-2-виды-отношений-между-объектами',
        title: 'ВИДЫ ОТНОШЕНИЙ МЕЖДУ ОБЪЕКТАМИ',
        markdownFile: 'chapters/chapter-2-виды-отношений-между-объектами.md',
      },
      {
        id: 'chapter-2-видимость-объектов',
        title: 'ВИДИМОСТЬ ОБЪЕКТОВ',
        markdownFile: 'chapters/chapter-2-видимость-объектов.md',
      },
      {
        id: 'chapter-2-общая-характеристика-классов',
        title: 'ОБЩАЯ ХАРАКТЕРИСТИКА КЛАССОВ',
        markdownFile: 'chapters/chapter-2-общая-характеристика-классов.md',
      },
      {
        id: 'chapter-2-виды-отношений-между-классами',
        title: 'ВИДЫ ОТНОШЕНИЙ МЕЖДУ КЛАССАМИ',
        markdownFile: 'chapters/chapter-2-виды-отношений-между-классами.md',
      },
      {
        id: 'chapter-2-ассоциации-классов',
        title: 'АССОЦИАЦИИ КЛАССОВ',
        markdownFile: 'chapters/chapter-2-ассоциации-классов.md',
      },
      {
        id: 'chapter-2-контрольные-вопросы',
        title: 'Контрольные вопросы',
        markdownFile: 'chapters/chapter-2-контрольные-вопросы.md',
      },
    ],
  },
  {
    id: 'chapter-3',
    title: 'БАЗИС ЯЗЫКА  ВИЗУАЛЬНОГО МОДЕЛИРОВАНИЯ',
    sections: [
      {
        id: 'chapter-3-1',
        title: 'БАЗИС ЯЗЫКА  ВИЗУАЛЬНОГО МОДЕЛИРОВАНИЯ',
        markdownFile: 'chapters/chapter-3-1.md',
      },
      {
        id: 'chapter-3-унифицированный-язык-моделирования',
        title: 'УНИФИЦИРОВАННЫЙ ЯЗЫК МОДЕЛИРОВАНИЯ',
        markdownFile: 'chapters/chapter-3-унифицированный-язык-моделирования.md',
      },
      {
        id: 'chapter-3-контрольные-вопросы',
        title: 'Контрольные вопросы',
        markdownFile: 'chapters/chapter-3-контрольные-вопросы.md',
      },
    ],
  },
  {
    id: 'chapter-4',
    title: 'ОРГАНИЗАЦИЯ ПРОЦЕССА КОНСТРУИРОВАНИЯ',
    sections: [
      {
        id: 'chapter-4-1',
        title: 'ОРГАНИЗАЦИЯ ПРОЦЕССА КОНСТРУИРОВАНИЯ',
        markdownFile: 'chapters/chapter-4-1.md',
      },
      {
        id: 'chapter-4-определение-технологии-конструирования-программного-обеспечения',
        title: 'ОПРЕДЕЛЕНИЕ ТЕХНОЛОГИИ КОНСТРУИРОВАНИЯ  ПРОГРАММНОГО ОБЕСПЕЧЕНИЯ',
        markdownFile: 'chapters/chapter-4-определение-технологии-конструирования-программного-обеспечения.md',
      },
      {
        id: 'chapter-4-классический-жизненный-цикл',
        title: 'КЛАССИЧЕСКИЙ ЖИЗНЕННЫЙ ЦИКЛ',
        markdownFile: 'chapters/chapter-4-классический-жизненный-цикл.md',
      },
      {
        id: 'chapter-4-стратегии-конструирования-программного-обеспечения',
        title: 'СТРАТЕГИИ КОНСТРУИРОВАНИЯ  ПРОГРАММНОГО ОБЕСПЕЧЕНИЯ',
        markdownFile: 'chapters/chapter-4-стратегии-конструирования-программного-обеспечения.md',
      },
      {
        id: 'chapter-4-инкрементная-модель',
        title: 'ИНКРЕМЕНТНАЯ МОДЕЛЬ',
        markdownFile: 'chapters/chapter-4-инкрементная-модель.md',
      },
      {
        id: 'chapter-4-быстрая-разработка-приложений',
        title: 'БЫСТРАЯ РАЗРАБОТКА ПРИЛОЖЕНИЙ',
        markdownFile: 'chapters/chapter-4-быстрая-разработка-приложений.md',
      },
      {
        id: 'chapter-4-спиральная-модель',
        title: 'СПИРАЛЬНАЯ МОДЕЛЬ',
        markdownFile: 'chapters/chapter-4-спиральная-модель.md',
      },
      {
        id: 'chapter-4-модели-качества-процессов-конструирования',
        title: 'МОДЕЛИ КАЧЕСТВА ПРОЦЕССОВ КОНСТРУИРОВАНИЯ',
        markdownFile: 'chapters/chapter-4-модели-качества-процессов-конструирования.md',
      },
      {
        id: 'chapter-4-контрольные-вопросы',
        title: 'Контрольные вопросы',
        markdownFile: 'chapters/chapter-4-контрольные-вопросы.md',
      },
    ],
  },
  {
    id: 'conclusion',
    title: 'Заключение',
    sections: [
      {
        id: 'conclusion-1',
        title: 'Заключение',
        markdownFile: 'chapters/conclusion-1.md',
      },
    ],
  },
];