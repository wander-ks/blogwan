import request from './request'

export const register = (data) => request.post('/auth/register/', data)
export const login = (data) => request.post('/auth/login/', data)
export const refresh = (refreshToken) => request.post('/auth/login/refresh/', { refresh: refreshToken })
export const getProfile = () => request.get('/auth/profile/')
export const updateProfile = (data) => request.put('/auth/profile/', data)