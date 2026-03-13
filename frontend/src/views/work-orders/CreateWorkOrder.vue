<template>
  <div class="create-work-order">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>创建工单</span>
          <el-button @click="$router.back()">返回</el-button>
        </div>
      </template>

      <el-form :model="form" label-width="120px" ref="formRef">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="工单类别" required>
              <el-select v-model="form.category" placeholder="选择工单类别" style="width: 100%" @change="onCategoryChange">
                <el-option
                  v-for="cat in categories"
                  :key="cat.name"
                  :label="cat.name"
                  :value="cat.name"
                />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="工单号" required>
              <el-input v-model="form.order_number" placeholder="如：WO20250115001" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="产品型号/编码" required>
              <el-input v-model="form.product_model" placeholder="如：ZEF650(4P)_Main" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="产品名称">
              <el-input v-model="form.product_name" placeholder="如：4P 限流式保护器" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="8">
            <el-form-item label="数量" required>
              <el-input-number v-model="form.quantity" :min="1" style="width: 100%" />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="优先级">
              <el-select v-model="form.priority" style="width: 100%">
                <el-option label="普通" value="普通" />
                <el-option label="紧急" value="紧急" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="计划完成">
              <el-date-picker
                v-model="form.plan_end"
                type="date"
                placeholder="选择日期"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
        </el-row>

        <el-divider content-position="left">📋 工序步骤</el-divider>

        <el-alert
          type="info"
          :closable="false"
          style="margin-bottom: 15px"
        >
          已根据工单类别 <strong>{{ form.category || '未选择' }}</strong> 自动配置工序步骤，可手动调整
        </el-alert>

        <el-table :data="form.steps" border style="margin-bottom: 20px">
          <el-table-column label="序号" width="60" type="index" />
          <el-table-column label="步骤名称" width="150">
            <template #default="{ row, $index }">
              <el-input v-model="row.step_name" placeholder="步骤名称" size="small" />
            </template>
          </el-table-column>
          <el-table-column label="步骤内容描述">
            <template #default="{ row }">
              <el-input v-model="row.step_content" placeholder="步骤内容描述" size="small" />
            </template>
          </el-table-column>
          <el-table-column label="标准日产量" width="120">
            <template #default="{ row }">
              <el-input-number v-model="row.standard_qty" :min="1" size="small" style="width: 100%" />
            </template>
          </el-table-column>
          <el-table-column label="计划数量" width="100">
            <template #default="{ row }">
              <el-input-number v-model="row.planned_qty" :min="1" size="small" style="width: 100%" />
            </template>
          </el-table-column>
          <el-table-column label="操作" width="80">
            <template #default="{ $index }">
              <el-button type="danger" link size="small" @click="removeStep($index)">删除</el-button>
            </template>
          </el-table-column>
        </el-table>

        <el-form-item label="备注">
          <el-input v-model="form.remark" type="textarea" :rows="3" placeholder="备注信息" />
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="handleSubmit" :loading="submitting">创建工单</el-button>
          <el-button @click="$router.back()">取消</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import axios from 'axios'

const router = useRouter()
const formRef = ref()
const submitting = ref(false)

const categories = ref([])

const form = reactive({
  category: '',
  order_number: 'WO' + new Date().toISOString().slice(0,10).replace(/-/g, '') + '001',
  product_model: '',
  product_name: '',
  quantity: 100,
  priority: '普通',
  plan_end: '',
  steps: [],
  remark: ''
})

const onCategoryChange = () => {
  const cat = categories.value.find(c => c.name === form.category)
  if (cat) {
    form.steps = cat.steps.map((step, index) => ({
      step_number: index + 1,
      step_name: step,
      step_content: '',
      standard_qty: form.quantity,
      planned_qty: form.quantity
    }))
  }
}

const removeStep = (index) => {
  form.steps.splice(index, 1)
  form.steps.forEach((step, i) => step.step_number = i + 1)
}

const handleSubmit = async () => {
  if (!form.category || !form.order_number || !form.product_model) {
    ElMessage.warning('请填写必填项')
    return
  }
  if (form.steps.length === 0) {
    ElMessage.warning('请至少添加一个工序步骤')
    return
  }

  submitting.value = true
  try {
    await axios.post('/api/work-orders', {
      ...form,
      plan_start: new Date().toISOString(),
      plan_end: form.plan_end ? new Date(form.plan_end).toISOString() : null
    })
    ElMessage.success('工单创建成功')
    router.push('/work-orders')
  } catch (error) {
    ElMessage.error('创建失败：' + (error.response?.data?.detail || error.message))
  } finally {
    submitting.value = false
  }
}

onMounted(async () => {
  try {
    const res = await axios.get('/api/work-order-categories')
    categories.value = res.data
  } catch (error) {
    console.error('Failed to load categories:', error)
  }
})
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.create-work-order {
  max-width: 1000px;
  margin: 0 auto;
}
</style>
