import { useState } from 'react'
import { motion } from 'framer-motion'
import VoiceMic from '../voice/VoiceMic'

export default function ChatBox({ onSend, onVoiceBlob, loading }) {
  const [text, setText] = useState('')

  const submit = () => {
    if (!text.trim() || loading) return
    onSend(text.trim())
    setText('')
  }

  return (
    <div className="p-4 border-t border-white/5 bg-[#0B1220]">
      <div className="flex items-end gap-2 bg-[#1F2937] border border-white/8 rounded-2xl px-4 py-3 focus-within:border-orange-500/40 transition-colors">
        {/* Voice mic — left side */}
        <div className="shrink-0 mb-0.5">
          <VoiceMic
            onResult={onVoiceBlob}
            onError={msg => console.warn('[Voice]', msg)}
            continuous={true}
            disabled={loading}
          />
        </div>

        <textarea
          rows={1}
          className="flex-1 bg-transparent text-sm text-gray-100 placeholder-gray-500 outline-none resize-none max-h-32 leading-relaxed"
          placeholder="Speak or type your question…"
          value={text}
          onChange={e => setText(e.target.value)}
          onKeyDown={e => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); submit() } }}
          style={{ height: 'auto' }}
          onInput={e => { e.target.style.height='auto'; e.target.style.height=e.target.scrollHeight+'px' }}
        />

        {/* Send button */}
        <motion.button whileTap={{ scale: 0.9 }} onClick={submit}
          disabled={loading || !text.trim()}
          className="shrink-0 w-8 h-8 rounded-xl bg-[#F97316] hover:bg-[#EA6C0A] disabled:opacity-30 disabled:cursor-not-allowed flex items-center justify-center transition-colors">
          <svg className="w-3.5 h-3.5 text-white" viewBox="0 0 24 24" fill="currentColor">
            <path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"/>
          </svg>
        </motion.button>
      </div>
      <p className="text-center text-[10px] text-gray-600 mt-2">🎤 Tap mic to speak · Enter to send · Shift+Enter for new line</p>
    </div>
  )
}
