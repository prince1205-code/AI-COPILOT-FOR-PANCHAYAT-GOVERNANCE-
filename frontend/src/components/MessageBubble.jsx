import { useState } from 'react'
import { motion } from 'framer-motion'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter'
import { oneDark } from 'react-syntax-highlighter/dist/esm/styles/prism'

function CopyBtn({ text }) {
  const [copied, setCopied] = useState(false)
  const copy = () => {
    navigator.clipboard.writeText(text)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }
  return (
    <button onClick={copy}
      className="opacity-0 group-hover:opacity-100 transition-opacity text-xs text-gray-500 hover:text-gray-300 px-2 py-1 rounded border border-gray-700 hover:border-gray-500">
      {copied ? '✓ Copied' : 'Copy'}
    </button>
  )
}

function SpeakingWords({ text }) {
  const words = text.replace(/\s+/g, ' ').trim().split(' ').slice(0, 18)
  if (!words.length) return null

  return (
    <div className="mt-2 flex flex-wrap gap-1.5">
      {words.map((word, index) => (
        <motion.span
          key={`${word}-${index}`}
          className="text-[10px] text-indigo-100/80 bg-indigo-400/10 px-1.5 py-0.5 rounded"
          animate={{ opacity: [0.35, 1, 0.35], y: [0, -2, 0] }}
          transition={{ repeat: Infinity, duration: 1.15, delay: (index % 8) * 0.08 }}
        >
          {word}
        </motion.span>
      ))}
    </div>
  )
}

export default function MessageBubble({ role, content, timestamp, isSpeaking = false }) {
  const isUser = role === 'user'
  return (
    <motion.div initial={{opacity:0,y:8}} animate={{opacity:1,y:0}}
      className={`group flex gap-3 ${isUser ? 'flex-row-reverse' : ''}`}>

      {/* Avatar */}
      <div className={`w-8 h-8 rounded-full flex items-center justify-center shrink-0 text-[11px] font-bold ${
        isUser
          ? 'bg-gradient-to-br from-orange-400 to-orange-600 text-white'
          : 'bg-gradient-to-br from-indigo-500 to-violet-600 text-white'
      }`}>
        {isUser ? 'You' : 'SA'}
      </div>

      <div className={`flex flex-col gap-1 max-w-[78%] ${isUser ? 'items-end' : 'items-start'}`}>
        {/* Bubble */}
        <div className={`px-4 py-3 rounded-2xl text-sm leading-relaxed ${
          isUser
            ? 'bg-[#F97316] text-white rounded-tr-sm'
            : 'bg-[#1F2937] text-gray-100 rounded-tl-sm border border-white/5'
        }`}>
          {isUser ? (
            <p className="whitespace-pre-wrap">{content}</p>
          ) : (
            <ReactMarkdown remarkPlugins={[remarkGfm]}
              components={{
                code({inline, className, children}) {
                  const lang = /language-(\w+)/.exec(className||'')?.[1]
                  return !inline && lang ? (
                    <SyntaxHighlighter style={oneDark} language={lang} PreTag="div"
                      className="rounded-lg text-xs my-2 !bg-gray-900">
                      {String(children).replace(/\n$/,'')}
                    </SyntaxHighlighter>
                  ) : (
                    <code className="bg-gray-700 px-1.5 py-0.5 rounded text-orange-300 text-xs">{children}</code>
                  )
                },
                p: ({children}) => <p className="mb-2 last:mb-0">{children}</p>,
                ul: ({children}) => <ul className="list-disc pl-4 mb-2 space-y-1">{children}</ul>,
                ol: ({children}) => <ol className="list-decimal pl-4 mb-2 space-y-1">{children}</ol>,
                li: ({children}) => <li className="text-gray-200">{children}</li>,
                strong: ({children}) => <strong className="text-white font-semibold">{children}</strong>,
              }}>
              {content}
            </ReactMarkdown>
          )}
          {!isUser && isSpeaking && <SpeakingWords text={content} />}
        </div>

        {/* Footer row */}
        <div className={`flex items-center gap-2 ${isUser ? 'flex-row-reverse' : ''}`}>
          {timestamp && <span className="text-[10px] text-gray-600">{timestamp}</span>}
          {!isUser && <CopyBtn text={content} />}
        </div>
      </div>
    </motion.div>
  )
}
