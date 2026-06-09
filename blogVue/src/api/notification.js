import request from './request'

export const getMessages = (params) => request.get('/notifications/messages/', { params })
export const getUnreadCount = () => request.get('/notifications/messages/unread_count/')
export const deleteMessage = (id) => request.delete(`/notifications/messages/${id}/delete/`)
export const markAllRead = () => request.post('/notifications/messages/mark-all-read/')
export const markMessageRead = (id) => request.post(`/notifications/messages/${id}/mark_read/`)