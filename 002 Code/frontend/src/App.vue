<template>
  <div id="app" class="min-h-screen bg-gray-50">
    <!-- 햄버거 메뉴 버튼 -->
    <button 
      class="fixed top-5 left-5 z-50 bg-primary-600 hover:bg-primary-700 text-white w-11 h-11 rounded-lg flex flex-col justify-center items-center gap-1 transition-all duration-300 shadow-lg hover:shadow-xl"
      @click="toggleSidebar" 
      :class="{ 'active': sidebarOpen }"
    >
      <span class="w-6 h-0.5 bg-white rounded transition-all duration-300" :class="{ 'rotate-45 translate-y-1.5': sidebarOpen }"></span>
      <span class="w-6 h-0.5 bg-white rounded transition-all duration-300" :class="{ 'opacity-0': sidebarOpen }"></span>
      <span class="w-6 h-0.5 bg-white rounded transition-all duration-300" :class="{ '-rotate-45 -translate-y-1.5': sidebarOpen }"></span>
    </button>

    <!-- 사이드바 오버레이 -->
    <div 
      v-if="sidebarOpen" 
      class="fixed inset-0 bg-black bg-opacity-50 z-40 transition-opacity duration-300"
      @click="closeSidebar"
    ></div>

    <!-- 사이드바 -->
    <nav 
      class="fixed top-0 left-0 h-full w-80 bg-white shadow-strong z-50 sidebar-transition transform"
      :class="sidebarOpen ? 'translate-x-0' : '-translate-x-full'"
    >
      <div class="flex items-center justify-between p-5 bg-primary-600 text-white border-b border-primary-700">
        <div class="flex items-center gap-3">
          <div class="w-12 h-12 bg-white bg-opacity-20 rounded-lg flex items-center justify-center text-2xl">
            🏢
          </div>
          <h2 class="text-lg font-semibold leading-tight">예산 관리 시스템</h2>
        </div>
        <button 
          class="w-8 h-8 flex items-center justify-center rounded-lg hover:bg-white hover:bg-opacity-20 transition-colors duration-200"
          @click="closeSidebar"
        >
          <span class="text-xl">&times;</span>
        </button>
      </div>
      
      <ul class="py-2">
        <li>
          <a 
            href="#" 
            @click="selectMenu('budget')" 
            class="flex items-center gap-3 px-5 py-4 text-gray-700 hover:bg-gray-50 hover:text-primary-600 transition-colors duration-200"
            :class="{ 'bg-primary-50 text-primary-600 border-r-4 border-primary-600': activeMenu === 'budget' }"
          >
            <span class="text-xl">💰</span>
            <span class="font-medium">예산관리</span>
          </a>
        </li>
        <li>
          <a 
            href="#" 
            @click="selectMenu('expenses')" 
            class="flex items-center gap-3 px-5 py-4 text-gray-700 hover:bg-gray-50 hover:text-primary-600 transition-colors duration-200"
            :class="{ 'bg-primary-50 text-primary-600 border-r-4 border-primary-600': activeMenu === 'expenses' }"
          >
            <span class="text-xl">📊</span>
            <span class="font-medium">지출내역</span>
          </a>
        </li>
        <li>
          <a 
            href="#" 
            @click="selectMenu('reports')" 
            class="flex items-center gap-3 px-5 py-4 text-gray-700 hover:bg-gray-50 hover:text-primary-600 transition-colors duration-200"
            :class="{ 'bg-primary-50 text-primary-600 border-r-4 border-primary-600': activeMenu === 'reports' }"
          >
            <span class="text-xl">📈</span>
            <span class="font-medium">리포트</span>
          </a>
        </li>
        <li>
          <a 
            href="#" 
            @click="selectMenu('departments')" 
            class="flex items-center gap-3 px-5 py-4 text-gray-700 hover:bg-gray-50 hover:text-primary-600 transition-colors duration-200"
            :class="{ 'bg-primary-50 text-primary-600 border-r-4 border-primary-600': activeMenu === 'departments' }"
          >
            <span class="text-xl">🏢</span>
            <span class="font-medium">부서관리</span>
          </a>
        </li>
        <li>
          <a 
            href="#" 
            @click="selectMenu('settings')" 
            class="flex items-center gap-3 px-5 py-4 text-gray-700 hover:bg-gray-50 hover:text-primary-600 transition-colors duration-200"
            :class="{ 'bg-primary-50 text-primary-600 border-r-4 border-primary-600': activeMenu === 'settings' }"
          >
            <span class="text-xl">⚙️</span>
            <span class="font-medium">설정</span>
          </a>
        </li>
      </ul>
    </nav>

    <!-- 메인 콘텐츠 -->
    <main class="min-h-screen transition-all duration-300" :class="{ 'ml-0': !sidebarOpen, 'lg:ml-80': sidebarOpen }">
      <header class="bg-white shadow-soft sticky top-0 z-30">
        <div class="px-4 sm:px-6 lg:px-8 py-6">
          <div class="flex items-center gap-4">
            <div class="w-14 h-14 bg-gradient-to-br from-primary-600 to-primary-700 rounded-xl flex items-center justify-center text-3xl shadow-lg">
              🏢
            </div>
            <h1 class="text-2xl sm:text-3xl font-bold text-gray-900">{{ getPageTitle() }}</h1>
          </div>
        </div>
      </header>
      
      <div class="px-4 sm:px-6 lg:px-8 py-8">
        <!-- 기본 메인 화면 -->
        <div v-if="activeMenu === 'home'" class="flex justify-center items-center min-h-[60vh]">
          <div class="card p-8 sm:p-12 max-w-lg w-full text-center">
            <div class="text-6xl mb-6">🏢</div>
            <h2 class="text-3xl sm:text-4xl font-bold text-gray-900 mb-4">예산 관리 시스템</h2>
            <p class="text-lg text-gray-600 leading-relaxed">사이드바 메뉴를 클릭하여 원하는 기능을 이용하세요.</p>
          </div>
        </div>
        
        <!-- 사이드바 메뉴 선택 시 컴포넌트 표시 -->
        <component v-else :is="currentComponent" />
      </div>
    </main>
  </div>
</template>

<script>
import { ref, computed } from 'vue'
import BudgetManagement from './components/BudgetManagement.vue'
import ExpenseHistory from './components/ExpenseHistory.vue'
import Reports from './components/Reports.vue'
import DepartmentManagement from './components/DepartmentManagement.vue'
import Settings from './components/Settings.vue'

export default {
  name: 'App',
  components: {
    BudgetManagement,
    ExpenseHistory,
    Reports,
    DepartmentManagement,
    Settings
  },
  setup() {
    const sidebarOpen = ref(false)
    const activeMenu = ref('home')

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

    return {
      sidebarOpen,
      activeMenu,
      toggleSidebar,
      closeSidebar,
      selectMenu,
      getPageTitle,
      currentComponent
    }
  }
}
</script>
