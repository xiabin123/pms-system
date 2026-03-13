<template>
  <div class="dashboard">
    <!-- 统计卡片 -->
    <el-row :gutter="20" class="stat-cards">
      <el-col :span="5">
        <el-card shadow="hover">
          <div class="stat-card">
            <div class="stat-icon" style="background: #409EFF">
              <el-icon :size="32"><Document /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stats.total }}</div>
              <div class="stat-label">全部工单</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="5">
        <el-card shadow="hover">
          <div class="stat-card">
            <div class="stat-icon" style="background: #67C23A">
              <el-icon :size="32"><CircleCheck /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stats.completed }}</div>
              <div class="stat-label">已完成</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="5">
        <el-card shadow="hover">
          <div class="stat-card">
            <div class="stat-icon" style="background: #E6A23C">
              <el-icon :size="32"><Clock /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stats.processing }}</div>
              <div class="stat-label">生产中</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="5">
        <el-card shadow="hover">
          <div class="stat-card">
            <div class="stat-icon" style="background: #909399">
              <el-icon :size="32"><Bell /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stats.pending }}</div>
              <div class="stat-label">待下发</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="4">
        <el-card shadow="hover">
          <div class="stat-card">
            <div class="stat-icon" style="background: #F56C6C">
              <el-icon :size="32"><Warning /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stats.delayed }}</div>
              <div class="stat-label">延误</div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 待办工单 -->
    <el-card style="margin-top: 20px">
      <template #header>
        <div class="card-header">
          <span>📋 我的待办</span>
          <el-button type="primary" link @click="$router.push('/work-orders')">查看全部</el-button>
        </div>
      </template>
      <el-table :data="pendingOrders" stripe>
        <el-table-column prop="order_number" label="工单号" width="150" />
        <el-table-column prop="category" label="类别" width="100">
          <template #default="{ row }">
            <el-tag size="small">{{ row.category }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="product_model" label="产品型号" width="160" />
        <el-table-column prop="quantity" label="数量" width="80" align="right" />
        <el-table-column prop="priority" label="优先级" width="70">
          <template #default="{ row }">
            <el-tag :type="row.priority === '紧急' ? 'danger' : 'info'" size="small">{{ row.priority }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="plan_end" label="计划完成" width="110" />
        <el-table-column label="状态" width="90">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)" size="small">{{ row.status }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="100" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" link size="small" @click="$router.push(`/work-orders/${row.id}`)">处理</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import axios from 'axios'

const stats = reactive({
  total: 0,
  completed: 0,
  processing: 0,
  pending: 0,
  delayed: 0
})

const pendingOrders = ref([])

const user = computed(() => JSON.parse(localStorage.getItem('user') || '{}'))

const getStatusType = (status) => {
  const map = { '待下发': 'info', '已下发': 'warning', '生产中': 'warning', '已完成': 'success', '延误': 'danger' }
  return map[status] || 'info'
}

const loadStats = async () => {
  try {
    const res = await axios.get('/api/stats/dashboard')
    Object.assign(stats, res.data)
  } catch (error) {
    console.error('Failed to load stats:', error)
  }
}

const loadPendingOrders = async () => {
  try {
    const res = await axios.get('/api/work-orders', { params: { status: '待下发，已下发，生产中', limit: 10 } })
    pendingOrders.value = res.data.data || []
  } catch (error) {
    console.error('Failed to load pending orders:', error)
  }
}

onMounted(() => {
  loadStats()
  loadPendingOrders()
})
</script>

<style scoped>
.stat-cards {
  margin-bottom: 20px;
}

.stat-card {
  display: flex;
  align-items: center;
}

.stat-icon {
  width: 64px;
  height: 64px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  margin-right: 16px;
}

.stat-info {
  flex: 1;
}

.stat-value {
  font-size: 28px;
  font-weight: bold;
  color: #303133;
}

.stat-label {
  font-size: 14px;
  color: #909399;
  margin-top: 4px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
