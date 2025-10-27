<template>
  <div class="min-h-screen bg-gray-50 flex items-center justify-center p-4">
    <div class="max-w-md w-full">
      <!-- 로고 및 제목 -->
      <div class="text-center mb-8">
        <div class="w-16 h-16 bg-blue-500 rounded-3xl flex items-center justify-center text-3xl mx-auto mb-6 shadow-lg">
          🏢
        </div>
        <h1 class="text-2xl font-bold text-gray-900 mb-2">예산 관리 시스템</h1>
        <p class="text-gray-500 text-sm">{{ isRegistering ? '새 계정을 만들어보세요' : '계정에 로그인하세요' }}</p>
      </div>

      <!-- 로그인/회원가입 폼 -->
      <div class="bg-white rounded-3xl p-8 shadow-lg border border-gray-100">
        <!-- 탭 전환 -->
        <div class="flex mb-8 bg-gray-50 rounded-2xl p-1">
          <button type="button" @click="isRegistering = false"
            class="flex-1 py-3 px-4 rounded-xl text-sm font-semibold transition-all"
            :class="!isRegistering ? 'bg-white text-blue-600 shadow-sm' : 'text-gray-500 hover:text-gray-700'">
            로그인
          </button>
          <button type="button" @click="isRegistering = true"
            class="flex-1 py-3 px-4 rounded-xl text-sm font-semibold transition-all"
            :class="isRegistering ? 'bg-white text-blue-600 shadow-sm' : 'text-gray-500 hover:text-gray-700'">
            회원가입
          </button>
        </div>

        <!-- 로그인 폼 -->
        <form v-if="!isRegistering" @submit.prevent="handleLogin" class="space-y-6">
          <!-- 이메일 입력 -->
          <div>
            <label for="email" class="block text-sm font-medium text-gray-700 mb-2">
              이메일
            </label>
            <input id="email" v-model="loginForm.email" type="email" required class="input-field"
              placeholder="이메일을 입력하세요" />
          </div>

          <!-- 비밀번호 입력 -->
          <div>
            <label for="password" class="block text-sm font-medium text-gray-700 mb-2">
              비밀번호
            </label>
            <div class="relative">
              <input id="password" v-model="loginForm.password" :type="showPassword ? 'text' : 'password'" required
                class="input-field pr-12" placeholder="비밀번호를 입력하세요" />
              <button type="button" @click="showPassword = !showPassword"
                class="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600 transition-colors duration-200">
                <span v-if="showPassword" class="text-xl">👁️</span>
                <span v-else class="text-xl">👁️‍🗨️</span>
              </button>
            </div>
          </div>

          <!-- 로그인 유지 -->
          <div class="flex items-center">
            <input id="remember" v-model="loginForm.remember" type="checkbox"
              class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded" />
            <label for="remember" class="ml-2 block text-sm text-gray-700">
              로그인 상태 유지
            </label>
          </div>

          <!-- 로그인 버튼 -->
          <button type="submit" :disabled="isLoading" class="w-full btn-primary flex items-center justify-center gap-2"
            :class="{ 'opacity-50 cursor-not-allowed': isLoading }">
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

        <!-- 회원가입 폼 -->
        <form v-else @submit.prevent="handleRegister" class="space-y-6">
          <!-- 이름 입력 -->
          <div>
            <label for="register-name" class="block text-sm font-medium text-gray-700 mb-2">
              이름
            </label>
            <input id="register-name" v-model="registerForm.name" type="text" required class="input-field"
              placeholder="이름을 입력하세요" />
          </div>

          <!-- 이메일 입력 -->
          <div>
            <label for="register-email" class="block text-sm font-medium text-gray-700 mb-2">
              이메일
            </label>
            <input id="register-email" v-model="registerForm.email" type="email" required class="input-field"
              placeholder="이메일을 입력하세요" />
          </div>

          <!-- 비밀번호 입력 -->
          <div>
            <label for="register-password" class="block text-sm font-medium text-gray-700 mb-2">
              비밀번호
            </label>
            <input id="register-password" v-model="registerForm.password" type="password" required class="input-field"
              placeholder="비밀번호를 입력하세요" />
          </div>

          <!-- 비밀번호 확인 -->
          <div>
            <label for="register-password-confirm" class="block text-sm font-medium text-gray-700 mb-2">
              비밀번호 확인
            </label>
            <input id="register-password-confirm" v-model="registerForm.passwordConfirm" type="password" required
              class="input-field" placeholder="비밀번호를 다시 입력하세요" />
          </div>

          <!-- 회원가입 버튼 -->
          <button type="submit" :disabled="isLoading" class="w-full btn-primary flex items-center justify-center gap-2"
            :class="{ 'opacity-50 cursor-not-allowed': isLoading }">
            <span v-if="isLoading" class="animate-spin">⏳</span>
            <span v-else>✨</span>
            {{ isLoading ? '가입 중...' : '회원가입' }}
          </button>

          <!-- 오류 메시지 -->
          <div v-if="errorMessage" class="bg-red-50 border border-red-200 rounded-lg p-4">
            <div class="flex items-center gap-2">
              <span class="text-red-500">⚠️</span>
              <p class="text-red-700 text-sm">{{ errorMessage }}</p>
            </div>
          </div>

          <!-- 성공 메시지 -->
          <div v-if="successMessage" class="bg-green-50 border border-green-200 rounded-lg p-4">
            <div class="flex items-center gap-2">
              <span class="text-green-500">✅</span>
              <p class="text-green-700 text-sm">{{ successMessage }}</p>
            </div>
          </div>
        </form>

        <!-- 데모 계정 정보 (로그인 탭일 때만 표시) -->
        <div v-if="!isRegistering" class="mt-6 p-4 bg-blue-50 rounded-lg">
          <h3 class="text-sm font-medium text-blue-900 mb-2">테스트 계정</h3>
          <div class="text-xs text-blue-700 space-y-1">
            <p><strong>이메일:</strong> test@example.com</p>
            <p><strong>비밀번호:</strong> password123</p>
            <p class="text-blue-600 mt-2">※ 백엔드 API와 연동되어 있습니다</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive } from 'vue'
