import request from '@/utils/request'

export function getList(params) {
  return request({
    url: '/users/',
    method: 'get',
    params
  })
}

export function getBooksList(params) {
  return request({
    url: '/books/',
    method: 'get',
    params
  })
}

export function delBooks(params) {
  return request({
    url: `/books/${params}`,
    method: 'delete',
    params
  })
}
