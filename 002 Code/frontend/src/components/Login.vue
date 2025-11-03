<template>
  <div class="min-h-screen bg-gray-50 flex items-center justify-center p-4">
    <div class="max-w-md w-full">
      <!-- 로고 및 제목 -->
      <div class="text-center mb-8">

        <h1 class="text-5xl font-bold mb-2" style="color: #3e56f6;">Budgetly</h1>
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

          <!-- 학교 선택 -->
          <div>
            <label for="register-school" class="block text-sm font-medium text-gray-700 mb-2">
              학교
            </label>
            <select id="register-school" v-model="registerForm.school" @change="handleSchoolChange" class="input-field">
              <option value="">학교 선택</option>
              <option v-for="school in universities" :key="school" :value="school">
                {{ school }}
              </option>
            </select>
          </div>

          <!-- 학과 선택 -->
          <div>
            <label for="register-department" class="block text-sm font-medium text-gray-700 mb-2">
              학과
            </label>
            <select id="register-department" v-model="registerForm.department" class="input-field">
              <option value="">학과 선택</option>
              <option v-for="dept in departments" :key="dept" :value="dept">
                {{ dept }}
              </option>
            </select>
          </div>

          <!-- 조직 유형 선택 -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              조직 유형
            </label>
            <div class="flex gap-4">
              <label class="flex items-center">
                <input type="radio" v-model="registerForm.organizationType" value="자치기구"
                  class="mr-2 text-primary-600 focus:ring-primary-500" />
                <span class="text-sm text-gray-700">자치기구</span>
              </label>
              <label class="flex items-center">
                <input type="radio" v-model="registerForm.organizationType" value="학생회"
                  class="mr-2 text-primary-600 focus:ring-primary-500" />
                <span class="text-sm text-gray-700">학생회</span>
              </label>
            </div>
          </div>

          <!-- 자치기구 세부 유형 선택 -->
          <div v-if="registerForm.organizationType === '자치기구'">
            <label class="block text-sm font-medium text-gray-700 mb-2">
              자치기구 유형
            </label>
            <div class="flex gap-4">
              <label class="flex items-center">
                <input type="radio" v-model="registerForm.organizationSubType" value="총동아리연합회"
                  class="mr-2 text-primary-600 focus:ring-primary-500" />
                <span class="text-sm text-gray-700">총동아리연합회</span>
              </label>
              <label class="flex items-center">
                <input type="radio" v-model="registerForm.organizationSubType" value="총학생회"
                  class="mr-2 text-primary-600 focus:ring-primary-500" />
                <span class="text-sm text-gray-700">총학생회</span>
              </label>
            </div>
          </div>

          <!-- 조직 이름 입력 -->
          <div v-if="registerForm.organizationType">
            <label for="register-organization-name" class="block text-sm font-medium text-gray-700 mb-2">
              {{ registerForm.organizationType === '자치기구' ? '자치기구 이름' : '학생회 이름' }}
            </label>
            <input id="register-organization-name" v-model="registerForm.organizationName" type="text" 
              class="input-field"
              :placeholder="registerForm.organizationType === '자치기구' ? '자치기구 이름을 입력하세요 (예: 한밭대학교 총학생회)' : '학생회 이름을 입력하세요 (예: 컴퓨터공학과 학생회)'" />
          </div>

          <!-- 직책명 입력 -->
          <div>
            <label for="register-position" class="block text-sm font-medium text-gray-700 mb-2">
              직책명
            </label>
            <input id="register-position" v-model="registerForm.position" type="text" class="input-field"
              placeholder="직책명을 입력하세요 (예: 회장, 총무)" />
          </div>

          <!-- 회원가입 버튼 -->
          <button type="submit" :disabled="isLoading" class="w-full btn-primary flex items-center justify-center gap-2"
            :class="{ 'opacity-50 cursor-not-allowed': isLoading }">
            <span v-if="isLoading" class="animate-spin">⏳</span>
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


      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'
