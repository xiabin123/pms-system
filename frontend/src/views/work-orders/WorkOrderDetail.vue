<template>
  <div class="work-order-detail">
    <el-card>
      <template #header>
        <div class="card-header">
          <div>
            <el-page-header @back="$router.back()">
              <template #content>
                <span class="page-title">工单详情</span>
                <el-tag :type="getStatusType(order.status)" style="margin-left: 12px">{{ order.status }}</el-tag>
                <el-tag type="warning" style="margin-left: 8px">{{ order.priority }}</el-tag>
              </template>
            </el-page-header>
          </div>
          <div>
            <el-button type="primary" @click="handleAssign" v-if="order.status === '待下发'">下发工单</el-button>
            <el-button type="success" @click="showRecordDialog = true" v-if="order.status === '已下发' || order.status === '生产中'">步骤登记</el-button>
          </div>
        </div>
      </template>

      <!-- 工单基本信息 -->
      <el-descriptions :column="3" border>
        <el-descriptions-item label="工单号">{{ order.order_number }}</el-descriptions-item>
        <el-descriptions-item label="工单类别">{{ order.category }}</el-descriptions-item>
        <el-descriptions-item label="产品型号">{{ order.product_model }}</el-descriptions-item>
        <el-descriptions-item label="产品名称">{{ order.product_name }}</el-descriptions-item>
        <el-descriptions-item label="数量">{{ order.quantity }}</el-descriptions-item>
        <el-descriptions-item label="创建人">{{ order.created_by }}</el-descriptions-item>
        <el-descriptions-item label="计划开始">{{ formatDate(order.plan_start) }}</el-descriptions-item>
        <el-descriptions-item label="计划结束">{{ formatDate(order.plan_end) }}</el-descriptions-item>
        <el-descriptions-item label="创建时间">{{ formatDate(order.created_at) }}</el-descriptions-item>
      </el-descriptions>

      <!-- 工序流程 -->
      <el-divider content-position="left">📋 工序流程</el-divider>
      
      <div class="process-flow">
        <div
          v-for="(step, index) in steps"
          :key="step.id"
          class="process-node"
          :class="getStepStatusClass(step.status)"
        >
          <div class="node-icon">
            <el-icon :size="24">
              <component :is="getStepIcon(step.status)" />
            </el-icon>
          </div>
          <div class="node-content">
            <div class="node-title">{{ step.step_name }}</div>
            <div class="node-info">{{ step.step_content || '无描述' }}</div>
            <div class="node-progress">
              <el-progress
                :percentage="getProgress(step)"
                :status="step.status === '已完成' ? 'success' : (step.status === '进行中' ? 'warning' : undefined)"
                :stroke-width="8"
              />
            </div>
            <div class="node-qty">
              <span>计划：{{ step.planned_qty }}</span>
              <span>完成：{{ step.actual_qty || 0 }}</span>
            </div>
          </div>
          <div v-if="index < steps.length - 1" class="process-arrow">
            <el-icon><ArrowRight /></el-icon>
          </div>
        </div>
      </div>

      <!-- 登记记录 -->
      <el-divider content-position="left">📝 登记记录</el-divider>
      
      <el-table :data="records" stripe>
        <el-table-column prop="step_id" label="步骤" width="120">
          <template #default="{ row }">
            {{ getStepName(row.step_id) }}
          </template>
        </el-table-column>
        <el-table-column prop="operator_name" label="操作员" width="100" />
        <el-table-column prop="completed_qty" label="完成数量" width="100" />
        <el-table-column prop="work_hours" label="工时 (h)" width="80" />
        <el-table-column prop="work_ratio" label="工作量比例" width="100">
          <template #default="{ row }">{{ (row.work_ratio * 100).toFixed(0) }}%</template>
        </el-table-column>
        <el-table-column prop="record_time" label="登记时间" width="160">
          <template #default="{ row }">{{ formatDate(row.record_time) }}</template>
        </el-table-column>
        <el-table-column prop="remark" label="备注" />
      </el-table>
    </el-card>

    <!-- 步骤登记对话框 -->
    <el-dialog v-model="showRecordDialog" title="步骤登记" width="500px">
      <el-form :model="recordForm" label-width="100px">
        <el-form-item label="选择步骤">
          <el-select v-model="recordForm.step_id" style="width: 100%">
            <el-option
              v-for="step in steps.filter(s => s.status !== '已完成')"
              :key="step.id"
              :label="step.step_name"
              :value="step.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="操作员">
          <el-input v-model="recordForm.operator_name" placeholder="输入操作员姓名" />
        </el-form-item>
        <el-form-item label="完成数量">
          <el-input-number v-model="recordForm.completed_qty" :min="0" style="width: 100%" />
        </el-form-item>
        <el-form-item label="工时 (小时)">
          <el-input-number v-model="recordForm.work_hours" :min="0" :step="0.5" style="width: 100%" />
        </el-form-item>
        <el-form-item label="工作量比例">
          <el-slider v-model="recordForm.work_ratio" :min="0" :max="2" :step="0.1" show-input />
          <div class="slider-tip">默认 1.0 为均分，可调高/低表示工作量占比</div>
        </el-form-item>
        <el-form-item label="备注">
          <el-input v-model="recordForm.remark" type="textarea" :rows="2" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showRecordDialog = false">取消</el-button>
        <el-button type="primary" @click="submitRecord">提交登记</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import axios from 'axios'

