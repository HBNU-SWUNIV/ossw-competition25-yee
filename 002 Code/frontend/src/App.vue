<template>
  <div id="app">
    <!-- 햄버거 메뉴 버튼 -->
    <button class="hamburger-btn" @click="toggleSidebar" :class="{ active: sidebarOpen }">
      <span></span>
      <span></span>
      <span></span>
    </button>

    <!-- 사이드바 오버레이 -->
    <div class="sidebar-overlay" v-if="sidebarOpen" @click="closeSidebar"></div>

    <!-- 사이드바 -->
    <nav class="sidebar" :class="{ open: sidebarOpen }">
      <div class="sidebar-header">
        <h2>메뉴</h2>
        <button class="close-btn" @click="closeSidebar">&times;</button>
      </div>
      
      <ul class="sidebar-menu">
        <li>
          <a href="#" @click="selectMenu('budget')" :class="{ active: activeMenu === 'budget' }">
            <span class="icon">💰</span>
            예산관리
          </a>
        </li>
        <li>
          <a href="#" @click="selectMenu('expenses')" :class="{ active: activeMenu === 'expenses' }">
            <span class="icon">📊</span>
            지출내역
          </a>
        </li>
        <li>
          <a href="#" @click="selectMenu('reports')" :class="{ active: activeMenu === 'reports' }">
            <span class="icon">📈</span>
            리포트
          </a>
        </li>
        <li>
          <a href="#" @click="selectMenu('departments')" :class="{ active: activeMenu === 'departments' }">
            <span class="icon">🏢</span>
            부서관리
          </a>
        </li>
        <li>
          <a href="#" @click="selectMenu('settings')" :class="{ active: activeMenu === 'settings' }">
            <span class="icon">⚙️</span>
            설정
          </a>
        </li>
      </ul>
    </nav>

    <!-- 메인 콘텐츠 -->
    <main class="main-content" :class="{ 'sidebar-open': sidebarOpen }">
      <header class="main-header">
        <h1>{{ getPageTitle() }}</h1>
      </header>
      
      <div class="content">
        <!-- 기본 메인 화면 -->
        <div v-if="activeMenu === 'home'" class="home-screen">
          <div class="welcome-message">
            <h2>🏢 예산 관리 시스템</h2>
            <p>사이드바 메뉴를 클릭하여 원하는 기능을 이용하세요.</p>
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

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

#app {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  height: 100vh;
  background-color: #f5f5f5;
}

/* 햄버거 메뉴 버튼 */
.hamburger-btn {
  position: fixed;
  top: 20px;
  left: 20px;
  z-index: 1001;
  background: #2c3e50;
  border: none;
  width: 45px;
  height: 45px;
  border-radius: 8px;
  cursor: pointer;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 4px;
  transition: all 0.3s ease;
}

.hamburger-btn:hover {
  background: #34495e;
}

.hamburger-btn span {
  width: 25px;
  height: 3px;
  background: white;
  border-radius: 2px;
  transition: all 0.3s ease;
}

.hamburger-btn.active span:nth-child(1) {
  transform: rotate(45deg) translate(6px, 6px);
}

.hamburger-btn.active span:nth-child(2) {
  opacity: 0;
}

.hamburger-btn.active span:nth-child(3) {
  transform: rotate(-45deg) translate(6px, -6px);
}

/* 사이드바 오버레이 */
.sidebar-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  z-index: 999;
}

/* 사이드바 */
.sidebar {
  position: fixed;
  top: 0;
  left: -280px;
  width: 280px;
  height: 100vh;
  background: white;
  box-shadow: 2px 0 10px rgba(0, 0, 0, 0.1);
  z-index: 1000;
  transition: left 0.3s ease;
  overflow-y: auto;
}

.sidebar.open {
  left: 0;
}

.sidebar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  border-bottom: 1px solid #eee;
  background: #2c3e50;
  color: white;
}

.sidebar-header h2 {
  font-size: 1.5rem;
  font-weight: 600;
}

.close-btn {
  background: none;
  border: none;
  color: white;
  font-size: 24px;
  cursor: pointer;
  padding: 5px;
  border-radius: 4px;
}

.close-btn:hover {
  background: rgba(255, 255, 255, 0.1);
}

.sidebar-menu {
  list-style: none;
  padding: 0;
  margin: 0;
}

.sidebar-menu li {
  border-bottom: 1px solid #f0f0f0;
}

.sidebar-menu a {
  display: flex;
  align-items: center;
  padding: 16px 20px;
  text-decoration: none;
  color: #333;
  transition: all 0.3s ease;
  font-weight: 500;
}

.sidebar-menu a:hover {
  background: #f8f9fa;
  color: #2c3e50;
}

.sidebar-menu a.active {
  background: #e3f2fd;
  color: #1976d2;
  border-right: 4px solid #1976d2;
}

.sidebar-menu .icon {
  margin-right: 12px;
  font-size: 1.2rem;
}

/* 메인 콘텐츠 */
.main-content {
  margin-left: 0;
  min-height: 100vh;
  transition: margin-left 0.3s ease;
}

.main-header {
  background: white;
  padding: 25px 100px 25px 100px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  margin-bottom: 0;
  position: sticky;
  top: 0;
  z-index: 100;
}

.main-header h1 {
  color: #2c3e50;
  font-size: 2.2rem;
  font-weight: 700;
  letter-spacing: -0.5px;
}

