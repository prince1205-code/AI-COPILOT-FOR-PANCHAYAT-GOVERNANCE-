import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'

const LEVEL_STYLE = {
  Central: 'bg-blue-500/10 text-blue-400 border-blue-500/20',
  State:   'bg-green-500/10 text-green-400 border-green-500/20',
}

function ConfidenceBar({ value }) {
  const num = parseInt(value)
  const label = num >= 90 ? 'Excellent Match' : num >= 70 ? 'Good Match' : 'Partial Match'
  const color = num >= 90 ? '#22c55e' : num >= 70 ? '#F97316' : '#6b7280'
  return (
    <div className="mt-3">
      <div className="flex justify-between items-center mb-1.5">
        <span className="text-xs text-gray-500">Match Confidence</span>
        <div className="flex items-center gap-1.5">
          <span className="text-xs font-semibold" style={{color}}>{label}</span>
          <span className="text-sm font-bold text-white">{value}</span>
        </div>
      </div>
      <div className="h-1.5 bg-gray-800 rounded-full overflow-hidden">
        <motion.div initial={{width:0}} animate={{width:`${num}%`}}
          transition={{duration:0.9, ease:'easeOut', delay:0.1}}
          className="h-full rounded-full"
          style={{background:`linear-gradient(90deg, ${color}, ${color}cc)`}}/>
      </div>
    </div>
  )
}

export default function RecommendationCard({ scheme, index, onSelect }) {
  const [open, setOpen] = useState(false)

  return (
    <motion.div
      initial={{opacity:0, y:20}} animate={{opacity:1, y:0}}
      transition={{delay: index * 0.04}}
      className="bg-[#111827] border border-white/6 rounded-2xl p-5 card-hover cursor-pointer"
      onClick={() => onSelect(scheme)}>

      {/* Badges */}
      <div className="flex items-center gap-2 mb-3">
        <span className={`text-[11px] font-medium px-2.5 py-0.5 rounded-full border ${LEVEL_STYLE[scheme.level] ?? 'bg-gray-700/50 text-gray-400 border-gray-600'}`}>
          {scheme.level}
        </span>
        <span className="text-[11px] text-gray-500 truncate">{scheme.category.split(',')[0]}</span>
      </div>

      {/* Title */}
      <h3 className="font-semibold text-white text-sm leading-snug mb-1 line-clamp-2">{scheme.scheme_name}</h3>

      {/* Confidence bar */}
      <ConfidenceBar value={scheme.confidence} />

      {/* Why am I eligible */}
      <button
        onClick={e => { e.stopPropagation(); setOpen(o=>!o) }}
        className="mt-3 flex items-center gap-1.5 text-xs text-indigo-400 hover:text-indigo-300 transition-colors font-medium">
        <svg className={`w-3 h-3 transition-transform ${open?'rotate-180':''}`} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
          <path d="M19 9l-7 7-7-7"/>
        </svg>
        Why am I eligible?
      </button>

      <AnimatePresence>
        {open && (
          <motion.div initial={{height:0,opacity:0}} animate={{height:'auto',opacity:1}}
            exit={{height:0,opacity:0}} className="overflow-hidden">
            <ul className="mt-2.5 space-y-1.5 pt-2.5 border-t border-white/5">
              {scheme.why.map((b, i) => (
                <li key={i} className="flex items-start gap-2 text-xs text-gray-300">
                  <svg className="w-3.5 h-3.5 text-green-400 mt-0.5 shrink-0" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
                    <path d="M20 6L9 17l-5-5"/>
                  </svg>
                  {b}
                </li>
              ))}
            </ul>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  )
}
