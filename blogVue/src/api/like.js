import request from './request'

export const likeArticle = (articleId) => request.post(`/articles/${articleId}/like/`)