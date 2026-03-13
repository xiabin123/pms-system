<template>
  <div class="step-register">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>步骤登记</span>
          <el-tag>{{ user.real_name }} - {{ user.department }}</el-tag>
        </div>
      </template>

      <el-alert
        type="info"
        :closable="false"
        style="margin-bottom: 20px"
      >
        选择要登记的工单步骤，填写实际完成的数量和工时。工作量比例可用于调节多人协作时的分配比例。
      </el-alert>

      <el-form :model="searchForm" :inline="true" style="margin-bottom: 20px">
        <el-form-item label="工单类别">
          <el-select v-model="searchForm.category" placeholder="全部" clearable style="width: 150px">
            <el-option label="线路板工单" value="线路板工单" />
            <el-option label="半成品工单" value="半成品工单" />
            <el-option label="成品工单" value="成品工单" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="loadWorkOrders">查询</el-button>
        </el-form-item>
      </el-form>

      <el-table :data="workOrders" stripe v-loading="loading">
        <el-table-column prop="order_number" label="工单号" width="150" />
        <el-table-column prop="category" label="类别" width="100" />
        <el-table-column prop="product_model" label="产品型号" width="160" />
        <el-table-column prop="quantity" label="数量" width="70" />
        <el-table-column label="工序步骤" min-width="300">
          <template #default="{ row }">
            <div class="steps-container">
              <el-tag
                v-for="step in row.steps"
                :key="step.id"
                :type="getStepTagType(step.status)"
                size="small"
                style="margin-right: 8px; margin-bottom: 4px"
                @click="showRegisterDialog(row, step)"
              >
                {{ step.step_name }}
                <el-icon v-if="step.status === '待开始'" style="margin-left: 4px"><Pointer /></el-icon>
                <el-icon v-else-if="step.status === '进行中'" style="margin-left: 4px"><Loading /></el-icon>
                <el-icon v-else style="margin-left: 4px"><CircleCheck /></el-icon>
              </el-tag>
            </div>
          </template>
        </el-table-column>
        <el-table-column label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)" size="small">{{ row.status }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="100" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" link size="small" @click="handleViewDetail(row)">详情</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 登记对话框 -->
    <el-dialog v-model="showDialog" :title="'登记：' + currentStep?.step_name" width="500px">
      <div class="dialog-info" v-if="currentOrder && currentStep">
        <p><strong>工单：</strong>{{ currentOrder.order_number }}</p>
        <p><strong>步骤：</strong>{{ currentStep.step_name }}</p>
        <p><strong>计划数量：</strong>{{ currentStep.planned_qty }}</p>
        <p><strong>已完成：</strong>{{ currentStep.actual_qty || 0 }}</p>
      </div>
      
      <el-form :model="recordForm" label-width="100px">
        <el-form-item label="操作员">
          <el-input v-model="recordForm.operator_name" :value="user.real_name" readonly />
        </el-form-item>
        <el-form-item label="完成数量">
          <el-input-number v-model="recordForm.completed_qty" :min="0" :max="currentStep?.planned_qty" style="width: 100%" />
        </el-form-item>
        <el-form-item label="工时 (小时)">
          <el-input-number v-model="recordForm.work_hours" :min="0" :step="0.5" style="width: 100%" />
        </el-form-item>
        <el-form-item label="工作量比例">
          <el-slider v-model="recordForm.work_ratio" :min="0.1" :max="2" :step="0.1" show-input />
          <div class="slider-tip">1.0 = 平均分配，调高表示承担更多工作量</div>
        </el-form-item>
        <el-form-item label="备注">
          <el-input v-model="recordForm.remark" type="textarea" :rows="2" placeholder="可选填写" />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <el-button @click="showDialog = false">取消</el-button>
        <el-button type="primary" @click="submitRecord">提交登记</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import axios from 'axios'

const router = useRouter()
const loading = ref(false)
const showDialog = ref(false)

const user = computed(() => JSON.parse(localStorage.getItem('user') || '{}'))

const searchForm = reactive({
  category: ''
})

const workOrders = ref([])
const currentOrder = ref(null)
const currentStep = ref(null)

const recordForm = reactive({
  step_id: null,
  operator_name: '',
  completed_qty: 0,
  work_hours: 0,
  work_ratio: 1.0,
  remark: ''
})

const getStatusType = (status) => {
  const map = { '待下发': 'info', '已下发': 'warning', '生产中': 'warning', '已完成': 'success', '延误': 'danger' }
  return map[status] || 'info'
}

const getStepTagType = (status) => {
  const map = { '待开始': 'info', '进行中': 'warning', '已完成': 'success' }
  return map[status] || 'info'
}

const showRegisterDialog = (order, step) => {
  if (step.status === '已完成') {
    ElMessage.info('此步骤已完成，无需登记')
    return
  }
  
  currentOrder.value = order
  currentStep.value = step
  recordForm.step_id = step.id
  recordForm.operator_name = user.value.real_name
  recordForm.completed_qty = 0
  recordForm.work_hours = 0
  recordForm.work_ratio = 1.0
  recordForm.remark = ''
  showDialog.value = true
}

const submitRecord = async () => {
  if (!recordForm.step_id || !recordForm.completed_qty) {
    ElMessage.warning('请填写完成数量')
    return
  }
  
  try {
    await axios.post(
      `/api/work-orders/${currentOrder.value.id}/steps/${recordForm.step_id}/record`,
      recordForm
    )
    ElMessage.success('登记成功')
    showDialog.value = false
    loadWorkOrders()
  } catch (error) {
    ElMessage.error('登记失败：' + (error.response?.data?.detail || error.message))
  }
}

const handleViewDetail = (row) => {
  router.push(`/work-orders/${row.id}`)
}

const loadWorkOrders = async () => {
  loading.value = true
  try {
    const params = { status: '已下发，生产中', limit: 50 }
    if (searchForm.category) params.category = searchForm.category
    
    const res = await axios.get('/api/work-orders', { params })
    workOrders.value = res.data.data || []
  } catch (error) {
    ElMessage.error('加载失败')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadWorkOrders()
})
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.steps-container {
  display: flex;
  flex-wrap: wrap;
}

.dialog-info {
  background: #f5f7fa;
  padding: 15px;
  border-radius: 6px;
  margin-bottom: 20px;
}

.dialog-info p {
  margin: 4px 0;
  font-size: 14px;
}

.slider-tip {
  font-size: 12px;
  color: #909399;
  margin-top: 4px;
}
</style>
