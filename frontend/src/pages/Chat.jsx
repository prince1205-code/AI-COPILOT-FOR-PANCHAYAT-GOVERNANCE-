import { useState, useRef, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { v4 as uuid } from 'uuid'
import MessageBubble from '../components/MessageBubble'
import ChatBox from '../components/ChatBox'
import { detectLanguage, postScheme } from '../services/api'
import { processVoice } from '../voice/voiceApi'
import { speakText, stopSpeech } from '../voice/ttsApi'

const SESSION_KEY = 'sahayak_session_id'
function getSession() {
  let id = sessionStorage.getItem(SESSION_KEY)
  if (!id) { id = uuid(); sessionStorage.setItem(SESSION_KEY, id) }
  return id
}

const SUGGESTIONS = [
  'What is PM Kisan Yojana?',
  'Tell me about Ayushman Bharat',
  'Housing scheme for poor families',
  'Scholarship for SC/ST students',
  'MGNREGA employment scheme',
  'Sukanya Samriddhi Yojana',
]

function TypingIndicator() {
  return (
    <motion.div initial={{opacity:0,y:8}} animate={{opacity:1,y:0}} exit={{opacity:0}}
      className="flex gap-3 items-end">
      <div className="w-8 h-8 rounded-full bg-gradient-to-br from-indigo-500 to-violet-600 flex items-center justify-center text-[11px] font-bold text-white shrink-0">
        SA
      </div>
      <div className="bg-[#1F2937] border border-white/5 px-4 py-3 rounded-2xl rounded-tl-sm flex gap-1.5 items-center">
        {[0,0.18,0.36].map((d,i)=>(
          <motion.span key={i} className="w-1.5 h-1.5 bg-gray-400 rounded-full block"
            animate={{y:[0,-4,0]}} transition={{repeat:Infinity,duration:0.7,delay:d}}/>
        ))}
      </div>
    </motion.div>
  )
}

function SpeakingPanel({ speech, onReplay, onPause, onStop, onMute, onSpeed }) {
  const isBusy = speech.status === 'generating' || speech.status === 'speaking'
  const isPaused = speech.status === 'paused'
  const label =
    speech.status === 'generating' ? 'Preparing voice...' :
    speech.status === 'ready' ? 'Ready to replay' :
    speech.status === 'error' ? 'Voice unavailable' :
    isPaused ? 'Paused' :
    'Speaking...'

  if (speech.status === 'idle') return null

  return (
    <motion.div
      initial={{ opacity: 0, y: -6 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -6 }}
      className="max-w-3xl mx-auto mt-3 rounded-xl border border-indigo-400/20 bg-[#111827] px-3 py-2"
    >
      <div className="flex flex-wrap items-center gap-3">
        <motion.div
          className="w-8 h-8 rounded-xl bg-gradient-to-br from-indigo-500 to-violet-600 flex items-center justify-center text-[11px] font-bold text-white"
          animate={isBusy ? { scale: [1, 1.08, 1] } : { scale: 1 }}
          transition={{ repeat: isBusy ? Infinity : 0, duration: 1 }}
        >
          SA
        </motion.div>
        <div className="min-w-0 flex-1">
          <div className="flex items-center gap-2">
            <span className="text-xs font-medium text-indigo-100">🔊 {label}</span>
            {speech.language && <span className="text-[10px] text-gray-500">{speech.language}</span>}
          </div>
          <div className="mt-1 flex h-5 items-end gap-1">
            {[0.35, 0.75, 0.5, 0.9, 0.45, 0.7, 0.4, 0.85].map((height, index) => (
              <motion.span
                key={index}
                className="w-1 rounded-full bg-indigo-300"
                animate={isBusy ? { height: [`${height * 8}px`, `${height * 22}px`, `${height * 8}px`] } : { height: '7px' }}
                transition={{ repeat: isBusy ? Infinity : 0, duration: 0.75, delay: index * 0.06 }}
              />
            ))}
          </div>
        </div>
        <div className="flex items-center gap-1.5">
          <button onClick={onReplay} className="text-xs px-2.5 py-1.5 rounded-lg bg-white/5 hover:bg-white/10 text-gray-200">Replay</button>
          <button
            onClick={onPause}
            disabled={speech.status === 'generating' || speech.status === 'ready' || speech.status === 'error'}
            className="text-xs px-2.5 py-1.5 rounded-lg bg-white/5 hover:bg-white/10 disabled:opacity-40 disabled:cursor-not-allowed text-gray-200"
          >
            {isPaused ? 'Resume' : 'Pause'}
          </button>
          <button onClick={onStop} className="text-xs px-2.5 py-1.5 rounded-lg bg-red-500/15 hover:bg-red-500/25 text-red-100">Stop</button>
          <button onClick={onMute} className="text-xs px-2.5 py-1.5 rounded-lg bg-white/5 hover:bg-white/10 text-gray-200">
            {speech.muted ? 'Unmute' : 'Mute'}
          </button>
          <select
            value={speech.speed}
            onChange={e => onSpeed(Number(e.target.value))}
            className="text-xs rounded-lg bg-[#0B1220] border border-white/10 px-2 py-1.5 text-gray-200 outline-none"
          >
            {[0.75, 1, 1.25, 1.5].map(speed => <option key={speed} value={speed}>{speed}x</option>)}
          </select>
        </div>
      </div>
    </motion.div>
  )
}

function ExecutionProgress({ trace, speechStatus }) {
  const steps = trace?.length ? trace : []
  if (!steps.length && speechStatus === 'idle') return null

  return (
    <motion.div
      initial={{ opacity: 0, y: -4 }}
      animate={{ opacity: 1, y: 0 }}
      className="max-w-3xl mx-auto mt-3 rounded-xl border border-white/8 bg-[#111827] px-3 py-2"
    >
      <div className="flex flex-wrap items-center gap-2 text-[11px]">
        {steps.map(step => (
          <span
            key={step.task_id || step.name}
            className={`px-2 py-1 rounded-full border ${
              step.status === 'completed'
                ? 'bg-green-400/10 border-green-400/20 text-green-200'
                : step.status === 'failed'
                  ? 'bg-red-400/10 border-red-400/20 text-red-200'
                  : 'bg-indigo-400/10 border-indigo-400/20 text-indigo-200'
            }`}
          >
            {step.status === 'completed' ? '✓' : step.status === 'failed' ? '!' : '•'} {step.label}
          </span>
        ))}
        {speechStatus !== 'idle' && (
          <span className="px-2 py-1 rounded-full border bg-indigo-400/10 border-indigo-400/20 text-indigo-200">
            🔊 Speaking
          </span>
        )}
      </div>
    </motion.div>
  )
}

function EmptyState({ onSuggest }) {
  return (
    <div className="flex-1 flex flex-col items-center justify-center py-12 px-4">
      <div className="w-14 h-14 rounded-2xl bg-gradient-to-br from-indigo-500/20 to-violet-600/20 border border-indigo-500/20 flex items-center justify-center mb-4">
        <svg className="w-7 h-7 text-indigo-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
          <path d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"/>
        </svg>
      </div>
      <h3 className="font-semibold text-gray-200 mb-1">Ask Sahayak AI</h3>
      <p className="text-xs text-gray-500 mb-8 text-center max-w-xs">
        Get instant answers about government schemes, eligibility, benefits, and application process.
      </p>
      <div className="flex flex-wrap gap-2 justify-center max-w-md">
        {SUGGESTIONS.map(s=>(
          <button key={s} onClick={()=>onSuggest(s)}
            className="text-xs bg-[#1F2937] hover:bg-[#374151] border border-white/8 hover:border-white/15 text-gray-300 px-3.5 py-2 rounded-xl transition-all">
            {s}
          </button>
        ))}
      </div>
    </div>
  )
}

function fmt(ts) {
  return new Date(ts).toLocaleTimeString('en-IN',{hour:'2-digit',minute:'2-digit'})
}

export default function Chat() {
  const [messages,  setMessages]  = useState([])
  const [loading,    setLoading]   = useState(false)
  const [detectedLang, setDetectedLang] = useState(null)
  const [executionTrace, setExecutionTrace] = useState([])
  const [speech, setSpeech] = useState({
    status: 'idle',
    text: '',
    language: '',
    messageId: null,
    muted: false,
    speed: 1,
  })
  const sessionId = useRef(getSession())
  const bottomRef = useRef(null)
  const audioRef = useRef(null)
  const abortRef = useRef(null)
  const objectUrlRef = useRef(null)
  const speechSettingsRef = useRef({ muted: false, speed: 1 })

  useEffect(()=>{ bottomRef.current?.scrollIntoView({behavior:'smooth'}) },[messages,loading])

  useEffect(() => () => {
    abortRef.current?.abort()
    if (audioRef.current) audioRef.current.pause()
    if (objectUrlRef.current) URL.revokeObjectURL(objectUrlRef.current)
  }, [])

  const resetAudio = () => {
    abortRef.current?.abort()
    abortRef.current = null
    if (audioRef.current) {
      audioRef.current.pause()
      audioRef.current.src = ''
      audioRef.current = null
    }
    if (objectUrlRef.current) {
      URL.revokeObjectURL(objectUrlRef.current)
      objectUrlRef.current = null
    }
  }

  const speakReply = async (text, language, messageId) => {
    resetAudio()
    const controller = new AbortController()
    abortRef.current = controller
    setSpeech(current => ({
      ...current,
      status: 'generating',
      text,
      language,
      messageId,
    }))

    try {
      const blob = await speakText({ text, language, sessionId: sessionId.current, signal: controller.signal })
      if (!blob || controller.signal.aborted) return

      const url = URL.createObjectURL(blob)
      objectUrlRef.current = url
      const audio = new Audio(url)
      audioRef.current = audio
      audio.muted = speechSettingsRef.current.muted
      audio.playbackRate = speechSettingsRef.current.speed
      audio.onplay = () => setSpeech(current => ({ ...current, status: 'speaking' }))
      audio.onpause = () => {
        if (!audio.ended) setSpeech(current => ({ ...current, status: 'paused' }))
      }
      audio.onended = () => setSpeech(current => ({ ...current, status: 'ready' }))
      audio.onerror = () => setSpeech(current => ({ ...current, status: 'error' }))
      await audio.play()
    } catch (err) {
      if (err.name !== 'CanceledError' && err.name !== 'AbortError') {
        console.warn('[TTS]', err)
        setSpeech(current => ({ ...current, status: 'error' }))
      }
    }
  }

  const stopCurrentSpeech = async () => {
    resetAudio()
    setSpeech(current => ({ ...current, status: 'idle', messageId: null }))
    try {
      await stopSpeech(sessionId.current)
    } catch (err) {
      console.warn('[TTS stop]', err)
    }
  }

  const pauseOrResumeSpeech = () => {
    const audio = audioRef.current
    if (!audio) return
    if (audio.paused) audio.play().catch(err => console.warn('[TTS resume]', err))
    else audio.pause()
  }

  const replaySpeech = () => {
    const audio = audioRef.current
    if (audio) {
      audio.currentTime = 0
      audio.play().catch(err => console.warn('[TTS replay]', err))
      return
    }
    if (speech.text) speakReply(speech.text, speech.language || 'Hindi', speech.messageId)
  }

  const toggleMute = () => {
    setSpeech(current => {
      const muted = !current.muted
      speechSettingsRef.current.muted = muted
      if (audioRef.current) audioRef.current.muted = muted
      return { ...current, muted }
    })
  }

  const setPlaybackSpeed = (speed) => {
    speechSettingsRef.current.speed = speed
    if (audioRef.current) audioRef.current.playbackRate = speed
    setSpeech(current => ({ ...current, speed }))
  }

  const send = async (text) => {
    const ts = new Date().toISOString()
    const userMessage = { id: uuid(), role:'user', content:text, timestamp:fmt(ts) }
    setMessages(m=>[...m,userMessage])
    setExecutionTrace([
      { task_id: 'planning', name: 'planning', label: 'Understanding Request', status: 'running' },
    ])
    setLoading(true)
    const [res] = await Promise.allSettled([
      postScheme(sessionId.current, text),
      new Promise(r=>setTimeout(r,1000)),
    ])
    setLoading(false)
    const reply = res.status==='fulfilled'
      ? res.value.data.answer
      : '⚠️ Could not reach the server. Please try again.'
    if (res.status === 'fulfilled') {
      setExecutionTrace(res.value.data.execution_trace || [])
      if (res.value.data.detected_language) setDetectedLang(res.value.data.detected_language)
    }
    const assistantMessage = { id: uuid(), role:'assistant', content:reply, timestamp:fmt(new Date().toISOString()) }
    setMessages(m=>[...m,assistantMessage])

    let language = detectedLang || 'Hindi'
    try {
      const langRes = await detectLanguage(sessionId.current, text)
      language = langRes.data.detected_language || language
      setDetectedLang(language)
    } catch (err) {
      console.warn('[Language detect]', err)
    }
    speakReply(reply, language, assistantMessage.id)
  }

  // Voice blob handler — calls /voice/process, reuses same message flow
  const handleVoiceBlob = async (blob) => {
    setLoading(true)
    setDetectedLang(null)
    try {
      setExecutionTrace([
        { task_id: 'voice', name: 'voice', label: 'Understanding Request', status: 'running' },
      ])
      const result = await processVoice(blob, sessionId.current)
      if (result.detected_language) setDetectedLang(result.detected_language)
      const ts = fmt(new Date().toISOString())
      const assistantMessage = { id: uuid(), role: 'assistant', content: result.answer, timestamp: ts }
      setMessages(m => [
        ...m,
        { id: uuid(), role: 'user', content: `🎤 ${result.transcript}`, timestamp: ts },
        assistantMessage,
      ])
      setExecutionTrace([
        { task_id: 'voice-language', name: 'detect_language', label: 'Detecting Language', status: 'completed' },
        { task_id: 'voice-memory', name: 'update_memory', label: 'Updating Memory', status: 'completed' },
        { task_id: 'voice-schemes', name: 'searching_schemes', label: 'Searching Schemes', status: 'completed' },
        { task_id: 'voice-response', name: 'generate_response', label: 'Generating Response', status: 'completed' },
      ])
      speakReply(result.answer, result.detected_language || 'Hindi', assistantMessage.id)
    } catch (err) {
      const msg = err?.response?.data?.detail || 'Voice processing failed. Please try again.'
      setMessages(m=>[...m,{id: uuid(), role:'assistant',content:`⚠️ ${msg}`,timestamp:fmt(new Date().toISOString())}])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="flex flex-col h-screen bg-[#0B1220]">
          <div className="shrink-0 border-b border-white/5 px-5 pt-[78px] pb-4 bg-[#0B1220]">
        <div className="max-w-3xl mx-auto flex items-center justify-between gap-3">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-indigo-500 to-violet-600 flex items-center justify-center text-xs font-bold text-white">
              SA
            </div>
            <div>
              <h2 className="font-semibold text-white text-sm">Sahayak AI Assistant</h2>
              <div className="flex items-center gap-1.5">
                <span className="w-1.5 h-1.5 rounded-full bg-green-400 animate-pulse"/>
                <span className="text-xs text-gray-500">Online · Powered by Gemini</span>
              </div>
            </div>
          </div>
          <AnimatePresence>
            {(loading || detectedLang) && (
              <motion.div
                initial={{ opacity: 0, y: -4 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -4 }}
                className="text-xs text-indigo-300 bg-indigo-500/10 border border-indigo-500/20 px-3 py-1 rounded-full">
                {loading && !detectedLang ? '🎤 Processing…' : `🌐 Detected Language: ${detectedLang}`}
              </motion.div>
            )}
          </AnimatePresence>
        </div>
        <ExecutionProgress trace={executionTrace} speechStatus={speech.status} />
        <AnimatePresence>
          <SpeakingPanel
            speech={speech}
            onReplay={replaySpeech}
            onPause={pauseOrResumeSpeech}
            onStop={stopCurrentSpeech}
            onMute={toggleMute}
            onSpeed={setPlaybackSpeed}
          />
        </AnimatePresence>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto">
        <div className="max-w-3xl mx-auto px-5 py-6">
          {messages.length === 0
            ? <EmptyState onSuggest={send}/>
            : (
              <div className="space-y-5">
                {messages.map((m,i)=><MessageBubble key={m.id || i} {...m} isSpeaking={speech.messageId === m.id && speech.status === 'speaking'}/>)}
                <AnimatePresence>{loading && <TypingIndicator/>}</AnimatePresence>
                <div ref={bottomRef}/>
              </div>
            )
          }
        </div>
      </div>

      {/* Input */}
      <div className="shrink-0 max-w-3xl mx-auto w-full px-5 pb-2">
        <ChatBox onSend={send} onVoiceBlob={handleVoiceBlob} loading={loading}/>
      </div>
    </div>
  )
}
