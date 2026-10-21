import { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { api } from '../services/api';
import Navbar from '../components/Navbar';
import UserCard from '../components/UserCard';
import type { CandidateInfo, PhotoResponse} from 'C:/WorkForPraktila(front)/src/types/api';
import ProfileModal from '../components/ProfileModal';  // для модалки
import AHPComparison from '../components/AHPComparison';

function MainPage() {
    const { user, logout, updateUser } = useAuth();
    const [activeTab, setActiveTab] = useState<'profile' | 'candidates' | 'matches'>('candidates');
    const [recommendations, setRecommendations] = useState<CandidateInfo[]>([]);
    const [matches, setMatches] = useState<CandidateInfo[]>([]);
    const [loading, setLoading] = useState(true);
    const [likedUsers, setLikedUsers] = useState<Set<number>>(new Set());
    const [userPhotos, setUserPhotos] = useState<PhotoResponse[]>([]);
    const [uploading, setUploading] = useState(false);
    const [savedWeights, setSavedWeights] = useState<Record<string, number> | null>(null);
    const [selectedUserId, setSelectedUserId] = useState<number | null>(null);  // для модалки
    

    

    

    // Загрузка рекомендаций
    const loadRecommendations = async () => {
        if (!user) return;
        setLoading(true);
        try {
            const data = await api.getRecommendations(user.id, 20);
            setRecommendations(data.recommendations);
        } catch (error) {
            console.error('Ошибка загрузки рекомендаций:', error);
        } finally {
            setLoading(false);
        }
    };

    

    // Загрузка мэтчей
    const loadMatches = async () => {
        if (!user) return;
        try {
            const data = await api.getMatches(user.id);
            setMatches(data.matches);
        } catch (error) {
            console.error('Ошибка загрузки мэтчей:', error);
        }
    };

    // Загрузка полученных лайков
    const loadReceivedLikes = async () => {
        if (!user) return;
        try {
            const data = await api.getReceivedLikes(user.id);
            const likedIds = new Set(data.received_likes.map(l => l.candidate_id));
            setLikedUsers(likedIds);
        } catch (error) {
            console.error('Ошибка загрузки лайков:', error);
        }
    };

    // Загрузка фото пользователя
    const loadUserPhotos = async () => {
        if (!user) return;
        try {
            const data = await api.getUserPhotos(user.id);
            setUserPhotos(data.photos);
        } catch (error) {
            console.error('Ошибка загрузки фото:', error);
        }
    };

    const loadSavedWeights = async () => {
        if (!user) return;
        try {
            const data = await api.getWeights(user.id);
            setSavedWeights(data.raw_weights);
        } catch (error) {
            console.error('Ошибка загрузки весов:', error);
        }
    };


    useEffect(() => {
        if (user) {
            
            loadRecommendations();
            loadMatches();
            loadReceivedLikes();
            loadUserPhotos();
            loadSavedWeights();
            
        }
    }, [user]);

    // Обработка лайка
    const handleLike = async (candidateId: number) => {
        if (!user) return;
        
        try {
            const result = await api.like({
                from_user_id: user.id,
                to_user_id: candidateId
            });
            
            if (result.is_match) {
                alert(`🎉 Взаимный лайк! Совместимость: ${result.compatibility_score}%`);
                loadMatches();
                loadReceivedLikes();
            } else {
                alert(result.message);
            }
            
            setLikedUsers(prev => new Set(prev).add(candidateId));
        } catch (error: any) {
            alert(error.message);
        }
    };

    // Загрузка фото
    const handlePhotoUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
        const file = e.target.files?.[0];
        if (!file || !user) return;

        if (!file.type.startsWith('image/')) {
            alert('Пожалуйста, выберите изображение');
            return;
        }

        if (file.size > 5 * 1024 * 1024) {
            alert('Файл слишком большой (макс. 5MB)');
            return;
        }

        setUploading(true);
        try {
            const base64 = await new Promise<string>((resolve, reject) => {
                const reader = new FileReader();
                reader.onload = () => {
                    const result = reader.result as string;
                    const base64Data = result.split(',')[1];
                    resolve(base64Data);
                };
                reader.onerror = reject;
                reader.readAsDataURL(file);
            });

            const result = await api.uploadPhoto(user.id, base64, file.name);
            alert('Фото загружено!');
            loadUserPhotos();
            
            // Если это первое фото, предлагаем сделать аватаром
            if (userPhotos.length === 0) {
                if (confirm('Сделать это фото аватаром?')) {
                    await api.setAvatar(user.id, result.photo_id);
                    await updateUser({});
                    loadUserPhotos();
                }
            }
        } catch (error: any) {
            alert('Ошибка загрузки: ' + error.message);
        } finally {
            setUploading(false);
        }
    };

    // Установка аватара
    const handleSetAvatar = async (photoId: string) => {
        if (!user) return;
        try {
            await api.setAvatar(user.id, photoId);
            alert('Аватар обновлён');
            //await updateUser();
            loadUserPhotos();
        } catch (error: any) {
            alert('Ошибка: ' + error.message);
        }
    };

    // Удаление фото
    const handleDeletePhoto = async (photoId: string) => {
        if (!user) return;
        if (!confirm('Удалить это фото?')) return;

        try {
            await api.deletePhoto(user.id, photoId);
            alert('Фото удалено');
            await loadUserPhotos();     
            //await updateUser({});       
        } catch (error: any) {
            alert('Ошибка: ' + error.message);
        }
    };

    

    const renderCandidates = () => {
        if (loading) {
            return <div style={styles.loading}>Загрузка кандидатов...</div>;
        }

        if (recommendations.length === 0) {
            return <div style={styles.empty}>Нет подходящих кандидатов</div>;
        }

        return (
            <div style={styles.grid}>
                {recommendations.map(candidate => {
                    const avatarUrl = candidate.candidate_avatar
                        ? api.getPhotoUrl(candidate.candidate_avatar)
                        : `https://ui-avatars.com/api/?name=${encodeURIComponent(candidate.candidate_name)}&background=ff6b6b&color=fff`;

                    const isLiked = likedUsers.has(candidate.candidate_id);

                    const likeButton = (
                        <button
                            onClick={() => handleLike(candidate.candidate_id)}
                            disabled={isLiked}
                            style={{
                                padding: '6px 12px',
                                backgroundColor: isLiked ? '#ccc' : '#ff6b6b',
                                color: 'white',
                                border: 'none',
                                borderRadius: '20px',
                                cursor: 'pointer',
                                fontSize: '12px',
                                whiteSpace: 'nowrap'
                            }}
                        >
                            {isLiked ? '❤️ Лайкнут' : '🤍 Лайкнуть'}
                        </button>
                    );

                    return (
                        <UserCard
                            key={candidate.candidate_id}
                            user={{
                                id: candidate.candidate_id,
                                name: candidate.candidate_name,
                                age: candidate.candidate_age || 0,
                                city: candidate.candidate_city || '',
                                photo: avatarUrl,
                                description: `Совместимость: ${candidate.compatibility_score}%`,
                                interests: []
                            }}
                            onClick={() => setSelectedUserId(candidate.candidate_id)}
                            likeButton={likeButton}
                        />
                    );
                })}
            </div>
        );
    };

    const renderMatches = () => {
        if (matches.length === 0) {
            return <div style={styles.empty}>Пока нет взаимных симпатий</div>;
        }

        return (
            <div style={styles.grid}>
                {matches.map(match => {
                    const avatarUrl = match.candidate_avatar
                        ? api.getPhotoUrl(match.candidate_avatar)
                        : `https://ui-avatars.com/api/?name=${encodeURIComponent(match.candidate_name)}&background=ff6b6b&color=fff`;
                    return (
                        <UserCard 
                            key={match.candidate_id}
                            user={{
                                id: match.candidate_id,
                                name: match.candidate_name,
                                age: match.candidate_age || 0,
                                city: match.candidate_city || '',
                                photo: avatarUrl,
                                description: `Совместимость: ${match.compatibility_score}%`,
                                interests: []
                            }}
                            onClick={() => setSelectedUserId(match.candidate_id)}
                        />
                    );
                })}
            </div>
        );
    };

    const renderProfile = () => {
        const avatarUrl = user?.avatar_url
            ? api.getPhotoUrl(user.avatar_url)   
            : user?.avatar || `https://ui-avatars.com/api/?name=${encodeURIComponent(user?.name || '')}&background=ff6b6b&color=fff&size=150`;
        return (
            <div style={styles.profile}>
                {/* Шапка */}
                <div style={styles.profileHeader}>
                    <img
                        src={avatarUrl}
                        alt={user?.name}
                        style={styles.profileAvatar}
                    />
                    <div style={styles.profileInfo}>
                        <h2 style={{ color: '#000000' }}>{user?.name}, {user?.age} лет</h2>
                        <p>📍 {user?.city}</p>
                        <p>📧 {user?.email}</p>
                        <p>🎯 Ищет: {user?.looking_for === 'male' ? 'Мужчину' : 'Женщину'}</p>
                        {user?.bio && <p>📝 {user.bio}</p>}
                    </div>
                </div>

                {/* фотографии */}
                <div style={styles.photosSection}>
                    <h3>Мои фото</h3>
                    <div style={styles.photosGrid}>
                        {userPhotos.map(photo => (
                            <div key={photo.photo_id} style={styles.photoItem}>
                                <img
                                    src={api.getPhotoUrl(photo.photo_id)}
                                    alt="Фото"
                                    style={styles.photoThumb}
                                />
                                <div style={styles.photoActions}>
                                    {!photo.is_avatar && (
                                        <button
                                            onClick={() => handleSetAvatar(photo.photo_id)}
                                            style={styles.photoButton}
                                        >
                                            👑 Аватар
                                        </button>
                                    )}
                                    {photo.is_avatar && (
                                        <span style={styles.avatarBadge}>⭐ Аватар</span>
                                    )}
                                    <button
                                        onClick={() => handleDeletePhoto(photo.photo_id)}
                                        style={{ ...styles.photoButton, backgroundColor: '#dc3545' }}
                                    >
                                        🗑️ Удалить
                                    </button>
                                </div>
                            </div>
                        ))}
                        <label style={styles.uploadBox}>
                            {uploading ? '⏳ Загрузка...' : '📸 + Добавить фото'}
                            <input
                                type="file"
                                accept="image/*"
                                onChange={handlePhotoUpload}
                                disabled={uploading}
                                style={{ display: 'none' }}
                            />
                        </label>
                    </div>
                </div>
                <div style={styles.savedWeightsSection}>
                    <h4>🎯 Текущие веса критериев</h4>
                    {savedWeights ? (
                        <div style={styles.weightsPreview}>
                            {Object.entries(savedWeights).map(([criterion, weight]) => (
                                <div key={criterion} style={styles.weightItem}>
                                    <span>{criterion}:</span>
                                    <span>{(weight * 100).toFixed(1)}%</span>
                                </div>
                            ))}
                        </div>
                    ) : (
                        <p>Веса ещё не заданы. Используйте форму ниже.</p>
                    )}
                </div>
                <div style={styles.weightsSection}>
                    <AHPComparison
                        userId={user!.id}
                        criteria={['возраст', 'город', 'образование', 'доход', 'внешность', 'интересы', 'религия']}
                        onWeightsSaved={() => {
                            loadRecommendations();   // обновить рекомендации
                        }}
                    />
                </div>
            </div>
        );
    };

    return (
        <div style={styles.container}>
            <div style={styles.header}>
                <h1>💕 Подбор супруга</h1>
                <div style={styles.userInfo}>
                    <span>👤 {user?.name}</span>
                    <button onClick={logout} style={styles.logoutButton}>Выйти</button>
                </div>
            </div>
            
            <Navbar activeTab={activeTab} onTabChange={setActiveTab} />
            
            {activeTab === 'candidates' && renderCandidates()}
            {activeTab === 'matches' && renderMatches()}
            {activeTab === 'profile' && renderProfile()}
            {selectedUserId && (
            <ProfileModal 
                userId={selectedUserId} 
                onClose={() => setSelectedUserId(null)} 
            />
        )}
        </div>
    );
}

