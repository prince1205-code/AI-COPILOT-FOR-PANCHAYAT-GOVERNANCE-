import { useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'

const STATS = [
  { value:'3397+', label:'Government Schemes' },
  { value:'29',    label:'States Supported' },
  { value:'95%',   label:'Recommendation Accuracy' },
  { value:'24×7',  label:'AI Powered Assistant' },
]

const FEATURES = [
  {
    grad:'from-orange-500/20 to-orange-600/5',
    icon:(
      <svg className="w-5 h-5 text-orange-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8">
        <path d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/>
        <path d="M9 12h6M9 16h4"/>
      </svg>
    ),
    title:'Smart Recommendations',
    desc:'Get matched to 3,000+ government schemes based on your profile, state, income, and occupation.',
  },
  {
    grad:'from-indigo-500/20 to-indigo-600/5',
    icon:(
      <svg className="w-5 h-5 text-indigo-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8">
        <path d="M12 2a10 10 0 110 20A10 10 0 0112 2z"/>
        <path d="M12 16v-4M12 8h.01"/>
      </svg>
    ),
    title:'AI Chat Assistant',
    desc:'Ask anything about government schemes in plain language. Get instant, accurate answers powered by Gemini.',
  },
  {
    grad:'from-green-500/20 to-green-600/5',
    icon:(
      <svg className="w-5 h-5 text-green-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8">
        <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
      </svg>
    ),
    title:'Why Am I Eligible?',
    desc:'Transparent AI decisions — see exactly why each scheme was recommended with a full eligibility breakdown.',
  },
]

function HeroIllustration() {
  const cards = [
    { label:'PM Kisan',  conf:'95%', color:'#22c55e', top:'8%',  left:'-5%',  delay:0   },
    { label:'PMAY',      conf:'87%', color:'#F97316', top:'62%', left:'-10%', delay:0.3 },
    { label:'Ayushman',  conf:'82%', color:'#6366f1', top:'12%', right:'-5%', delay:0.6 },
  ]
  return (
    <motion.div initial={{opacity:0,scale:0.92}} animate={{opacity:1,scale:1}}
      transition={{duration:0.8}} className="relative w-[280px] h-[280px] mx-auto">

      {/* Glow */}
      <div className="absolute inset-0 rounded-full bg-orange-500/10 blur-3xl"/>

      {/* Center circle */}
      <div className="absolute inset-10 rounded-full bg-[#111827] border border-white/8 flex items-center justify-center shadow-2xl">
        <svg viewBox="0 0 100 100" fill="none" className="w-20 h-20">
          <circle cx="50" cy="50" r="46" stroke="url(#hi)" strokeWidth="1.5" strokeDasharray="5 3"/>
          <circle cx="50" cy="50" r="28" fill="url(#hi)" opacity="0.08"/>
          <circle cx="50" cy="50" r="9"  fill="url(#hi)"/>
          {Array.from({length:12}).map((_,i)=>{
            const a=(i*30*Math.PI)/180
            return <line key={i}
              x1={50+12*Math.cos(a)} y1={50+12*Math.sin(a)}
              x2={50+26*Math.cos(a)} y2={50+26*Math.sin(a)}
              stroke="url(#hi)" strokeWidth="1.5" strokeLinecap="round"/>
          })}
          {Array.from({length:12}).map((_,i)=>{
            const a=((i*30+15)*Math.PI)/180
            return <circle key={i} cx={50+38*Math.cos(a)} cy={50+38*Math.sin(a)} r="1.2" fill="url(#hi)" opacity="0.5"/>
          })}
          <defs>
            <linearGradient id="hi" x1="0" y1="0" x2="100" y2="100" gradientUnits="userSpaceOnUse">
              <stop stopColor="#F97316"/><stop offset="1" stopColor="#FB923C"/>
            </linearGradient>
          </defs>
        </svg>
      </div>

      {/* Floating cards */}
      {cards.map((c,i)=>(
        <motion.div key={i}
          animate={{y:[0,-7,0]}} transition={{repeat:Infinity,duration:3+i*0.5,delay:c.delay}}
          style={{top:c.top,left:c.left,right:c.right}}
          className="absolute glass rounded-xl px-3 py-2 text-xs shadow-xl">
          <div className="font-semibold text-white text-[11px]">{c.label}</div>
          <div className="font-bold text-[11px]" style={{color:c.color}}>{c.conf} match</div>
        </motion.div>
      ))}
    </motion.div>
  )
}

function Footer() {
  return (
    <footer className="border-t border-white/5 mt-20 py-10 px-5">
      <div className="max-w-5xl mx-auto flex flex-col md:flex-row items-center justify-between gap-6">
        <div>
          <div className="font-bold text-base gradient-text mb-1">Sahayak AI</div>
          <p className="text-xs text-gray-500">Powered by Gemini · Built by Prince Kumar</p>
          <p className="text-xs text-gray-600 mt-0.5">Made with ❤️ for Digital India Initiative</p>
        </div>
        <div className="flex items-center gap-5">
          <a href="https://github.com/prince1205-code" target="_blank" rel="noreferrer"
            className="text-gray-500 hover:text-white transition-colors">
            <svg className="w-5 h-5" viewBox="0 0 24 24" fill="currentColor">
              <path d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z"/>
            </svg>
          </a>
          <a href="https://linkedin.com" target="_blank" rel="noreferrer"
            className="text-gray-500 hover:text-blue-400 transition-colors">
            <svg className="w-5 h-5" viewBox="0 0 24 24" fill="currentColor">
              <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 01-2.063-2.065 2.064 2.064 0 112.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>
            </svg>
          </a>
          <span className="text-xs text-gray-600">© 2025 Sahayak AI</span>
        </div>
      </div>
    </footer>
  )
}

const fadeUp = (delay=0) => ({
  initial:{opacity:0,y:24},
  animate:{opacity:1,y:0},
  transition:{duration:0.5,delay},
})

export default function Home() {
  const nav = useNavigate()
  return (
    <div className="min-h-screen flex flex-col mesh-bg">

      {/* Hero */}
      <section className="flex-1 flex flex-col md:flex-row items-center justify-center gap-16 px-6 pt-28 pb-16 max-w-6xl mx-auto w-full">
        <motion.div {...fadeUp(0)} className="flex-1 text-center md:text-left max-w-lg">
          <div className="inline-flex items-center gap-2 bg-orange-500/8 border border-orange-500/20 text-orange-400 text-xs font-medium px-3.5 py-1.5 rounded-full mb-7">
            <span className="w-1.5 h-1.5 rounded-full bg-orange-400 animate-pulse"/>
            🇮🇳 AI Copilot for Panchayat Governance
          </div>
          <h1 className="text-5xl md:text-[58px] font-extrabold leading-[1.1] tracking-tight mb-5">
            <span className="gradient-text">Sahayak AI</span>
            <br/>
            <span className="text-gray-100 text-4xl md:text-5xl font-bold">for Every Citizen</span>
          </h1>
          <p className="text-gray-400 text-base leading-relaxed mb-10 max-w-md">
            Discover government schemes you are eligible for. AI-powered recommendations, instant answers, transparent decisions.
          </p>
          <div className="flex gap-3 flex-wrap justify-center md:justify-start">
            <motion.button whileHover={{scale:1.02}} whileTap={{scale:0.98}}
              onClick={()=>nav('/recommend')}
              className="bg-[#F97316] hover:bg-[#EA6C0A] text-white font-semibold px-7 py-3 rounded-xl text-sm transition-colors shadow-lg shadow-orange-500/20">
              Find My Schemes →
            </motion.button>
            <motion.button whileHover={{scale:1.02}} whileTap={{scale:0.98}}
              onClick={()=>nav('/chat')}
              className="bg-white/5 hover:bg-white/8 border border-white/10 text-white font-semibold px-7 py-3 rounded-xl text-sm transition-colors">
              Ask AI Assistant
            </motion.button>
          </div>
        </motion.div>

        <motion.div {...fadeUp(0.2)} className="flex-1 flex justify-center">
          <HeroIllustration/>
        </motion.div>
      </section>

      {/* Stats */}
      <section className="max-w-5xl mx-auto w-full px-6 mb-16">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
          {STATS.map((s,i)=>(
            <motion.div key={i} {...fadeUp(0.3+i*0.08)}
              className="bg-[#111827] border border-white/6 rounded-2xl p-5 text-center card-hover">
              <div className="text-2xl font-extrabold gradient-text mb-1">{s.value}</div>
              <div className="text-xs text-gray-500">{s.label}</div>
            </motion.div>
          ))}
        </div>
      </section>

      {/* Features */}
      <section className="max-w-5xl mx-auto w-full px-6 mb-8">
        <motion.h2 {...fadeUp(0.4)} className="text-center text-xl font-bold text-gray-200 mb-8">
          Everything you need to access government benefits
        </motion.h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
          {FEATURES.map((f,i)=>(
            <motion.div key={i} {...fadeUp(0.5+i*0.1)}
              className="bg-[#111827] border border-white/6 rounded-2xl p-6 card-hover">
              <div className={`w-10 h-10 rounded-xl bg-gradient-to-br ${f.grad} border border-white/8 flex items-center justify-center mb-4`}>
                {f.icon}
              </div>
              <h3 className="font-semibold text-white mb-2 text-sm">{f.title}</h3>
              <p className="text-xs text-gray-400 leading-relaxed">{f.desc}</p>
            </motion.div>
          ))}
        </div>
      </section>

      <Footer/>
    </div>
  )
}
