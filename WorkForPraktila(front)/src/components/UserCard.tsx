

interface UserCardProps {
    user: any;  // временно
    onClick: () => void;
    likeButton?: React.ReactNode;
}

function UserCard({ user, onClick, likeButton }: UserCardProps) {
    return (
        <div
            onClick={onClick}
            style={{
                border: '1px solid #ddd',
                borderRadius: '15px',
                padding: '15px',
                width: '250px',
                cursor: 'pointer',
                transition: 'transform 0.2s',
                backgroundColor: 'white',
                boxShadow: '0 2px 5px rgba(0,0,0,0.1)'
            }}
            onMouseEnter={(e) => e.currentTarget.style.transform = 'scale(1.02)'}
            onMouseLeave={(e) => e.currentTarget.style.transform = 'scale(1)'}
        >
            <img
                src={user.photo}
                alt={user.name}
                style={{
                    width: '100%',
                    height: '200px',
                    objectFit: 'cover',
                    borderRadius: '10px'
                }}
            />
            <h3>{user.name}, {user.age} лет</h3>
            <p>📍 {user.city}</p>

            {/* Блок: совместимость слева, кнопка справа */}
            <div style={{
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                margin: '10px 0'
            }}>
                <p style={{ color: '#666', fontSize: '14px', margin: 0 }}>
                    {user.description.length > 80
                        ? user.description.slice(0, 80) + '...'
                        : user.description}
                </p>
                {likeButton && <div onClick={(e) => e.stopPropagation()}>{likeButton}</div>}
            </div>

            <div style={{ display: 'flex', gap: '5px', flexWrap: 'wrap', marginTop: '10px' }}>
                {user.interests.slice(0, 3).map((interest, i) => (
                    <span key={i} style={{
                        backgroundColor: '#f0f0f0',
                        padding: '3px 8px',
                        borderRadius: '15px',
                        fontSize: '12px'
                    }}>
                        {interest}
                    </span>
                ))}
            </div>
        </div>
    );
}

export default UserCard;