.content {
  padding: 50px 100px;
  max-width: 1600px;
  margin: 0 auto;
}

/* 홈 화면 스타일 */
.home-screen {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 60vh;
}

.welcome-message {
  text-align: center;
  padding: 60px 40px;
  background: white;
  border-radius: 20px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  max-width: 500px;
  width: 100%;
}

.welcome-message h2 {
  color: #2c3e50;
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 20px;
  letter-spacing: -0.5px;
}

.welcome-message p {
  color: #7f8c8d;
  font-size: 1.2rem;
  line-height: 1.6;
  margin: 0;
}

/* PC 최적화 (1200px 이상) */
@media (min-width: 1200px) {
  .main-header {
    padding: 30px 120px 30px 120px;
  }
  
  .main-header h1 {
    font-size: 2.4rem;
  }
  
  .content {
    padding: 60px 120px;
    max-width: 1800px;
  }
  
  .hamburger-btn {
    width: 50px;
    height: 50px;
    top: 25px;
    left: 25px;
  }
  
  .hamburger-btn span {
    width: 28px;
    height: 3px;
  }
  
  .sidebar {
    width: 320px;
    left: -320px;
  }
}

/* 대형 PC (1600px 이상) */
@media (min-width: 1600px) {
  .content {
    padding: 80px 150px;
    max-width: 2000px;
  }
  
  .main-header {
    padding: 35px 150px 35px 150px;
  }
}

/* 태블릿 (768px - 1199px) */
@media (max-width: 1199px) and (min-width: 769px) {
  .main-header {
    padding: 20px 60px 20px 80px;
  }
  
  .main-header h1 {
    font-size: 2rem;
  }
  
  .content {
    padding: 40px 60px;
  }
  
  .hamburger-btn {
    width: 45px;
    height: 45px;
    top: 20px;
    left: 20px;
  }
}

/* 모바일 (768px 이하) */
@media (max-width: 768px) {
  .hamburger-btn {
    top: 15px;
    left: 15px;
    width: 44px;
    height: 44px;
    border-radius: 12px;
  }
  
  .hamburger-btn span {
    width: 24px;
    height: 3px;
  }
  
  .main-header {
    padding: 18px 20px 18px 75px;
    position: sticky;
    top: 0;
  }
  
  .main-header h1 {
    font-size: 1.6rem;
    font-weight: 600;
  }
  
  .content {
    padding: 25px 20px;
  }
  
  .welcome-message {
    padding: 40px 30px;
    margin: 20px;
  }
  
  .welcome-message h2 {
    font-size: 2rem;
  }
  
  .welcome-message p {
    font-size: 1.1rem;
  }
  
  .sidebar {
    width: 85%;
    max-width: 320px;
    left: -85%;
  }
  
  .sidebar.open {
    left: 0;
  }
  
  .sidebar-header {
    padding: 20px;
  }
  
  .sidebar-menu a {
    padding: 18px 20px;
    font-size: 1rem;
  }
  
  .sidebar-menu .icon {
    margin-right: 15px;
    font-size: 1.3rem;
  }
}

/* 소형 모바일 (480px 이하) */
@media (max-width: 480px) {
  .hamburger-btn {
    top: 12px;
    left: 12px;
    width: 40px;
    height: 40px;
    border-radius: 10px;
  }
  
  .hamburger-btn span {
    width: 22px;
    height: 2.5px;
  }
  
  .main-header {
    padding: 15px 15px 15px 65px;
  }
  
  .main-header h1 {
    font-size: 1.4rem;
  }
  
  .content {
    padding: 20px 15px;
  }
  
  .welcome-message {
    padding: 30px 20px;
    margin: 15px;
  }
  
  .welcome-message h2 {
    font-size: 1.8rem;
  }
  
  .welcome-message p {
    font-size: 1rem;
  }
  
  .sidebar {
    width: 90%;
  }
  
  .sidebar-header {
    padding: 18px;
  }
  
  .sidebar-header h2 {
    font-size: 1.4rem;
  }
  
  .sidebar-menu a {
    padding: 16px 18px;
    font-size: 0.95rem;
  }
  
  .sidebar-menu .icon {
    margin-right: 12px;
    font-size: 1.2rem;
  }
}

/* 초소형 모바일 (360px 이하) */
@media (max-width: 360px) {
  .hamburger-btn {
    top: 10px;
    left: 10px;
    width: 36px;
    height: 36px;
  }
  
  .hamburger-btn span {
    width: 20px;
    height: 2px;
  }
  
  .main-header {
    padding: 12px 12px 12px 58px;
  }
  
  .main-header h1 {
    font-size: 1.2rem;
  }
  
  .content {
    padding: 15px 12px;
  }
  
  .welcome-message {
    padding: 25px 15px;
    margin: 10px;
  }
  
  .welcome-message h2 {
    font-size: 1.6rem;
  }
  
  .welcome-message p {
    font-size: 0.95rem;
  }
  
  .sidebar {
    width: 95%;
  }
  
  .sidebar-header {
    padding: 15px;
  }
  
  .sidebar-header h2 {
    font-size: 1.2rem;
  }
  
  .sidebar-menu a {
    padding: 14px 15px;
    font-size: 0.9rem;
  }
  
  .sidebar-menu .icon {
    margin-right: 10px;
    font-size: 1.1rem;
  }
}
</style>