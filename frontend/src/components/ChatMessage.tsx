import ReactMarkdown from 'react-markdown'
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter'
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism'
import { User, Bot } from 'lucide-react'
import { format } from 'date-fns'

interface Message {
  role: 'user' | 'assistant'
  content: string
  timestamp: Date
  visualization?: any
  sql_query?: string
  data?: any[]
}

interface ChatMessageProps {
  message: Message
}

export default function ChatMessage({ message }: ChatMessageProps) {
  const isUser = message.role === 'user'

  return (
    <div className={`flex gap-4 ${isUser ? 'flex-row-reverse' : ''}`}>
      <div
        className={`w-10 h-10 rounded-full flex items-center justify-center flex-shrink-0 ${
          isUser ? 'bg-primary-600' : 'bg-gradient-to-br from-purple-600 to-blue-600'
        }`}
      >
        {isUser ? (
          <User className="w-5 h-5 text-white" />
        ) : (
          <Bot className="w-5 h-5 text-white" />
        )}
      </div>

      <div className={`flex-1 ${isUser ? 'max-w-2xl' : 'max-w-4xl'}`}>
        <div className="flex items-center gap-2 mb-1">
          <span className="text-sm font-semibold">
            {isUser ? 'You' : 'COGNIX AI'}
          </span>
          <span className="text-xs text-gray-500">
            {format(message.timestamp, 'h:mm a')}
          </span>
        </div>

        <div
          className={`rounded-2xl p-4 ${
            isUser
              ? 'bg-primary-600 text-white'
              : 'bg-white border border-gray-200'
          }`}
        >
          {isUser ? (
            <p className="whitespace-pre-wrap">{message.content}</p>
          ) : (
            <div className="prose prose-sm max-w-none">
              <ReactMarkdown>{message.content}</ReactMarkdown>
            </div>
          )}

          {message.sql_query && (
            <div className="mt-4 rounded-lg overflow-hidden">
              <div className="bg-gray-800 px-3 py-2 text-white text-xs font-semibold">
                SQL Query
              </div>
              <SyntaxHighlighter
                language="sql"
                style={vscDarkPlus}
                customStyle={{ margin: 0, borderRadius: 0 }}
              >
                {message.sql_query}
              </SyntaxHighlighter>
            </div>
          )}

          {message.visualization && (
            <div className="mt-4 p-4 bg-gray-50 rounded-lg">
              <h4 className="text-sm font-semibold mb-2">
                {message.visualization.title}
              </h4>
              {/* Visualization component would render here */}
              <div className="text-xs text-gray-500">
                Chart: {message.visualization.type}
              </div>
            </div>
          )}

          {message.data && message.data.length > 0 && (
            <div className="mt-4">
              <div className="text-xs font-semibold mb-2">
                Data ({message.data.length} rows)
              </div>
              <div className="overflow-x-auto">
                <table className="min-w-full text-xs">
                  <thead>
                    <tr className="border-b">
                      {Object.keys(message.data[0]).map((key) => (
                        <th key={key} className="px-2 py-1 text-left font-semibold">
                          {key}
                        </th>
                      ))}
                    </tr>
                  </thead>
                  <tbody>
                    {message.data.slice(0, 5).map((row, idx) => (
                      <tr key={idx} className="border-b">
                        {Object.values(row).map((value: any, vidx) => (
                          <td key={vidx} className="px-2 py-1">
                            {String(value)}
                          </td>
                        ))}
                      </tr>
                    ))}
                  </tbody>
                </table>
                {message.data.length > 5 && (
                  <div className="text-xs text-gray-500 mt-2">
                    ... and {message.data.length - 5} more rows
                  </div>
                )}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
