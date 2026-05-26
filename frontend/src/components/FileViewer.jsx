import { useSelector, useDispatch } from 'react-redux'
import { setActiveFile, setFileContent } from '../store/careerSlice'

const FILE_META = {
    resume: { icon: '📄', color: '#7c6ef7', label: 'Resume', desc: 'Tailored HTML resume' },
    dashboard: { icon: '🎯', color: '#1ddf8a', label: 'Dashboard', desc: 'Interactive career dashboard' },
    cover_letter: { icon: '✉️', color: '#f5c542', label: 'Cover Letter', desc: 'Personalized cover letter' },
    interview: { icon: '❓', color: '#22d9f3', label: 'Interview Prep', desc: '15 questions with hints' },
}

function getFileMeta(filename) {
    for (const [key, meta] of Object.entries(FILE_META)) {
        if (filename.toLowerCase().includes(key)) return meta
    }
    return { icon: '📁', color: '#8888aa', label: 'File', desc: 'Generated file' }
}

function formatSize(bytes) {
    if (bytes < 1024) return `${bytes}B`
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)}KB`
    return `${(bytes / (1024 * 1024)).toFixed(1)}MB`
}

export default function FileViewer() {
    const dispatch = useDispatch()
    const { files, activeFile, fileContent } = useSelector(s => s.career)

    const openFile = async (filename) => {
        dispatch(setActiveFile(filename))
        if (filename.endsWith('.html')) {
            window.open(`http://localhost:8000/preview/${filename}`, '_blank')
            return
        }
        const res = await fetch(`http://localhost:8000/files/${filename}`)
        const data = await res.json()
        dispatch(setFileContent(data.content))
    }

    return (
        <div style={{
            background: 'rgba(15,15,28,0.9)', backdropFilter: 'blur(20px)',
            border: '1px solid rgba(26,26,48,0.8)', borderRadius: '16px',
            overflow: 'hidden', height: '100%', minHeight: '420px',
            display: 'flex', flexDirection: 'column',
        }}>
            {/* Header */}
            <div style={{
                padding: '14px 20px', borderBottom: '1px solid rgba(26,26,48,0.8)',
                display: 'flex', alignItems: 'center', justifyContent: 'space-between',
            }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                    <span style={{ fontSize: '14px', fontWeight: 700, color: '#eeeeff', fontFamily: 'Space Grotesk' }}>
                        Generated Files
                    </span>
                </div>
                <span style={{
                    fontSize: '11px', padding: '3px 10px', borderRadius: '20px',
                    background: 'rgba(124,110,247,0.15)', color: '#a89cf8',
                    border: '1px solid rgba(124,110,247,0.25)', fontFamily: 'JetBrains Mono',
                }}>{files.length} files</span>
            </div>

            {/* File list */}
            <div style={{ padding: '16px', display: 'flex', flexDirection: 'column', gap: '10px' }}>
                {files.map((file, i) => {
                    const meta = getFileMeta(typeof file === 'string' ? file : file.name)
                    const filename = typeof file === 'string' ? file : file.name
                    const isActive = activeFile === filename

                    return (
                        <div
                            key={i}
                            onClick={() => openFile(filename)}
                            style={{
                                display: 'flex', alignItems: 'center', gap: '14px',
                                padding: '14px 16px', borderRadius: '12px', cursor: 'pointer',
                                background: isActive ? 'rgba(124,110,247,0.1)' : 'rgba(8,8,16,0.8)',
                                border: `1px solid ${isActive ? 'rgba(124,110,247,0.4)' : 'rgba(26,26,48,0.8)'}`,
                                transition: 'all 0.2s',
                            }}
                        >
                            <div style={{
                                width: '40px', height: '40px', borderRadius: '10px', flexShrink: 0,
                                background: `${meta.color}15`, border: `1px solid ${meta.color}30`,
                                display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '18px',
                            }}>{meta.icon}</div>

                            <div style={{ flex: 1, minWidth: 0 }}>
                                <div style={{ fontSize: '13px', fontWeight: 600, color: meta.color, fontFamily: 'Space Grotesk' }}>
                                    {meta.label}
                                </div>
                                <div style={{ fontSize: '11px', color: '#44446a', fontFamily: 'JetBrains Mono', marginTop: '2px' }}>
                                    {filename}
                                </div>
                            </div>

                            <div style={{
                                fontSize: '10px', padding: '3px 8px', borderRadius: '6px',
                                background: 'rgba(26,26,48,0.8)', color: '#44446a', fontFamily: 'JetBrains Mono',
                                flexShrink: 0,
                            }}>
                                {filename.endsWith('.html') ? 'HTML' : 'TXT'}
                            </div>
                        </div>
                    )
                })}
            </div>

            {/* Text content preview */}
            {fileContent && activeFile && !activeFile.endsWith('.html') && (
                <div style={{
                    margin: '0 16px 16px', padding: '14px', borderRadius: '10px',
                    background: 'rgba(4,4,10,0.9)', border: '1px solid rgba(26,26,48,0.8)',
                    flex: 1, overflow: 'hidden', display: 'flex', flexDirection: 'column',
                }}>
                    <div style={{ fontSize: '11px', color: '#44446a', fontFamily: 'JetBrains Mono', marginBottom: '8px' }}>
                        ── {activeFile} ──
                    </div>
                    <pre style={{
                        fontSize: '12px', color: '#8888aa', fontFamily: 'JetBrains Mono',
                        whiteSpace: 'pre-wrap', wordBreak: 'break-word',
                        overflowY: 'auto', flex: 1, lineHeight: 1.7,
                    }}>{fileContent}</pre>
                </div>
            )}
        </div>
    )
}