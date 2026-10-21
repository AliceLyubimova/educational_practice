// src/App.tsx
import { useState } from 'react';  // добавить этот импорт
import { AuthProvider, useAuth } from './contexts/AuthContext';
import MainPage from './pages/MainPage';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';

function AppContent() {
    const { user, isLoading } = useAuth();
    const [isRegistering, setIsRegistering] = useState(false);

    if (isLoading) {
        return <div style={styles.loading}>Загрузка...</div>;
    }

    if (!user) {
        if (isRegistering) {
            return (
                <div>
                    <RegisterPage />
                    <button 
                        onClick={() => setIsRegistering(false)}
                        style={styles.switchButton}
                    >
                        Уже есть аккаунт? Войти
                    </button>
                </div>
            );
        }
        return (
            <div>
                <LoginPage />
                <button 
                    onClick={() => setIsRegistering(true)}
                    style={styles.switchButton}
                >
                    Нет аккаунта? Зарегистрироваться
                </button>
            </div>
        );
    }

    return <MainPage />;
}

function App() {
    return (
        <AuthProvider>
            <AppContent />
        </AuthProvider>
    );
}

const styles = {
    switchButton: {
        display: 'block',
        margin: '20px auto',
        padding: '10px 20px',
        backgroundColor: 'transparent',
        border: '1px solid #ff6b6b',
        borderRadius: '25px',
        color: '#ff6b6b',
        cursor: 'pointer',
        fontSize: '14px'
    },
    loading: {
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        minHeight: '100vh',
        fontSize: '18px',
        color: '#666'
    }
};

export default App;