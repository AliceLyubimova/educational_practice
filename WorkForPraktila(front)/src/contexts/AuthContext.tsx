// src/contexts/AuthContext.tsx
import React, { createContext, useContext, useState, useEffect } from 'react';
import { api } from '../services/api';
import type { UserResponse } from 'C:/WorkForPraktila(front)/src/types/api';

interface User extends UserResponse {}

interface AuthContextType {
    user: User | null;
    isLoading: boolean;
    login: (email: string, password: string) => Promise<void>;
    register: (data: any) => Promise<void>;
    logout: () => void;
    updateUser: (data: Partial<User>) => Promise<void>;
    refreshUser: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
    const [user, setUser] = useState<User | null>(null);
    const [isLoading, setIsLoading] = useState(true);
    
    

    useEffect(() => {
        const loadUser = async () => {
            const savedUserId = localStorage.getItem('userId');
            if (savedUserId) {
                try {
                    const userData = await api.getUserById(parseInt(savedUserId));
                    setUser(userData);
                    localStorage.setItem('user', JSON.stringify(userData));
                } catch (error) {
                    console.error('Ошибка загрузки пользователя:', error);
                    localStorage.removeItem('userId');
                    localStorage.removeItem('user');
                }
            }
            setIsLoading(false);
        };
        
        loadUser();
    }, []);

    const login = async (email: string, password: string) => {
        const response = await api.login({ email, password });
        const userData = await api.getUserById(response.user_id);
        
        setUser(userData);
        localStorage.setItem('user', JSON.stringify(userData));
        localStorage.setItem('userId', String(userData.id));
    };

    const register = async (data: any) => {
        await api.register(data);
        await login(data.email, data.password);
    };

    const logout = () => {
        setUser(null);
        localStorage.removeItem('user');
        localStorage.removeItem('userId');
    };

    const updateUser = async (data: Partial<User>) => {
        if (!user) return;
        await api.updateUser(user.id, data);
        const updatedUser = await api.getUserById(user.id);
        setUser(updatedUser);
        localStorage.setItem('user', JSON.stringify(updatedUser));
    };
    const refreshUser = async () => {
        if (!user) return;
        const updatedUser = await api.getUserById(user.id);
        setUser(updatedUser);
        localStorage.setItem('user', JSON.stringify(updatedUser));
    };

    return (
        <AuthContext.Provider value={{ user, isLoading, login, register, logout, updateUser, refreshUser }}>
            {children}
        </AuthContext.Provider>
    );
}

export function useAuth() {
    const context = useContext(AuthContext);
    if (!context) {
        throw new Error('useAuth must be used within AuthProvider');
    }
    return context;
}