import { authAPI, dataAPI } from '../services/api'

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
      passwordConfirm: '',
      school: '',
      department: '',
      organizationType: '', // 자치기구 or 학생회
      organizationSubType: '', // 총동아리연합회 or 총학생회
      organizationName: '', // 조직 이름
      position: ''
    })

    const universities = ref([])
    const departments = ref([])
    const showPassword = ref(false)
    const isLoading = ref(false)
    const errorMessage = ref('')
    const successMessage = ref('')

    // 데이터 로드
    onMounted(async () => {
      try {
        const data = await dataAPI.getAll()
        universities.value = data.universities || []
        departments.value = data.departments || []
      } catch (error) {
        console.error('데이터 로드 실패:', error)
      }
    })

    // 학교 변경 시 해당 학교 학과 로드
    const handleSchoolChange = async () => {
      // 학과 선택 초기화
      registerForm.department = ''
      
      if (!registerForm.school) {
        // 학교가 선택되지 않았으면 기본 목록 유지
        try {
          const data = await dataAPI.getAll()
          departments.value = data.departments || []
        } catch (error) {
          console.error('데이터 로드 실패:', error)
        }
        return
      }

      // 선택된 학교의 학과 로드
      try {
        console.log('선택된 학교:', registerForm.school)
        const deptList = await dataAPI.getDepartments(registerForm.school)
        console.log('불러온 학과 목록:', deptList)
        departments.value = deptList
      } catch (error) {
        console.error('학과 로드 실패:', error)
        // 실패 시 기본 목록 유지
      }
    }

    const handleLogin = async () => {
      isLoading.value = true
      errorMessage.value = ''

      try {
        // 백엔드 API 호출
        const result = await authAPI.login(loginForm.email, loginForm.password)

        // JWT 토큰 저장
        localStorage.setItem('access_token', result.access_token)
        localStorage.setItem('isLoggedIn', 'true')

        // 사용자 정보 조회
        const userResult = await authAPI.getMe()

        const userInfo = {
          ...userResult,
          loginTime: new Date().toISOString(),
          remember: loginForm.remember
        }

        // 로컬 스토리지에 사용자 정보 저장
        localStorage.setItem('userInfo', JSON.stringify(userInfo))

        // 부모 컴포넌트에 로그인 성공 알림
        emit('login-success', userInfo)

      } catch (error) {
        errorMessage.value = error.message || '로그인 중 오류가 발생했습니다.'
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
        const registerData = {
          name: registerForm.name,
          email: registerForm.email,
          password: registerForm.password
        }
        
        // 선택 입력된 경우에만 추가
        if (registerForm.school) {
          registerData.school = registerForm.school
        }
        if (registerForm.department) {
          registerData.department = registerForm.department
        }
        if (registerForm.organizationType) {
          registerData.organizationType = registerForm.organizationType
        }
        if (registerForm.organizationSubType) {
          registerData.organizationSubType = registerForm.organizationSubType
        }
        if (registerForm.organizationName) {
          registerData.organizationName = registerForm.organizationName
        }
        if (registerForm.position) {
          registerData.position = registerForm.position
        }
        
        await authAPI.register(registerData)

        // 회원가입 성공
        successMessage.value = '회원가입이 완료되었습니다. 로그인 해주세요.'

        // 폼 초기화
        registerForm.name = ''
        registerForm.email = ''
        registerForm.password = ''
        registerForm.passwordConfirm = ''
        registerForm.school = ''
        registerForm.department = ''
        registerForm.organizationType = ''
        registerForm.organizationSubType = ''
        registerForm.organizationName = ''
        registerForm.position = ''

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
      universities,
      departments,
      showPassword,
      isLoading,
      errorMessage,
      successMessage,
      handleLogin,
      handleRegister,
      handleSchoolChange
    }
  }
}
</script>
