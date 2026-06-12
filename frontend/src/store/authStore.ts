import { create, SetState } from 'zustand'
import { User } from '../types'

interface AuthState {
  user: User | null
  token: string | null
  setAuth: (user: User, token: string) => void
  logout: () => void
  loadFromStorage: () => void
}

export const useAuthStore = create<AuthState>((set: SetState<AuthState>) => ({
  user: null,
  token: null,
  setAuth: (user: User, token: string) => {
    localStorage.setItem('token', token)
    localStorage.setItem('user', JSON.stringify(user))
    set({ user, token })
  },
  logout: () => {
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    set({ user: null, token: null })
  },
  loadFromStorage: () => {
    const token = localStorage.getItem('token')
    const user = localStorage.getItem('user')
    if (token && user) {
      try {
        set({ token, user: JSON.parse(user) })
      } catch {
        localStorage.removeItem('token')
        localStorage.removeItem('user')
      }
    }
  },
}))

// Load auth on app init
useAuthStore.getState().loadFromStorage()
