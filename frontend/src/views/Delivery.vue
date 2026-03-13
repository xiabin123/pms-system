<template>
  <div class="delivery">
    <el-card>
      <template #header>
        <span>📦 发货管理</span>
      </template>

      <el-alert type="info" :closable="false" style="margin-bottom: 20px">
        管理成品工单的发货流程：核对 → 装箱 → 物流登记
      </el-alert>

      <el-table :data="deliveryOrders" stripe>
        <el-table-column prop="order_number" label="发货单号" width="150" />
        <el-table-column prop="work_order" label="关联工单" width="150" />
        <el-table-column prop="product" label="产品信息" width="200" />
        <el-table-column prop="recipient" label="收货人" width="120" />
        <el-table-column prop="address" label="收货地址" min-width="200" />
        <el-table-column prop="logistics" label="物流信息" width="180" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.status === '已发货' ? 'success' : 'warning'">{{ row.status }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="150" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" link size="small" @click="handleShip(row)">发货</el-button>
            <el-button type="info" link size="small">详情</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'

const deliveryOrders = ref([
  { order_number: 'FH20250115001', work_order: 'WO20250115003', product: 'ZEF650-4PC40 × 200', recipient: '张三', address: '上海市浦东新区', logistics: '-', status: '待发货' },
  { order_number: 'FH20250115002', work_order: 'WO20250115004', product: 'ZE750-9Z × 100', recipient: '李四', address: '北京市朝阳区', logistics: '顺丰 SF1234567890', status: '已发货' }
])

const handleShip = (row) => {
  ElMessage.success('发货成功')
}
</script>
