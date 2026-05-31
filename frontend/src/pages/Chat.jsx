import { useState, useRef, useEffect } from 'react';
import { useChatMutation } from '../store/api';

const SUGGESTIONS = [
    "Which is the best Go project for my resume?",
    "What shoud i do today?",
    "What skills are missing for Zerodha?",
    "Summarize my GitHub activity",
    "What did I complete this week?",
    "What pages are in my Notion?",
]

function Message({ msg }) {
    const isUser = msg.role === 'user'

    return (
        <div style={{
            display: 'flex',
            justifyContent: isUser ? 'flex-end' : 'flex-start',
            marginBottom: '16px',
            animation: 'fadeUp 0.3s ease',
        }}>
            {!isUser && (
                <div style={{
                    width: '32px', height: '32px', borderRadius: '10px', flexShrink: 0,
                    background: 'linear-gradient(135deg, #5b4de0, #7c6ef7)',
                    display: 'flex', alignItems: 'center', justifyContent: 'center',
                    fontSize: '14px', marginRight: '10px', alignSelf: 'flex-start',
                    boxShadow: '0 0 12px rgba(124,110,247,0.4)',
                }}>⚡</div>
            )}

            <div style={{
                maxWidth: '75%',
                padding: '14px 18px',
                borderRadius: isUser ? '18px 18px 4px 18px' : '18px 18px 18px 4px',
                background: isUser
                    ? 'linear-gradient(135deg, #5b4de0, #7c6ef7)'
                    : 'rgba(15,15,28,0.9)',
                border: isUser ? 'none' : '1px solid rgba(26,26,48,0.8)',
                color: '#eeeeff',
                fontSize: '14px',
                lineHeight: 1.7,
                fontFamily: 'Space Grotesk, sans-serif',
                boxShadow: isUser
                    ? '0 4px 20px rgba(124,110,247,0.3)'
                    : '0 2px 12px rgba(0,0,0,0.3)',
                whiteSpace: 'pre-wrap',
                wordBreak: 'break-word',
            }}>
                {msg.content}
            </div>

            {isUser && (
                <div style={{
                    width: '32px', height: '32px', borderRadius: '10px', flexShrink: 0,
                    background: 'rgba(26,26,48,0.8)', border: '1px solid rgba(42,42,66,0.8)',
                    display: 'flex', alignItems: 'center', justifyContent: 'center',
                    fontSize: '14px', marginLeft: '10px', alignSelf: 'flex-start',
                }}>👤</div>
            )}
        </div>
    )
}

function TypingIndicator() {
    return (
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '16px' }}>
            <div style={{
                width: '32px', height: '32px', borderRadius: '10px',
                background: 'linear-gradient(135deg, #5b4de0, #7c6ef7)',
                display: 'flex', alignItems: 'center', justifyContent: 'center',
                fontSize: '14px', boxShadow: '0 0 12px rgba(124,110,247,0.4)',
            }}>⚡</div>
            <div style={{
                padding: '14px 18px', borderRadius: '18px 18px 18px 4px',
                background: 'rgba(15,15,28,0.9)', border: '1px solid rgba(26,26,48,0.8)',
                display: 'flex', alignItems: 'center', gap: '6px',
            }}>
                {[0, 1, 2].map(i => (
                    <div key={i} style={{
                        width: '8px', height: '8px', borderRadius: '50%',
                        background: '#7c6ef7',
                        animation: `bounce 1.2s ease infinite`,
                        animationDelay: `${i * 0.2}s`,
                    }} />
                ))}
            </div>
        </div>
    )
}