import { authAPI } from '../api/auth'

export default {
  name: 'Login',
  emits: ['login-success'],
  setup(props, { emit }) {
    const isRegistering = ref(false)

    const loginForm = reactive({
      email: '',
      password: '',
      remember: false
    })

    const registerForm = reactive({
      name: '',
      email: '',
      password: '',
      passwordConfirm: ''
    })

    const showPassword = ref(false)
    const isLoading = ref(false)
    const errorMessage = ref('')
    const successMessage = ref('')

    const handleLogin = async () => {
      isLoading.value = true
      errorMessage.value = ''

      try {
        // 백엔드 API 호출
        const result = await authAPI.login(loginForm.email, loginForm.password)

        if (!result.success) {
          errorMessage.value = result.error
          return
        }

        // JWT 토큰 저장
        localStorage.setItem('access_token', result.data.access_token)
        localStorage.setItem('isLoggedIn', 'true')

        // 사용자 정보 조회
        const userResult = await authAPI.getCurrentUser()

        if (userResult.success) {
          const userInfo = {
            ...userResult.data,
            loginTime: new Date().toISOString(),
            remember: loginForm.remember
          }

          // 로컬 스토리지에 사용자 정보 저장
          localStorage.setItem('userInfo', JSON.stringify(userInfo))

          // 부모 컴포넌트에 로그인 성공 알림
          emit('login-success', userInfo)
        } else {
          errorMessage.value = '사용자 정보를 가져오는데 실패했습니다.'
        }

      } catch (error) {
        errorMessage.value = '로그인 중 오류가 발생했습니다.'
      } finally {
        isLoading.value = false
      }
    }

    const handleRegister = async () => {
      isLoading.value = true
      errorMessage.value = ''
      successMessage.value = ''

      try {
        // 비밀번호 확인
        if (registerForm.password !== registerForm.passwordConfirm) {
          errorMessage.value = '비밀번호가 일치하지 않습니다.'
          return
        }

        // 백엔드 API 호출
        const result = await authAPI.register({
          name: registerForm.name,
          email: registerForm.email,
          password: registerForm.password
        })

        if (!result.success) {
          errorMessage.value = result.error
          return
        }

        // 회원가입 성공
        successMessage.value = '회원가입이 완료되었습니다. 로그인 해주세요.'

        // 폼 초기화
        registerForm.name = ''
        registerForm.email = ''
        registerForm.password = ''
        registerForm.passwordConfirm = ''

        // 3초 후 로그인 탭으로 전환
        setTimeout(() => {
          isRegistering.value = false
          successMessage.value = ''
        }, 3000)

      } catch (error) {
        errorMessage.value = '회원가입 중 오류가 발생했습니다.'
      } finally {
        isLoading.value = false
      }
    }

    return {
      isRegistering,
      loginForm,
      registerForm,
      showPassword,
      isLoading,
      errorMessage,
      successMessage,
      handleLogin,
      handleRegister
    }
  }
}
</script>
