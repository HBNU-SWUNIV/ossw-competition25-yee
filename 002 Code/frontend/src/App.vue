<template>
  <!-- 로그인 화면 -->
  <Login v-if="!isLoggedIn" @login-success="handleLoginSuccess" />

  <!-- 메인 애플리케이션 -->
  <div v-else id="app" class="min-h-screen bg-gray-50">
    <!-- 햄버거 메뉴 버튼 -->
    <button
      class="fixed top-6 left-6 z-50 bg-white hover:bg-gray-50 text-gray-700 w-12 h-12 rounded-2xl flex flex-col justify-center items-center gap-1 transition-all duration-300 shadow-medium border border-gray-200"
      @click="toggleSidebar" :class="{ 'active': sidebarOpen }">
      <span class="w-5 h-0.5 bg-gray-600 rounded transition-all duration-300"
        :class="{ 'rotate-45 translate-y-1.5': sidebarOpen }"></span>
      <span class="w-5 h-0.5 bg-gray-600 rounded transition-all duration-300"
        :class="{ 'opacity-0': sidebarOpen }"></span>
      <span class="w-5 h-0.5 bg-gray-600 rounded transition-all duration-300"
        :class="{ '-rotate-45 -translate-y-1.5': sidebarOpen }"></span>
    </button>

    <!-- 사이드바 오버레이 -->
    <div v-if="sidebarOpen" class="fixed inset-0 bg-black bg-opacity-50 z-40 transition-opacity duration-300"
      @click="closeSidebar"></div>

    <!-- 사이드바 -->
    <nav
      class="fixed top-0 left-0 h-full w-80 bg-white shadow-toss z-50 sidebar-transition transform border-r border-gray-100 flex flex-col"
      :class="sidebarOpen ? 'translate-x-0' : '-translate-x-full'">
      <div class="flex items-center justify-between p-6 border-b border-gray-100 flex-shrink-0">
        <h2 class="text-lg font-bold leading-tight" style="color: #3e56f6;">Budgetly</h2>
        <button
          class="w-10 h-10 flex items-center justify-center rounded-2xl hover:bg-gray-100 transition-colors duration-200"
          @click="closeSidebar">
          <span class="text-xl text-gray-400">&times;</span>
        </button>
      </div>

      <div class="flex-1 overflow-y-auto">
        <ul class="px-4 py-2 space-y-1">
          <li>
            <a href="#" @click="selectMenu('home')"
              class="flex items-center px-4 py-3 text-gray-700 hover:bg-gray-50 rounded-2xl transition-all duration-200"
              :class="{ 'bg-blue-50 text-blue-600 font-semibold': activeMenu === 'home' }">
              <span class="font-medium">홈</span>
            </a>
          </li>
          <li>
            <a href="#" @click="selectMenu('budget')"
              class="flex items-center px-4 py-3 text-gray-700 hover:bg-gray-50 rounded-2xl transition-all duration-200"
              :class="{ 'bg-blue-50 text-blue-600 font-semibold': activeMenu === 'budget' }">
              <span class="font-medium">예산관리</span>
            </a>
          </li>
          <li>
            <a href="#" @click="selectMenu('expenses')"
              class="flex items-center px-4 py-3 text-gray-700 hover:bg-gray-50 rounded-2xl transition-all duration-200"
              :class="{ 'bg-blue-50 text-blue-600 font-semibold': activeMenu === 'expenses' }">
              <span class="font-medium">지출내역</span>
            </a>
          </li>
          <li>
            <a href="#" @click="selectMenu('reports')"
              class="flex items-center px-4 py-3 text-gray-700 hover:bg-gray-50 rounded-2xl transition-all duration-200"
              :class="{ 'bg-blue-50 text-blue-600 font-semibold': activeMenu === 'reports' }">
              <span class="font-medium">리포트</span>
            </a>
          </li>
          <li>
            <a href="#" @click="selectMenu('departments')"
              class="flex items-center px-4 py-3 text-gray-700 hover:bg-gray-50 rounded-2xl transition-all duration-200"
              :class="{ 'bg-blue-50 text-blue-600 font-semibold': activeMenu === 'departments' }">
              <span class="font-medium">자치기구 관리</span>
            </a>
          </li>
          <li>
            <a href="#" @click="selectMenu('settings')"
              class="flex items-center px-4 py-3 text-gray-700 hover:bg-gray-50 rounded-2xl transition-all duration-200"
              :class="{ 'bg-blue-50 text-blue-600 font-semibold': activeMenu === 'settings' }">
              <span class="font-medium">설정</span>
            </a>
          </li>
        </ul>
      </div>

      <!-- 사용자 정보 및 로그아웃 -->
      <div class="flex-shrink-0 p-4 border-t border-gray-100 bg-white">
        <div class="flex items-center justify-between p-4 bg-gray-50 rounded-2xl">
          <div class="flex-1">
            <p class="text-sm font-semibold text-gray-900">{{ userInfo?.name }}</p>
            <p class="text-xs text-gray-500">{{ userInfo?.role === 'admin' ? '관리자' : '사용자' }}</p>
          </div>
          <button @click="handleLogout"
            class="px-3 py-2 text-sm font-semibold text-gray-600 hover:text-gray-800 hover:bg-gray-200 rounded-xl transition-all duration-200">
            로그아웃
          </button>
        </div>
      </div>
    </nav>

    <!-- 메인 콘텐츠 -->
    <main class="min-h-screen transition-all duration-300" :class="{ 'ml-0': !sidebarOpen, 'lg:ml-80': sidebarOpen }">
      <div class="flex justify-center px-4 sm:px-6 lg:px-8 pt-20 sm:pt-24 pb-12">
        <div class="w-full max-w-6xl">
          <!-- 대시보드 메인 화면 -->
          <div v-if="activeMenu === 'home'" class="space-y-8">
            <!-- 환영 메시지 -->
            <div
              class="bg-gradient-to-br from-blue-500 to-blue-600 rounded-3xl p-8 text-white relative overflow-hidden">
              <div class="relative z-10">
                <h2 class="text-2xl font-bold mb-2">안녕하세요, {{ userInfo?.name }}님!</h2>
                <p class="text-blue-100 text-base opacity-90">효율적인 예산 관리를 시작해보세요</p>
              </div>
              <div class="absolute -bottom-4 -right-4 w-24 h-24 bg-white opacity-10 rounded-full"></div>
            </div>


            <!-- 빠른 액션 버튼 -->
            <div class="bg-white rounded-2xl p-6 border border-gray-100">
              <h3 class="text-lg font-bold text-gray-900 mb-6">빠른 작업</h3>
              <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
                <button @click="selectMenu('budget')"
                  class="flex flex-col items-center p-6 bg-gray-50 hover:bg-blue-50 rounded-2xl transition-all duration-200 border border-transparent hover:border-blue-200">
                  <p class="font-semibold text-gray-900 text-center">예산 등록</p>
                  <p class="text-xs text-gray-500 text-center mt-1">새 예산 계획 수립</p>
                </button>

                <button @click="selectMenu('expenses')"
                  class="flex flex-col items-center p-6 bg-gray-50 hover:bg-red-50 rounded-2xl transition-all duration-200 border border-transparent hover:border-red-200">
                  <p class="font-semibold text-gray-900 text-center">지출 추가</p>
                  <p class="text-xs text-gray-500 text-center mt-1">새 지출 내역 등록</p>
                </button>

                <button @click="selectMenu('reports')"
                  class="flex flex-col items-center p-6 bg-gray-50 hover:bg-green-50 rounded-2xl transition-all duration-200 border border-transparent hover:border-green-200">
                  <p class="font-semibold text-gray-900 text-center">리포트 보기</p>
                  <p class="text-xs text-gray-500 text-center mt-1">상세 분석 리포트</p>
                </button>

                <button @click="selectMenu('departments')"
                  class="flex flex-col items-center p-6 bg-gray-50 hover:bg-purple-50 rounded-2xl transition-all duration-200 border border-transparent hover:border-purple-200">
                  <p class="font-semibold text-gray-900 text-center">자치기구 관리</p>
                  <p class="text-xs text-gray-500 text-center mt-1">자치기구 정보 확인</p>
                </button>
              </div>
            </div>

            <!-- 시작하기 안내 -->
            <div class="bg-white rounded-2xl p-8 border border-gray-100 text-center">
              <h3 class="text-xl font-bold text-gray-900 mb-3">예산 관리를 시작해보세요</h3>
              <p class="text-gray-600 mb-6 max-w-md mx-auto">
                효율적인 예산 관리를 위해 먼저 예산을 등록하고 지출 내역을 추가해보세요.
              </p>
              <div class="flex flex-col sm:flex-row gap-3 justify-center">
                <button @click="selectMenu('budget')"
                  class="px-6 py-3 bg-blue-500 hover:bg-blue-600 text-white font-semibold rounded-xl transition-colors duration-200">
                  예산 등록하기
                </button>
                <button @click="selectMenu('expenses')"
                  class="px-6 py-3 bg-gray-100 hover:bg-gray-200 text-gray-700 font-semibold rounded-xl transition-colors duration-200">
                  지출 추가하기
                </button>
              </div>
            </div>
          </div>

          <!-- 사이드바 메뉴 선택 시 컴포넌트 표시 -->
          <component v-else :is="currentComponent" />
        </div>
      </div>
    </main>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import Login from './components/Login.vue'
