import request from './request'

// export const getComments = (articleId) => request.get('/comments/', { params: { article: articleId } })
export const createComment = (data) => request.post('/comments/', data)
export const deleteComment = (id) => request.delete(`/comments/${id}/`)
export const getReplies = (parentId) => request.get('/comments/', { params: { parent: parentId } })
export const getComments = (params) => {  // 注意：DRF 分页使用查询参数 ?page=2
  return request.get('/comments/', { params })
}
export const getCommentDetail = (id) => request.get(`/comments/${id}/`)