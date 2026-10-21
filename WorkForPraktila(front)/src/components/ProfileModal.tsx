import { useEffect, useState } from 'react';
import { api } from '../services/api';
import type { FullUserProfile } from 'C:/WorkForPraktila(front)/src/types/api';
import CommentsSection from './CommentsSection';
interface ProfileModalProps {
    userId: number;
    onClose: () => void;
}

function ProfileModal({ userId, onClose }: ProfileModalProps) {
    const [profile, setProfile] = useState<FullUserProfile | null>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        api.getUserProfileWithPhotos(userId)
            .then(setProfile)
            .catch(console.error)
            .finally(() => setLoading(false));
    }, [userId]);

    if (loading) return <div style={styles.modal}>Загрузка...</div>;
    if (!profile) return <div style={styles.modal}>Ошибка загрузки</div>;

    // Находим аватар среди фото
    const avatarPhoto = profile.photos.find(p => p.is_avatar);
    const avatarUrl = avatarPhoto
        ? api.getPhotoUrl(avatarPhoto.photo_id)
        : `https://ui-avatars.com/api/?name=${encodeURIComponent(profile.name)}&background=ff6b6b&color=fff`;

    return (
        <div style={styles.overlay} onClick={onClose}>
            <div style={styles.modal} onClick={e => e.stopPropagation()}>
                <button style={styles.closeBtn} onClick={onClose}>✕</button>

                <img src={avatarUrl} alt={profile.name} style={styles.avatar} />
                <h2 style={{ color: '#000000' }}>{profile.name}, {profile.age} лет</h2>
                <p>📍 {profile.city}</p>
                <p>📝 {profile.bio || 'Нет описания'}</p>

                <h3>Фотографии</h3>
                <div style={styles.photosGrid}>
                    {profile.photos.map(photo => (
                        <img
                            key={photo.photo_id}
                            src={api.getPhotoUrl(photo.photo_id)}
                            alt="Фото"
                            style={styles.photo}
                        />
                    ))}
                </div>
                <CommentsSection targetUserId={userId} />
            </div>
        </div>
    );
}

const styles: { [key: string]: React.CSSProperties } = {
    overlay: {
        position: 'fixed',
        top: 0, left: 0, right: 0, bottom: 0,
        backgroundColor: 'rgba(0,0,0,0.7)',
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        zIndex: 2000,
    },
    modal: {
        backgroundColor: 'white',
        borderRadius: '20px',
        padding: '20px',
        maxWidth: '600px',
        width: '90%',
        maxHeight: '90vh',
        overflowY: 'auto',
        position: 'relative',
    },
    closeBtn: {
        position: 'absolute',
        top: '10px',
        right: '15px',
        background: 'none',
        border: 'none',
        fontSize: '24px',
        cursor: 'pointer',
    },
    avatar: {
        width: '120px',
        height: '120px',
        borderRadius: '50%',
        objectFit: 'cover',
        margin: '0 auto 15px',
        display: 'block',
    },
    photosGrid: {
        display: 'flex',
        flexWrap: 'wrap',
        gap: '10px',
        marginTop: '10px',
    },
    photo: {
        width: '100px',
        height: '100px',
        objectFit: 'cover',
        borderRadius: '10px',
    },
};

export default ProfileModal;