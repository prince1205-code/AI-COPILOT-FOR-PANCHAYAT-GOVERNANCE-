import { motion } from 'framer-motion'

const LEVEL_STYLE = {
  Central: 'bg-blue-500/10 text-blue-400 border-blue-500/20',
  State:   'bg-green-500/10 text-green-400 border-green-500/20',
}

export default function SchemeDetails({ scheme, onClose }) {
  const num = parseInt(scheme.confidence)
  const label = num>=90?'Excellent Match':num>=70?'Good Match':'Partial Match'
  const barColor = num>=90?'#22c55e':num>=70?'#F97316':'#6b7280'

  return (
    <motion.div initial={{opacity:0}} animate={{opacity:1}} exit={{opacity:0}}
      className="fixed inset-0 z-50 bg-black/60 backdrop-blur-sm flex items-center justify-center p-4"
      onClick={onClose}>
      <motion.div initial={{scale:0.96,y:16}} animate={{scale:1,y:0}} exit={{scale:0.96,y:16}}
        transition={{type:'spring',bounce:0.2,duration:0.4}}
        className="bg-[#111827] border border-white/8 rounded-2xl p-6 max-w-lg w-full max-h-[85vh] overflow-y-auto shadow-2xl"
        onClick={e=>e.stopPropagation()}>

        {/* Close */}
        <div className="flex justify-between items-start mb-5">
          <div className="flex-1 pr-4">
            <div className="flex items-center gap-2 mb-2">
              <span className={`text-[11px] font-medium px-2.5 py-0.5 rounded-full border ${LEVEL_STYLE[scheme.level]??'bg-gray-700/50 text-gray-400 border-gray-600'}`}>
                {scheme.level}
              </span>
              <span className="text-[11px] text-gray-500">{scheme.category.split(',')[0]}</span>
            </div>
            <h2 className="text-base font-bold text-white leading-snug">{scheme.scheme_name}</h2>
          </div>
          <button onClick={onClose}
            className="w-8 h-8 rounded-lg bg-white/5 hover:bg-white/10 flex items-center justify-center text-gray-400 hover:text-white transition-colors shrink-0">
            <svg className="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M18 6L6 18M6 6l12 12"/>
            </svg>
          </button>
        </div>

        {/* Confidence */}
        <div className="bg-[#0B1220] border border-white/6 rounded-xl p-4 mb-5">
          <div className="flex justify-between items-center mb-2">
            <span className="text-xs text-gray-500 font-medium">Match Confidence</span>
            <div className="flex items-center gap-2">
              <span className="text-xs font-semibold" style={{color:barColor}}>{label}</span>
              <span className="text-lg font-extrabold text-white">{scheme.confidence}</span>
            </div>
          </div>
          <div className="h-2 bg-gray-800 rounded-full overflow-hidden">
            <motion.div initial={{width:0}} animate={{width:`${num}%`}}
              transition={{duration:1,ease:'easeOut'}}
              className="h-full rounded-full"
              style={{background:`linear-gradient(90deg,${barColor},${barColor}99)`}}/>
          </div>
        </div>

        {/* Why eligible */}
        <div className="mb-5">
          <h4 className="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-3">Why Am I Eligible?</h4>
          <ul className="space-y-2">
            {scheme.why.map((b,i)=>(
              <li key={i} className="flex items-start gap-2.5 text-sm text-gray-300">
                <svg className="w-4 h-4 text-green-400 mt-0.5 shrink-0" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
                  <path d="M20 6L9 17l-5-5"/>
                </svg>
                {b}
              </li>
            ))}
          </ul>
        </div>

        {/* Score breakdown */}
        <div className="border-t border-white/5 pt-4">
          <h4 className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2">Score Breakdown</h4>
          <p className="text-xs text-gray-600 leading-relaxed">{scheme.reason}</p>
        </div>
      </motion.div>
    </motion.div>
  )
}
