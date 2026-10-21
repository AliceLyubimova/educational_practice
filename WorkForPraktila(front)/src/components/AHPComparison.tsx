import { useState } from 'react';
import { api } from '../services/api';

interface AHPComparisonProps {
  userId: number;
  criteria: string[];               // 'возраст', 'город',
  onWeightsSaved: () => void;      
}

// Шкала Саати для выбора
const SAATY_OPTIONS = [
  { label: '1/9', value: 1/9 },
  { label: '1/7', value: 1/7 },
  { label: '1/5', value: 1/5 },
  { label: '1/3', value: 1/3 },
  { label: '1',   value: 1 },
  { label: '3',   value: 3 },
  { label: '5',   value: 5 },
  { label: '7',   value: 7 },
  { label: '9',   value: 9 },
];

// Генерируем все уникальные пары (i < j)
function generatePairs(criteria: string[]): [string, string][] {
  const pairs: [string, string][] = [];
  for (let i = 0; i < criteria.length; i++) {
    for (let j = i + 1; j < criteria.length; j++) {
      pairs.push([criteria[i], criteria[j]]);
    }
  }
  return pairs;
}

export default function AHPComparison({ userId, criteria, onWeightsSaved }: AHPComparisonProps) {
  const pairs = generatePairs(criteria);
  // Для каждой пары храним выбранное значение (по умолчанию 1)
  const [values, setValues] = useState<Record<string, number>>(() => {
    const init: Record<string, number> = {};
    pairs.forEach(([a, b]) => {
      init[`${a}|${b}`] = 1;
    });
    return init;
  });

  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<{ weights: Record<string, number>; cr: number } | null>(null);
  const [error, setError] = useState('');

  const handleChange = (pairKey: string, val: number) => {
    setValues(prev => ({ ...prev, [pairKey]: val }));
    // После изменения сбрасываем предыдущий результат
    setResult(null);
    setError('');
  };

  const handleCalculate = async () => {
    setLoading(true);
    setError('');
    setResult(null);

    // Формируем массив сравнений
    const comparisons = pairs.map(([a, b]) => ({
      criterion_a: a,
      criterion_b: b,
      value: values[`${a}|${b}`],
    }));

    try {
      const response = await api.calculateWeights(criteria, comparisons);
      setResult({ weights: response.weights, cr: response.cr });
    } catch (err: any) {
      setError(err.message || 'Ошибка расчёта весов');
    } finally {
      setLoading(false);
    }
  };

  const handleSave = async () => {
    if (!result) return;
    setLoading(true);
    try {
      // Сохраняем полученные веса 
      await api.saveWeights(userId, result.weights);
      alert('Веса успешно сохранены!');
      onWeightsSaved(); 
    } catch (err: any) {
      setError(err.message || 'Ошибка сохранения');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: '800px', margin: '0 auto' }}>
      <h3>🎯 Попарное сравнение критериев (шкала Саати)</h3>
      <p style={{ fontSize: '14px', color: '#666' }}>
        Для каждой пары укажите, насколько <strong>левая</strong> важность превосходит <strong>правую</strong>.<br/>
        1 – равны, 3 – умеренное, 5 – сильное, 7 – очень сильное, 9 – абсолютное превосходство.
      </p>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '12px', marginBottom: '20px' }}>
        {pairs.map(([a, b]) => {
          const pairKey = `${a}|${b}`;
          return (
            <div key={pairKey} style={{ display: 'flex', alignItems: 'center', gap: '15px', flexWrap: 'wrap' }}>
              <span style={{ width: '120px', fontWeight: 'bold' }}>{a}</span>
              <select
                value={values[pairKey]}
                onChange={(e) => handleChange(pairKey, parseFloat(e.target.value))}
                style={{ padding: '6px', borderRadius: '6px' }}
              >
                {SAATY_OPTIONS.map(opt => (
                  <option key={opt.label} value={opt.value}>{opt.label}</option>
                ))}
              </select>
              <span style={{ width: '120px', fontWeight: 'bold' }}>{b}</span>
            </div>
          );
        })}
      </div>

      <div style={{ display: 'flex', gap: '15px', marginBottom: '20px' }}>
        <button onClick={handleCalculate} disabled={loading} style={styles.primaryButton}>
          {loading ? 'Расчёт...' : '🧮 Рассчитать веса'}
        </button>
      </div>

      {error && <div style={{ color: 'red', marginBottom: '10px' }}>{error}</div>}

      {result && (
        <div style={{ border: '1px solid #ddd', padding: '15px', borderRadius: '12px', marginBottom: '20px' }}>
          <h4>Результат расчёта</h4>
          <p>Коэффициент согласованности (CR): <strong>{result.cr.toFixed(4)}</strong>
            {result.cr > 0.1 && <span style={{ color: 'orange' }}> (CR &gt; 0.1 – желательно пересмотреть сравнения)</span>}
            {result.cr <= 0.1 && <span style={{ color: 'green' }}> (✓ согласованно)</span>}
          </p>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '12px', marginTop: '10px' }}>
            {Object.entries(result.weights).map(([criterion, weight]) => (
              <div key={criterion} style={{ background: '#f0f0f0', padding: '5px 12px', borderRadius: '20px' }}>
                {criterion}: {(weight * 100).toFixed(1)}%
              </div>
            ))}
          </div>
          <button onClick={handleSave} disabled={loading} style={{ ...styles.primaryButton, marginTop: '15px', backgroundColor: '#28a745' }}>
            💾 Сохранить эти веса
          </button>
        </div>
      )}
    </div>
  );
}

const styles = {
  primaryButton: {
    padding: '10px 20px',
    backgroundColor: '#ff6b6b',
    color: 'white',
    border: 'none',
    borderRadius: '8px',
    cursor: 'pointer',
    fontSize: '16px',
  },
};
