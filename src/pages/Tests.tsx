import React, { useMemo, useState } from 'react';
import { tests, type TestBlock } from '../data/tests';
import './Tests.css';

type AnswersState = Record<string, Record<string, string | undefined>>; // testId -> questionId -> optionId

function scoreTest(test: TestBlock, answers: Record<string, string | undefined>) {
  const total = test.questions.length;
  const correct = test.questions.reduce((acc, q) => acc + (answers[q.id] === q.correctOptionId ? 1 : 0), 0);
  return { total, correct };
}

const Tests: React.FC = () => {
  const [activeTestId, setActiveTestId] = useState<string>(tests[0]?.id ?? '');
  const [submitted, setSubmitted] = useState<Record<string, boolean>>({});
  const [answersByTest, setAnswersByTest] = useState<AnswersState>({});

  const activeTest = useMemo(() => tests.find((t) => t.id === activeTestId) ?? tests[0], [activeTestId]);
  const activeAnswers = answersByTest[activeTest?.id ?? ''] ?? {};
  const isSubmitted = submitted[activeTest?.id ?? ''] ?? false;

  const result = useMemo(() => {
    if (!activeTest) return null;
    return scoreTest(activeTest, activeAnswers);
  }, [activeTest, activeAnswers]);

  if (!activeTest) {
    return (
      <div className="tests">
        <h1>Тесты</h1>
        <p>Пока нет доступных тестов.</p>
      </div>
    );
  }

  const setAnswer = (testId: string, questionId: string, optionId: string) => {
    setAnswersByTest((prev) => ({
      ...prev,
      [testId]: {
        ...(prev[testId] ?? {}),
        [questionId]: optionId,
      },
    }));
  };

  const handleSubmit = () => {
    setSubmitted((prev) => ({ ...prev, [activeTest.id]: true }));
  };

  const handleReset = () => {
    setSubmitted((prev) => ({ ...prev, [activeTest.id]: false }));
    setAnswersByTest((prev) => ({ ...prev, [activeTest.id]: {} }));
  };

  const answeredCount = activeTest.questions.filter((q) => !!activeAnswers[q.id]).length;
  const canSubmit = answeredCount === activeTest.questions.length;

  return (
    <div className="tests">
      <h1>Тесты</h1>
      <p className="tests-intro">Небольшие проверочные задания по темам пособия.</p>

      <div className="tests-layout">
        <aside className="tests-sidebar">
          <h2 className="tests-sidebar-title">Список тестов</h2>
          <div className="tests-list">
            {tests.map((t) => {
              const tAnswers = answersByTest[t.id] ?? {};
              const tSubmitted = submitted[t.id] ?? false;
              const tResult = tSubmitted ? scoreTest(t, tAnswers) : null;
              return (
                <button
                  key={t.id}
                  className={`tests-list-item ${t.id === activeTestId ? 'active' : ''}`}
                  onClick={() => setActiveTestId(t.id)}
                  type="button"
                >
                  <div className="tests-list-item-title">{t.title}</div>
                  <div className="tests-list-item-meta">
                    {tSubmitted && tResult ? (
                      <span>
                        Результат: {tResult.correct}/{tResult.total}
                      </span>
                    ) : (
                      <span>
                        Ответов: {Object.keys(tAnswers).length}/{t.questions.length}
                      </span>
                    )}
                  </div>
                </button>
              );
            })}
          </div>
        </aside>

        <section className="tests-content">
          <div className="tests-card">
            <div className="tests-card-header">
              <div>
                <h2 className="tests-title">{activeTest.title}</h2>
                {activeTest.description && <p className="tests-description">{activeTest.description}</p>}
              </div>
              {isSubmitted && result && (
                <div className="tests-score">
                  <div className="tests-score-number">
                    {result.correct}/{result.total}
                  </div>
                  <div className="tests-score-label">правильных</div>
                </div>
              )}
            </div>

            <div className="tests-progress">
              <div className="tests-progress-bar">
                <div
                  className="tests-progress-bar-fill"
                  style={{ width: `${Math.round((answeredCount / activeTest.questions.length) * 100)}%` }}
                />
              </div>
              <div className="tests-progress-text">
                Ответов: {answeredCount}/{activeTest.questions.length}
              </div>
            </div>

            <div className="tests-questions">
              {activeTest.questions.map((q, idx) => {
                const chosen = activeAnswers[q.id];
                const isCorrect = chosen === q.correctOptionId;
                return (
                  <div key={q.id} className={`tests-question ${isSubmitted ? (isCorrect ? 'correct' : 'wrong') : ''}`}>
                    <div className="tests-question-title">
                      <span className="tests-question-index">{idx + 1}.</span> {q.prompt}
                    </div>

                    <div className="tests-options">
                      {q.options.map((opt) => {
                        const checked = chosen === opt.id;
                        const showCorrect = isSubmitted && opt.id === q.correctOptionId;
                        const showWrong = isSubmitted && checked && opt.id !== q.correctOptionId;
                        return (
                          <label
                            key={opt.id}
                            className={`tests-option ${checked ? 'checked' : ''} ${showCorrect ? 'correct' : ''} ${
                              showWrong ? 'wrong' : ''
                            }`}
                          >
                            <input
                              type="radio"
                              name={`${activeTest.id}:${q.id}`}
                              value={opt.id}
                              checked={checked}
                              onChange={() => setAnswer(activeTest.id, q.id, opt.id)}
                              disabled={isSubmitted}
                            />
                            <span className="tests-option-text">{opt.text}</span>
                          </label>
                        );
                      })}
                    </div>

                    {isSubmitted && q.explanation && (
                      <div className="tests-explanation">
                        <strong>Пояснение:</strong> {q.explanation}
                      </div>
                    )}
                  </div>
                );
              })}
            </div>

            <div className="tests-actions">
              {!isSubmitted ? (
                <>
                  <button className="tests-btn secondary" type="button" onClick={handleReset} disabled={answeredCount === 0}>
                    Сбросить
                  </button>
                  <button className="tests-btn primary" type="button" onClick={handleSubmit} disabled={!canSubmit}>
                    Проверить
                  </button>
                </>
              ) : (
                <button className="tests-btn primary" type="button" onClick={handleReset}>
                  Пройти заново
                </button>
              )}
              {!isSubmitted && !canSubmit && (
                <span className="tests-hint">Ответьте на все вопросы, чтобы проверить тест.</span>
              )}
            </div>
          </div>
        </section>
      </div>
    </div>
  );
};

export default Tests;


