import axios from 'axios'

export async function speakText({ text, language, sessionId, signal }) {
  const { data, status } = await axios.post(
    '/api/v1/tts/speak',
    { text, language, session_id: sessionId },
    { responseType: 'blob', signal, validateStatus: status => status === 200 || status === 204 },
  )

  if (status === 204) return null
  return data
}

export async function stopSpeech(sessionId) {
  const { data } = await axios.post('/api/v1/tts/stop', { session_id: sessionId })
  return data
}
