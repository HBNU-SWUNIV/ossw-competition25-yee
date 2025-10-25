<template>
  <!-- 로그인 화면 -->
  <Login v-if="!isLoggedIn" @login-success="handleLoginSuccess" />

  <!-- 메인 애플리케이션 -->
  <div v-else id="app" class="min-h-screen bg-gray-50">
    <!-- 햄버거 메뉴 버튼 -->
    <button
      class="fixed top-5 left-5 z-50 bg-primary-600 hover:bg-primary-700 text-white w-11 h-11 rounded-lg flex flex-col justify-center items-center gap-1 transition-all duration-300 shadow-lg hover:shadow-xl"
      @click="toggleSidebar" :class="{ 'active': sidebarOpen }">
      <span class="w-6 h-0.5 bg-white rounded transition-all duration-300"
        :class="{ 'rotate-45 translate-y-1.5': sidebarOpen }"></span>
      <span class="w-6 h-0.5 bg-white rounded transition-all duration-300" :class="{ 'opacity-0': sidebarOpen }"></span>
      <span class="w-6 h-0.5 bg-white rounded transition-all duration-300"
        :class="{ '-rotate-45 -translate-y-1.5': sidebarOpen }"></span>
    </button>

    <!-- 사이드바 오버레이 -->
    <div v-if="sidebarOpen" class="fixed inset-0 bg-black bg-opacity-50 z-40 transition-opacity duration-300"
      @click="closeSidebar"></div>

    <!-- 사이드바 -->
    <nav class="fixed top-0 left-0 h-full w-80 bg-white shadow-strong z-50 sidebar-transition transform"
      :class="sidebarOpen ? 'translate-x-0' : '-translate-x-full'">
      <div class="flex items-center justify-between p-5 bg-primary-600 text-white border-b border-primary-700">
        <button @click="selectMenu('home')"
          class="flex items-center gap-3 hover:bg-white hover:bg-opacity-10 rounded-lg p-2 -m-2 transition-colors duration-200 cursor-pointer">
          <div class="w-12 h-12 bg-white bg-opacity-20 rounded-lg flex items-center justify-center text-2xl">
            🏢
          </div>
          <h2 class="text-lg font-semibold leading-tight">예산 관리 시스템</h2>
        </button>
        <button
          class="w-8 h-8 flex items-center justify-center rounded-lg hover:bg-white hover:bg-opacity-20 transition-colors duration-200"
          @click="closeSidebar">
          <span class="text-xl">&times;</span>
        </button>
      </div>

      <ul class="py-2">
        <li>
          <a href="#" @click="selectMenu('budget')"
            class="flex items-center gap-3 px-5 py-4 text-gray-700 hover:bg-gray-50 hover:text-primary-600 transition-colors duration-200"
            :class="{ 'bg-primary-50 text-primary-600 border-r-4 border-primary-600': activeMenu === 'budget' }">
            <span class="text-xl">💰</span>
            <span class="font-medium">예산관리</span>
          </a>
        </li>
        <li>
          <a href="#" @click="selectMenu('expenses')"
            class="flex items-center gap-3 px-5 py-4 text-gray-700 hover:bg-gray-50 hover:text-primary-600 transition-colors duration-200"
            :class="{ 'bg-primary-50 text-primary-600 border-r-4 border-primary-600': activeMenu === 'expenses' }">
            <span class="text-xl">📊</span>
            <span class="font-medium">지출내역</span>
          </a>
        </li>
        <li>
          <a href="#" @click="selectMenu('reports')"
            class="flex items-center gap-3 px-5 py-4 text-gray-700 hover:bg-gray-50 hover:text-primary-600 transition-colors duration-200"
            :class="{ 'bg-primary-50 text-primary-600 border-r-4 border-primary-600': activeMenu === 'reports' }">
            <span class="text-xl">📈</span>
            <span class="font-medium">리포트</span>
          </a>
        </li>
        <li>
          <a href="#" @click="selectMenu('departments')"
            class="flex items-center gap-3 px-5 py-4 text-gray-700 hover:bg-gray-50 hover:text-primary-600 transition-colors duration-200"
            :class="{ 'bg-primary-50 text-primary-600 border-r-4 border-primary-600': activeMenu === 'departments' }">
            <span class="text-xl">🏢</span>
            <span class="font-medium">부서관리</span>
          </a>
        </li>
        <li>
          <a href="#" @click="selectMenu('settings')"
            class="flex items-center gap-3 px-5 py-4 text-gray-700 hover:bg-gray-50 hover:text-primary-600 transition-colors duration-200"
            :class="{ 'bg-primary-50 text-primary-600 border-r-4 border-primary-600': activeMenu === 'settings' }">
            <span class="text-xl">⚙️</span>
            <span class="font-medium">설정</span>
          </a>
        </li>
      </ul>
    </nav>

    <!-- 메인 콘텐츠 -->
    <main class="min-h-screen transition-all duration-300" :class="{ 'ml-0': !sidebarOpen, 'lg:ml-80': sidebarOpen }">
      <header class="bg-white shadow-soft sticky top-0 z-30">
        <div class="pl-20 pr-4 sm:pl-24 sm:pr-6 lg:pr-8 py-6">
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-4">
              <button @click="selectMenu('home')"
                class="w-14 h-14 bg-gradient-to-br from-primary-600 to-primary-700 rounded-xl flex items-center justify-center text-3xl shadow-lg hover:shadow-xl hover:scale-105 transition-all duration-200 cursor-pointer">
                🏢
              </button>
              <h1 class="text-2xl sm:text-3xl font-bold text-gray-900">{{ getPageTitle() }}</h1>
            </div>

            <!-- 사용자 정보 및 로그아웃 -->
            <div class="flex items-center gap-4">
              <div class="text-right">
                <p class="text-sm font-medium text-gray-900">{{ userInfo?.name }}</p>
                <p class="text-xs text-gray-500">{{ userInfo?.role === 'admin' ? '관리자' : '사용자' }}</p>
              </div>
              <button @click="handleLogout"
                class="flex items-center gap-2 px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 hover:bg-gray-200 rounded-lg transition-colors duration-200">
                <span>🚪</span>
                로그아웃
              </button>
            </div>
          </div>
        </div>
      </header>

      <div class="px-4 sm:px-6 lg:px-8 py-8">
        <!-- 대시보드 메인 화면 -->
        <div v-if="activeMenu === 'home'" class="space-y-8">
          <!-- 환영 메시지 -->
          <div class="bg-gradient-to-r from-primary-600 to-primary-700 rounded-xl p-8 text-white">
            <div class="flex items-center justify-between">
              <div>
                <h2 class="text-3xl font-bold mb-2">안녕하세요, {{ userInfo?.name }}님!</h2>
                <p class="text-primary-100 text-lg">오늘도 효율적인 예산 관리를 시작해보세요.</p>
              </div>
              <div class="text-6xl opacity-20">🏢</div>
            </div>
          </div>

          <!-- 주요 통계 카드 -->
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <div class="bg-white rounded-xl p-6 shadow-soft hover:shadow-medium transition-shadow duration-300">
              <div class="flex items-center justify-between">
                <div>
                  <p class="text-sm font-medium text-gray-600">총 예산</p>
                  <p class="text-2xl font-bold text-gray-900">₩10,000,000</p>
                </div>
                <div class="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center text-2xl">💰</div>
              </div>
              <div class="mt-4">
                <div class="flex items-center text-sm text-green-600">
                  <span class="mr-1">↗</span>
                  <span>전월 대비 5% 증가</span>
                </div>
              </div>
            </div>

            <div class="bg-white rounded-xl p-6 shadow-soft hover:shadow-medium transition-shadow duration-300">
              <div class="flex items-center justify-between">
                <div>
                  <p class="text-sm font-medium text-gray-600">이번 달 지출</p>
                  <p class="text-2xl font-bold text-gray-900">₩3,250,000</p>
                </div>
                <div class="w-12 h-12 bg-red-100 rounded-lg flex items-center justify-center text-2xl">📊</div>
              </div>
              <div class="mt-4">
                <div class="flex items-center text-sm text-red-600">
                  <span class="mr-1">↗</span>
                  <span>예산의 32.5% 사용</span>
                </div>
              </div>
            </div>

            <div class="bg-white rounded-xl p-6 shadow-soft hover:shadow-medium transition-shadow duration-300">
              <div class="flex items-center justify-between">
                <div>
                  <p class="text-sm font-medium text-gray-600">절약 금액</p>
                  <p class="text-2xl font-bold text-gray-900">₩6,750,000</p>
                </div>
                <div class="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center text-2xl">📈</div>
              </div>
              <div class="mt-4">
                <div class="flex items-center text-sm text-green-600">
                  <span class="mr-1">↗</span>
                  <span>절약률 67.5%</span>
                </div>
              </div>
            </div>

            <div class="bg-white rounded-xl p-6 shadow-soft hover:shadow-medium transition-shadow duration-300">
              <div class="flex items-center justify-between">
                <div>
                  <p class="text-sm font-medium text-gray-600">활성 부서</p>
                  <p class="text-2xl font-bold text-gray-900">12개</p>
                </div>
                <div class="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center text-2xl">🏢</div>
              </div>
              <div class="mt-4">
                <div class="flex items-center text-sm text-gray-600">
                  <span class="mr-1">→</span>
                  <span>전체 부서 운영 중</span>
                </div>
              </div>
            </div>
          </div>

          <!-- 빠른 액션 버튼 -->
          <div class="bg-white rounded-xl p-6 shadow-soft">
            <h3 class="text-lg font-semibold text-gray-900 mb-4">빠른 작업</h3>
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
              <button @click="selectMenu('budget')"
                class="flex items-center gap-3 p-4 bg-blue-50 hover:bg-blue-100 rounded-lg transition-colors duration-200 text-left">
                <div class="w-10 h-10 bg-blue-500 rounded-lg flex items-center justify-center text-white text-lg">💰
                </div>
                <div>
                  <p class="font-medium text-gray-900">예산 등록</p>
                  <p class="text-sm text-gray-600">새 예산 계획 수립</p>
                </div>
              </button>

              <button @click="selectMenu('expenses')"
                class="flex items-center gap-3 p-4 bg-red-50 hover:bg-red-100 rounded-lg transition-colors duration-200 text-left">
                <div class="w-10 h-10 bg-red-500 rounded-lg flex items-center justify-center text-white text-lg">📊
                </div>
                <div>
                  <p class="font-medium text-gray-900">지출 추가</p>
                  <p class="text-sm text-gray-600">새 지출 내역 등록</p>
                </div>
              </button>

              <button @click="selectMenu('reports')"
                class="flex items-center gap-3 p-4 bg-green-50 hover:bg-green-100 rounded-lg transition-colors duration-200 text-left">
                <div class="w-10 h-10 bg-green-500 rounded-lg flex items-center justify-center text-white text-lg">📈
                </div>
                <div>
                  <p class="font-medium text-gray-900">리포트 보기</p>
                  <p class="text-sm text-gray-600">상세 분석 리포트</p>
                </div>
              </button>

              <button @click="selectMenu('departments')"
                class="flex items-center gap-3 p-4 bg-purple-50 hover:bg-purple-100 rounded-lg transition-colors duration-200 text-left">
                <div class="w-10 h-10 bg-purple-500 rounded-lg flex items-center justify-center text-white text-lg">🏢
                </div>
                <div>
                  <p class="font-medium text-gray-900">부서 관리</p>
                  <p class="text-sm text-gray-600">부서 정보 확인</p>
                </div>
              </button>
            </div>
          </div>

          <!-- 최근 활동 -->
          <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div class="bg-white rounded-xl p-6 shadow-soft">
              <h3 class="text-lg font-semibold text-gray-900 mb-4">최근 지출 내역</h3>
              <div class="space-y-3">
                <div class="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                  <div class="flex items-center gap-3">
                    <div class="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center text-sm">🖥️</div>
                    <div>
                      <p class="font-medium text-gray-900">사무용품 구매</p>
                      <p class="text-sm text-gray-600">2024-01-15</p>
                    </div>
                  </div>
                  <span class="font-semibold text-gray-900">₩150,000</span>
                </div>

                <div class="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                  <div class="flex items-center gap-3">
                    <div class="w-8 h-8 bg-green-100 rounded-full flex items-center justify-center text-sm">🍽️</div>
                    <div>
                      <p class="font-medium text-gray-900">회의 식사비</p>
                      <p class="text-sm text-gray-600">2024-01-14</p>
                    </div>
                  </div>
                  <span class="font-semibold text-gray-900">₩80,000</span>
                </div>

                <div class="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                  <div class="flex items-center gap-3">
                    <div class="w-8 h-8 bg-purple-100 rounded-full flex items-center justify-center text-sm">🚗</div>
                    <div>
                      <p class="font-medium text-gray-900">교통비</p>
                      <p class="text-sm text-gray-600">2024-01-13</p>
                    </div>
                  </div>
                  <span class="font-semibold text-gray-900">₩45,000</span>
                </div>
              </div>
            </div>

            <div class="bg-white rounded-xl p-6 shadow-soft">
              <h3 class="text-lg font-semibold text-gray-900 mb-4">부서별 예산 현황</h3>
              <div class="space-y-4">
                <div>
                  <div class="flex justify-between items-center mb-2">
                    <span class="text-sm font-medium text-gray-700">개발팀</span>
                    <span class="text-sm text-gray-600">75% 사용</span>
                  </div>
                  <div class="w-full bg-gray-200 rounded-full h-2">
                    <div class="bg-blue-500 h-2 rounded-full" style="width: 75%"></div>
                  </div>
                </div>

                <div>
                  <div class="flex justify-between items-center mb-2">
                    <span class="text-sm font-medium text-gray-700">마케팅팀</span>
                    <span class="text-sm text-gray-600">45% 사용</span>
                  </div>
                  <div class="w-full bg-gray-200 rounded-full h-2">
                    <div class="bg-green-500 h-2 rounded-full" style="width: 45%"></div>
                  </div>
                </div>

                <div>
                  <div class="flex justify-between items-center mb-2">
                    <span class="text-sm font-medium text-gray-700">인사팀</span>
                    <span class="text-sm text-gray-600">30% 사용</span>
                  </div>
                  <div class="w-full bg-gray-200 rounded-full h-2">
                    <div class="bg-yellow-500 h-2 rounded-full" style="width: 30%"></div>
                  </div>
                </div>

                <div>
                  <div class="flex justify-between items-center mb-2">
                    <span class="text-sm font-medium text-gray-700">총무팀</span>
                    <span class="text-sm text-gray-600">60% 사용</span>
                  </div>
                  <div class="w-full bg-gray-200 rounded-full h-2">
                    <div class="bg-purple-500 h-2 rounded-full" style="width: 60%"></div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 사이드바 메뉴 선택 시 컴포넌트 표시 -->
        <component v-else :is="currentComponent" />
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
        departments: '부서관리',
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
