import { useDomainStore } from '../stores/domainStore'
import { useQuery } from '@tanstack/react-query'
import api from '../services/api'

export default function DomainSelector() {
  const { currentDomain, setDomain, setDomains, domains } = useDomainStore()

  const { isLoading } = useQuery({
    queryKey: ['domains'],
    queryFn: async () => {
      const response = await api.get('/api/domains')
      setDomains(response.data.domains)
      return response.data.domains
    },
  })

  const handleDomainChange = async (domainName: string) => {
    setDomain(domainName as any)
    // Optionally call API to persist selection
    await api.post('/api/domains/select', { domain: domainName })
  }

  if (isLoading) {
    return <div className="text-sm text-gray-500">Loading domains...</div>
  }

  return (
    <div>
      <label className="text-xs font-semibold text-gray-700 uppercase tracking-wide">
        Select Domain
      </label>
      <select
        value={currentDomain || ''}
        onChange={(e) => handleDomainChange(e.target.value)}
        className="mt-2 w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 text-sm"
      >
        <option value="">Choose a domain...</option>
        {domains.map((domain) => (
          <option key={domain.name} value={domain.name}>
            {domain.icon} {domain.display_name}
          </option>
        ))}
      </select>

      {currentDomain && (
        <div className="mt-3 text-xs text-gray-600">
          <p className="font-medium mb-1">Key Metrics:</p>
          <div className="space-y-1">
            {domains
              .find((d) => d.name === currentDomain)
              ?.kpis.slice(0, 3)
              .map((kpi) => (
                <div key={kpi} className="flex items-center gap-1">
                  <span className="w-1.5 h-1.5 bg-primary-600 rounded-full"></span>
                  <span>{kpi}</span>
                </div>
              ))}
          </div>
        </div>
      )}
    </div>
  )
}
