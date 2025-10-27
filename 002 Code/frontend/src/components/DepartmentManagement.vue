<template>
  <div class="autonomous-management">
    <!-- 페이지 헤더 -->
    <div class="page-header">
      <h2 class="page-title">자치기구 관리</h2>
      <div class="header-stats">
        <div class="stat-item">
          <span class="stat-label">총 자치기구</span>
          <span class="stat-value">{{ organizations.length }}개</span>
        </div>
        <div class="stat-item">
          <span class="stat-label">총 예산</span>
          <span class="stat-value">₩{{ totalBudget.toLocaleString() }}</span>
        </div>
      </div>
    </div>

    <!-- 검색 및 필터 -->
    <div class="filters">
      <input v-model="searchQuery" type="text" placeholder="자치기구명 또는 회장명 검색..." class="search-input">
      <select v-model="sortBy" class="sort-select">
        <option value="order">기본 순서</option>
        <option value="name">이름순</option>
        <option value="budget">예산순</option>
        <option value="usage">사용률순</option>
      </select>
    </div>

    <!-- 자치기구 카드 그리드 -->
    <div class="organizations-grid">
      <div v-for="org in filteredOrganizations" :key="org.id" class="organization-card"
        :class="{ 'over-budget': org.usageRate > 90, 'warning': org.usageRate > 80 }">
        <!-- 카드 헤더 -->
        <div class="card-header">
          <div class="org-main-info">
            <div class="org-number">#{{ org.order }}</div>
            <div class="org-details">
              <h3 class="org-name">{{ org.name }}</h3>
              <p class="org-subtitle">{{ org.subtitle }}</p>
            </div>
          </div>
          <div class="budget-status" :class="getBudgetStatusClass(org.usageRate)">
            {{ getBudgetStatusText(org.usageRate) }}
          </div>
        </div>

        <!-- 예산 정보 -->
        <div class="budget-section">
          <div class="budget-info">
            <div class="budget-item">
              <span class="budget-label">배정 예산</span>
              <span class="budget-amount">₩{{ org.budget.toLocaleString() }}</span>
            </div>
            <div class="budget-item">
              <span class="budget-label">사용 예산</span>
              <span class="budget-amount used">₩{{ org.usedBudget.toLocaleString() }}</span>
            </div>
          </div>

          <div class="usage-progress">
            <div class="progress-header">
              <span class="progress-label">예산 사용률</span>
              <span class="progress-value">{{ org.usageRate }}%</span>
            </div>
            <div class="progress-bar">
              <div class="progress-fill" :style="{ width: org.usageRate + '%' }"
                :class="getProgressClass(org.usageRate)"></div>
            </div>
          </div>
        </div>

        <!-- 회장 정보 -->
        <div class="president-section">
          <div class="president-info">
            <div class="president-avatar">👤</div>
            <div class="president-details">
              <span class="president-name">{{ org.president }}</span>
              <span class="president-title">회장</span>
            </div>
          </div>
        </div>

        <!-- 임원 정보 -->
        <div class="officers-section">
          <h4 class="section-title">임원 정보</h4>
          <div class="officers-list">
            <div v-for="officer in org.officers" :key="officer.id" class="officer-item">
              <span class="officer-name">{{ officer.name }}</span>
              <span class="officer-role">{{ officer.role }}</span>
            </div>
          </div>
        </div>

        <!-- 액션 버튼 -->
        <div class="card-actions">
          <button class="action-btn primary" @click="viewExpenseHistory(org.id)">
            📊 사용내역서 보기
          </button>
          <button class="action-btn secondary" @click="viewDetails(org.id)">
            📋 상세 정보
          </button>
        </div>
      </div>
    </div>

    <!-- 사용내역서 모달 -->
    <div v-if="showExpenseModal" class="modal-overlay" @click="closeExpenseModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>{{ selectedOrg?.name }} 사용내역서</h3>
          <button class="close-btn" @click="closeExpenseModal">×</button>
        </div>
        <div class="modal-body">
          <div class="expense-summary">
            <div class="summary-item">
              <span class="summary-label">총 지출</span>
              <span class="summary-value">₩{{ selectedOrg?.usedBudget.toLocaleString() }}</span>
            </div>
            <div class="summary-item">
              <span class="summary-label">잔여 예산</span>
              <span class="summary-value">₩{{ (selectedOrg?.budget - selectedOrg?.usedBudget).toLocaleString() }}</span>
            </div>
          </div>

          <div class="expense-list">
            <div class="expense-header">
              <span>날짜</span>
              <span>내용</span>
              <span>금액</span>
            </div>
            <div v-for="expense in selectedOrgExpenses" :key="expense.id" class="expense-item">
              <span class="expense-date">{{ formatDate(expense.date) }}</span>
              <span class="expense-description">{{ expense.description }}</span>
              <span class="expense-amount">₩{{ expense.amount.toLocaleString() }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue'

export default {
  name: 'DepartmentManagement',
  setup() {
    const searchQuery = ref('')
    const sortBy = ref('order')
    const showExpenseModal = ref(false)
    const selectedOrg = ref(null)

    // 자치기구 데이터
    const organizations = ref([
      {
        id: 1,
        order: 1,
        name: '총학생회',
        subtitle: '한밭대학교 총학생회',
        president: '김총학',
        budget: 50000000,
        usedBudget: 35000000,
        usageRate: 70,
        officers: [
          { id: 1, name: '이부회장', role: '부회장' },
          { id: 2, name: '박총무', role: '총무' },
          { id: 3, name: '최기획', role: '기획부장' },
          { id: 4, name: '정홍보', role: '홍보부장' }
        ]
      },
      {
        id: 2,
        order: 2,
        name: '총동아리',
        subtitle: '한밭대학교 총동아리연합회',
        president: '김동아리',
        budget: 30000000,
        usedBudget: 28500000,
        usageRate: 95,
        officers: [
          { id: 5, name: '이동연', role: '부회장' },
          { id: 6, name: '박동아리', role: '총무' },
          { id: 7, name: '최활동', role: '활동부장' }
        ]
      },
      {
        id: 3,
        order: 3,
        name: '컴퓨터공학과',
        subtitle: '컴퓨터공학과 학생회',
        president: '김컴공',
        budget: 15000000,
        usedBudget: 9750000,
        usageRate: 65,
        officers: [
          { id: 8, name: '이코딩', role: '부회장' },
          { id: 9, name: '박프로그래밍', role: '총무' },
          { id: 10, name: '최개발', role: '학술부장' }
        ]
      },
      {
        id: 4,
        order: 4,
        name: '건설환경공학과',
        subtitle: '건설환경공학과 학생회',
        president: '김건설',
        budget: 12000000,
        usedBudget: 10800000,
        usageRate: 90,
        officers: [
          { id: 11, name: '이환경', role: '부회장' },
          { id: 12, name: '박토목', role: '총무' },
          { id: 13, name: '최구조', role: '학술부장' }
        ]
      }
    ])

    // 샘플 지출 내역 데이터
    const expenseData = ref({
      1: [ // 총학생회
        { id: 1, date: '2024-10-15', description: '학생회 정기총회 진행비', amount: 2500000 },
        { id: 2, date: '2024-10-10', description: '동아리 지원금', amount: 5000000 },
        { id: 3, date: '2024-10-05', description: '학생복지 개선 사업', amount: 3000000 },
        { id: 4, date: '2024-09-28', description: '축제 준비 비용', amount: 8000000 },
        { id: 5, date: '2024-09-20', description: '학생회실 운영비', amount: 1500000 }
      ],
      2: [ // 총동아리
        { id: 6, date: '2024-10-12', description: '동아리 박람회 개최', amount: 4500000 },
        { id: 7, date: '2024-10-08', description: '동아리 활동 지원금', amount: 8000000 },
        { id: 8, date: '2024-09-25', description: '동아리 장비 구입', amount: 6000000 },
        { id: 9, date: '2024-09-15', description: '동아리 연합회 운영비', amount: 2000000 }
      ],
      3: [ // 컴퓨터공학과
        { id: 10, date: '2024-10-14', description: '학과 세미나 개최', amount: 1500000 },
        { id: 11, date: '2024-10-07', description: '프로그래밍 대회 상금', amount: 2000000 },
        { id: 12, date: '2024-09-30', description: '학과 MT 지원', amount: 3000000 },
        { id: 13, date: '2024-09-18', description: '학습 자료 구입', amount: 1250000 }
      ],
      4: [ // 건설환경공학과
        { id: 14, date: '2024-10-11', description: '현장 견학 비용', amount: 3500000 },
        { id: 15, date: '2024-10-03', description: '학과 워크샵', amount: 2800000 },
        { id: 16, date: '2024-09-22', description: '실험 장비 구입', amount: 2500000 },
        { id: 17, date: '2024-09-12', description: '학과 행사 진행비', amount: 2000000 }
      ]
    })

    const selectedOrgExpenses = computed(() => {
      return selectedOrg.value ? expenseData.value[selectedOrg.value.id] || [] : []
    })

    const totalBudget = computed(() =>
      organizations.value.reduce((sum, org) => sum + org.budget, 0)
    )

    const filteredOrganizations = computed(() => {
      let filtered = organizations.value.filter(org =>
        org.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
        org.subtitle.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
        org.president.toLowerCase().includes(searchQuery.value.toLowerCase())
      )

      // 정렬
      filtered.sort((a, b) => {
        switch (sortBy.value) {
          case 'name':
            return a.name.localeCompare(b.name)
          case 'budget':
            return b.budget - a.budget
          case 'usage':
            return b.usageRate - a.usageRate
          default:
            return a.order - b.order
        }
      })

      return filtered
    })

    // 예산 상태 관련 함수들
    const getBudgetStatusText = (usageRate) => {
      if (usageRate > 90) return '예산 초과 위험'
      if (usageRate > 80) return '예산 사용 주의'
      if (usageRate < 50) return '예산 여유'
      return '정상 범위'
    }

    const getBudgetStatusClass = (usageRate) => {
      if (usageRate > 90) return 'danger'
      if (usageRate > 80) return 'warning'
      return 'normal'
    }

    const getProgressClass = (usageRate) => {
      if (usageRate > 90) return 'danger'
      if (usageRate > 80) return 'warning'
      return 'normal'
    }

    // 모달 관련 함수들
    const viewExpenseHistory = (orgId) => {
      selectedOrg.value = organizations.value.find(org => org.id === orgId)
      showExpenseModal.value = true
    }

    const closeExpenseModal = () => {
      showExpenseModal.value = false
      selectedOrg.value = null
    }

    const viewDetails = (orgId) => {
      const org = organizations.value.find(o => o.id === orgId)
      alert(`${org.name} 상세 정보\n\n회장: ${org.president}\n예산: ₩${org.budget.toLocaleString()}\n사용률: ${org.usageRate}%`)
    }

    const formatDate = (dateString) => {
      const date = new Date(dateString)
      return date.toLocaleDateString('ko-KR', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit'
      })
    }

    return {
      searchQuery,
      sortBy,
      showExpenseModal,
      selectedOrg,
      organizations,
      selectedOrgExpenses,
      totalBudget,
      filteredOrganizations,
      getBudgetStatusText,
      getBudgetStatusClass,
      getProgressClass,
      viewExpenseHistory,
      closeExpenseModal,
      viewDetails,
      formatDate
    }
  }
}
</script>

