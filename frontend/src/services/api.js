import axios from 'axios'

const api = axios.create({ baseURL: '/api/v1' })

export const getHealth       = ()           => api.get('/health')
export const postRecommend   = (profile)    => api.post('/recommend', profile)
export const postNLRecommend = (text, top_k=10) => api.post('/profile/recommend', { text, top_k })
export const postChat        = (session_id, message) => api.post('/chat', { session_id, message })
export const postScheme      = (session_id, query)   => api.post('/scheme', { session_id, query })
export const getHistory      = (session_id) => api.get(`/history/${session_id}`)
export const detectLanguage  = (session_id, text) => api.post('/language/detect', { session_id, text })
