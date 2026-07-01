import { useState, useEffect } from 'react'
import { Link, useLocation } from 'react-router-dom'
import { motion, AnimatePresence } from 'framer-motion'

const NAV_LINKS = [
  { to: '/',          label: 'Home' },
  { to: '/recommend', label: 'Schemes' },
  { to: '/chat',      label: 'AI Assistant' },
]

function Logo() {
  return (
    <Link to="/" className="flex items-center gap-2.5">
      <svg viewBox="0 0 36 36" fill="none" className="w-8 h-8 shrink-0">
        <circle cx="18" cy="18" r="17" stroke="url(#nl)" strokeWidth="1.5"/>
        <circle cx="18" cy="18" r="9"  fill="url(#nl)" opacity="0.12"/>
        <circle cx="18" cy="18" r="3.5" fill="url(#nl)"/>
        {Array.from({length:8}).map((_,i)=>{
          const a=(i*45*Math.PI)/180
          return <line key={i}
            x1={18+5.5*Math.cos(a)} y1={18+5.5*Math.sin(a)}
            x2={18+11*Math.cos(a)}  y2={18+11*Math.sin(a)}
            stroke="url(#nl)" strokeWidth="1.5" strokeLinecap="round"/>
        })}
        {Array.from({length:8}).map((_,i)=>{
          const a=((i*45+22.5)*Math.PI)/180
          return <circle key={i} cx={18+14*Math.cos(a)} cy={18+14*Math.sin(a)} r="1" fill="url(#nl)" opacity="0.5"/>
        })}
        <defs>
          <linearGradient id="nl" x1="0" y1="0" x2="36" y2="36" gradientUnits="userSpaceOnUse">
            <stop stopColor="#F97316"/><stop offset="1" stopColor="#FB923C"/>
          </linearGradient>
        </defs>
      </svg>
      <span className="font-bold text-[17px] tracking-tight gradient-text">Sahayak AI</span>
    </Link>
  )
}

export default function Navbar() {
  const { pathname } = useLocation()
  const [scrolled,   setScrolled]   = useState(false)
  const [mobileOpen, setMobileOpen] = useState(false)

  useEffect(() => {
    const fn = () => setScrolled(window.scrollY > 12)
    window.addEventListener('scroll', fn)
    return () => window.removeEventListener('scroll', fn)
  }, [])

  return (
    <>
      <nav className={`fixed top-0 inset-x-0 z-50 transition-all duration-300 ${scrolled ? 'glass-dark shadow-black/30 shadow-lg' : 'bg-transparent'}`}>
        <div className="max-w-6xl mx-auto px-5 h-[62px] flex items-center justify-between">
          <Logo />

          {/* Desktop */}
          <div className="hidden md:flex items-center gap-1">
            {NAV_LINKS.map(l => {
              const active = pathname === l.to
              return (
                <Link key={l.to} to={l.to}
                  className={`relative px-4 py-2 text-sm font-medium rounded-lg transition-colors ${active ? 'text-white' : 'text-gray-400 hover:text-gray-200 hover:bg-white/5'}`}>
                  {active && (
                    <motion.span layoutId="nav-pill" transition={{type:'spring',bounce:0.2,duration:0.4}}
                      className="absolute inset-0 rounded-lg bg-white/8 border border-white/10"/>
                  )}
                  <span className="relative">{l.label}</span>
                </Link>
              )
            })}
          </div>

          <div className="hidden md:block">
            <Link to="/recommend"
              className="bg-[#F97316] hover:bg-[#EA6C0A] text-white text-sm font-semibold px-5 py-2 rounded-lg transition-colors">
              Get Started
            </Link>
          </div>

          {/* Hamburger */}
          <button className="md:hidden p-2 text-gray-400 hover:text-white" onClick={() => setMobileOpen(o=>!o)}>
            <div className="w-5 space-y-1.5">
              <span className={`block h-0.5 bg-current transition-all duration-200 ${mobileOpen?'rotate-45 translate-y-2':''}`}/>
              <span className={`block h-0.5 bg-current transition-all duration-200 ${mobileOpen?'opacity-0':''}`}/>
              <span className={`block h-0.5 bg-current transition-all duration-200 ${mobileOpen?'-rotate-45 -translate-y-2':''}`}/>
            </div>
          </button>
        </div>
      </nav>

      <AnimatePresence>
        {mobileOpen && (
          <motion.div initial={{opacity:0,y:-8}} animate={{opacity:1,y:0}} exit={{opacity:0,y:-8}}
            className="fixed top-[62px] inset-x-0 z-40 glass-dark md:hidden">
            <div className="px-5 py-4 space-y-1">
              {NAV_LINKS.map(l => (
                <Link key={l.to} to={l.to} onClick={()=>setMobileOpen(false)}
                  className={`block px-4 py-2.5 rounded-lg text-sm font-medium transition-colors ${pathname===l.to?'bg-orange-500/10 text-orange-400':'text-gray-300 hover:bg-white/5'}`}>
                  {l.label}
                </Link>
              ))}
              <Link to="/recommend" onClick={()=>setMobileOpen(false)}
                className="block mt-2 bg-[#F97316] text-white text-sm font-semibold px-4 py-2.5 rounded-lg text-center">
                Get Started
              </Link>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  )
}
