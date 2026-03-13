<template>
  <el-container class="layout-container">
    <!-- 侧边栏 -->
    <el-aside width="220px">
      <div class="logo">
        <el-icon><Monitor /></el-icon>
        <span>PMS 生产管理系统</span>
      </div>
      <el-menu
        :default-active="activeMenu"
        background-color="#304156"
        text-color="#bfcbd9"
        active-text-color="#409EFF"
        router
      >
        <el-menu-item
          v-for="route in visibleRoutes"
          :key="route.path"
          :index="'/' + route.path"
        >
          <el-icon><component :is="route.meta.icon" /></el-icon>
          <span>{{ route.meta.title }}</span>
        </el-menu-item>
      </el-menu>
    </el-aside>

    <!-- 主内容区 -->
    <el-container>
      <el-header>
        <div class="header-content">
          <div class="breadcrumb">
            <el-breadcrumb separator="/">
              <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
              <el-breadcrumb-item>{{ currentTitle }}</el-breadcrumb-item>
            </el-breadcrumb>
          </div>
          <div class="user-info">
            <el-tag size="small" effect="plain">{{ user.department }}</el-tag>
            <el-dropdown style="margin-left: 12px">
              <span class="user-name">
                <el-avatar :size="32" icon="User" />
                <span style="margin-left: 8px">{{ user.real_name || user.username }}</span>
                <el-icon style="margin-left: 4px"><ArrowDown /></el-icon>
              </span>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item>
                    <el-tag size="small" type="info">{{ roleLabel }}</el-tag>
                  </el-dropdown-item>
                  <el-dropdown-item divided @click="logout">退出登录</el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </div>
        </div>
      </el-header>

      <el-main>
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

const user = computed(() => JSON.parse(localStorage.getItem('user') || '{}'))

const roleLabel = computed(() => {
  const roleMap = {
    admin: '系统管理员',
    planner: '计划员',
    hanjie: '焊接工',
    zhuangpei: '装配工',
    ceshi: '调试工',
    laohua: '老化工',
    jianyan: '检验员',
    baozhuang: '包装工',
    fahuo: '发货员',
    shouhou: '售后员'
  }
  return roleMap[user.value.role] || user.value.role
})

const visibleRoutes = computed(() => {
  const allRoutes = router.options.routes.find(r => r.path === '/')?.children || []
  const userRole = user.value.role
  
  return allRoutes.filter(r => {
    if (r.meta?.hidden) return false
    if (!r.meta?.roles) return true
    if (r.meta.roles.includes('all')) return true
    return r.meta.roles.includes(userRole)
  })
})

const activeMenu = computed(() => {
  const matched = route.matched.find(m => m.meta?.title)
  return matched?.path || route.path
})

const currentTitle = computed(() => {
  const allRoutes = router.options.routes.find(r => r.path === '/')?.children || []
  const currentRoute = allRoutes.find(r => r.path === route.path.slice(1))
  return currentRoute?.meta?.title || '未知页面'
})

const logout = () => {
  localStorage.removeItem('token')
  localStorage.removeItem('user')
  router.push('/login')
}
</script>

<style scoped>
.layout-container {
  height: 100vh;
}

.el-aside {
  background-color: #304156;
  color: #fff;
  overflow-x: hidden;
}

.logo {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 60px;
  font-size: 16px;
  font-weight: bold;
  color: #fff;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.logo .el-icon {
  font-size: 24px;
  margin-right: 8px;
}

.el-menu {
  border-right: none;
}

.el-header {
  background-color: #fff;
  border-bottom: 1px solid #e6e6e6;
  padding: 0 20px;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 100%;
}

.user-info {
  display: flex;
  align-items: center;
}

.user-name {
  display: flex;
  align-items: center;
  cursor: pointer;
}

.el-main {
  background-color: #f5f7fa;
  padding: 20px;
}
</style>
