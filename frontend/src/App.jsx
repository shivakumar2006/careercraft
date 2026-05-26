import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { useEffect } from 'react'
import { Provider } from 'react-redux'
import { store } from './store'
import Navbar from './components/Navbar'
import Home from './pages/Home'
import Analyze from './pages/Analyze'
import "./App.css";

function CursorEffect() {
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

export default function App() {
  return (
    <Provider store={store}>
      <BrowserRouter>
        <div className="grid-bg" />
        <div className="orb orb-1" />
        <div className="orb orb-2" />
        <div className="orb orb-3" />
        <CursorEffect />
        <Navbar />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/analyze" element={<Analyze />} />
        </Routes>
      </BrowserRouter>
    </Provider>
  )
}