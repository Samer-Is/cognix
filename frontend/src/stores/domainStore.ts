import { create } from 'zustand'

export type DomainType = 'telecom' | 'banking' | 'digital_marketing' | 'healthcare' | 'fmcg'

interface Domain {
  name: DomainType
  display_name: string
  description: string
  icon: string
  tables: string[]
  kpis: string[]
}

interface DomainState {
  currentDomain: DomainType | null
  domains: Domain[]
  setDomain: (domain: DomainType) => void
  setDomains: (domains: Domain[]) => void
}

export const useDomainStore = create<DomainState>()((set) => ({
  currentDomain: null,
  domains: [],
  setDomain: (domain) => set({ currentDomain: domain }),
  setDomains: (domains) => set({ domains }),
}))
