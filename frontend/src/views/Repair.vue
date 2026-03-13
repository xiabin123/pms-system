<template>
  <div class="repair">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>🔧 维修/售后管理</span>
          <el-button type="primary" @click="showCreateDialog = true">
            <el-icon><Plus /></el-icon>
            新建售后单
          </el-button>
        </div>
      </template>

      <el-tabs v-model="activeTab">
        <el-tab-pane label="维修工单" name="repair">
          <el-table :data="repairOrders" stripe>
            <el-table-column prop="order_number" label="维修单号" width="150" />
            <el-table-column prop="product_model" label="产品型号" width="150" />
            <el-table-column prop="customer" label="客户" width="120" />
            <el-table-column prop="issue" label="问题描述" min-width="200" />
            <el-table-column prop="handler" label="处理人" width="100" />
            <el-table-column prop="status" label="状态" width="100">
              <template #default="{ row }">
                <el-tag :type="row.status === '已完成' ? 'success' : 'warning'">{{ row.status }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column label="操作" width="120" fixed="right">
              <template #default="{ row }">
                <el-button type="primary" link size="small" @click="handleProcess(row)">处理</el-button>
                <el-button type="success" link size="small" v-if="row.status !== '已完成'" @click="handleComplete(row)">完成</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>
        <el-tab-pane label="售后工单" name="after_sales">
          <el-table :data="afterSalesOrders" stripe>
            <el-table-column prop="order_number" label="售后单号" width="150" />
            <el-table-column prop="product_model" label="产品型号" width="150" />
            <el-table-column prop="customer" label="客户" width="120" />
            <el-table-column prop="issue" label="问题描述" min-width="200" />
            <el-table-column prop="handler" label="处理人" width="100" />
            <el-table-column prop="status" label="状态" width="100">
              <template #default="{ row }">
                <el-tag :type="row.status === '已完成' ? 'success' : 'warning'">{{ row.status }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column label="操作" width="120" fixed="right">
              <template #default="{ row }">
                <el-button type="primary" link size="small" @click="handleProcess(row)">处理</el-button>
                <el-button type="success" link size="small" v-if="row.status !== '已完成'" @click="handleComplete(row)">完成</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>
      </el-tabs>
    </el-card>

    <el-dialog v-model="showCreateDialog" title="新建售后单" width="500px">
      <el-form :model="createForm" label-width="100px">
        <el-form-item label="类型">
          <el-select v-model="createForm.type" style="width: 100%">
            <el-option label="维修" value="维修" />
            <el-option label="售后" value="售后" />
          </el-select>
        </el-form-item>
        <el-form-item label="产品型号">
          <el-input v-model="createForm.product_model" placeholder="如：ZE750-9Z" />
        </el-form-item>
        <el-form-item label="客户名称">
          <el-input v-model="createForm.customer" placeholder="客户名称" />
        </el-form-item>
        <el-form-item label="联系方式">
          <el-input v-model="createForm.contact" placeholder="电话/微信" />
        </el-form-item>
        <el-form-item label="问题描述">
          <el-input v-model="createForm.issue" type="textarea" :rows="3" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showCreateDialog = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit">创建</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus'

const activeTab = ref('repair')
const showCreateDialog = ref(false)

const createForm = reactive({
  type: '维修',
  product_model: '',
  customer: '',
  contact: '',
  issue: ''
})

const repairOrders = ref([
  { order_number: 'WX20250115001', product_model: 'ZE750-9Z', customer: '张三', issue: '显示屏不亮', handler: '郑一', status: '处理中' },
  { order_number: 'WX20250115002', product_model: 'ZE750-7H', customer: '李四', issue: '按键失灵', handler: '郑一', status: '已完成' }
])

const afterSalesOrders = ref([
  { order_number: 'SH20250115001', product_model: 'iZ750', customer: '王五', issue: '通信异常', handler: '郑一', status: '待处理' }
])

const handleProcess = (row) => {
  ElMessage.info('处理：' + row.order_number)
}

const handleComplete = (row) => {
  row.status = '已完成'
  ElMessage.success('已完成')
}

const handleSubmit = () => {
  showCreateDialog.value = false
  ElMessage.success('创建成功')
}
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