<style scoped>
.autonomous-management {
  padding: 2rem;
  max-width: 1400px;
  margin: 0 auto;
}

/* 페이지 헤더 */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.page-title {
  color: #2c3e50;
  font-size: 2rem;
  font-weight: 700;
  margin: 0;
}

.header-stats {
  display: flex;
  gap: 2rem;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.stat-label {
  font-size: 0.9rem;
  color: #666;
  margin-bottom: 0.25rem;
}

.stat-value {
  font-size: 1.2rem;
  font-weight: 700;
  color: #2c3e50;
}

/* 필터 섹션 */
.filters {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
  flex-wrap: wrap;
}

.search-input {
  flex: 1;
  min-width: 300px;
  padding: 12px 16px;
  border: 2px solid #e1e5e9;
  border-radius: 12px;
  font-size: 1rem;
  transition: border-color 0.3s ease;
}

.search-input:focus {
  outline: none;
  border-color: #3b82f6;
}

.sort-select {
  padding: 12px 16px;
  border: 2px solid #e1e5e9;
  border-radius: 12px;
  background: white;
  font-size: 1rem;
  cursor: pointer;
}

/* 자치기구 그리드 */
.organizations-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 2rem;
}

.organization-card {
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  overflow: hidden;
  transition: all 0.3s ease;
  border: 2px solid transparent;
}

