import { Link } from 'react-router-dom'
import { useEffect, useRef } from 'react'

const FEATURES = [
    {
        icon: '⚡',
        color: '#7c6ef7',
        title: 'GitHub Intelligence',
        desc: 'Coral queries your actual repos, languages, and projects in real-time. No manual input needed.',
    },
    {
        icon: '🎯',
        color: '#1ddf8a',
        title: 'Match Score',
        desc: 'Claude analyzes your profile against the JD — skill gaps, matched skills, and company insights.',
    },
    {
        icon: '📄',
        color: '#f5c542',
        title: 'Tailored Resume',
        desc: 'Beautiful HTML resume generated specifically for the role. Download and send.',
    },
    {
        icon: '✉️',
        color: '#22d9f3',
        title: 'Cover Letter',
        desc: 'Compelling, personalized cover letter that highlights your most relevant experience.',
    },
    {
        icon: '❓',
        color: '#ff4d6a',
        title: 'Interview Prep',
        desc: '15 likely questions with answer hints — technical, behavioral, and company-specific.',
    },
    {
        icon: '🗓️',
        color: '#a89cf8',
        title: '30-Day Plan',
        desc: 'Interactive preparation checklist — week by week, day by day. Close every skill gap.',
    },
]

const TECH = ['Coral SQL', 'Claude AI', 'GitHub API', 'Notion API', 'React', 'FastAPI', 'Cross-Source Joins']

const STEPS = [
    { num: '01', title: 'Paste JD', desc: 'Paste any job description — internship, full-time, anything.' },
    { num: '02', title: 'Coral Queries', desc: 'Agent queries your GitHub + Notion via SQL in real-time.' },
    { num: '03', title: 'AI Analysis', desc: 'Claude compares your profile against the role requirements.' },
    { num: '04', title: 'Career Pack', desc: 'Resume, cover letter, prep plan — all generated instantly.' },
]

