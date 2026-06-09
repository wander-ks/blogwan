const ACCESS_KEY = 'blog_access_token'
const REFRESH_KEY = 'blog_refresh_token'

export const getToken = () => localStorage.getItem(ACCESS_KEY)
export const setToken = (token) => localStorage.setItem(ACCESS_KEY, token)
export const removeToken = () => localStorage.removeItem(ACCESS_KEY)

export const getRefreshToken = () => localStorage.getItem(REFRESH_KEY)
export const setRefreshToken = (token) => localStorage.setItem(REFRESH_KEY, token)
export const removeRefreshToken = () => localStorage.removeItem(REFRESH_KEY)

export const clearAuth = () => {
  removeToken()
  removeRefreshToken()
}