import { BrowserRouter, Routes, Route, useLocation } from 'react-router-dom'
import { useEffect } from 'react'
import { Provider } from 'react-redux'
import { store } from './store'
import Navbar from './components/Navbar'
import Home from './pages/Home'
import Analyze from './pages/Analyze'
import Chat from './pages/Chat'
import "./App.css";

function CursorEffect() {

  const location = useLocation();

  useEffect(() => {
    const cursor = document.querySelector('.cursor')
    const ring = document.querySelector('.cursor-ring')
    const move = (e) => {
      cursor.style.left = e.clientX - 6 + 'px'
      cursor.style.top = e.clientY - 6 + 'px'
      ring.style.left = e.clientX - 18 + 'px'
      ring.style.top = e.clientY - 18 + 'px'
    }
    window.addEventListener('mousemove', move)
    return () => window.removeEventListener('mousemove', move)
  }, [])
  return (
    <>
      <div className="cursor" />
      <div className="cursor-ring" />
    </>
  )
}

function AppContent() {
  const location = useLocation();

  return (
    <>
      <div className="grid-bg" />
      <div className="orb orb-1" />
      <div className="orb orb-2" />
      <div className="orb orb-3" />
      <CursorEffect />

      {location.pathname !== '/chat' && <Navbar />}

      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/analyze" element={<Analyze />} />
        <Route path="/chat" element={<Chat />} />
      </Routes>
    </>
  );
}

export default function App() {
  return (
    <Provider store={store}>
      <BrowserRouter>
        <AppContent />
      </BrowserRouter>
    </Provider>
  )
}