.organization-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
}

.organization-card.warning {
  border-color: #f59e0b;
}

.organization-card.over-budget {
  border-color: #ef4444;
}

/* 카드 헤더 */
.card-header {
  padding: 1.5rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.org-main-info {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.org-number {
  background: rgba(255, 255, 255, 0.2);
  padding: 8px 12px;
  border-radius: 50%;
  font-weight: 700;
  font-size: 1.1rem;
  min-width: 40px;
  text-align: center;
}

.org-details h3 {
  margin: 0 0 0.25rem 0;
  font-size: 1.4rem;
  font-weight: 700;
}

.org-subtitle {
  margin: 0;
  font-size: 0.9rem;
  opacity: 0.9;
}

.budget-status {
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 600;
  background: rgba(255, 255, 255, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.3);
}

.budget-status.warning {
  background: rgba(245, 158, 11, 0.2);
  border-color: rgba(245, 158, 11, 0.4);
}

.budget-status.danger {
  background: rgba(239, 68, 68, 0.2);
  border-color: rgba(239, 68, 68, 0.4);
}

/* 예산 섹션 */
.budget-section {
  padding: 1.5rem;
  border-bottom: 1px solid #f1f5f9;
}

.budget-info {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
  margin-bottom: 1rem;
}

.budget-item {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.budget-label {
  font-size: 0.85rem;
  color: #64748b;
  font-weight: 500;
}

.budget-amount {
  font-size: 1.1rem;
  font-weight: 700;
  color: #1e293b;
}

.budget-amount.used {
  color: #dc2626;
}

.usage-progress {
  margin-top: 1rem;
}

.progress-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.progress-label {
  font-size: 0.9rem;
  color: #64748b;
  font-weight: 500;
}

.progress-value {
  font-size: 0.9rem;
  font-weight: 700;
  color: #1e293b;
}

.progress-bar {
  width: 100%;
  height: 8px;
  background: #e2e8f0;
  border-radius: 4px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  transition: width 0.3s ease;
  border-radius: 4px;
}

.progress-fill.normal {
  background: #10b981;
}

.progress-fill.warning {
  background: #f59e0b;
}

.progress-fill.danger {
  background: #ef4444;
}

/* 회장 섹션 */
.president-section {
  padding: 1rem 1.5rem;
  border-bottom: 1px solid #f1f5f9;
}

.president-info {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.president-avatar {
  width: 40px;
  height: 40px;
  background: #e2e8f0;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
}

.president-details {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.president-name {
  font-weight: 700;
  color: #1e293b;
}

.president-title {
  font-size: 0.85rem;
  color: #64748b;
}

/* 임원 섹션 */
.officers-section {
  padding: 1rem 1.5rem;
  border-bottom: 1px solid #f1f5f9;
}

.section-title {
  margin: 0 0 1rem 0;
  font-size: 1rem;
  font-weight: 600;
  color: #374151;
}

.officers-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.officer-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem 0;
}

.officer-name {
  font-weight: 500;
  color: #1e293b;
}

.officer-role {
  font-size: 0.85rem;
  color: #64748b;
  background: #f1f5f9;
  padding: 2px 8px;
  border-radius: 12px;
}

/* 액션 버튼 */
.card-actions {
  padding: 1.5rem;
  display: flex;
  gap: 0.75rem;
}

.action-btn {
  flex: 1;
  padding: 10px 16px;
  border: none;
  border-radius: 8px;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.action-btn.primary {
  background: #3b82f6;
  color: white;
}

.action-btn.primary:hover {
  background: #2563eb;
}

.action-btn.secondary {
  background: #f1f5f9;
  color: #64748b;
  border: 1px solid #e2e8f0;
}

.action-btn.secondary:hover {
  background: #e2e8f0;
  color: #374151;
}

/* 모달 스타일 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 1rem;
}

.modal-content {
  background: white;
  border-radius: 16px;
  max-width: 600px;
  width: 100%;
  max-height: 80vh;
  overflow: hidden;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

.modal-header {
  padding: 1.5rem;
  border-bottom: 1px solid #e2e8f0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #f8fafc;
}

.modal-header h3 {
  margin: 0;
  font-size: 1.3rem;
  font-weight: 700;
  color: #1e293b;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #64748b;
  padding: 0;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: background-color 0.2s ease;
}

.close-btn:hover {
  background: #e2e8f0;
}

.modal-body {
  padding: 1.5rem;
  max-height: 60vh;
  overflow-y: auto;
}

.expense-summary {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
  margin-bottom: 1.5rem;
  padding: 1rem;
  background: #f8fafc;
  border-radius: 8px;
}

.summary-item {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.summary-label {
  font-size: 0.85rem;
  color: #64748b;
  font-weight: 500;
}

.summary-value {
  font-size: 1.2rem;
  font-weight: 700;
  color: #1e293b;
}

.expense-list {
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  overflow: hidden;
}

.expense-header {
  display: grid;
  grid-template-columns: 100px 1fr 120px;
  gap: 1rem;
  padding: 1rem;
  background: #f1f5f9;
  font-weight: 600;
  color: #374151;
  font-size: 0.9rem;
}

.expense-item {
  display: grid;
  grid-template-columns: 100px 1fr 120px;
  gap: 1rem;
  padding: 1rem;
  border-top: 1px solid #e2e8f0;
  font-size: 0.9rem;
}

.expense-date {
  color: #64748b;
}

.expense-description {
  color: #1e293b;
  font-weight: 500;
}

.expense-amount {
  color: #dc2626;
  font-weight: 600;
  text-align: right;
}

/* 반응형 디자인 */
@media (max-width: 768px) {
  .autonomous-management {
    padding: 1rem;
  }

  .page-title {
    font-size: 1.5rem;
  }

  .header-stats {
    gap: 1rem;
  }

  .filters {
    flex-direction: column;
  }

  .search-input {
    min-width: auto;
  }

  .organizations-grid {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }

  .card-header {
    flex-direction: column;
    gap: 1rem;
    align-items: stretch;
  }

  .org-main-info {
    justify-content: space-between;
  }

  .budget-info {
    grid-template-columns: 1fr;
  }

  .card-actions {
    flex-direction: column;
  }

  .modal-content {
    margin: 1rem;
    max-height: 90vh;
  }

  .expense-header,
  .expense-item {
    grid-template-columns: 80px 1fr 100px;
    gap: 0.5rem;
    padding: 0.75rem;
  }

  .expense-summary {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 480px) {
  .page-header {
    flex-direction: column;
    align-items: stretch;
    text-align: center;
  }

  .org-main-info {
    flex-direction: column;
    align-items: center;
    text-align: center;
    gap: 0.5rem;
  }

  .expense-header,
  .expense-item {
    grid-template-columns: 1fr;
    gap: 0.25rem;
    text-align: left;
  }

  .expense-amount {
    text-align: left;
  }
}
</style>
.department-management {
padding: 0;
}

.page-header {
display: flex;
justify-content: space-between;
align-items: center;
margin-bottom: 2rem;
flex-wrap: wrap;
gap: 1rem;
}

.page-header h2 {
color: #2c3e50;
font-size: 1.8rem;
margin: 0;
}

/* 내 부서 정보 스타일 */
.my-department-section {
margin-bottom: 2rem;
}

.my-department-section h3 {
color: #2c3e50;
font-size: 1.3rem;
margin-bottom: 1rem;
font-weight: 600;
}

.my-department-card {
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
border-radius: 16px;
padding: 2rem;
color: white;
box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
position: relative;
overflow: hidden;
}

.my-department-card::before {
content: '';
position: absolute;
top: -50%;
right: -50%;
width: 100%;
height: 100%;
background: rgba(255, 255, 255, 0.1);
border-radius: 50%;
z-index: 1;
}

.dept-header {
display: flex;
justify-content: space-between;
align-items: flex-start;
margin-bottom: 1.5rem;
position: relative;
z-index: 2;
}

.dept-main-info h4 {
font-size: 1.8rem;
margin: 0 0 0.5rem 0;
font-weight: 700;
}

.dept-code {
background: rgba(255, 255, 255, 0.2);
padding: 4px 12px;
border-radius: 20px;
font-size: 0.8rem;
font-weight: 600;
margin-right: 0.5rem;
}

.my-role {
background: rgba(255, 255, 255, 0.3);
padding: 4px 12px;
border-radius: 20px;
font-size: 0.8rem;
font-weight: 600;
}

.dept-status {
padding: 8px 16px;
border-radius: 20px;
font-size: 0.9rem;
font-weight: 600;
background: rgba(76, 175, 80, 0.2);
border: 1px solid rgba(76, 175, 80, 0.3);
}

.dept-status.warning {
background: rgba(255, 152, 0, 0.2);
border-color: rgba(255, 152, 0, 0.3);
}

.dept-status.over-budget {
background: rgba(244, 67, 54, 0.2);
border-color: rgba(244, 67, 54, 0.3);
}

.dept-details {
position: relative;
z-index: 2;
}

.detail-row {
display: grid;
grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
gap: 1rem;
margin-bottom: 1.5rem;
}

.detail-item {
display: flex;
flex-direction: column;
gap: 0.25rem;
}

.detail-item .label {
font-size: 0.85rem;
opacity: 0.8;
font-weight: 500;
}

.detail-item .value {
font-size: 1.1rem;
font-weight: 600;
}

.detail-item .value.budget {
color: #81c784;
}

.detail-item .value.used {
color: #ffb74d;
}

.budget-progress {
margin-bottom: 1.5rem;
}

.progress-header {
display: flex;
justify-content: space-between;
align-items: center;
margin-bottom: 0.5rem;
}

.usage-rate {
font-weight: 700;
font-size: 1.1rem;
}

.budget-progress .progress-bar {
width: 100%;
height: 12px;
background: rgba(255, 255, 255, 0.2);
border-radius: 6px;
overflow: hidden;
}

.budget-progress .progress {
height: 100%;
background: #4caf50;
transition: width 0.3s ease;
border-radius: 6px;
}

.budget-progress .progress.warning {
background: #ff9800;
}

.budget-progress .progress.danger {
background: #f44336;
}

.contact-section {
display: flex;
flex-wrap: wrap;
gap: 1rem;
}

.contact-item {
display: flex;
align-items: center;
gap: 0.5rem;
background: rgba(255, 255, 255, 0.1);
padding: 0.5rem 1rem;
border-radius: 20px;
font-size: 0.9rem;
}

.contact-icon {
font-size: 1rem;
}

.department-stats {
display: grid;
grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
gap: 1.5rem;
margin-bottom: 2rem;
}

.stat-card {
background: white;
border-radius: 12px;
padding: 1.5rem;
box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
display: flex;
align-items: center;
}

.stat-icon {
font-size: 2.5rem;
margin-right: 1rem;
}

.stat-content h3 {
color: #666;
font-size: 0.9rem;
margin: 0 0 0.5rem 0;
font-weight: 500;
}

.stat-number {
font-size: 1.5rem;
font-weight: bold;
color: #2c3e50;
margin: 0;
}

.department-filters {
display: flex;
gap: 1rem;
margin-bottom: 2rem;
flex-wrap: wrap;
}

.search-input {
flex: 1;
min-width: 250px;
padding: 12px 16px;
border: 1px solid #ddd;
border-radius: 8px;
font-size: 1rem;
}

.sort-select {
padding: 12px 16px;
border: 1px solid #ddd;
border-radius: 8px;
background: white;
font-size: 1rem;
}

.department-grid {
display: grid;
grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
gap: 1.5rem;
}

.department-card {
background: white;
border-radius: 12px;
box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
overflow: hidden;
transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.department-card:hover {
transform: translateY(-2px);
box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
}

.card-header {
display: flex;
justify-content: space-between;
align-items: center;
padding: 1.5rem 1.5rem 1rem 1.5rem;
border-bottom: 1px solid #f0f0f0;
}

.dept-info h3 {
color: #2c3e50;
margin: 0 0 0.25rem 0;
font-size: 1.3rem;
}

.dept-code {
background: #e3f2fd;
color: #1976d2;
padding: 2px 8px;
border-radius: 12px;
font-size: 0.8rem;
font-weight: 600;
}

.card-actions {
display: flex;
gap: 0.5rem;
}



.card-body {
padding: 1rem 1.5rem;
}

.info-row {
display: flex;
justify-content: space-between;
align-items: center;
margin-bottom: 0.75rem;
}

.info-row:last-child {
margin-bottom: 0;
}

.label {
color: #666;
font-size: 0.9rem;
font-weight: 500;
}

.value {
font-weight: 600;
color: #2c3e50;
}

.value.budget {
color: #1976d2;
}

.value.usage {
color: #4caf50;
}

.value.usage.high-usage {
color: #f44336;
}

.card-footer {
padding: 1rem 1.5rem 1.5rem 1.5rem;
background: #f8f9fa;
}

.progress-section {
margin-bottom: 1rem;
}

.progress-label {
display: flex;
justify-content: space-between;
align-items: center;
margin-bottom: 0.5rem;
font-size: 0.9rem;
color: #666;
}

.progress-bar {
width: 100%;
height: 8px;
background: #e0e0e0;
border-radius: 4px;
overflow: hidden;
}

.progress {
height: 100%;
background: #4caf50;
transition: width 0.3s ease;
}

.progress.warning {
background: #ff9800;
}

.progress.danger {
background: #f44336;
}

.contact-info {
display: flex;
flex-direction: column;
gap: 0.5rem;
}

.contact-item {
display: flex;
align-items: center;
gap: 0.5rem;
font-size: 0.9rem;
}

.contact-label {
font-size: 0.8rem;
}

.contact-value {
color: #666;
}



/* PC 최적화 (1200px 이상) */
@media (min-width: 1200px) {
.department-stats {
grid-template-columns: repeat(3, 1fr);
gap: 2rem;
}

.stat-card {
padding: 2rem;
}

.stat-icon {
font-size: 3rem;
}

.stat-number {
font-size: 1.8rem;
}

.department-grid {
grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
gap: 2rem;
}

.department-card {
padding: 0;
}

.card-header {
padding: 2rem 2rem 1.5rem 2rem;
}

.card-body {
padding: 1.5rem 2rem;
}

.card-footer {
padding: 1.5rem 2rem 2rem 2rem;
}

.search-input {
padding: 14px 18px;
font-size: 1.1rem;
}
}

/* 태블릿 (769px - 1199px) */
@media (max-width: 1199px) and (min-width: 769px) {
.department-stats {
grid-template-columns: repeat(2, 1fr);
}

.department-grid {
grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
}
}

/* 모바일 (768px 이하) */
@media (max-width: 768px) {
.my-department-card {
padding: 1.5rem;
}

.dept-header {
flex-direction: column;
gap: 1rem;
}

.detail-row {
grid-template-columns: 1fr;
gap: 0.8rem;
}

.contact-section {
flex-direction: column;
gap: 0.5rem;
}

.department-stats {
grid-template-columns: 1fr;
gap: 1.2rem;
}

.stat-card {
padding: 1.5rem;
flex-direction: row;
}

.stat-icon {
font-size: 2.2rem;
}

.department-filters {
flex-direction: column;
gap: 1rem;
}

.search-input {
padding: 14px 16px;
font-size: 1rem;
}

.sort-select {
padding: 14px 16px;
font-size: 1rem;
}

.department-grid {
grid-template-columns: 1fr;
gap: 1.2rem;
}

.card-header {
flex-direction: column;
align-items: stretch;
gap: 1rem;
padding: 1.5rem;
}

.dept-info {
display: flex;
justify-content: space-between;
align-items: center;
}

.card-actions {
justify-content: center;
}

.card-body {
padding: 1rem 1.5rem;
}

.card-footer {
padding: 1rem 1.5rem 1.5rem 1.5rem;
}

.contact-info {
gap: 0.8rem;
}
}

/* 소형 모바일 (480px 이하) */
@media (max-width: 480px) {
.page-header h2 {
font-size: 1.5rem;
}

.stat-card {
flex-direction: column;
text-align: center;
padding: 1.2rem;
}

.stat-icon {
margin: 0 0 1rem 0;
font-size: 2.5rem;
}

.department-card {
margin: 0;
}

.card-header {
padding: 1.2rem;
}

.dept-info {
flex-direction: column;
align-items: stretch;
gap: 0.5rem;
}

.dept-info h3 {
font-size: 1.1rem;
}

.card-body {
padding: 1rem 1.2rem;
}

.card-footer {
padding: 1rem 1.2rem 1.2rem 1.2rem;
}

.modal-content {
padding: 1.5rem;
margin: 1rem;
}

.form-actions {
flex-direction: column;
gap: 0.8rem;
}

.cancel-btn,
.save-btn {
width: 100%;
}
}
</style>