<template>
  <div class="login-container">
    <div class="login-box">
      <div class="login-header">
        <el-icon :size="48"><Monitor /></el-icon>
        <h1>PMS 生产管理系统</h1>
        <p>生产工单流程管理平台</p>
      </div>
      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="80px"
      >
        <el-form-item label="用户名" prop="username">
          <el-input
            v-model="form.username"
            placeholder="请输入用户名"
            prefix-icon="User"
            size="large"
          />
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input
            v-model="form.password"
            type="password"
            placeholder="请输入密码"
            prefix-icon="Lock"
            size="large"
            show-password
            @keyup.enter="handleLogin"
          />
        </el-form-item>
        <el-form-item>
          <el-button
            type="primary"
            size="large"
            :loading="loading"
            @click="handleLogin"
            style="width: 100%"
          >
            登录
          </el-button>
        </el-form-item>
      </el-form>
      
      <div class="login-tip">
        <p style="margin-bottom: 8px">📋 测试账号：</p>
        <el-descriptions :column="2" size="small" border>
          <el-descriptions-item label="管理员">admin / admin123</el-descriptions-item>
          <el-descriptions-item label="计划员">plan001 / 123456</el-descriptions-item>
          <el-descriptions-item label="焊接工">hb001 / 123456</el-descriptions-item>
          <el-descriptions-item label="装配工">zp001 / 123456</el-descriptions-item>
          <el-descriptions-item label="调试工">cs001 / 123456</el-descriptions-item>
          <el-descriptions-item label="检验员">jy001 / 123456</el-descriptions-item>
          <el-descriptions-item label="发货员">fh001 / 123456</el-descriptions-item>
          <el-descriptions-item label="售后员">sh001 / 123456</el-descriptions-item>
        </el-descriptions>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import axios from 'axios'

const router = useRouter()
const formRef = ref()
const loading = ref(false)

const form = reactive({
  username: 'admin',
  password: 'admin123'
})

const rules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }]
}

const handleLogin = async () => {
  await formRef.value.validate()
  loading.value = true
  
  try {
    const response = await axios.post('/api/auth/login', {
      username: form.username,
      password: form.password
    })
    
    const { token, user } = response.data
    localStorage.setItem('token', token)
    localStorage.setItem('user', JSON.stringify(user))
    
    ElMessage.success(`欢迎，${user.real_name}！`)
    router.push('/')
  } catch (error) {
    console.error('Login failed:', error)
    ElMessage.error(error.response?.data?.detail || '登录失败，请检查用户名和密码')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.login-box {
  width: 500px;
  padding: 40px;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

.login-header {
  text-align: center;
  margin-bottom: 30px;
}

.login-header h1 {
  margin-top: 10px;
  font-size: 26px;
  color: #304156;
}

.login-header p {
  color: #909399;
  font-size: 14px;
  margin-top: 8px;
}

.login-tip {
  margin-top: 20px;
  padding: 15px;
  background: #f5f7fa;
  border-radius: 6px;
  font-size: 12px;
}

.login-tip p {
  color: #606266;
  font-weight: bold;
  margin: 0 0 8px 0;
}
</style>
