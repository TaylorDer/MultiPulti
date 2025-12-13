import React, { useState } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import './Playground.css';

interface IterationData {
  iteration: number;
  value: number;
  gradient: number;
}

const Playground: React.FC = () => {
  const [iterations, setIterations] = useState<IterationData[]>([]);
  const [isRunning, setIsRunning] = useState(false);
  const [alpha, setAlpha] = useState(0.1);
  const [initialValue, setInitialValue] = useState(5);
  const [targetValue, setTargetValue] = useState(0);

  const runGradientDescent = () => {
    setIsRunning(true);
    const data: IterationData[] = [];
    let currentValue = initialValue;
    const maxIterations = 50;

    for (let i = 0; i <= maxIterations; i++) {
      // Простая функция: минимизируем (x - target)^2
      const gradient = 2 * (currentValue - targetValue);
      currentValue = currentValue - alpha * gradient;

      data.push({
        iteration: i,
        value: currentValue,
        gradient: Math.abs(gradient),
      });

      if (Math.abs(gradient) < 0.001) break;
    }

    setIterations(data);
    setIsRunning(false);
  };

  const reset = () => {
    setIterations([]);
  };

  return (
    <div className="playground">
      <h1>Интерактивный Playground</h1>
      <p className="playground-subtitle">
        Визуализация алгоритма градиентного спуска
      </p>

      <div className="playground-controls">
        <div className="control-group">
          <label>
            Начальное значение (x₀):
            <input
              type="number"
              value={initialValue}
              onChange={(e) => setInitialValue(parseFloat(e.target.value))}
              step="0.1"
              disabled={isRunning}
            />
          </label>
        </div>

        <div className="control-group">
          <label>
            Целевое значение:
            <input
              type="number"
              value={targetValue}
              onChange={(e) => setTargetValue(parseFloat(e.target.value))}
              step="0.1"
              disabled={isRunning}
            />
          </label>
        </div>

        <div className="control-group">
          <label>
            Шаг обучения (α):
            <input
              type="number"
              value={alpha}
              onChange={(e) => setAlpha(parseFloat(e.target.value))}
              step="0.01"
              min="0.01"
              max="1"
              disabled={isRunning}
            />
          </label>
        </div>

        <div className="control-buttons">
          <button onClick={runGradientDescent} disabled={isRunning} className="playground-btn primary">
            {isRunning ? 'Вычисление...' : 'Запустить'}
          </button>
          <button onClick={reset} disabled={isRunning || iterations.length === 0} className="playground-btn">
            Сбросить
          </button>
        </div>
      </div>

      {iterations.length > 0 && (
        <div className="playground-results">
          <div className="result-info">
            <h3>Результаты оптимизации</h3>
            <p>
              Итераций выполнено: <strong>{iterations.length}</strong>
            </p>
            <p>
              Финальное значение: <strong>{iterations[iterations.length - 1].value.toFixed(4)}</strong>
            </p>
            <p>
              Финальный градиент: <strong>{iterations[iterations.length - 1].gradient.toFixed(6)}</strong>
            </p>
          </div>

          <div className="chart-container">
            <h3>Траектория значения</h3>
            <ResponsiveContainer width="100%" height={400}>
              <LineChart data={iterations}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="iteration" label={{ value: 'Итерация', position: 'insideBottom', offset: -5 }} />
                <YAxis label={{ value: 'Значение', angle: -90, position: 'insideLeft' }} />
                <Tooltip />
                <Legend />
                <Line
                  type="monotone"
                  dataKey="value"
                  stroke="#2563eb"
                  strokeWidth={2}
                  name="Значение функции"
                  dot={{ r: 4 }}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>

          <div className="chart-container">
            <h3>Градиент по итерациям</h3>
            <ResponsiveContainer width="100%" height={400}>
              <LineChart data={iterations}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="iteration" label={{ value: 'Итерация', position: 'insideBottom', offset: -5 }} />
                <YAxis label={{ value: '|Градиент|', angle: -90, position: 'insideLeft' }} />
                <Tooltip />
                <Legend />
                <Line
                  type="monotone"
                  dataKey="gradient"
                  stroke="#ef4444"
                  strokeWidth={2}
                  name="Модуль градиента"
                  dot={{ r: 4 }}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>

          <div className="iterations-table">
            <h3>Детали итераций</h3>
            <div className="table-wrapper">
              <table>
                <thead>
                  <tr>
                    <th>Итерация</th>
                    <th>Значение</th>
                    <th>|Градиент|</th>
                  </tr>
                </thead>
                <tbody>
                  {iterations.map((item, idx) => (
                    <tr key={idx}>
                      <td>{item.iteration}</td>
                      <td>{item.value.toFixed(4)}</td>
                      <td>{item.gradient.toFixed(6)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}

      {iterations.length === 0 && (
        <div className="playground-empty">
          <p>Настройте параметры и нажмите "Запустить" для визуализации алгоритма</p>
        </div>
      )}
    </div>
  );
};

export default Playground;


