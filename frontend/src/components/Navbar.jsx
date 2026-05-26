import { Link, useLocation } from 'react-router-dom'

export default function Navbar() {
    const location = useLocation()

    return (
        <nav style={{
            position: 'fixed', top: 0, left: 0, right: 0, zIndex: 50,
            height: '64px', display: 'flex', alignItems: 'center',
            justifyContent: 'space-between', padding: '0 2rem',
            background: 'rgba(4,4,10,0.85)', backdropFilter: 'blur(24px)',
            borderBottom: '1px solid rgba(26,26,48,0.8)',
        }}>
            <Link to="/" style={{ display: 'flex', alignItems: 'center', gap: '12px', textDecoration: 'none' }}>
                <div style={{
                    width: '34px', height: '34px', borderRadius: '10px',
                    background: 'linear-gradient(135deg, #5b4de0, #7c6ef7)',
                    boxShadow: '0 0 20px rgba(124,110,247,0.5)',
                    display: 'flex', alignItems: 'center', justifyContent: 'center',
                    fontFamily: 'JetBrains Mono', fontWeight: 700, fontSize: '12px', color: '#fff',
                }}>CC</div>
                <span style={{
                    fontFamily: 'Syne, sans-serif', fontWeight: 800, fontSize: '18px',
                    background: 'linear-gradient(135deg, #eeeeff, #a89cf8)',
                    WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent',
                }}>CareerCraft</span>
            </Link>

            <div style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
                {[{ to: '/', label: 'Home' }, { to: '/analyze', label: 'Analyze' }].map(({ to, label }) => (
                    <Link key={to} to={to} style={{
                        padding: '8px 16px', borderRadius: '10px', fontSize: '14px',
                        fontWeight: 500, textDecoration: 'none', fontFamily: 'Space Grotesk',
                        transition: 'all 0.2s',
                        color: location.pathname === to ? '#a89cf8' : '#8888aa',
                        background: location.pathname === to ? 'rgba(124,110,247,0.12)' : 'transparent',
                        border: location.pathname === to ? '1px solid rgba(124,110,247,0.25)' : '1px solid transparent',
                    }}>{label}</Link>
                ))}
                <Link to="/analyze" style={{
                    marginLeft: '12px', padding: '9px 20px', borderRadius: '12px',
                    fontSize: '14px', fontWeight: 600, textDecoration: 'none',
                    background: 'linear-gradient(135deg, #5b4de0, #7c6ef7)',
                    color: '#fff', fontFamily: 'Space Grotesk',
                    boxShadow: '0 4px 20px rgba(124,110,247,0.3)',
                    transition: 'all 0.3s',
                }}>Get Started →</Link>
            </div>
        </nav>
    )
}