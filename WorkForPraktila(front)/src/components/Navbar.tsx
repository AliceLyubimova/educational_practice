// src/components/Navbar.tsx
interface NavbarProps {
    activeTab: 'profile' | 'candidates' | 'matches';
    onTabChange: (tab: 'profile' | 'candidates' | 'matches') => void;
}

function Navbar({ activeTab, onTabChange }: NavbarProps) {
    const tabs = [
        { id: 'profile' as const, label: '👤 Мой профиль' },
        { id: 'candidates' as const, label: '💑 Кандидаты' },
        { id: 'matches' as const, label: '💕 Мэтчи' }
    ];

    return (
        <nav style={{
            display: 'flex',
            gap: '20px',
            backgroundColor: '#ff6b6b',
            padding: '15px 30px',
            borderRadius: '10px',
            marginBottom: '30px'
        }}>
            {tabs.map(tab => (
                <button
                    key={tab.id}
                    onClick={() => onTabChange(tab.id)}
                    style={{
                        backgroundColor: activeTab === tab.id ? '#fff' : 'transparent',
                        color: activeTab === tab.id ? '#ff6b6b' : '#fff',
                        border: 'none',
                        padding: '10px 20px',
                        borderRadius: '25px',
                        cursor: 'pointer',
                        fontSize: '16px',
                        fontWeight: 'bold',
                        transition: 'all 0.2s'
                    }}
                >
                    {tab.label}
                </button>
            ))}
        </nav>
    );
}

export default Navbar;