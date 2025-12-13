import React from 'react';
import './About.css';

const About: React.FC = () => {
  return (
    <div className="about">
      <h1>О пособии</h1>

      <section className="about-section">
        <h2>Описание</h2>
        <p>
          Данное мультимедийное веб-пособие предназначено для изучения дисциплины
          «Методы оптимизации проектных решений». Пособие содержит структурированный
          теоретический материал, интерактивные примеры и визуализации алгоритмов.
        </p>
        <p>
          Пособие основано на учебном материале по получению оптимальных проектных решений
          и их анализу с использованием математических моделей.
        </p>
      </section>

      <section className="about-section">
        <h2>Как пользоваться</h2>
        <ul>
          <li>
            <strong>Навигация:</strong> Используйте боковое меню для перехода между
            главами и разделами. На мобильных устройствах меню открывается через
            кнопку-бургер в шапке.
          </li>
          <li>
            <strong>Чтение:</strong> Прогресс чтения отслеживается автоматически и
            сохраняется в браузере. Вы можете вернуться к последнему прочитанному
            разделу.
          </li>
          <li>
            <strong>Настройки:</strong> Используйте кнопки A+ и A- в боковом меню для
            изменения размера шрифта. Настройки сохраняются автоматически.
          </li>
          <li>
            <strong>Изображения:</strong> Нажмите на любое изображение для просмотра
            в увеличенном виде.
          </li>
          <li>
            <strong>Playground:</strong> Раздел с интерактивными примерами позволяет
            экспериментировать с параметрами алгоритмов и визуализировать результаты.
          </li>
        </ul>
      </section>

      <section className="about-section">
        <h2>Источник</h2>
        <div style={{ 
          marginBottom: '1.5rem', 
          padding: '1.5rem', 
          backgroundColor: '#f9f9f9', 
          borderRadius: '8px',
          border: '1px solid #e0e0e0'
        }}>
          <p style={{ marginBottom: '0.5rem', fontSize: '0.9em', color: '#666' }}>
            Министерство образования и науки Российской Федерации
          </p>
          <p style={{ marginBottom: '0.5rem', fontSize: '0.9em', color: '#666' }}>
            ГОУ ВПО «Тамбовский государственный технический университет»
          </p>
          <p style={{ marginTop: '1rem', marginBottom: '0.5rem', fontSize: '1.1em', fontWeight: 'bold' }}>
            Ю.В. ЛИТОВКА
          </p>
          <p style={{ marginBottom: '1rem', fontSize: '1.1em', fontWeight: 'bold', lineHeight: '1.4' }}>
            ПОЛУЧЕНИЕ ОПТИМАЛЬНЫХ ПРОЕКТНЫХ РЕШЕНИЙ И ИХ АНАЛИЗ С ИСПОЛЬЗОВАНИЕМ МАТЕМАТИЧЕСКИХ МОДЕЛЕЙ
          </p>
          <p style={{ marginTop: '1rem', marginBottom: '0.5rem', fontSize: '0.95em', fontStyle: 'italic' }}>
            Утверждено Ученым советом университета в качестве учебного пособия
          </p>
          <p style={{ marginTop: '1rem', marginBottom: '0.5rem', fontSize: '0.95em' }}>
            Тамбов
          </p>
          <p style={{ marginBottom: '0.5rem', fontSize: '0.95em' }}>
            Издательство ТГТУ
          </p>
          <p style={{ marginBottom: '0.5rem', fontSize: '0.95em' }}>
            2006
          </p>
          <hr style={{ margin: '1rem 0', border: 'none', borderTop: '1px solid #ddd' }} />
          <p style={{ marginTop: '1rem', marginBottom: '0.5rem', fontSize: '0.9em' }}>
            <strong>УДК:</strong> 681.5.001 2-52(076)
          </p>
          <p style={{ marginBottom: '0.5rem', fontSize: '0.9em' }}>
            <strong>ББК:</strong> Л11-1с116я73-5+Ж2-5-05я73-5
          </p>
          <p style={{ marginBottom: '0.5rem', fontSize: '0.9em' }}>
            <strong>ISBN:</strong> 5-8265-0540-0
          </p>
          <p style={{ marginTop: '1rem', marginBottom: '0.5rem', fontSize: '0.9em' }}>
            <strong>Объем:</strong> 160 с.
          </p>
          <p style={{ marginBottom: '0.5rem', fontSize: '0.9em' }}>
            <strong>Тираж:</strong> 200 экз.
          </p>
        </div>
        
        <div style={{ 
          marginBottom: '1.5rem', 
          padding: '1rem', 
          backgroundColor: '#f5f5f5', 
          borderRadius: '8px',
          fontSize: '0.9em'
        }}>
          <p style={{ marginBottom: '0.75rem', fontWeight: 'bold' }}>Рецензенты:</p>
          <p style={{ marginBottom: '0.5rem' }}>
            Заведующий кафедрой «Компьютерное и математическое моделирование» Тамбовского государственного университета им. Г.Р. Державина, доктор технических наук, профессор <strong>А.А. Арзамасцев</strong>
          </p>
          <p style={{ marginBottom: '0.5rem' }}>
            Доцент кафедры «Автоматизированное проектирование технологического оборудования» Тамбовского государственного технического университета, кандидат технических наук <strong>В.Н. Немтинов</strong>
          </p>
        </div>

        <p style={{ marginBottom: '1rem' }}>
          Предложено использование вычислительной техники для решения вычислительных задач на алгоритмическом языке высокого уровня (С++, Паскаль и др.), а также материалы для осваивания пакета прикладных программ автоматизированного моделирования ChemCAD.
        </p>
        <p>
          Предназначено для выполнения лабораторных работ по дисциплинам «Модели и методы анализа проектных решений» 
          и «Оптимизация», а также выполнения курсовой работы по дисциплине «Модели и методы анализа проектных решений» 
          студентами специальности САПР 3–4 курсов.
        </p>
      </section>

      <section className="about-section">
        <h2>Технологии</h2>
        <p>Пособие создано с использованием современных веб-технологий:</p>
        <ul>
          <li>React + TypeScript</li>
          <li>Vite</li>
          <li>React Router</li>
          <li>KaTeX для рендеринга математических формул</li>
          <li>Recharts для построения графиков</li>
          <li>React Markdown для отображения контента</li>
        </ul>
      </section>

      <section className="about-section">
        <h2>О веб-пособии</h2>
        <p>
          Мультимедийное веб-пособие разработано для образовательных целей на основе учебного пособия 
          Ю.В. Литовки. Все материалы используются в образовательных целях.
        </p>
      </section>
    </div>
  );
};

export default About;