export default function Home() {
    const revealRefs = useRef([])

    useEffect(() => {
        const observer = new IntersectionObserver(
            (entries) => entries.forEach(e => {
                if (e.isIntersecting) e.target.classList.add('visible')
            }),
            { threshold: 0.1 }
        )
        revealRefs.current.forEach(el => el && observer.observe(el))
        return () => observer.disconnect()
    }, [])

    const addRef = (el) => {
        if (el && !revealRefs.current.includes(el)) revealRefs.current.push(el)
    }

    return (
        <div style={{ position: 'relative', zIndex: 1, paddingTop: '64px' }}>

            {/* ── HERO ── */}
            <section style={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', padding: '80px 2rem' }}>
                <div style={{ maxWidth: '900px', width: '100%', textAlign: 'center' }}>

                    {/* Badge */}
                    <div style={{
                        display: 'inline-flex', alignItems: 'center', gap: '8px',
                        padding: '6px 16px', borderRadius: '20px', marginBottom: '32px',
                        background: 'rgba(124,110,247,0.1)', border: '1px solid rgba(124,110,247,0.25)',
                        fontFamily: 'JetBrains Mono', fontSize: '12px', color: '#a89cf8',
                    }}>
                        <span style={{
                            width: '6px', height: '6px', borderRadius: '50%',
                            background: '#1ddf8a', display: 'inline-block',
                            boxShadow: '0 0 8px #1ddf8a',
                        }} />
                        Powered by Coral + Claude AI
                    </div>

                    {/* Headline */}
                    <h1 style={{
                        fontFamily: 'Syne, sans-serif', fontWeight: 800, lineHeight: 1.05,
                        fontSize: 'clamp(3rem, 8vw, 7rem)', marginBottom: '24px', letterSpacing: '-2px',
                    }}>
                        <span style={{ color: '#eeeeff' }}>Your AI</span>
                        <br />
                        <span style={{
                            background: 'linear-gradient(135deg, #7c6ef7 0%, #22d9f3 50%, #1ddf8a 100%)',
                            WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent',
                            backgroundSize: '200% auto', animation: 'shimmer 3s linear infinite',
                        }}>Career Agent</span>
                    </h1>

                    {/* Sub */}
                    <p style={{
                        fontSize: 'clamp(16px, 2vw, 20px)', color: '#8888aa', lineHeight: 1.7,
                        maxWidth: '600px', margin: '0 auto 48px', fontFamily: 'Space Grotesk',
                    }}>
                        Paste a job description. CareerCraft queries your GitHub profile via Coral SQL,
                        analyzes your fit with Claude AI, and generates a complete career pack in seconds.
                    </p>

                    {/* CTA */}
                    <div style={{ display: 'flex', gap: '16px', justifyContent: 'center', flexWrap: 'wrap' }}>
                        <Link to="/analyze" style={{
                            padding: '16px 40px', borderRadius: '14px', fontSize: '16px', fontWeight: 700,
                            background: 'linear-gradient(135deg, #5b4de0, #7c6ef7)',
                            color: '#fff', textDecoration: 'none', fontFamily: 'Space Grotesk',
                            boxShadow: '0 8px 30px rgba(124,110,247,0.4)',
                            transition: 'all 0.3s', display: 'inline-block',
                            animation: 'pulse-glow 3s infinite',
                        }}>
                            Start Analyzing →
                        </Link>
                        <a href="https://github.com/shivakumar2006/careercraft" target="_blank" rel="noreferrer" style={{
                            padding: '16px 32px', borderRadius: '14px', fontSize: '16px', fontWeight: 600,
                            background: 'transparent', color: '#8888aa', textDecoration: 'none',
                            fontFamily: 'Space Grotesk', border: '1px solid rgba(26,26,48,0.8)',
                            transition: 'all 0.2s',
                        }}>
                            View on GitHub
                        </a>
                    </div>

                    {/* Terminal preview */}
                    <div style={{
                        marginTop: '64px', borderRadius: '20px', overflow: 'hidden',
                        border: '1px solid rgba(26,26,48,0.8)',
                        background: 'rgba(5,5,8,0.9)', backdropFilter: 'blur(20px)',
                        textAlign: 'left', animation: 'fadeUp 0.8s ease 0.3s forwards', opacity: 0,
                    }}>
                        <div style={{
                            padding: '12px 16px', borderBottom: '1px solid rgba(26,26,48,0.8)',
                            display: 'flex', alignItems: 'center', gap: '8px', background: 'rgba(15,15,28,0.9)',
                        }}>
                            {['#ff5f57', '#febc2e', '#28c840'].map((c, i) => (
                                <div key={i} style={{ width: '12px', height: '12px', borderRadius: '50%', background: c }} />
                            ))}
                            <span style={{ marginLeft: '8px', fontFamily: 'JetBrains Mono', fontSize: '12px', color: '#44446a' }}>
                                careercraft — agent
                            </span>
                        </div>
                        <div style={{ padding: '24px', fontFamily: 'JetBrains Mono', fontSize: '13px', lineHeight: 2 }}>
                            {[
                                { prompt: '❯', text: '🔍 Fetching your GitHub repos via Coral SQL...', color: '#22d9f3' },
                                { prompt: '❯', text: '✅ Found 57 repos, 6 languages', color: '#1ddf8a' },
                                { prompt: '❯', text: '🧠 Analyzing JD vs your profile with Claude...', color: '#a89cf8' },
                                { prompt: '❯', text: '✅ Match Score: 78/100 — Strong Go candidate', color: '#1ddf8a' },
                                { prompt: '❯', text: '📄 Generating tailored resume...', color: '#f5c542' },
                                { prompt: '❯', text: '🎯 Building interactive dashboard...', color: '#f5c542' },
                                { prompt: '❯', text: '✅ Career pack ready — 4 files generated', color: '#1ddf8a' },
                            ].map((line, i) => (
                                <div key={i} style={{ display: 'flex', gap: '12px' }}>
                                    <span style={{ color: '#7c6ef7' }}>{line.prompt}</span>
                                    <span style={{ color: line.color }}>{line.text}</span>
                                </div>
                            ))}
                            <div style={{ display: 'flex', gap: '12px' }}>
                                <span style={{ color: '#7c6ef7' }}>❯</span>
                                <span style={{
                                    display: 'inline-block', width: '8px', height: '16px',
                                    background: '#7c6ef7', animation: 'blink 1s infinite', verticalAlign: 'middle',
                                }} />
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            {/* ── MARQUEE ── */}
            <div style={{ overflow: 'hidden', padding: '20px 0', borderTop: '1px solid rgba(26,26,48,0.6)', borderBottom: '1px solid rgba(26,26,48,0.6)', marginBottom: '100px' }}>
                <div className="marquee-track">
                    {[...TECH, ...TECH].map((t, i) => (
                        <span key={i} style={{
                            fontFamily: 'JetBrains Mono', fontSize: '13px', color: '#44446a',
                            padding: '0 32px', whiteSpace: 'nowrap',
                        }}>
                            <span style={{ color: '#7c6ef7', marginRight: '16px' }}>◆</span>
                            {t}
                        </span>
                    ))}
                </div>
            </div>

            {/* ── HOW IT WORKS ── */}
            <section style={{ maxWidth: '1000px', margin: '0 auto', padding: '0 2rem 120px' }} ref={addRef} className="reveal">
                <div style={{ textAlign: 'center', marginBottom: '60px' }}>
                    <div style={{
                        fontFamily: 'JetBrains Mono', fontSize: '11px', color: '#7c6ef7',
                        letterSpacing: '0.2em', textTransform: 'uppercase', marginBottom: '12px',
                    }}>How it works</div>
                    <h2 style={{ fontFamily: 'Syne', fontWeight: 800, fontSize: 'clamp(2rem, 4vw, 3rem)', color: '#eeeeff' }}>
                        Four steps to your{' '}
                        <span style={{ background: 'linear-gradient(135deg, #7c6ef7, #22d9f3)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
                            dream job
                        </span>
                    </h2>
                </div>

                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '24px' }}>
                    {STEPS.map((step, i) => (
                        <div key={i} style={{
                            padding: '28px', borderRadius: '16px',
                            background: 'rgba(15,15,28,0.8)', border: '1px solid rgba(26,26,48,0.8)',
                            position: 'relative', overflow: 'hidden',
                            transition: 'all 0.3s',
                        }}>
                            <div style={{
                                fontFamily: 'Syne', fontWeight: 800, fontSize: '48px',
                                color: 'rgba(124,110,247,0.12)', lineHeight: 1, marginBottom: '16px',
                            }}>{step.num}</div>
                            <div style={{ fontFamily: 'Space Grotesk', fontWeight: 700, fontSize: '16px', color: '#eeeeff', marginBottom: '8px' }}>
                                {step.title}
                            </div>
                            <div style={{ fontFamily: 'Space Grotesk', fontSize: '14px', color: '#8888aa', lineHeight: 1.6 }}>
                                {step.desc}
                            </div>
                        </div>
                    ))}
                </div>
            </section>

            {/* ── FEATURES ── */}
            <section style={{ maxWidth: '1100px', margin: '0 auto', padding: '0 2rem 120px' }} ref={addRef} className="reveal">
                <div style={{ textAlign: 'center', marginBottom: '60px' }}>
                    <div style={{ fontFamily: 'JetBrains Mono', fontSize: '11px', color: '#7c6ef7', letterSpacing: '0.2em', textTransform: 'uppercase', marginBottom: '12px' }}>
                        Features
                    </div>
                    <h2 style={{ fontFamily: 'Syne', fontWeight: 800, fontSize: 'clamp(2rem, 4vw, 3rem)', color: '#eeeeff' }}>
                        Everything you need to{' '}
                        <span style={{ background: 'linear-gradient(135deg, #1ddf8a, #22d9f3)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
                            land the role
                        </span>
                    </h2>
                </div>

                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '20px' }}>
                    {FEATURES.map((f, i) => (
                        <div key={i} style={{
                            padding: '28px', borderRadius: '16px',
                            background: 'rgba(15,15,28,0.8)', border: '1px solid rgba(26,26,48,0.8)',
                            transition: 'all 0.3s', cursor: 'default',
                        }}
                            onMouseEnter={e => {
                                e.currentTarget.style.borderColor = `${f.color}40`
                                e.currentTarget.style.transform = 'translateY(-4px)'
                                e.currentTarget.style.boxShadow = `0 20px 40px ${f.color}10`
                            }}
                            onMouseLeave={e => {
                                e.currentTarget.style.borderColor = 'rgba(26,26,48,0.8)'
                                e.currentTarget.style.transform = 'none'
                                e.currentTarget.style.boxShadow = 'none'
                            }}
                        >
                            <div style={{
                                width: '48px', height: '48px', borderRadius: '12px', marginBottom: '16px',
                                background: `${f.color}15`, border: `1px solid ${f.color}30`,
                                display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '22px',
                            }}>{f.icon}</div>
                            <div style={{ fontFamily: 'Space Grotesk', fontWeight: 700, fontSize: '16px', color: '#eeeeff', marginBottom: '8px' }}>
                                {f.title}
                            </div>
                            <div style={{ fontFamily: 'Space Grotesk', fontSize: '14px', color: '#8888aa', lineHeight: 1.65 }}>
                                {f.desc}
                            </div>
                        </div>
                    ))}
                </div>
            </section>

            {/* ── CTA FOOTER ── */}
            <section style={{ maxWidth: '800px', margin: '0 auto', padding: '0 2rem 120px', textAlign: 'center' }} ref={addRef} className="reveal">
                <div style={{
                    padding: '60px 40px', borderRadius: '24px',
                    background: 'linear-gradient(135deg, rgba(91,77,224,0.15), rgba(124,110,247,0.08))',
                    border: '1px solid rgba(124,110,247,0.2)',
                    position: 'relative', overflow: 'hidden',
                }}>
                    <div style={{
                        position: 'absolute', inset: 0,
                        background: 'radial-gradient(ellipse at 50% 0%, rgba(124,110,247,0.12) 0%, transparent 60%)',
                        pointerEvents: 'none',
                    }} />
                    <h2 style={{ fontFamily: 'Syne', fontWeight: 800, fontSize: 'clamp(1.8rem, 4vw, 2.8rem)', color: '#eeeeff', marginBottom: '16px' }}>
                        Ready to land your dream role?
                    </h2>
                    <p style={{ fontFamily: 'Space Grotesk', fontSize: '16px', color: '#8888aa', marginBottom: '36px', lineHeight: 1.7 }}>
                        Paste a JD, let Coral query your GitHub, let Claude do the analysis.
                        Your entire career pack in under 60 seconds.
                    </p>
                    <Link to="/analyze" style={{
                        padding: '16px 48px', borderRadius: '14px', fontSize: '16px', fontWeight: 700,
                        background: 'linear-gradient(135deg, #5b4de0, #7c6ef7)',
                        color: '#fff', textDecoration: 'none', fontFamily: 'Space Grotesk',
                        boxShadow: '0 8px 30px rgba(124,110,247,0.4)',
                        display: 'inline-block', transition: 'all 0.3s',
                    }}>
                        Start Now — It's Free →
                    </Link>
                </div>
            </section>

        </div>
    )
}