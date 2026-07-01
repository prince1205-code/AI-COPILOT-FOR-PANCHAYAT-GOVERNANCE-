import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import ProfileForm from '../components/ProfileForm'
import RecommendationCard from '../components/RecommendationCard'
import SchemeDetails from './SchemeDetails'
import { postRecommend } from '../services/api'

const STEPS = [
  { icon:'🔍', text:'Analysing your profile' },
  { icon:'✓',  text:'Checking eligibility criteria' },
  { icon:'✓',  text:'Matching your state' },
  { icon:'✓',  text:'Finding best schemes' },
  { icon:'✓',  text:'Ranking recommendations' },
]

function LoadingSteps() {
  const [step, setStep] = useState(0)
  useState(()=>{
    const id = setInterval(()=>setStep(s=>Math.min(s+1,STEPS.length-1)),700)
    return ()=>clearInterval(id)
  })
  return (
    <motion.div initial={{opacity:0}} animate={{opacity:1}}
      className="bg-[#111827] border border-white/6 rounded-2xl p-6 space-y-3">
      <p className="text-xs text-gray-500 font-medium uppercase tracking-wider mb-4">Processing</p>
      {STEPS.map((s,i)=>(
        <motion.div key={i} initial={{opacity:0,x:-8}} animate={{opacity:i<=step?1:0.2,x:0}}
          transition={{delay:i*0.7}}
          className={`flex items-center gap-3 text-sm font-medium ${
            i===0?'text-orange-400':i<=step?'text-green-400':'text-gray-600'
          }`}>
          <span className="text-base w-5 text-center">{s.icon}</span>
          {s.text}
          {i<=step && i>0 && (
            <motion.svg initial={{scale:0}} animate={{scale:1}} className="w-3.5 h-3.5 ml-auto"
              viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
              <path d="M20 6L9 17l-5-5"/>
            </motion.svg>
          )}
        </motion.div>
      ))}
    </motion.div>
  )
}

function EmptyState() {
  return (
    <div className="text-center py-16">
      <div className="w-14 h-14 rounded-2xl bg-orange-500/10 border border-orange-500/20 flex items-center justify-center mx-auto mb-4">
        <svg className="w-7 h-7 text-orange-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
          <path d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/>
        </svg>
      </div>
      <h3 className="font-semibold text-gray-300 mb-1">Fill your profile above</h3>
      <p className="text-xs text-gray-500">We'll match you with eligible government schemes instantly.</p>
    </div>
  )
}

export default function Recommendation() {
  const [results,  setResults]  = useState([])
  const [selected, setSelected] = useState(null)
  const [loading,  setLoading]  = useState(false)
  const [error,    setError]    = useState('')
  const [searched, setSearched] = useState(false)

  const handleSubmit = async (form) => {
    setLoading(true); setError(''); setResults([]); setSearched(true)
    try {
      const { data } = await postRecommend(form)
      setResults(data.results)
    } catch {
      setError('Could not fetch recommendations. Is the backend running?')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-[#0B1220] mesh-bg">
      <div className="max-w-5xl mx-auto px-5 pt-[90px] pb-16">

        {/* Header */}
        <motion.div initial={{opacity:0,y:16}} animate={{opacity:1,y:0}} className="mb-8">
          <h1 className="text-2xl font-bold text-white mb-1">Find Your Schemes</h1>
          <p className="text-sm text-gray-400">Fill your profile — we'll match you with eligible government schemes.</p>
        </motion.div>

        {/* Form */}
        <motion.div initial={{opacity:0,y:16}} animate={{opacity:1,y:0}} transition={{delay:0.1}}
          className="bg-[#111827] border border-white/6 rounded-2xl p-6 mb-8">
          <ProfileForm onSubmit={handleSubmit} loading={loading}/>
        </motion.div>

        {/* Error */}
        {error && (
          <div className="bg-red-500/10 border border-red-500/20 text-red-400 text-sm rounded-xl px-4 py-3 mb-6">
            {error}
          </div>
        )}

        {/* Loading */}
        <AnimatePresence mode="wait">
          {loading && <LoadingSteps key="loading"/>}
        </AnimatePresence>

        {/* Results */}
        {!loading && results.length > 0 && (
          <motion.div initial={{opacity:0}} animate={{opacity:1}}>
            <div className="flex items-center justify-between mb-5">
              <p className="text-sm text-gray-400">
                Found <span className="text-orange-400 font-semibold">{results.length}</span> matching schemes
              </p>
              <span className="text-xs text-gray-600">Click any card for details</span>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {results.map((s,i)=>(
                <RecommendationCard key={i} scheme={s} index={i} onSelect={setSelected}/>
              ))}
            </div>
          </motion.div>
        )}

        {/* Empty state */}
        {!loading && !error && searched && results.length === 0 && (
          <div className="text-center py-12 text-gray-500 text-sm">No schemes found for this profile.</div>
        )}
        {!loading && !searched && <EmptyState/>}

        <AnimatePresence>
          {selected && <SchemeDetails scheme={selected} onClose={()=>setSelected(null)}/>}
        </AnimatePresence>
      </div>
    </div>
  )
}
