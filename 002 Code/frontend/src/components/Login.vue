<template>
  <div class="min-h-screen bg-gradient-to-br from-primary-50 to-primary-100 flex items-center justify-center p-4">
    <div class="max-w-md w-full">
      <!-- 로고 및 제목 -->
      <div class="text-center mb-8">
        <div class="w-20 h-20 bg-gradient-to-br from-primary-600 to-primary-700 rounded-2xl flex items-center justify-center text-4xl mx-auto mb-4 shadow-lg">
          🏢
        </div>
        <h1 class="text-3xl font-bold text-gray-900 mb-2">예산 관리 시스템</h1>
        <p class="text-gray-600">로그인하여 시스템에 접속하세요</p>
      </div>

      <!-- 로그인 폼 -->
      <div class="card p-8">
        <form @submit.prevent="handleLogin" class="space-y-6">
          <!-- 사용자명 입력 -->
          <div>
            <label for="username" class="block text-sm font-medium text-gray-700 mb-2">
              사용자명
            </label>
            <input
              id="username"
              v-model="loginForm.username"
              type="text"
              required
              class="input-field"
              placeholder="사용자명을 입력하세요"
            />
          </div>

          <!-- 비밀번호 입력 -->
          <div>
            <label for="password" class="block text-sm font-medium text-gray-700 mb-2">
              비밀번호
            </label>
            <div class="relative">
              <input
                id="password"
                v-model="loginForm.password"
                :type="showPassword ? 'text' : 'password'"
                required
                class="input-field pr-12"
                placeholder="비밀번호를 입력하세요"
              />
              <button
                type="button"
                @click="showPassword = !showPassword"
                class="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600 transition-colors duration-200"
              >
                <span v-if="showPassword" class="text-xl">👁️</span>
                <span v-else class="text-xl">👁️‍🗨️</span>
              </button>
            </div>
          </div>

          <!-- 로그인 유지 -->
          <div class="flex items-center">
            <input
              id="remember"
              v-model="loginForm.remember"
              type="checkbox"
              class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
            />
            <label for="remember" class="ml-2 block text-sm text-gray-700">
              로그인 상태 유지
            </label>
          </div>

          <!-- 로그인 버튼 -->
          <button
            type="submit"
            :disabled="isLoading"
            class="w-full btn-primary flex items-center justify-center gap-2"
            :class="{ 'opacity-50 cursor-not-allowed': isLoading }"
          >
            <span v-if="isLoading" class="animate-spin">⏳</span>
            <span v-else>🔐</span>
            {{ isLoading ? '로그인 중...' : '로그인' }}
          </button>

          <!-- 오류 메시지 -->
          <div v-if="errorMessage" class="bg-red-50 border border-red-200 rounded-lg p-4">
            <div class="flex items-center gap-2">
              <span class="text-red-500">⚠️</span>
              <p class="text-red-700 text-sm">{{ errorMessage }}</p>
            </div>
          </div>
        </form>

        <!-- 데모 계정 정보 -->
        <div class="mt-6 p-4 bg-blue-50 rounded-lg">
          <h3 class="text-sm font-medium text-blue-900 mb-2">테스트 계정</h3>
          <div class="text-xs text-blue-700 space-y-1">
            <p><strong>사용자명:</strong> user</p>
            <p><strong>비밀번호:</strong> 1234</p>
            <p class="text-blue-600 mt-2">※ Firebase 연결 후 실제 인증으로 변경됩니다</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive } from 'vue'
import { loginUser } from '../firebase/auth'

export default {
  name: 'Login',
  emits: ['login-success'],
  setup(props, { emit }) {
    const loginForm = reactive({
      username: '',
      password: '',
      remember: false
    })
    
    const showPassword = ref(false)
    const isLoading = ref(false)
    const errorMessage = ref('')


    const handleLogin = async () => {
      isLoading.value = true
      errorMessage.value = ''

      try {
        // Firebase 인증 함수 사용 (임시 구현)
        const result = await loginUser(loginForm.username, loginForm.password)
        
        if (!result.success) {
          errorMessage.value = result.error
          return
        }

        // 로그인 성공 - 사용자 정보 저장
        const userInfo = {
          username: loginForm.username,
          name: '사용자',
          email: 'user@company.com',
          role: 'user',
          loginTime: new Date().toISOString(),
          remember: loginForm.remember
        }

        // 로컬 스토리지에 저장
        localStorage.setItem('userInfo', JSON.stringify(userInfo))
        localStorage.setItem('isLoggedIn', 'true')

        // 부모 컴포넌트에 로그인 성공 알림
        emit('login-success', userInfo)

      } catch (error) {
        errorMessage.value = '로그인 중 오류가 발생했습니다.'
      } finally {
        isLoading.value = false
      }
    }

    return {
      loginForm,
      showPassword,
      isLoading,
      errorMessage,
      handleLogin
    }
  }
}
</script>
