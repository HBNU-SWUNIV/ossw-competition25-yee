<template>
  <div class="budget-management">
    <div class="page-header">
      <h2>예산 관리</h2>
      <button class="add-btn" @click="showAddModal = true">+ 새 예산 추가</button>
    </div>

    <div class="stats-overview">
      <div class="stat-card">
        <div class="stat-icon">💰</div>
        <div class="stat-content">
          <h3>총 예산</h3>
          <p class="amount">₩{{ totalBudget.toLocaleString() }}</p>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon">📊</div>
        <div class="stat-content">
          <h3>사용된 예산</h3>
          <p class="amount used">₩{{ usedBudget.toLocaleString() }}</p>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon">💳</div>
        <div class="stat-content">
          <h3>남은 예산</h3>
          <p class="amount remaining">₩{{ remainingBudget.toLocaleString() }}</p>
        </div>
      </div>
    </div>

    <div class="budget-list">
      <h3>부서별 예산 현황</h3>
      <div class="budget-items">
        <div v-for="budget in budgets" :key="budget.id" class="budget-item">
          <div class="budget-info">
            <h4>{{ budget.department }}</h4>
            <p class="budget-period">{{ budget.period }}</p>
          </div>
          <div class="budget-amounts">
            <div class="allocated">
              <span class="label">배정:</span>
              <span class="amount">₩{{ budget.allocated.toLocaleString() }}</span>
            </div>
            <div class="spent">
              <span class="label">사용:</span>
              <span class="amount">₩{{ budget.spent.toLocaleString() }}</span>
            </div>
          </div>
          <div class="progress-bar">
            <div class="progress" :style="{ width: (budget.spent / budget.allocated * 100) + '%' }"></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue'

export default {
  name: 'BudgetManagement',
  setup() {
    const showAddModal = ref(false)

    const budgets = ref([
      { id: 1, department: '마케팅팀', period: '2024년 10월', allocated: 5000000, spent: 3200000 },
      { id: 2, department: '개발팀', period: '2024년 10월', allocated: 8000000, spent: 4500000 },
      { id: 3, department: '영업팀', period: '2024년 10월', allocated: 3000000, spent: 1800000 },
      { id: 4, department: '인사팀', period: '2024년 10월', allocated: 2000000, spent: 900000 }
    ])

    const totalBudget = computed(() =>
      budgets.value.reduce((sum, budget) => sum + budget.allocated, 0)
    )

    const usedBudget = computed(() =>
      budgets.value.reduce((sum, budget) => sum + budget.spent, 0)
    )

    const remainingBudget = computed(() => totalBudget.value - usedBudget.value)

    return {
      showAddModal,
      budgets,
      totalBudget,
      usedBudget,
      remainingBudget
    }
  }
}
</script>

<style scoped>
.budget-management {
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

.add-btn {
  background: #1976d2;
  color: white;
  border: none;
  padding: 12px 20px;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  transition: background 0.3s ease;
}

.add-btn:hover {
  background: #1565c0;
}

.stats-overview {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
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
  transition: transform 0.2s ease;
}

.stat-card:hover {
  transform: translateY(-2px);
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

.amount {
  font-size: 1.5rem;
  font-weight: bold;
  margin: 0;
  color: #2c3e50;
}

.amount.used {
  color: #f44336;
}

.amount.remaining {
  color: #4caf50;
}

.budget-list {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.budget-list h3 {
  color: #2c3e50;
  margin: 0 0 1.5rem 0;
  font-size: 1.3rem;
}

.budget-items {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.budget-item {
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 1.5rem;
  transition: border-color 0.3s ease;
}

.budget-item:hover {
  border-color: #1976d2;
}

.budget-info h4 {
  color: #2c3e50;
  margin: 0 0 0.5rem 0;
  font-size: 1.1rem;
}

.budget-period {
  color: #666;
  margin: 0 0 1rem 0;
  font-size: 0.9rem;
}

.budget-amounts {
  display: flex;
  justify-content: space-between;
  margin-bottom: 1rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.allocated,
.spent {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.label {
  font-size: 0.8rem;
  color: #666;
  margin-bottom: 0.25rem;
}

.budget-amounts .amount {
  font-size: 1.1rem;
  font-weight: 600;
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
  background: linear-gradient(90deg, #4caf50 0%, #ff9800 70%, #f44336 100%);
  transition: width 0.3s ease;
}

/* PC 최적화 (1200px 이상) */
@media (min-width: 1200px) {
  .stats-overview {
    grid-template-columns: repeat(3, 1fr);
    gap: 2rem;
  }

  .stat-card {
    padding: 2rem;
  }

  .stat-icon {
    font-size: 3rem;
  }

  .amount {
    font-size: 1.8rem;
  }

  .budget-list {
    padding: 2rem;
  }

  .budget-item {
    padding: 2rem;
  }
}

/* 태블릿 (769px - 1199px) */
@media (max-width: 1199px) and (min-width: 769px) {
  .stats-overview {
    grid-template-columns: repeat(2, 1fr);
    gap: 1.5rem;
  }

  .page-header {
    gap: 1.5rem;
  }
}

/* 모바일 (768px 이하) */
@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    align-items: stretch;
    gap: 1rem;
  }

  .add-btn {
    width: 100%;
    padding: 14px 20px;
    font-size: 1.1rem;
  }

  .stats-overview {
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

  .budget-list {
    padding: 1.5rem;
  }

  .budget-item {
    padding: 1.5rem;
  }

  .budget-amounts {
    flex-direction: column;
    gap: 1rem;
  }

  .allocated,
  .spent {
    flex-direction: row;
    justify-content: space-between;
    padding: 0.5rem 0;
  }
}

/* 소형 모바일 (480px 이하) */
@media (max-width: 480px) {
  .page-header h2 {
    font-size: 1.5rem;
  }

  .add-btn {
    padding: 16px 20px;
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

  .budget-list {
    padding: 1rem;
  }

  .budget-item {
    padding: 1.2rem;
  }

  .budget-info h4 {
    font-size: 1rem;
  }

  .budget-amounts .amount {
    font-size: 1rem;
  }
}
</style>