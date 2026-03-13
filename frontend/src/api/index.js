import request from './request'

// 工单管理
export const workOrderApi = {
  getList: (params) => request.get('/work-orders', { params }),
  getById: (id) => request.get(`/work-orders/${id}`),
  create: (data) => request.post('/work-orders', data),
  update: (id, data) => request.put(`/work-orders/${id}`, data)
}

// 物料管理
export const materialApi = {
  getList: (params) => request.get('/materials', { params }),
  getById: (id) => request.get(`/materials/${id}`),
  create: (data) => request.post('/materials', data),
  import: () => request.post('/materials/import')
}

// 工序管理
export const processApi = {
  getList: () => request.get('/processes'),
  create: (data) => request.post('/processes', data)
}

// 产品型号
export const productModelApi = {
  getList: () => request.get('/product-models'),
  create: (data) => request.post('/product-models', data)
}
