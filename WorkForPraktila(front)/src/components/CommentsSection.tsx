// src/components/CommentsSection.tsx
import { useState, useEffect } from 'react';
import { api } from '../services/api';
import { useAuth } from '../contexts/AuthContext';

interface Comment {
    id: number;
    user_id: number;
    user_name: string;
    text: string;
    created_at: string;
}

interface Props {
    targetUserId: number;
}

function CommentsSection({ targetUserId }: Props) {
    const { user } = useAuth();
    const [comments, setComments] = useState<Comment[]>([]);
    const [newComment, setNewComment] = useState('');
    const [loading, setLoading] = useState(false);
    const [sending, setSending] = useState(false);

    const loadComments = async () => {
        setLoading(true);
        try {
            const data = await api.getComments(targetUserId);
            setComments(data.comments);
        } catch (err) {
            console.error('Ошибка загрузки комментариев', err);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        loadComments();
    }, [targetUserId]);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!user) {
            alert('Войдите, чтобы оставить отзыв');
            return;
        }
        if (!newComment.trim()) return;
        setSending(true);
        try {
            await api.addComment(user.id, targetUserId, newComment.trim());
            setNewComment('');
            await loadComments(); // перезагрузить
        } catch (err: any) {
            alert(err.message || 'Ошибка при отправке');
        } finally {
            setSending(false);
        }
    };

    const formatDate = (iso: string) => {
        const date = new Date(iso);
        return date.toLocaleString('ru-RU');
    };

    return (
        <div style={styles.container}>
            <h3>📝 Отзывы о пользователе</h3>

            {user && user.id !== targetUserId && (
                <form onSubmit={handleSubmit} style={styles.form}>
                    <textarea
                        value={newComment}
                        onChange={(e) => setNewComment(e.target.value)}
                        placeholder="Напишите ваш отзыв о кандидате..."
                        rows={3}
                        style={styles.textarea}
                    />
                    <button type="submit" disabled={sending} style={styles.button}>
                        {sending ? 'Отправка...' : 'Отправить отзыв'}
                    </button>
                </form>
            )}

            {loading && <div>Загрузка отзывов...</div>}

            <div style={styles.commentsList}>
                {comments.length === 0 && !loading && (
                    <div style={styles.empty}>Пока нет отзывов. Будьте первым!</div>
                )}
                {comments.map(comment => (
                    <div key={comment.id} style={styles.comment}>
                        <div style={styles.commentHeader}>
                            <strong>{comment.user_name}</strong>
                            <span style={styles.date}>{formatDate(comment.created_at)}</span>
                        </div>
                        <div style={styles.commentText}>{comment.text}</div>
                    </div>
                ))}
            </div>
        </div>
    );
}

const styles: { [key: string]: React.CSSProperties } = {
    container: {
        marginTop: '30px',
        borderTop: '1px solid #eee',
        paddingTop: '20px',
    },
    form: {
        marginBottom: '20px',
    },
    textarea: {
        width: '100%',
        padding: '10px',
        borderRadius: '8px',
        border: '1px solid #ddd',
        fontFamily: 'inherit',
        fontSize: '14px',
        resize: 'vertical',
    },
    button: {
        marginTop: '10px',
        padding: '8px 16px',
        backgroundColor: '#ff6b6b',
        color: 'white',
        border: 'none',
        borderRadius: '8px',
        cursor: 'pointer',
    },
    commentsList: {
        display: 'flex',
        flexDirection: 'column',
        gap: '15px',
    },
    comment: {
        backgroundColor: '#f9f9f9',
        borderRadius: '10px',
        padding: '12px',
    },
    commentHeader: {
        display: 'flex',
        justifyContent: 'space-between',
        marginBottom: '8px',
        fontSize: '14px',
        color: '#666',
    },
    date: {
        fontSize: '12px',
    },
    commentText: {
        fontSize: '14px',
        lineHeight: '1.4',
    },
    empty: {
        textAlign: 'center',
        color: '#999',
        padding: '20px',
    },
};

export default CommentsSection;