<template>
  <div class="department-management">
    <div class="page-header">
      <h2>부서 관리</h2>
    </div>

    <!-- 내 부서 정보 -->
    <div class="my-department-section">
      <h3>내 부서 정보</h3>
      <div class="my-department-card">
        <div class="dept-header">
          <div class="dept-main-info">
            <h4>{{ myDepartment.name }}</h4>
            <span class="dept-code">{{ myDepartment.code }}</span>
            <span class="my-role">{{ myDepartment.myRole }}</span>
          </div>
          <div class="dept-status"
            :class="{ 'over-budget': myDepartment.usageRate > 90, 'warning': myDepartment.usageRate > 80 }">
            <span class="status-text">{{ getBudgetStatus(myDepartment.usageRate) }}</span>
          </div>
        </div>

        <div class="dept-details">
          <div class="detail-row">
            <div class="detail-item">
              <span class="label">담당자</span>
              <span class="value">{{ myDepartment.manager }}</span>
            </div>
            <div class="detail-item">
              <span class="label">직원 수</span>
              <span class="value">{{ myDepartment.employees }}명</span>
            </div>
            <div class="detail-item">
              <span class="label">배정 예산</span>
              <span class="value budget">₩{{ myDepartment.budget.toLocaleString() }}</span>
            </div>
            <div class="detail-item">
              <span class="label">사용 예산</span>
              <span class="value used">₩{{ myDepartment.usedBudget.toLocaleString() }}</span>
            </div>
          </div>

          <div class="budget-progress">
            <div class="progress-header">
              <span>예산 사용률</span>
              <span class="usage-rate">{{ myDepartment.usageRate }}%</span>
            </div>
            <div class="progress-bar">
              <div class="progress" :style="{ width: myDepartment.usageRate + '%' }" :class="{
                'warning': myDepartment.usageRate > 70 && myDepartment.usageRate <= 90,
                'danger': myDepartment.usageRate > 90
              }"></div>
            </div>
          </div>

          <div class="contact-section">
            <div class="contact-item">
              <span class="contact-icon">📧</span>
              <span class="contact-text">{{ myDepartment.email }}</span>
            </div>
            <div class="contact-item">
              <span class="contact-icon">📞</span>
              <span class="contact-text">{{ myDepartment.phone }}</span>
            </div>
            <div class="contact-item">
              <span class="contact-icon">📍</span>
              <span class="contact-text">{{ myDepartment.location }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="department-stats">
      <div class="stat-card">
        <div class="stat-icon">🏢</div>
        <div class="stat-content">
          <h3>총 부서 수</h3>
          <p class="stat-number">{{ departments.length }}개</p>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon">👥</div>
        <div class="stat-content">
          <h3>총 직원 수</h3>
          <p class="stat-number">{{ totalEmployees }}명</p>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon">💰</div>
        <div class="stat-content">
          <h3>총 예산</h3>
          <p class="stat-number">₩{{ totalBudget.toLocaleString() }}</p>
        </div>
      </div>
    </div>

    <div class="department-filters">
      <input v-model="searchQuery" type="text" placeholder="부서명 또는 담당자 검색..." class="search-input">
      <select v-model="sortBy" class="sort-select">
        <option value="name">부서명순</option>
        <option value="employees">직원수순</option>
        <option value="budget">예산순</option>
      </select>
    </div>

    <div class="department-grid">
      <div v-for="dept in filteredDepartments" :key="dept.id" class="department-card">
        <div class="card-header">
          <div class="dept-info">
            <h3>{{ dept.name }}</h3>
            <span class="dept-code">{{ dept.code }}</span>
          </div>
        </div>

        <div class="card-body">
          <div class="info-row">
            <span class="label">담당자:</span>
            <span class="value">{{ dept.manager }}</span>
          </div>
          <div class="info-row">
            <span class="label">직원 수:</span>
            <span class="value">{{ dept.employees }}명</span>
          </div>
          <div class="info-row">
            <span class="label">예산:</span>
            <span class="value budget">₩{{ dept.budget.toLocaleString() }}</span>
          </div>
          <div class="info-row">
            <span class="label">사용률:</span>
            <span class="value usage" :class="{ 'high-usage': dept.usageRate > 80 }">
              {{ dept.usageRate }}%
            </span>
          </div>
        </div>

        <div class="card-footer">
          <div class="progress-section">
            <div class="progress-label">
              <span>예산 사용률</span>
              <span>{{ dept.usageRate }}%</span>
            </div>
            <div class="progress-bar">
              <div class="progress" :style="{ width: dept.usageRate + '%' }" :class="{
                'warning': dept.usageRate > 70 && dept.usageRate <= 90,
                'danger': dept.usageRate > 90
              }"></div>
            </div>
          </div>

          <div class="contact-info">
            <div class="contact-item">
              <span class="contact-label">📧</span>
              <span class="contact-value">{{ dept.email }}</span>
            </div>
            <div class="contact-item">
              <span class="contact-label">📞</span>
              <span class="contact-value">{{ dept.phone }}</span>
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
    const sortBy = ref('name')

    // 내 부서 정보 (더미 데이터)
    const myDepartment = ref({
      name: '개발팀',
      code: 'DEV',
      manager: '김개발',
      myRole: '팀원',
      employees: 15,
      budget: 8000000,
      usedBudget: 6000000,
      usageRate: 75,
      email: 'dev@company.com',
      phone: '02-1234-5678',
      location: '본사 3층 개발실'
    })

    const departments = ref([
      {
        id: 1,
        name: '개발팀',
        code: 'DEV',
        manager: '김개발',
        employees: 15,
        budget: 8000000,
        usageRate: 75,
        email: 'dev@company.com',
        phone: '02-1234-5678'
      },
      {
        id: 2,
        name: '마케팅팀',
        code: 'MKT',
        manager: '이마케팅',
        employees: 8,
        budget: 5000000,
        usageRate: 92,
        email: 'marketing@company.com',
        phone: '02-1234-5679'
      },
      {
        id: 3,
        name: '영업팀',
        code: 'SALES',
        manager: '박영업',
        employees: 12,
        budget: 3000000,
        usageRate: 68,
        email: 'sales@company.com',
        phone: '02-1234-5680'
      },
      {
        id: 4,
        name: '인사팀',
        code: 'HR',
        manager: '최인사',
        employees: 5,
        budget: 2000000,
        usageRate: 45,
        email: 'hr@company.com',
        phone: '02-1234-5681'
      },
      {
        id: 5,
        name: '총무팀',
        code: 'GA',
        manager: '정총무',
        employees: 6,
        budget: 2500000,
        usageRate: 83,
        email: 'ga@company.com',
        phone: '02-1234-5682'
      }
    ])

    const totalEmployees = computed(() =>
      departments.value.reduce((sum, dept) => sum + dept.employees, 0)
    )

    const totalBudget = computed(() =>
      departments.value.reduce((sum, dept) => sum + dept.budget, 0)
    )

    const filteredDepartments = computed(() => {
      let filtered = departments.value.filter(dept =>
        dept.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
        dept.manager.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
        dept.code.toLowerCase().includes(searchQuery.value.toLowerCase())
      )

      // 정렬
      filtered.sort((a, b) => {
        switch (sortBy.value) {
          case 'employees':
            return b.employees - a.employees
          case 'budget':
            return b.budget - a.budget
          default:
            return a.name.localeCompare(b.name)
        }
      })

      return filtered
    })

    // 예산 상태 텍스트 반환 함수
    const getBudgetStatus = (usageRate) => {
      if (usageRate > 90) return '예산 초과 위험'
      if (usageRate > 80) return '예산 사용 주의'
      if (usageRate < 50) return '예산 여유'
      return '정상 범위'
    }

    return {
      myDepartment,
      searchQuery,
      sortBy,
      departments,
      totalEmployees,
      totalBudget,
      filteredDepartments,
      getBudgetStatus
    }
  }
}
</script>

<style scoped>
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