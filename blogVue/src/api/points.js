import request from './request'

export const signIn = () => request.post('/points/sign/')
export const getUserPoints = () => request.get('/points/me/')