<template>
  <div class="materials">
    <el-card>
      <div class="toolbar">
        <el-form :inline="true">
          <el-form-item label="物料编号">
            <el-input v-model="searchForm.code" placeholder="请输入物料编号" clearable />
          </el-form-item>
          <el-form-item label="品名">
            <el-input v-model="searchForm.name" placeholder="请输入品名" clearable />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="handleSearch">查询</el-button>
            <el-button @click="resetSearch">重置</el-button>
          </el-form-item>
        </el-form>
        <div>
          <el-button type="success" @click="handleImport">
            <el-icon><Upload /></el-icon>
            导入 Excel
          </el-button>
          <el-button type="primary" @click="showCreateDialog = true">
            <el-icon><Plus /></el-icon>
            新建物料
          </el-button>
        </div>
      </div>

      <el-table :data="tableData" stripe v-loading="loading">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="code" label="物料编号" width="140" />
        <el-table-column prop="name" label="品名" width="150" />
        <el-table-column prop="specification" label="型号规格" />
        <el-table-column prop="createdAt" label="创建时间" width="160" />
        <el-table-column label="操作" fixed="right" width="150">
          <template #default="{ row }">
            <el-button type="primary" link @click="handleEdit(row)">编辑</el-button>
            <el-button type="danger" link @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination">
        <el-pagination
          v-model:current-page="pagination.page"
          v-model:page-size="pagination.pageSize"
          :total="pagination.total"
          :page-sizes="[20, 50, 100, 200]"
          layout="total, sizes, prev, pager, next"
        />
      </div>
    </el-card>

    <!-- 新建/编辑对话框 -->
    <el-dialog
      v-model="showCreateDialog"
      :title="editMode ? '编辑物料' : '新建物料'"
      width="500px"
    >
      <el-form :model="form" label-width="100px">
        <el-form-item label="物料编号">
          <el-input v-model="form.code" placeholder="如：B100000001" />
        </el-form-item>
        <el-form-item label="品名">
          <el-input v-model="form.name" placeholder="如：多功能表" />
        </el-form-item>
        <el-form-item label="型号规格">
          <el-input v-model="form.specification" placeholder="如：ZE750-9ZK4J2" />
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
import { ElMessage, ElMessageBox } from 'element-plus'

const loading = ref(false)
const showCreateDialog = ref(false)
const editMode = ref(false)

const searchForm = reactive({
  code: '',
  name: ''
})

const pagination = reactive({
  page: 1,
  pageSize: 20,
  total: 3487
})

const form = reactive({
  code: '',
  name: '',
  specification: ''
})

const tableData = ref([
  { id: 1, code: 'B100000001', name: '多功能表', specification: 'ZE750-9ZK4J2', createdAt: '2025-01-01' },
  { id: 2, code: 'B100000002', name: '多功能表', specification: 'ZE750-9EK4J2', createdAt: '2025-01-01' },
  { id: 3, code: 'B100000003', name: '多功能表', specification: 'ZE750-9HK4J2(T)', createdAt: '2025-01-01' },
  { id: 4, code: 'B100000004', name: '多功能表', specification: 'ZE750-7EK2J2', createdAt: '2025-01-01' },
  { id: 5, code: 'B100000005', name: '多功能表', specification: 'ZE750-7HK2J2', createdAt: '2025-01-01' }
])

const handleSearch = () => {
  ElMessage.info('查询功能待对接后端')
}

const resetSearch = () => {
  searchForm.code = ''
  searchForm.name = ''
}

const handleImport = async () => {
  try {
    await ElMessageBox.confirm('确定要从 Excel 导入物料数据吗？', '导入确认', { type: 'info' })
    ElMessage.success('导入成功！')
  } catch {
    // 取消
  }
}

const handleEdit = (row) => {
  editMode.value = true
  Object.assign(form, row)
  showCreateDialog.value = true
}

const handleDelete = (row) => {
  ElMessageBox.confirm(`确定删除物料 "${row.code}" 吗？`, '删除确认', { type: 'warning' })
    .then(() => {
      ElMessage.success('删除成功')
    })
    .catch(() => {})
}

const handleSubmit = () => {
  showCreateDialog.value = false
  ElMessage.success(editMode.value ? '更新成功' : '创建成功')
}
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
</style>
