/**
 * VoiceMic — Voice UI component
 * Props:
 *   onResult(blob)  — called with audio Blob when recording stops
 *   onError(msg)    — called on any error
 *   continuous      — enable silence-detection auto-stop (default true)
 *   disabled        — disable the button
 */
import { useCallback } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import useVoiceAgent, { VOICE_STATE } from './useVoiceAgent'

function fmt(s) {
  const m   = Math.floor(s / 60).toString().padStart(2, '0')
  const sec = (s % 60).toString().padStart(2, '0')
  return `${m}:${sec}`
}

export default function VoiceMic({ onResult, onError, continuous = true, disabled = false }) {
  const {
    state, elapsed,
    startRecording, stopRecording, cancelRecording, requestPermission,
    isRecording, isProcessing, permGranted,
  } = useVoiceAgent({ onResult, onError, continuous })

  const handleClick = useCallback(() => {
    if (disabled) return
    if (!permGranted && state === VOICE_STATE.IDLE) { requestPermission(); return }
    if (isRecording)   { stopRecording();  return }
    if (!isProcessing)   startRecording()
  }, [disabled, permGranted, state, isRecording, isProcessing,
      startRecording, stopRecording, requestPermission])

  const btnCls = isRecording
    ? 'bg-red-500 hover:bg-red-600 shadow-lg shadow-red-500/30'
    : isProcessing
      ? 'bg-indigo-500 cursor-wait'
      : 'bg-[#1F2937] hover:bg-[#374151] border border-white/10'

  return (
    <div className="flex items-center gap-2">
      {/* Mic button + wave rings */}
      <div className="relative">
        <AnimatePresence>
          {isRecording && [1, 2, 3].map(i => (
            <motion.span key={i}
              className="absolute inset-0 rounded-xl border border-red-500/40"
              initial={{ scale: 1, opacity: 0.6 }}
              animate={{ scale: 1 + i * 0.4, opacity: 0 }}
              transition={{ repeat: Infinity, duration: 1.6, delay: i * 0.28, ease: 'easeOut' }}
            />
          ))}
        </AnimatePresence>

        <motion.button whileTap={{ scale: 0.9 }} onClick={handleClick}
          disabled={disabled || isProcessing}
          title={isRecording ? 'Stop recording' : 'Start voice input'}
          className={`relative w-10 h-10 rounded-xl flex items-center justify-center transition-colors ${btnCls}`}>

          {isProcessing ? (
            <svg className="w-4 h-4 text-white animate-spin" viewBox="0 0 24 24" fill="none">
              <circle cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="3"
                strokeDasharray="32" strokeDashoffset="12"/>
            </svg>
          ) : isRecording ? (
            <svg className="w-3.5 h-3.5 text-white" viewBox="0 0 24 24" fill="currentColor">
              <rect x="6" y="6" width="12" height="12" rx="2"/>
            </svg>
          ) : (
            <svg className="w-4 h-4 text-gray-300" viewBox="0 0 24 24" fill="none"
              stroke="currentColor" strokeWidth="1.8">
              <path d="M12 1a3 3 0 00-3 3v8a3 3 0 006 0V4a3 3 0 00-3-3z"/>
              <path d="M19 10v2a7 7 0 01-14 0v-2M12 19v4M8 23h8"/>
            </svg>
          )}
        </motion.button>
      </div>

      {/* Timer + cancel */}
      <AnimatePresence>
        {isRecording && (
          <motion.div initial={{ opacity: 0, x: -6 }} animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -6 }} className="flex items-center gap-2">
            <span className="text-xs font-mono text-red-400 tabular-nums">{fmt(elapsed)}</span>
            <button onClick={cancelRecording}
              className="text-[10px] text-gray-500 hover:text-gray-300 px-1.5 py-0.5 rounded border border-white/10 hover:border-white/20 transition-colors">
              Cancel
            </button>
          </motion.div>
        )}
        {isProcessing && (
          <motion.span initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
            className="text-xs text-indigo-400">
            Transcribing…
          </motion.span>
        )}
      </AnimatePresence>
    </div>
  )
}