const route = useRoute()
const showRecordDialog = ref(false)

const order = ref({})
const steps = ref([])
const records = ref([])

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

const getStepStatusClass = (status) => {
  const map = { '待开始': 'todo', '进行中': 'doing', '已完成': 'done' }
  return map[status] || 'todo'
}

const getStepIcon = (status) => {
  const map = { '待开始': 'Clock', '进行中': 'Loading', '已完成': 'CircleCheck' }
  return map[status] || 'Circle'
}

const getProgress = (step) => {
  if (!step.planned_qty) return 0
  return Math.round((step.actual_qty || 0) / step.planned_qty * 100)
}

const getStepName = (stepId) => {
  const step = steps.value.find(s => s.id === stepId)
  return step?.step_name || '-'
}

const formatDate = (date) => {
  if (!date) return '-'
  return new Date(date).toLocaleString('zh-CN', { hour12: false })
}

const handleAssign = async () => {
  try {
    await axios.post(`/api/work-orders/${order.value.id}/assign`)
    ElMessage.success('工单已下发')
    loadDetail()
  } catch (error) {
    ElMessage.error('下发失败')
  }
}

const submitRecord = async () => {
  if (!recordForm.step_id || !recordForm.operator_name) {
    ElMessage.warning('请填写必填项')
    return
  }
  
  try {
    await axios.post(`/api/work-orders/${order.value.id}/steps/${recordForm.step_id}/record`, recordForm)
    ElMessage.success('登记成功')
    showRecordDialog.value = false
    loadDetail()
  } catch (error) {
    ElMessage.error('登记失败')
  }
}

const loadDetail = async () => {
  try {
    const res = await axios.get(`/api/work-orders/${route.params.id}`)
    order.value = res.data.order
    steps.value = res.data.steps
    records.value = res.data.records
  } catch (error) {
    ElMessage.error('加载失败')
  }
}

onMounted(() => {
  loadDetail()
})
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.page-title {
  font-size: 16px;
  font-weight: bold;
}

.process-flow {
  display: flex;
  align-items: stretch;
  gap: 10px;
  padding: 20px 0;
  overflow-x: auto;
}

.process-node {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 15px;
  border-radius: 8px;
  background: #f5f7fa;
  min-width: 180px;
  border: 2px solid transparent;
}

.process-node.todo {
  border-color: #909399;
}

.process-node.doing {
  border-color: #E6A23C;
  background: #fdf6ec;
}

.process-node.done {
  border-color: #67C23A;
  background: #f0f9ff;
}

.node-icon {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 10px;
}

.todo .node-icon { background: #909399; color: #fff; }
.doing .node-icon { background: #E6A23C; color: #fff; }
.done .node-icon { background: #67C23A; color: #fff; }

.node-content {
  flex: 1;
  width: 100%;
}

.node-title {
  font-weight: bold;
  text-align: center;
  margin-bottom: 4px;
}

.node-info {
  font-size: 12px;
  color: #909399;
  text-align: center;
  margin-bottom: 8px;
}

.node-progress {
  margin-bottom: 8px;
}

.node-qty {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
  color: #606266;
}

.process-arrow {
  display: flex;
  align-items: center;
  color: #909399;
}

.slider-tip {
  font-size: 12px;
  color: #909399;
  margin-top: 4px;
}
</style>
