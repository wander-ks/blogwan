import request from './request'

export const followUser = (userId) => request.post(`/follows/follow/${userId}/`)
export const unfollowUser = (userId) => request.post(`/follows/unfollow/${userId}/`)
export const getFollowerList = () => request.get('/follows/follower_list/')
export const getFollowStatus = (userId) => request.get(`/follows/status/${userId}/`)
export const getUserArticles = (username, params) => request.get('/articles/', { params: { author__username: username, ...params } })
export const getFollowingList = (params) => request.get('/follows/following_list/', { params })