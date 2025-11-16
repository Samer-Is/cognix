import { useState } from 'react'
import { useAuthStore } from '../stores/authStore'
import { useDomainStore } from '../stores/domainStore'
import { MessageSquare, Send, Sparkles, Menu, LogOut } from 'lucide-react'
import ChatMessage from '../components/ChatMessage'
import DomainSelector from '../components/DomainSelector'
import AgentViewer from '../components/AgentViewer'
import { useMutation } from '@tanstack/react-query'
import api from '../services/api'

interface Message {
  role: 'user' | 'assistant'
  content: string
  timestamp: Date
  visualization?: any
  sql_query?: string
  data?: any[]
}

interface AgentLog {
  agent_name: string
  action: string
  timestamp: string
  execution_time: number
}

export default function ChatPage() {
  const { user, logout } = useAuthStore()
  const { currentDomain } = useDomainStore()
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState('')
  const [agentLogs, setAgentLogs] = useState<AgentLog[]>([])
  const [showAgentViewer, setShowAgentViewer] = useState(true)
  const [showSidebar, setShowSidebar] = useState(true)

  const chatMutation = useMutation({
    mutationFn: async (message: string) => {
      const response = await api.post('/api/chat', {
        message,
        domain: currentDomain,
        include_agent_logs: true,
      })
      return response.data
    },
    onSuccess: (data) => {
      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          content: data.message,
          timestamp: new Date(),
          visualization: data.visualization,
          sql_query: data.sql_query,
          data: data.data,
        },
      ])
      if (data.agent_logs) {
        setAgentLogs(data.agent_logs)
      }
    },
  })

  const handleSend = () => {
    if (!input.trim()) return

    const userMessage: Message = {
      role: 'user',
      content: input,
      timestamp: new Date(),
    }

    setMessages((prev) => [...prev, userMessage])
    chatMutation.mutate(input)
    setInput('')
  }

  const handleLogout = () => {
    logout()
    window.location.href = '/login'
  }

  return (
    <div className="flex h-screen bg-gray-50">
      {/* Sidebar */}
      {showSidebar && (
        <div className="w-64 bg-white border-r border-gray-200 flex flex-col">
          <div className="p-4 border-b border-gray-200">
            <h1 className="text-2xl font-bold text-primary-600 flex items-center gap-2">
              <Sparkles className="w-6 h-6" />
              COGNIX AI
            </h1>
            <p className="text-sm text-gray-500 mt-1">Intelligent Analytics</p>
          </div>

          <div className="p-4 border-b border-gray-200">
            <DomainSelector />
          </div>

          <div className="flex-1 p-4">
            <h3 className="text-sm font-semibold text-gray-700 mb-2">Quick Actions</h3>
            <button className="w-full text-left px-3 py-2 rounded-lg hover:bg-gray-100 text-sm">
              📊 View Insights
            </button>
            <button className="w-full text-left px-3 py-2 rounded-lg hover:bg-gray-100 text-sm">
              📁 Upload Files
            </button>
            <button className="w-full text-left px-3 py-2 rounded-lg hover:bg-gray-100 text-sm">
              ⭐ Saved Queries
            </button>
          </div>

          <div className="p-4 border-t border-gray-200">
            <div className="flex items-center gap-2 mb-2">
              <div className="w-8 h-8 bg-primary-600 rounded-full flex items-center justify-center text-white font-semibold">
                {user?.username?.[0]?.toUpperCase()}
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium truncate">{user?.username}</p>
                <p className="text-xs text-gray-500">{user?.role}</p>
              </div>
            </div>
            <button
              onClick={handleLogout}
              className="w-full flex items-center gap-2 px-3 py-2 rounded-lg hover:bg-red-50 text-red-600 text-sm"
            >
              <LogOut className="w-4 h-4" />
              Logout
            </button>
          </div>
        </div>
      )}

      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col">
        {/* Header */}
        <div className="bg-white border-b border-gray-200 px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-4">
            <button
              onClick={() => setShowSidebar(!showSidebar)}
              className="p-2 hover:bg-gray-100 rounded-lg"
            >
              <Menu className="w-5 h-5" />
            </button>
            <div>
              <h2 className="text-lg font-semibold">Chat with COGNIX AI</h2>
              <p className="text-sm text-gray-500">
                {currentDomain
                  ? `Analyzing ${currentDomain.replace('_', ' ')} data`
                  : 'Select a domain to start'}
              </p>
            </div>
          </div>
          <button
            onClick={() => setShowAgentViewer(!showAgentViewer)}
            className="px-4 py-2 rounded-lg bg-primary-50 text-primary-600 hover:bg-primary-100 text-sm font-medium"
          >
            {showAgentViewer ? 'Hide' : 'Show'} Agent Activity
          </button>
        </div>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-6 space-y-4">
          {messages.length === 0 && (
            <div className="text-center py-12">
              <MessageSquare className="w-16 h-16 text-gray-300 mx-auto mb-4" />
              <h3 className="text-lg font-semibold text-gray-700 mb-2">
                Start a conversation
              </h3>
              <p className="text-gray-500">
                Ask me anything about your data. I'll analyze it and provide insights.
              </p>
            </div>
          )}
          {messages.map((message, index) => (
            <ChatMessage key={index} message={message} />
          ))}
          {chatMutation.isPending && (
            <div className="flex items-center gap-2 text-gray-500">
              <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-primary-600"></div>
              <span>AI is thinking...</span>
            </div>
          )}
        </div>

        {/* Input */}
        <div className="bg-white border-t border-gray-200 p-4">
          <div className="max-w-4xl mx-auto flex gap-2">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleSend()}
              placeholder={
                currentDomain
                  ? 'Ask a question about your data...'
                  : 'Select a domain first...'
              }
              disabled={!currentDomain || chatMutation.isPending}
              className="input-field flex-1"
            />
            <button
              onClick={handleSend}
              disabled={!currentDomain || !input.trim() || chatMutation.isPending}
              className="btn-primary"
            >
              <Send className="w-5 h-5" />
            </button>
          </div>
        </div>
      </div>

      {/* Agent Viewer Sidebar */}
      {showAgentViewer && (
        <div className="w-96 bg-white border-l border-gray-200">
          <AgentViewer logs={agentLogs} />
        </div>
      )}
    </div>
  )
}
