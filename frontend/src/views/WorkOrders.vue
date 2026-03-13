<template>
  <div class="work-orders">
    <el-card>
      <div class="toolbar">
        <el-form :inline="true">
          <el-form-item label="工单类别">
            <el-select v-model="searchForm.category" placeholder="全部" clearable style="width: 150px">
              <el-option label="线路板工单" value="线路板工单" />
              <el-option label="半成品工单" value="半成品工单" />
              <el-option label="成品工单" value="成品工单" />
              <el-option label="检验工单" value="检验工单" />
              <el-option label="发货工单" value="发货工单" />
              <el-option label="维修工单" value="维修工单" />
              <el-option label="售后工单" value="售后工单" />
            </el-select>
          </el-form-item>
          <el-form-item label="状态">
            <el-select v-model="searchForm.status" placeholder="全部" clearable style="width: 120px">
              <el-option label="待下发" value="待下发" />
              <el-option label="已下发" value="已下发" />
              <el-option label="生产中" value="生产中" />
              <el-option label="已完成" value="已完成" />
              <el-option label="延误" value="延误" />
            </el-select>
          </el-form-item>
          <el-form-item label="关键字">
            <el-input v-model="searchForm.keyword" placeholder="工单号/产品型号" clearable style="width: 200px" />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="handleSearch">查询</el-button>
            <el-button @click="resetSearch">重置</el-button>
          </el-form-item>
        </el-form>
        <div>
          <el-button type="primary" v-if="canCreate" @click="$router.push('/work-orders/create')">
            <el-icon><Plus /></el-icon>
            创建工单
          </el-button>
        </div>
      </div>

      <el-table :data="tableData" stripe v-loading="loading" @row-click="handleRowClick">
        <el-table-column prop="id" label="ID" width="60" />
        <el-table-column prop="order_number" label="工单号" width="150" />
        <el-table-column prop="category" label="类别" width="100">
          <template #default="{ row }">
            <el-tag size="small" effect="plain">{{ row.category }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="product_model" label="产品型号" width="160" />
        <el-table-column prop="product_name" label="产品名称" width="150" />
        <el-table-column prop="quantity" label="数量" width="70" align="right" />
        <el-table-column prop="status" label="状态" width="90">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)" size="small">{{ row.status }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="priority" label="优先级" width="70">
          <template #default="{ row }">
            <el-tag :type="row.priority === '紧急' ? 'danger' : 'info'" size="small">{{ row.priority }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="工序进度" min-width="250">
          <template #default="{ row }">
            <div class="step-progress">
              <template v-for="(step, idx) in getSteps(row)" :key="idx">
                <span class="step-dot" :class="step.status">{{ step.name[0] }}</span>
                <span v-if="idx < row.steps?.length - 1" class="step-line"></span>
              </template>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="plan_end" label="计划完成" width="110" />
        <el-table-column label="操作" fixed="right" width="180">
          <template #default="{ row }">
            <el-button type="primary" link @click.stop="handleView(row)">详情</el-button>
            <el-button 
              type="success" 
              link 
              v-if="row.status === '待下发'"
              @click.stop="handleAssign(row)"
            >下发</el-button>
            <el-button 
              type="warning" 
              link 
              v-if="row.status === '已下发' || row.status === '生产中'"
              @click.stop="handleRegister(row)"
            >登记</el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination">
        <el-pagination
          v-model:current-page="pagination.page"
          v-model:page-size="pagination.pageSize"
          :total="pagination.total"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next"
        />
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import axios from 'axios'

const router = useRouter()
const loading = ref(false)

const user = computed(() => JSON.parse(localStorage.getItem('user') || '{}'))
const canCreate = computed(() => ['admin', 'planner'].includes(user.value.role))

const searchForm = reactive({
  category: '',
  status: '',
  keyword: ''
})

const pagination = reactive({
  page: 1,
  pageSize: 20,
  total: 0
})

const tableData = ref([])

const getStatusType = (status) => {
  const map = { '待下发': 'info', '已下发': 'warning', '生产中': 'warning', '已完成': 'success', '延误': 'danger' }
  return map[status] || 'info'
}

const getSteps = (row) => {
  // 简化的步骤显示
  const steps = row.steps || []
  return steps.map(s => ({
    name: s.step_name || '步骤',
    status: s.status || 'todo'
  }))
}

const handleSearch = () => {
  loadData()
}

const resetSearch = () => {
  searchForm.category = ''
  searchForm.status = ''
  searchForm.keyword = ''
}

const handleRowClick = (row) => {
  router.push(`/work-orders/${row.id}`)
}

const handleView = (row) => {
  router.push(`/work-orders/${row.id}`)
}

const handleAssign = async (row) => {
  try {
    await axios.post(`/api/work-orders/${row.id}/assign`)
    ElMessage.success('工单已下发')
    loadData()
  } catch (error) {
    ElMessage.error('下发失败')
  }
}

const handleRegister = (row) => {
  router.push(`/work-orders/${row.id}`)
}

const loadData = async () => {
  loading.value = true
  try {
    const params = {
      skip: (pagination.page - 1) * pagination.pageSize,
      limit: pagination.pageSize
    }
    if (searchForm.category) params.category = searchForm.category
    if (searchForm.status) params.status = searchForm.status
    if (searchForm.keyword) params.keyword = searchForm.keyword

    const res = await axios.get('/api/work-orders', { params })
    tableData.value = res.data.data || []
    pagination.total = res.data.total || 0
  } catch (error) {
    ElMessage.error('加载失败')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadData()
})
</script>

<style scoped>
.toolbar {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

.step-progress {
  display: flex;
  align-items: center;
  gap: 4px;
}

.step-dot {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 11px;
  font-weight: bold;
  color: #fff;
  background: #909399;
}

.step-dot.todo { background: #909399; }
.step-dot.doing { background: #E6A23C; }
.step-dot.done { background: #67C23A; }

.step-line {
  width: 16px;
  height: 2px;
  background: #dcdfe6;
}
</style>
