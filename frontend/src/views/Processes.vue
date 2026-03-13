<template>
  <div class="processes">
    <el-card>
      <div class="toolbar">
        <el-button type="primary" @click="showCreateDialog = true">
          <el-icon><Plus /></el-icon>
          新建工序
        </el-button>
      </div>

      <el-table :data="tableData" stripe>
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="code" label="工序代码" width="120" />
        <el-table-column prop="name" label="工序名称" width="150" />
        <el-table-column prop="description" label="工序描述" />
        <el-table-column label="操作" fixed="right" width="150">
          <template #default="{ row }">
            <el-button type="primary" link @click="handleEdit(row)">编辑</el-button>
            <el-button type="danger" link @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog v-model="showCreateDialog" :title="editMode ? '编辑工序' : '新建工序'" width="500px">
      <el-form :model="form" label-width="100px">
        <el-form-item label="工序代码">
          <el-input v-model="form.code" placeholder="如：WB001" />
        </el-form-item>
        <el-form-item label="工序名称">
          <el-input v-model="form.name" placeholder="如：电路板焊接" />
        </el-form-item>
        <el-form-item label="工序描述">
          <el-input v-model="form.description" type="textarea" :rows="3" />
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
  code: '',
  name: '',
  description: ''
})

const tableData = ref([
  { id: 1, code: 'WB001', name: '电路板焊接', description: 'PCB 板元器件焊接' },
  { id: 2, code: 'ZP001', name: '组装', description: '产品整机组装' },
  { id: 3, code: 'CS001', name: '测试', description: '产品功能测试' },
  { id: 4, code: 'LH001', name: '老化', description: '产品老化测试' },
  { id: 5, code: 'BZ001', name: '包装', description: '产品包装' }
])

const handleEdit = (row) => {
  editMode.value = true
  Object.assign(form, row)
  showCreateDialog.value = true
}

const handleDelete = (row) => {
  ElMessage.success('删除成功')
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
