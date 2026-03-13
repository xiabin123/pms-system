<template>
  <div class="product-models">
    <el-card>
      <div class="toolbar">
        <el-button type="primary" @click="showCreateDialog = true">
          <el-icon><Plus /></el-icon>
          新建型号
        </el-button>
      </div>

      <el-table :data="tableData" stripe>
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="modelNumber" label="型号" width="150" />
        <el-table-column prop="name" label="产品名称" width="200" />
        <el-table-column prop="processRoute" label="工艺路线" />
        <el-table-column label="操作" fixed="right" width="150">
          <template #default="{ row }">
            <el-button type="primary" link @click="handleEdit(row)">编辑</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog v-model="showCreateDialog" :title="editMode ? '编辑型号' : '新建型号'" width="600px">
      <el-form :model="form" label-width="100px">
        <el-form-item label="型号">
          <el-input v-model="form.modelNumber" placeholder="如：ZE750-9Z" />
        </el-form-item>
        <el-form-item label="产品名称">
          <el-input v-model="form.name" placeholder="如：多功能表" />
        </el-form-item>
        <el-form-item label="工艺路线">
          <el-select v-model="form.processRoute" multiple placeholder="选择工序" style="width: 100%">
            <el-option label="电路板焊接" value="WB001" />
            <el-option label="组装" value="ZP001" />
            <el-option label="测试" value="CS001" />
            <el-option label="老化" value="LH001" />
            <el-option label="包装" value="BZ001" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showCreateDialog = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus'

const showCreateDialog = ref(false)
const editMode = ref(false)

const form = reactive({
  modelNumber: '',
  name: '',
  processRoute: []
})

const tableData = ref([
  { id: 1, modelNumber: 'ZE750-9Z', name: '多功能表', processRoute: 'WB001-ZP001-CS001-LH001-BZ001' },
  { id: 2, modelNumber: 'ZE750-9HL', name: '多功能表', processRoute: 'WB001-ZP001-CS001-BZ001' },
  { id: 3, modelNumber: 'ZE750-9H', name: '多功能表', processRoute: 'WB001-ZP001-CS001' },
  { id: 4, modelNumber: 'ZE750-9E', name: '多功能表', processRoute: 'WB001-ZP001-CS001-LH001' }
])

const handleEdit = (row) => {
  editMode.value = true
  Object.assign(form, row)
  showCreateDialog.value = true
}

const handleSubmit = () => {
  showCreateDialog.value = false
  ElMessage.success(editMode.value ? '更新成功' : '创建成功')
}
</script>

<style scoped>
.toolbar {
  margin-bottom: 20px;
}
</style>
