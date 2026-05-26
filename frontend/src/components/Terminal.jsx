import { useEffect, useRef } from 'react'
import { useSelector } from 'react-redux'

export default function Terminal() {
    const { logs, isRunning, isDone, error } = useSelector(s => s.career)
    const bottomRef = useRef(null)

    useEffect(() => {
        bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
    }, [logs])

    const getLogColor = (log) => {
        if (log.startsWith('✅')) return '#1ddf8a'
        if (log.startsWith('❌')) return '#ff4d6a'
        if (log.startsWith('🔍') || log.startsWith('💻') || log.startsWith('📋')) return '#22d9f3'
        if (log.startsWith('🧠')) return '#a89cf8'
        if (log.startsWith('📄') || log.startsWith('✉️') || log.startsWith('❓') || log.startsWith('🎯')) return '#f5c542'
        if (log.startsWith('💾')) return '#7c6ef7'
        if (log.startsWith('🚀')) return '#a89cf8'
        return '#eeeeff'
    }

    return (
        <div className="terminal-window" style={{ height: '100%', minHeight: '420px', position: 'relative' }}>
            <div className="scanline" />

            {/* Header */}
            <div className="terminal-bar">
                <div className="terminal-dot" style={{ background: '#ff5f57' }} />
                <div className="terminal-dot" style={{ background: '#febc2e' }} />
                <div className="terminal-dot" style={{ background: '#28c840' }} />
                <span style={{ marginLeft: '12px', fontSize: '12px', color: '#44446a', fontFamily: 'JetBrains Mono' }}>
                    careercraft — agent
                </span>
                <div style={{ marginLeft: 'auto', display: 'flex', alignItems: 'center', gap: '6px' }}>
                    {isRunning && (
                        <span style={{
                            fontSize: '11px', padding: '3px 10px', borderRadius: '20px',
                            background: 'rgba(124,110,247,0.15)', color: '#a89cf8',
                            border: '1px solid rgba(124,110,247,0.25)', fontFamily: 'JetBrains Mono',
                            display: 'flex', alignItems: 'center', gap: '6px',
                        }}>
                            <span style={{
                                width: '6px', height: '6px', borderRadius: '50%',
                                background: '#7c6ef7', animation: 'pulse-glow 1.5s infinite',
                                display: 'inline-block',
                            }} />
                            running
                        </span>
                    )}
                    {isDone && (
                        <span style={{
                            fontSize: '11px', padding: '3px 10px', borderRadius: '20px',
                            background: 'rgba(29,223,138,0.1)', color: '#1ddf8a',
                            border: '1px solid rgba(29,223,138,0.25)', fontFamily: 'JetBrains Mono',
                        }}>✓ done</span>
                    )}
                </div>
            </div>

            {/* Body */}
            <div className="terminal-body" style={{ height: 'calc(100% - 44px)', overflowY: 'auto' }}>
                {logs.length === 0 && (
                    <div style={{ color: '#44446a', fontFamily: 'JetBrains Mono', fontSize: '13px' }}>
                        <span style={{ color: '#7c6ef7' }}>~</span> Waiting for job description...
                    </div>
                )}

                {logs.map((log, i) => (
                    <div key={i} className="terminal-line" style={{ animationDelay: `${i * 0.05}s` }}>
                        <span className="terminal-prompt">❯</span>
                        <span style={{ color: getLogColor(log) }}>{log}</span>
                    </div>
                ))}

                {isRunning && (
                    <div className="terminal-line">
                        <span className="terminal-prompt">❯</span>
                        <span className="terminal-cursor" />
                    </div>
                )}

                {error && (
                    <div className="terminal-line">
                        <span className="terminal-prompt" style={{ color: '#ff4d6a' }}>✗</span>
                        <span style={{ color: '#ff4d6a' }}>Error: {error}</span>
                    </div>
                )}

                <div ref={bottomRef} />
            </div>
        </div>
    )
}