import BudgetManagement from './components/BudgetManagement.vue'
import ExpenseHistory from './components/ExpenseHistory.vue'
import Reports from './components/Reports.vue'
import DepartmentManagement from './components/DepartmentManagement.vue'
import Settings from './components/Settings.vue'

export default {
  name: 'App',
  components: {
    Login,
    BudgetManagement,
    ExpenseHistory,
    Reports,
    DepartmentManagement,
    Settings
  },
  setup() {
    const sidebarOpen = ref(false)
    const activeMenu = ref('home')
    const isLoggedIn = ref(false)
    const userInfo = ref(null)

    const toggleSidebar = () => {
      sidebarOpen.value = !sidebarOpen.value
    }

    const closeSidebar = () => {
      sidebarOpen.value = false
    }

    const selectMenu = (menu) => {
      activeMenu.value = menu
      closeSidebar()
    }

    const getPageTitle = () => {
      const titles = {
        home: '홈',
        budget: '예산관리',
        expenses: '지출내역',
        reports: '리포트',
        departments: '자치기구 관리',
        settings: '설정'
      }
      return titles[activeMenu.value] || '홈'
    }

    const currentComponent = computed(() => {
      const components = {
        budget: 'BudgetManagement',
        expenses: 'ExpenseHistory',
        reports: 'Reports',
        departments: 'DepartmentManagement',
        settings: 'Settings'
      }
      return components[activeMenu.value] || 'BudgetManagement'
    })

    // 로그인 상태 확인
    const checkLoginStatus = () => {
      const storedLoginStatus = localStorage.getItem('isLoggedIn')
      const storedUserInfo = localStorage.getItem('userInfo')

      if (storedLoginStatus === 'true' && storedUserInfo) {
        isLoggedIn.value = true
        userInfo.value = JSON.parse(storedUserInfo)
      }
    }

    // 로그인 성공 처리
    const handleLoginSuccess = (user) => {
      isLoggedIn.value = true
      userInfo.value = user
      activeMenu.value = 'home'
      sidebarOpen.value = false
    }

    // 로그아웃 처리
    const handleLogout = () => {
      localStorage.removeItem('isLoggedIn')
      localStorage.removeItem('userInfo')
      isLoggedIn.value = false
      userInfo.value = null
      activeMenu.value = 'home'
      sidebarOpen.value = false
    }

    // 컴포넌트 마운트 시 로그인 상태 확인
    onMounted(() => {
      checkLoginStatus()
    })

    return {
      sidebarOpen,
      activeMenu,
      isLoggedIn,
      userInfo,
      toggleSidebar,
      closeSidebar,
      selectMenu,
      getPageTitle,
      currentComponent,
      handleLoginSuccess,
      handleLogout
    }
  }
}
</script>
