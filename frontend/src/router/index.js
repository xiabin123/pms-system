import { createRouter, createWebHistory } from 'vue-router'
import { ElMessage } from 'element-plus'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/',
    name: 'Layout',
    component: () => import('@/components/Layout.vue'),
    redirect: '/dashboard',
    children: [
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: () => import('@/views/Dashboard.vue'),
        meta: { title: '工作台', icon: 'HomeFilled', roles: ['all'] }
      },
      {
        path: 'work-orders',
        name: 'WorkOrders',
        component: () => import('@/views/WorkOrders.vue'),
        meta: { title: '工单管理', icon: 'Document', roles: ['all'] }
      },
      {
        path: 'work-orders/create',
        name: 'CreateWorkOrder',
        component: () => import('@/views/work-orders/CreateWorkOrder.vue'),
        meta: { title: '创建工单', icon: 'Plus', roles: ['planner', 'admin'] }
      },
      {
        path: 'work-orders/:id',
        name: 'WorkOrderDetail',
        component: () => import('@/views/work-orders/WorkOrderDetail.vue'),
        meta: { title: '工单详情', hidden: true }
      },
      {
        path: 'step-register',
        name: 'StepRegister',
        component: () => import('@/views/StepRegister.vue'),
        meta: { title: '步骤登记', icon: 'Edit', roles: ['hanjie', 'zhuangpei', 'ceshi', 'laohua', 'jianyan', 'baozhuang'] }
      },
      {
        path: 'materials',
        name: 'Materials',
        component: () => import('@/views/Materials.vue'),
        meta: { title: '物料管理', icon: 'Box', roles: ['all'] }
      },
      {
        path: 'delivery',
        name: 'Delivery',
        component: () => import('@/views/Delivery.vue'),
        meta: { title: '发货管理', icon: 'Van', roles: ['fahuo', 'admin'] }
      },
      {
        path: 'repair',
        name: 'Repair',
        component: () => import('@/views/Repair.vue'),
        meta: { title: '维修/售后', icon: 'Tools', roles: ['shouhou', 'admin'] }
      },
      {
        path: 'reports',
        name: 'Reports',
        component: () => import('@/views/Reports.vue'),
        meta: { title: '统计报表', icon: 'TrendCharts', roles: ['all'] }
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  const user = JSON.parse(localStorage.getItem('user') || '{}')
  
  if (to.meta.requiresAuth !== false && !token) {
    ElMessage.warning('请先登录')
    next('/login')
    return
  }
  
  // 角色权限检查
  if (to.meta.roles && to.meta.roles.length > 0 && user.role) {
    if (!to.meta.roles.includes('all') && !to.meta.roles.includes(user.role)) {
      ElMessage.error('无权访问此页面')
      next('/dashboard')
      return
    }
  }
  
  next()
})

export default router
