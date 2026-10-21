// src/pages/RegisterPage.tsx
import { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';

function RegisterPage() {
    const { register } = useAuth();
    const [formData, setFormData] = useState({
        name: '',
        email: '',
        password: '',
        age: '',
        city: '',
        gender: 'female' as 'male' | 'female',
        bio: ''
    });
    const [error, setError] = useState('');

    // Автоматически подставляем looking_for в зависимости от пола
    const looking_for = formData.gender === 'male' ? 'female' : 'male';

    // Можно добавить эффект для лога (необязательно)
    useEffect(() => {
        console.log(`Пол: ${formData.gender}, ищет: ${looking_for}`);
    }, [formData.gender, looking_for]);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError('');

        try {
            await register({
                ...formData,
                age: parseInt(formData.age),
                looking_for, // передаём автоматическое значение
            });
        } catch (err: any) {
            setError(err.message);
        }
    };

    return (
        <div style={styles.container}>
            <form onSubmit={handleSubmit} style={styles.form}>
                <h1 style={styles.title}>Регистрация</h1>

                {error && <div style={styles.error}>{error}</div>}

                <input
                    type="text"
                    placeholder="Имя"
                    value={formData.name}
                    onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                    required
                    style={styles.input}
                />

                <input
                    type="email"
                    placeholder="Email"
                    value={formData.email}
                    onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                    required
                    style={styles.input}
                />

                <input
                    type="password"
                    placeholder="Пароль"
                    value={formData.password}
                    onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                    required
                    style={styles.input}
                />

                <input
                    type="number"
                    placeholder="Возраст"
                    value={formData.age}
                    onChange={(e) => setFormData({ ...formData, age: e.target.value })}
                    required
                    style={styles.input}
                />

                <input
                    type="text"
                    placeholder="Город"
                    value={formData.city}
                    onChange={(e) => setFormData({ ...formData, city: e.target.value })}
                    required
                    style={styles.input}
                />

                <select
                    value={formData.gender}
                    onChange={(e) => setFormData({ ...formData, gender: e.target.value as 'male' | 'female' })}
                    style={styles.input}
                >
                    <option value="female">Женский</option>
                    <option value="male">Мужской</option>
                </select>

                {/* Информируем пользователя, кого он будет искать */}
                <div style={styles.info}>
                    💕 Вы будете искать: {looking_for === 'male' ? 'Мужчину' : 'Женщину'}
                </div>

                <textarea
                    placeholder="О себе (необязательно)"
                    value={formData.bio}
                    onChange={(e) => setFormData({ ...formData, bio: e.target.value })}
                    style={{ ...styles.input, minHeight: '80px' }}
                />

                <button type="submit" style={styles.button}>
                    Зарегистрироваться
                </button>
            </form>
        </div>
    );
}

const styles = {
    container: {
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        minHeight: '100vh',
        backgroundColor: '#f5f5f5'
    },
    form: {
        backgroundColor: 'white',
        padding: '40px',
        borderRadius: '20px',
        boxShadow: '0 4px 15px rgba(0,0,0,0.1)',
        width: '400px'
    },
    title: {
        textAlign: 'center' as const,
        color: '#ff6b6b',
        marginBottom: '30px'
    },
    input: {
        width: '100%',
        padding: '12px',
        marginBottom: '15px',
        border: '1px solid #ddd',
        borderRadius: '8px',
        fontSize: '14px',
        boxSizing: 'border-box' as const
    },
    button: {
        width: '100%',
        padding: '12px',
        backgroundColor: '#ff6b6b',
        color: 'white',
        border: 'none',
        borderRadius: '8px',
        cursor: 'pointer',
        fontSize: '16px',
        fontWeight: 'bold'
    },
    error: {
        backgroundColor: '#fee',
        color: '#c33',
        padding: '10px',
        borderRadius: '8px',
        marginBottom: '15px',
        fontSize: '14px'
    },
    info: {
        backgroundColor: '#e8f0fe',
        padding: '10px',
        borderRadius: '8px',
        marginBottom: '15px',
        fontSize: '14px',
        textAlign: 'center' as const,
        color: '#0066cc'
    }
};

export default RegisterPage;