const styles: { [key: string]: React.CSSProperties } = {
    container: {
        padding: '20px',
        maxWidth: '1200px',
        margin: '0 auto'
    },
    header: {
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        marginBottom: '20px'
    },
    userInfo: {
        display: 'flex',
        gap: '15px',
        alignItems: 'center'
    },
    logoutButton: {
        padding: '8px 16px',
        backgroundColor: '#ddd',
        border: 'none',
        borderRadius: '8px',
        cursor: 'pointer'
    },
    grid: {
        display: 'flex',
        flexWrap: 'wrap',
        gap: '20px',
        justifyContent: 'center'
    },
    likeButton: {
        position: 'absolute',
        bottom: '10px',
        right: '10px',
        padding: '8px 16px',
        border: 'none',
        borderRadius: '20px',
        color: 'white',
        cursor: 'pointer',
        fontSize: '14px'
    },
    loading: {
        textAlign: 'center',
        padding: '40px',
        fontSize: '18px',
        color: '#666'
    },
    empty: {
        textAlign: 'center',
        padding: '40px',
        fontSize: '18px',
        color: '#999'
    },
    profile: {
        backgroundColor: 'white',
        borderRadius: '20px',
        padding: '30px',
        maxWidth: '800px',
        margin: '0 auto'
    },
    profileHeader: {
        display: 'flex',
        gap: '30px',
        marginBottom: '30px',
        flexWrap: 'wrap'
    },
    profileAvatar: {
        width: '150px',
        height: '150px',
        borderRadius: '50%',
        objectFit: 'cover',
        border: '4px solid #ff6b6b'
    },
    profileInfo: {
        flex: 1
    },
    photosSection: {
        marginTop: '30px',
        borderTop: '1px solid #eee',
        paddingTop: '20px'
    },
    photosGrid: {
        display: 'flex',
        flexWrap: 'wrap',
        gap: '15px',
        marginTop: '15px'
    },
    photoItem: {
        position: 'relative',
        width: '150px',
        marginBottom: '40px'
    },
    photoThumb: {
        width: '150px',
        height: '150px',
        objectFit: 'cover',
        borderRadius: '10px'
    },
    photoActions: {
        position: 'absolute',
        bottom: '-35px',
        left: '5px',
        right: '5px',
        display: 'flex',
        gap: '5px',
        flexWrap: 'wrap'
    },
    photoButton: {
        padding: '4px 8px',
        fontSize: '12px',
        backgroundColor: '#007bff',
        color: 'white',
        border: 'none',
        borderRadius: '5px',
        cursor: 'pointer'
    },
    avatarBadge: {
        padding: '4px 8px',
        fontSize: '12px',
        backgroundColor: '#ffc107',
        color: '#333',
        borderRadius: '5px'
    },
    uploadBox: {
        width: '150px',
        height: '150px',
        border: '2px dashed #ccc',
        borderRadius: '10px',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        cursor: 'pointer',
        fontSize: '14px',
        color: '#999',
    },
    weightsSection: {
    marginTop: '30px',
    borderTop: '1px solid #eee',
    paddingTop: '20px',
},
weightsPreview: {
    display: 'flex',
    flexWrap: 'wrap',
    gap: '10px',
    marginBottom: '15px',
},
weightItem: {
    backgroundColor: '#f0f0f0',
    padding: '5px 12px',
    borderRadius: '20px',
    fontSize: '14px',
},
editButton: {
    padding: '8px 16px',
    backgroundColor: '#ff6b6b',
    color: 'white',
    border: 'none',
    borderRadius: '8px',
    cursor: 'pointer',
},
sliderRow: {
    marginBottom: '12px',
},
note: {
    fontSize: '12px',
    color: '#888',
    marginBottom: '10px',
},
buttonsRow: {
    display: 'flex',
    gap: '10px',
    marginTop: '15px',
},
saveButton: {
    padding: '8px 16px',
    backgroundColor: '#28a745',
    color: 'white',
    border: 'none',
    borderRadius: '8px',
    cursor: 'pointer',
},
cancelButton: {
    padding: '8px 16px',
    backgroundColor: '#6c757d',
    color: 'white',
    border: 'none',
    borderRadius: '8px',
    cursor: 'pointer',
},
};

export default MainPage;
