/**
 * Voice API service
 * Sends audio blob to backend voice endpoints.
 */
import axios from 'axios'

/**
 * POST /api/v1/voice/transcribe
 * Returns { transcript }
 */
export async function transcribeAudio(blob) {
  const form = new FormData()
  form.append('audio', blob, 'recording.webm')
  const { data } = await axios.post('/api/v1/voice/transcribe', form)
  return data.transcript
}

/**
 * POST /api/v1/voice/process
 * Returns { session_id, transcript, answer }
 */
export async function processVoice(blob, sessionId) {
  const form = new FormData()
  form.append('audio',      blob, 'recording.webm')
  form.append('session_id', sessionId)
  const { data } = await axios.post('/api/v1/voice/process', form)
  return data
}
