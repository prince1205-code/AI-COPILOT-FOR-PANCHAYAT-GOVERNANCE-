/**
 * useVoiceAgent
 * Handles: mic permission, push-to-talk, continuous mode,
 * silence detection (VAD), recording timer, cancel, stop.
 * Returns audio blob → caller sends to /voice/process.
 */
import { useState, useRef, useCallback, useEffect } from 'react'

const SILENCE_THRESHOLD  = 0.01   // RMS below this = silence
const SILENCE_DURATION   = 2000   // ms of silence before auto-stop
const MAX_RECORD_MS      = 60_000 // 60 s hard limit
const SAMPLE_INTERVAL_MS = 100    // VAD polling interval

export const VOICE_STATE = {
  IDLE:        'idle',
  REQUESTING:  'requesting',
  READY:       'ready',
  RECORDING:   'recording',
  PROCESSING:  'processing',
  ERROR:       'error',
}

export default function useVoiceAgent({ onResult, onError, continuous = false }) {
  const [state,       setState]       = useState(VOICE_STATE.IDLE)
  const [elapsed,     setElapsed]     = useState(0)       // seconds
  const [volume,      setVolume]      = useState(0)       // 0–1 for wave animation
  const [transcript,  setTranscript]  = useState('')
  const [permGranted, setPermGranted] = useState(false)

  const mediaRecorder  = useRef(null)
  const audioChunks    = useRef([])
  const streamRef      = useRef(null)
  const analyserRef    = useRef(null)
  const silenceTimer   = useRef(null)
  const elapsedTimer   = useRef(null)
  const maxTimer       = useRef(null)
  const vadInterval    = useRef(null)
  const cancelledRef   = useRef(false)

  // ----------------------------------------------------------
  // Cleanup helpers
  // ----------------------------------------------------------

  const _clearTimers = () => {
    clearTimeout(silenceTimer.current)
    clearInterval(elapsedTimer.current)
    clearTimeout(maxTimer.current)
    clearInterval(vadInterval.current)
  }

  const _stopStream = () => {
    streamRef.current?.getTracks().forEach(t => t.stop())
    streamRef.current = null
  }

  // ----------------------------------------------------------
  // Request microphone permission
  // ----------------------------------------------------------

  const requestPermission = useCallback(async () => {
    setState(VOICE_STATE.REQUESTING)
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
      stream.getTracks().forEach(t => t.stop()) // just checking
      setPermGranted(true)
      setState(VOICE_STATE.READY)
    } catch (err) {
      setPermGranted(false)
      setState(VOICE_STATE.ERROR)
      onError?.('Microphone permission denied. Please allow microphone access.')
    }
  }, [onError])

  // ----------------------------------------------------------
  // VAD — volume analysis
  // ----------------------------------------------------------

  const _startVAD = (stream) => {
    const ctx      = new AudioContext()
    const source   = ctx.createMediaStreamSource(stream)
    const analyser = ctx.createAnalyser()
    analyser.fftSize = 256
    source.connect(analyser)
    analyserRef.current = analyser

    const buf = new Float32Array(analyser.fftSize)
    let silenceStart = null

    vadInterval.current = setInterval(() => {
      analyser.getFloatTimeDomainData(buf)
      const rms = Math.sqrt(buf.reduce((s, v) => s + v * v, 0) / buf.length)
      setVolume(Math.min(1, rms * 10))

      if (continuous) {
        if (rms < SILENCE_THRESHOLD) {
          if (!silenceStart) silenceStart = Date.now()
          else if (Date.now() - silenceStart > SILENCE_DURATION) {
            silenceStart = null
            _stopRecording()
          }
        } else {
          silenceStart = null
        }
      }
    }, SAMPLE_INTERVAL_MS)
  }

  // ----------------------------------------------------------
  // Start recording
  // ----------------------------------------------------------

  const startRecording = useCallback(async () => {
    if (state === VOICE_STATE.RECORDING) return
    cancelledRef.current = false
    audioChunks.current  = []

    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        audio: { echoCancellation: true, noiseSuppression: true, sampleRate: 16000 },
      })
      streamRef.current = stream
      setPermGranted(true)

      const mr = new MediaRecorder(stream, { mimeType: _bestMime() })
      mediaRecorder.current = mr

      mr.ondataavailable = e => { if (e.data.size > 0) audioChunks.current.push(e.data) }
      mr.onstop = _onStop

      mr.start(250) // collect chunks every 250 ms
      setState(VOICE_STATE.RECORDING)
      setElapsed(0)

      _startVAD(stream)

      // Elapsed timer
      elapsedTimer.current = setInterval(() => setElapsed(s => s + 1), 1000)

      // Hard max
      maxTimer.current = setTimeout(() => _stopRecording(), MAX_RECORD_MS)

    } catch (err) {
      setState(VOICE_STATE.ERROR)
      onError?.('Could not access microphone: ' + err.message)
    }
  }, [state, continuous, onError])

  // ----------------------------------------------------------
  // Stop recording (normal)
  // ----------------------------------------------------------

  const _stopRecording = () => {
    if (mediaRecorder.current?.state === 'recording') {
      mediaRecorder.current.stop()
    }
    _clearTimers()
    _stopStream()
    setVolume(0)
  }

  const stopRecording = useCallback(() => _stopRecording(), [])

  // ----------------------------------------------------------
  // Cancel recording
  // ----------------------------------------------------------

  const cancelRecording = useCallback(() => {
    cancelledRef.current = true
    _stopRecording()
    audioChunks.current = []
    setState(VOICE_STATE.READY)
    setElapsed(0)
    setTranscript('')
  }, [])

  // ----------------------------------------------------------
  // On MediaRecorder stop → build blob → call onResult
  // ----------------------------------------------------------

  const _onStop = async () => {
    if (cancelledRef.current) return

    const blob = new Blob(audioChunks.current, { type: _bestMime() })
    audioChunks.current = []

    if (blob.size < 1000) {
      setState(VOICE_STATE.READY)
      onError?.('Recording too short — please speak for at least 1 second.')
      return
    }

    setState(VOICE_STATE.PROCESSING)
    try {
      await onResult(blob)
    } finally {
      setState(VOICE_STATE.READY)
      setElapsed(0)
    }
  }

  // ----------------------------------------------------------
  // Cleanup on unmount
  // ----------------------------------------------------------

  useEffect(() => () => { _clearTimers(); _stopStream() }, [])

  return {
    state,
    elapsed,
    volume,
    transcript,
    permGranted,
    startRecording,
    stopRecording,
    cancelRecording,
    requestPermission,
    isRecording:   state === VOICE_STATE.RECORDING,
    isProcessing:  state === VOICE_STATE.PROCESSING,
  }
}

// ----------------------------------------------------------
// Helpers
// ----------------------------------------------------------

function _bestMime() {
  const types = ['audio/webm;codecs=opus', 'audio/webm', 'audio/ogg;codecs=opus', 'audio/mp4']
  return types.find(t => MediaRecorder.isTypeSupported(t)) || 'audio/webm'
}
