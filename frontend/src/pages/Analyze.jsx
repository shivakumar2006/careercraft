import { useState } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { addLog, setRunning, setDone, setError, reset } from '../store/careerSlice'
import Terminal from '../components/Terminal'
import FileViewer from '../components/FileViewer'
import { api } from '../store/api'

export default function Analyze() {
    const dispatch = useDispatch()
    const { isRunning, isDone, logs } = useSelector(s => s.career)
    const [jd, setJd] = useState('')

    // const [analyzeMutation] = useAnalyzeMutation();

    const [company, setCompany] = useState('')
    const [companyOrg, setCompanyOrg] = useState('')

    console.log("api key: ", import.meta.env)
    console.log("api key : ", import.meta.env.VITE_BACKEND_API_KEY)

    const handleRun = async () => {
        if (!jd.trim() || !company.trim()) return
        dispatch(reset())
        dispatch(setRunning(true))
        dispatch(addLog('🚀 CareerCraft starting...'))
        dispatch(addLog(`📌 Target company: ${company}`))

        try {
            const res = await fetch(`${import.meta.env.VITE_BACKEND_API_KEY}/analyze`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ jd, company, company_org: companyOrg }),
            })

            const reader = res.body.getReader()
            const decoder = new TextDecoder()

            while (true) {
                const { value, done } = await reader.read()
                if (done) break
                const lines = decoder.decode(value).split('\n').filter(Boolean)
                for (const line of lines) {
                    try {
                        const data = JSON.parse(line)
                        if (data.type === 'log') dispatch(addLog(data.msg))
                        if (data.type === 'done') {
                            dispatch(setDone({ files: data.files, analysis: data.analysis }))

                            dispatch(setRunning(false))

                            dispatch(api.util.invalidateTags(["Files"]))
                        }
                        if (data.type === 'error') dispatch(setError(data.msg))
                    } catch { }
                }
            }
        } catch (e) {
            dispatch(setRunning(false))
            dispatch(setError(e.message))
        }
    }

    const handleReset = () => {
        dispatch(reset())
        setJd('')
        setCompany('')
        setCompanyOrg('')
    }

    return (
        <div style={{ position: 'relative', zIndex: 1, paddingTop: '64px', minHeight: '100vh' }}>
            <div style={{ maxWidth: '1300px', margin: '0 auto', padding: '40px 2rem 80px' }}>

                {/* Page header */}
                <div style={{ marginBottom: '40px' }}>
                    <div style={{
                        fontFamily: 'JetBrains Mono', fontSize: '11px', color: '#7c6ef7',
                        letterSpacing: '0.2em', textTransform: 'uppercase', marginBottom: '8px',
                    }}>
                        Career Agent
                    </div>
                    <h1 style={{
                        fontFamily: 'Syne', fontWeight: 800, fontSize: 'clamp(2rem, 4vw, 3rem)',
                        color: '#eeeeff', letterSpacing: '-1px',
                    }}>
                        Paste your{' '}
                        <span style={{
                            background: 'linear-gradient(135deg, #7c6ef7, #22d9f3)',
                            WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent',
                        }}>Job Description</span>
                    </h1>
                    <p style={{ color: '#8888aa', fontSize: '15px', marginTop: '8px', fontFamily: 'Space Grotesk' }}>
                        CareerCraft will query your GitHub via Coral SQL and generate your complete career pack.
                    </p>
                </div>

                {/* Input card */}
                <div style={{
                    padding: '32px', borderRadius: '20px', marginBottom: '32px',
                    background: 'rgba(15,15,28,0.9)', backdropFilter: 'blur(20px)',
                    border: '1px solid rgba(26,26,48,0.8)',
                }}>
                    {/* Company inputs */}
                    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px', marginBottom: '20px' }}>
                        <div>
                            <label style={{ fontFamily: 'JetBrains Mono', fontSize: '11px', color: '#44446a', display: 'block', marginBottom: '8px', letterSpacing: '0.1em', textTransform: 'uppercase' }}>
                                Company Name *
                            </label>
                            <input
                                type="text"
                                placeholder="e.g. Visa, Zerodha, Razorpay"
                                value={company}
                                onChange={e => setCompany(e.target.value)}
                                style={{
                                    width: '100%', padding: '12px 16px', borderRadius: '12px',
                                    background: 'rgba(4,4,10,0.9)', border: '1px solid rgba(26,26,48,0.8)',
                                    color: '#eeeeff', fontSize: '14px', outline: 'none',
                                    fontFamily: 'Space Grotesk', transition: 'border-color 0.2s',
                                }}
                                onFocus={e => e.target.style.borderColor = 'rgba(124,110,247,0.5)'}
                                onBlur={e => e.target.style.borderColor = 'rgba(26,26,48,0.8)'}
                            />
                        </div>
                        <div>
                            <label style={{ fontFamily: 'JetBrains Mono', fontSize: '11px', color: '#44446a', display: 'block', marginBottom: '8px', letterSpacing: '0.1em', textTransform: 'uppercase' }}>
                                GitHub Org (optional)
                            </label>
                            <input
                                type="text"
                                placeholder="e.g. zerodhatech, razorpay"
                                value={companyOrg}
                                onChange={e => setCompanyOrg(e.target.value)}
                                style={{
                                    width: '100%', padding: '12px 16px', borderRadius: '12px',
                                    background: 'rgba(4,4,10,0.9)', border: '1px solid rgba(26,26,48,0.8)',
                                    color: '#eeeeff', fontSize: '14px', outline: 'none',
                                    fontFamily: 'Space Grotesk', transition: 'border-color 0.2s',
                                }}
                                onFocus={e => e.target.style.borderColor = 'rgba(124,110,247,0.5)'}
                                onBlur={e => e.target.style.borderColor = 'rgba(26,26,48,0.8)'}
                            />
                        </div>
                    </div>

                    {/* JD textarea */}
                    <div>
                        <label style={{ fontFamily: 'JetBrains Mono', fontSize: '11px', color: '#44446a', display: 'block', marginBottom: '8px', letterSpacing: '0.1em', textTransform: 'uppercase' }}>
                            Job Description *
                        </label>
                        <textarea
                            value={jd}
                            onChange={e => setJd(e.target.value)}
                            placeholder="Paste the full job description here — responsibilities, requirements, tech stack, everything..."
                            rows={10}
                            style={{
                                width: '100%', padding: '16px', borderRadius: '12px', resize: 'vertical',
                                background: 'rgba(4,4,10,0.9)', border: '1px solid rgba(26,26,48,0.8)',
                                color: '#eeeeff', fontSize: '14px', outline: 'none', lineHeight: 1.7,
                                fontFamily: 'Space Grotesk', transition: 'border-color 0.2s',
                            }}
                            onFocus={e => e.target.style.borderColor = 'rgba(124,110,247,0.5)'}
                            onBlur={e => e.target.style.borderColor = 'rgba(26,26,48,0.8)'}
                        />
                    </div>

                    {/* Buttons */}
                    <div style={{ display: 'flex', gap: '12px', marginTop: '20px', alignItems: 'center' }}>
                        <button
                            onClick={handleRun}
                            disabled={isRunning || !jd.trim() || !company.trim()}
                            style={{
                                padding: '14px 36px', borderRadius: '12px', fontSize: '15px', fontWeight: 700,
                                border: 'none', cursor: isRunning || !jd.trim() || !company.trim() ? 'not-allowed' : 'pointer',
                                background: isRunning || !jd.trim() || !company.trim()
                                    ? 'rgba(26,26,48,0.8)'
                                    : 'linear-gradient(135deg, #5b4de0, #7c6ef7)',
                                color: isRunning || !jd.trim() || !company.trim() ? '#44446a' : '#fff',
                                fontFamily: 'Space Grotesk',
                                boxShadow: isRunning ? 'none' : '0 8px 24px rgba(124,110,247,0.3)',
                                transition: 'all 0.3s',
                            }}
                        >
                            {isRunning ? '⏳ Generating Career Pack...' : '🚀 Generate Career Pack'}
                        </button>

                        {(isDone || logs.length > 0) && (
                            <button
                                onClick={handleReset}
                                style={{
                                    padding: '14px 24px', borderRadius: '12px', fontSize: '14px', fontWeight: 600,
                                    background: 'transparent', border: '1px solid rgba(26,26,48,0.8)',
                                    color: '#8888aa', cursor: 'pointer', fontFamily: 'Space Grotesk',
                                    transition: 'all 0.2s',
                                }}
                                onMouseEnter={e => { e.target.style.borderColor = 'rgba(124,110,247,0.4)'; e.target.style.color = '#a89cf8' }}
                                onMouseLeave={e => { e.target.style.borderColor = 'rgba(26,26,48,0.8)'; e.target.style.color = '#8888aa' }}
                            >
                                ↺ Reset
                            </button>
                        )}

                        {/* Info pills */}
                        <div style={{ marginLeft: 'auto', display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
                            {[
                                { icon: '⚡', label: 'Coral SQL', color: '#7c6ef7' },
                                { icon: '🧠', label: 'Claude AI', color: '#22d9f3' },
                                { icon: '🐙', label: 'GitHub', color: '#1ddf8a' },
                            ].map((pill, i) => (
                                <div key={i} style={{
                                    display: 'flex', alignItems: 'center', gap: '6px',
                                    padding: '6px 12px', borderRadius: '20px',
                                    background: `${pill.color}10`, border: `1px solid ${pill.color}25`,
                                    fontFamily: 'JetBrains Mono', fontSize: '11px', color: pill.color,
                                }}>
                                    {pill.icon} {pill.label}
                                </div>
                            ))}
                        </div>
                    </div>
                </div>

                {/* Terminal + Files */}
                {logs.length > 0 && (
                    <div style={{
                        display: 'grid',
                        gridTemplateColumns: isDone ? '1fr 1fr' : '1fr',
                        gap: '24px',
                        animation: 'fadeUp 0.5s ease',
                    }}>
                        <Terminal />
                        {isDone && <FileViewer />}
                    </div>
                )}

                {/* Done banner */}
                {isDone && (
                    <div style={{
                        marginTop: '24px', padding: '20px 28px', borderRadius: '16px',
                        background: 'rgba(29,223,138,0.08)', border: '1px solid rgba(29,223,138,0.25)',
                        display: 'flex', alignItems: 'center', gap: '16px',
                        animation: 'fadeUp 0.5s ease',
                    }}>
                        <span style={{ fontSize: '28px' }}>🎉</span>
                        <div>
                            <div style={{ fontFamily: 'Space Grotesk', fontWeight: 700, fontSize: '16px', color: '#1ddf8a', marginBottom: '2px' }}>
                                Career Pack Generated!
                            </div>
                            <div style={{ fontFamily: 'Space Grotesk', fontSize: '13px', color: '#8888aa' }}>
                                Click any file on the right to view or open it. HTML files open in a new tab.
                            </div>
                        </div>
                    </div>
                )}

            </div>
        </div>
    )
}