<template>
  <div class="reports">
    <el-row :gutter="20">
      <el-col :span="12">
        <el-card>
          <template #header>
            <span>工时统计</span>
          </template>
          <el-form :inline="true" size="small">
            <el-form-item label="开始日期">
              <el-date-picker v-model="dateRange.start" type="date" placeholder="选择日期" />
            </el-form-item>
            <el-form-item label="结束日期">
              <el-date-picker v-model="dateRange.end" type="date" placeholder="选择日期" />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="handleQuery">查询</el-button>
            </el-form-item>
          </el-form>
          <div ref="workTimeChart" style="height: 300px; margin-top: 20px"></div>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card>
          <template #header>
            <span>产量统计</span>
          </template>
          <div ref="outputChart" style="height: 300px"></div>
        </el-card>
      </el-col>
    </el-row>

    <el-card style="margin-top: 20px">
      <template #header>
        <span>员工效率排行</span>
      </template>
      <el-table :data="employeeRanking" stripe>
        <el-table-column prop="rank" label="排名" width="80" />
        <el-table-column prop="name" label="员工" width="120" />
        <el-table-column prop="department" label="部门" width="120" />
        <el-table-column prop="completedQty" label="完成数量" width="100" />
        <el-table-column prop="efficiency" label="效率" width="100">
          <template #default="{ row }">
            <el-tag :type="row.efficiency > 100 ? 'success' : 'primary'">{{ row.efficiency }}%</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="workHours" label="工时" width="100" />
      </el-table>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import * as echarts from 'echarts'

const dateRange = reactive({
  start: new Date(),
  end: new Date()
})

const workTimeChart = ref()
const outputChart = ref()

const employeeRanking = ref([
  { rank: 1, name: '张三', department: '焊接组', completedQty: 1250, efficiency: 125, workHours: 168 },
  { rank: 2, name: '李四', department: '组装组', completedQty: 1180, efficiency: 118, workHours: 168 },
  { rank: 3, name: '王五', department: '测试组', completedQty: 1100, efficiency: 110, workHours: 168 },
  { rank: 4, name: '赵六', department: '焊接组', completedQty: 1050, efficiency: 105, workHours: 168 },
  { rank: 5, name: '钱七', department: '包装组', completedQty: 980, efficiency: 98, workHours: 168 }
])

const handleQuery = () => {
  // 查询逻辑
}

onMounted(() => {
  // 工时统计柱状图
  const workTime = echarts.init(workTimeChart.value)
  workTime.setOption({
    tooltip: { trigger: 'axis' },
    xAxis: {
      type: 'category',
      data: ['焊接组', '组装组', '测试组', '老化组', '包装组']
    },
    yAxis: { type: 'value', name: '工时' },
    series: [{
      data: [420, 380, 350, 280, 320],
      type: 'bar',
      itemStyle: { color: '#409EFF' }
    }]
  })

  // 产量统计饼图
  const output = echarts.init(outputChart.value)
  output.setOption({
    tooltip: { trigger: 'item' },
    legend: { top: '5%', left: 'center' },
    series: [{
      name: '产量',
      type: 'pie',
      radius: ['40%', '70%'],
      data: [
        { value: 1048, name: 'ZE750-9Z' },
        { value: 735, name: 'ZE750-9HL' },
        { value: 580, name: 'ZE750-9H' },
        { value: 484, name: 'ZE750-9E' },
        { value: 300, name: '其他' }
      ]
    }]
  })

  window.addEventListener('resize', () => {
    workTime.resize()
    output.resize()
  })
})
</script>

<style scoped>
</style>