export default function Chat() {
    const [messages, setMessages] = useState([
        {
            role: 'assistant',
            content: `Hey! I'm CareerCraft AI — your personal career agent. 🚀

I have real-time access to your GitHub profile and Notion workspace via Coral SQL.

Ask me anything:
• "Mera best Go project konsa hai?"
• "Aaj kya karna hai mujhe?"
• "Zerodha ke liye kaunsi skills missing hain?"
• "Is week kya complete kiya?"

What's on your mind?`,
        }
    ])
    const [input, setInput] = useState('')

    const [chat] = useChatMutation();

    const [isLoading, setIsLoading] = useState(false)
    const [coralActive, setCoralActive] = useState(false)
    const bottomRef = useRef(null)
    const inputRef = useRef(null)

    useEffect(() => {
        bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
    }, [messages, isLoading])

    const sendMessage = async (text) => {
        const msg = text || input.trim()
        if (!msg || isLoading) return

        setInput('')
        setMessages(prev => [...prev, { role: 'user', content: msg }])
        setIsLoading(true)
        setCoralActive(true)

        try {
            const history = messages.map(m => ({ role: m.role, content: m.content }))

            const data = await chat({
                message: msg,
                history,
            }).unwrap()
            setMessages(prev => [...prev, { role: 'assistant', content: data.response }])
        } catch (e) {
            setMessages(prev => [...prev, {
                role: 'assistant',
                content: '❌ Connection error — make sure backend is running on localhost:8000',
            }])
        } finally {
            setIsLoading(false)
            setCoralActive(false)
            inputRef.current?.focus()
        }
    }

    const handleKey = (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault()
            sendMessage()
        }
    }

    const clearChat = () => {
        setMessages([{
            role: 'assistant',
            content: 'Chat cleared! What would you like to know?',
        }])
    }

    return (
        <div style={{
            position: 'relative', zIndex: 1, paddingTop: '64px',
            height: '100vh', display: 'flex', flexDirection: 'column',
        }}>
            <style>{`
        @keyframes fadeUp {
          from { opacity: 0; transform: translateY(10px); }
          to { opacity: 1; transform: translateY(0); }
        }
        @keyframes bounce {
          0%, 60%, 100% { transform: translateY(0); }
          30% { transform: translateY(-8px); }
        }
        @keyframes pulse-coral {
          0%, 100% { opacity: 1; }
          50% { opacity: 0.4; }
        }
      `}</style>

            {/* Header */}
            <div style={{
                padding: '16px 24px', borderBottom: '1px solid rgba(26,26,48,0.8)',
                background: 'rgba(4,4,10,0.9)', backdropFilter: 'blur(20px)',
                display: 'flex', alignItems: 'center', justifyContent: 'space-between',
                flexShrink: 0,
            }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                    <div style={{
                        width: '40px', height: '40px', borderRadius: '12px',
                        background: 'linear-gradient(135deg, #5b4de0, #7c6ef7)',
                        display: 'flex', alignItems: 'center', justifyContent: 'center',
                        fontSize: '18px', boxShadow: '0 0 16px rgba(124,110,247,0.4)',
                    }}>⚡</div>
                    <div>
                        <div style={{ fontFamily: 'Syne, sans-serif', fontWeight: 800, fontSize: '16px', color: '#eeeeff' }}>
                            CareerCraft AI
                        </div>
                        <div style={{ fontSize: '12px', color: '#44446a', fontFamily: 'JetBrains Mono' }}>
                            Powered by Coral SQL + Claude
                        </div>
                    </div>
                </div>

                <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                    {/* Coral status */}
                    <div style={{
                        display: 'flex', alignItems: 'center', gap: '6px',
                        padding: '6px 12px', borderRadius: '20px',
                        background: coralActive ? 'rgba(29,223,138,0.1)' : 'rgba(26,26,48,0.5)',
                        border: `1px solid ${coralActive ? 'rgba(29,223,138,0.3)' : 'rgba(42,42,66,0.5)'}`,
                        transition: 'all 0.3s',
                    }}>
                        <div style={{
                            width: '6px', height: '6px', borderRadius: '50%',
                            background: coralActive ? '#1ddf8a' : '#44446a',
                            boxShadow: coralActive ? '0 0 8px #1ddf8a' : 'none',
                            animation: coralActive ? 'pulse-coral 1s infinite' : 'none',
                        }} />
                        <span style={{ fontFamily: 'JetBrains Mono', fontSize: '11px', color: coralActive ? '#1ddf8a' : '#44446a' }}>
                            {coralActive ? 'querying coral...' : 'coral ready'}
                        </span>
                    </div>

                    <button onClick={clearChat} style={{
                        padding: '7px 14px', borderRadius: '8px', fontSize: '12px', fontWeight: 600,
                        background: 'transparent', border: '1px solid rgba(26,26,48,0.8)',
                        color: '#8888aa', cursor: 'pointer', fontFamily: 'Space Grotesk',
                        transition: 'all 0.2s',
                    }}
                        onMouseEnter={e => { e.target.style.borderColor = 'rgba(124,110,247,0.4)'; e.target.style.color = '#a89cf8' }}
                        onMouseLeave={e => { e.target.style.borderColor = 'rgba(26,26,48,0.8)'; e.target.style.color = '#8888aa' }}
                    >
                        Clear
                    </button>
                </div>
            </div>

            {/* Messages */}
            <div style={{
                flex: 1, overflowY: 'auto', padding: '24px',
                background: 'rgba(4,4,10,0.5)',
            }}>
                <div style={{ maxWidth: '800px', margin: '0 auto' }}>
                    {messages.map((msg, i) => (
                        <Message key={i} msg={msg} />
                    ))}
                    {isLoading && <TypingIndicator />}
                    <div ref={bottomRef} />
                </div>
            </div>

            {/* Suggestions */}
            {messages.length <= 1 && (
                <div style={{
                    padding: '0 24px 16px', background: 'rgba(4,4,10,0.9)',
                }}>
                    <div style={{ maxWidth: '800px', margin: '0 auto' }}>
                        <div style={{
                            fontFamily: 'JetBrains Mono', fontSize: '11px', color: '#44446a',
                            marginBottom: '10px', letterSpacing: '0.1em', textTransform: 'uppercase',
                        }}>Suggested questions</div>
                        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
                            {SUGGESTIONS.map((s, i) => (
                                <button key={i} onClick={() => sendMessage(s)} style={{
                                    padding: '8px 14px', borderRadius: '20px', fontSize: '12px', fontWeight: 500,
                                    background: 'rgba(15,15,28,0.9)', border: '1px solid rgba(26,26,48,0.8)',
                                    color: '#8888aa', cursor: 'pointer', fontFamily: 'Space Grotesk',
                                    transition: 'all 0.2s', textAlign: 'left',
                                }}
                                    onMouseEnter={e => {
                                        e.currentTarget.style.borderColor = 'rgba(124,110,247,0.4)'
                                        e.currentTarget.style.color = '#a89cf8'
                                        e.currentTarget.style.background = 'rgba(124,110,247,0.08)'
                                    }}
                                    onMouseLeave={e => {
                                        e.currentTarget.style.borderColor = 'rgba(26,26,48,0.8)'
                                        e.currentTarget.style.color = '#8888aa'
                                        e.currentTarget.style.background = 'rgba(15,15,28,0.9)'
                                    }}
                                >{s}</button>
                            ))}
                        </div>
                    </div>
                </div>
            )}

            {/* Input */}
            <div style={{
                padding: '16px 24px 24px', background: 'rgba(4,4,10,0.95)',
                borderTop: '1px solid rgba(26,26,48,0.8)', flexShrink: 0,
            }}>
                <div style={{ maxWidth: '800px', margin: '0 auto' }}>
                    <div style={{
                        display: 'flex', gap: '12px', alignItems: 'flex-end',
                        background: 'rgba(15,15,28,0.9)', border: '1px solid rgba(26,26,48,0.8)',
                        borderRadius: '16px', padding: '12px 16px',
                        transition: 'border-color 0.2s',
                    }}
                        onFocus={() => { }}
                    >
                        <textarea
                            ref={inputRef}
                            value={input}
                            onChange={e => setInput(e.target.value)}
                            onKeyDown={handleKey}
                            placeholder="Ask about your GitHub, Notion, career plans..."
                            rows={1}
                            style={{
                                flex: 1, background: 'transparent', border: 'none', outline: 'none',
                                color: '#eeeeff', fontSize: '14px', fontFamily: 'Space Grotesk',
                                resize: 'none', lineHeight: 1.6, maxHeight: '120px', overflowY: 'auto',
                            }}
                            onInput={e => {
                                e.target.style.height = 'auto'
                                e.target.style.height = Math.min(e.target.scrollHeight, 120) + 'px'
                            }}
                        />
                        <button
                            onClick={() => sendMessage()}
                            disabled={isLoading || !input.trim()}
                            style={{
                                width: '36px', height: '36px', borderRadius: '10px', border: 'none',
                                background: isLoading || !input.trim()
                                    ? 'rgba(26,26,48,0.8)'
                                    : 'linear-gradient(135deg, #5b4de0, #7c6ef7)',
                                color: isLoading || !input.trim() ? '#44446a' : '#fff',
                                cursor: isLoading || !input.trim() ? 'not-allowed' : 'pointer',
                                display: 'flex', alignItems: 'center', justifyContent: 'center',
                                fontSize: '16px', transition: 'all 0.2s', flexShrink: 0,
                                boxShadow: isLoading || !input.trim() ? 'none' : '0 4px 12px rgba(124,110,247,0.4)',
                            }}
                        >
                            {isLoading ? '⏳' : '→'}
                        </button>
                    </div>
                    <div style={{
                        marginTop: '8px', fontSize: '11px', color: '#44446a',
                        fontFamily: 'JetBrains Mono', textAlign: 'center',
                    }}>
                        Enter to send · Shift+Enter for new line · Coral SQL fetches real data
                    </div>
                </div>
            </div>
        </div>
    )
}