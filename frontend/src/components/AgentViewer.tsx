import { Activity, Clock } from 'lucide-react'

interface AgentLog {
  agent_name: string
  action: string
  timestamp: string
  execution_time: number
  input?: any
  output?: any
}

interface AgentViewerProps {
  logs: AgentLog[]
}

const agentColors: Record<string, string> = {
  'Welcoming Agent': 'bg-green-100 text-green-700 border-green-200',
  'Supervisor Agent': 'bg-purple-100 text-purple-700 border-purple-200',
  'Data Manager Agent': 'bg-blue-100 text-blue-700 border-blue-200',
  'Data Engineer Agent': 'bg-orange-100 text-orange-700 border-orange-200',
  'Analytics Expert Agent': 'bg-pink-100 text-pink-700 border-pink-200',
}

export default function AgentViewer({ logs }: AgentViewerProps) {
  return (
    <div className="h-full flex flex-col">
      <div className="p-4 border-b border-gray-200">
        <div className="flex items-center gap-2">
          <Activity className="w-5 h-5 text-primary-600" />
          <h3 className="font-semibold">Agent Activity</h3>
        </div>
        <p className="text-xs text-gray-500 mt-1">
          Real-time AI agent interactions
        </p>
      </div>

      <div className="flex-1 overflow-y-auto p-4 space-y-3">
        {logs.length === 0 ? (
          <div className="text-center py-8 text-gray-500 text-sm">
            <Activity className="w-12 h-12 text-gray-300 mx-auto mb-2" />
            <p>No agent activity yet</p>
            <p className="text-xs mt-1">
              Send a message to see agents in action
            </p>
          </div>
        ) : (
          logs.map((log, index) => (
            <div
              key={index}
              className={`p-3 rounded-lg border ${
                agentColors[log.agent_name] || 'bg-gray-100 text-gray-700 border-gray-200'
              }`}
            >
              <div className="flex items-start justify-between mb-2">
                <div className="font-semibold text-sm">{log.agent_name}</div>
                <div className="flex items-center gap-1 text-xs opacity-75">
                  <Clock className="w-3 h-3" />
                  {(log.execution_time * 1000).toFixed(0)}ms
                </div>
              </div>

              <div className="text-xs opacity-90">
                <strong>Action:</strong> {log.action}
              </div>

              {log.output && (
                <div className="mt-2 text-xs opacity-75">
                  {typeof log.output === 'string' 
                    ? log.output 
                    : JSON.stringify(log.output).slice(0, 100) + '...'}
                </div>
              )}
            </div>
          ))
        )}
      </div>

      <div className="p-4 border-t border-gray-200 bg-gray-50">
        <div className="text-xs text-gray-600">
          <div className="font-semibold mb-2">Agent Roles:</div>
          <div className="space-y-1">
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 rounded-full bg-green-500"></div>
              <span>Welcoming - Greets & Routes</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 rounded-full bg-purple-500"></div>
              <span>Supervisor - Orchestrates</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 rounded-full bg-blue-500"></div>
              <span>Data Manager - Schema Expert</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 rounded-full bg-orange-500"></div>
              <span>Data Engineer - SQL Execution</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 rounded-full bg-pink-500"></div>
              <span>Analytics Expert - Insights</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
