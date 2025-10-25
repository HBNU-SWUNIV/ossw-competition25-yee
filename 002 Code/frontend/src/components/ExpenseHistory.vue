<template>
  <div class="expense-history">
    <div class="page-header">
      <h2>지출 내역</h2>
      <div class="header-actions">
        <select v-model="selectedPeriod" class="period-select">
          <option value="this-month">이번 달</option>
          <option value="last-month">지난 달</option>
          <option value="this-year">올해</option>
        </select>
        <button class="add-btn" @click="showAddModal = true">+ 지출 추가</button>
      </div>
    </div>

    <div class="expense-summary">
      <div class="summary-card">
        <h3>총 지출</h3>
        <p class="total-amount">₩{{ totalExpense.toLocaleString() }}</p>
      </div>
      <div class="summary-card">
        <h3>평균 지출</h3>
        <p class="avg-amount">₩{{ avgExpense.toLocaleString() }}</p>
      </div>
      <div class="summary-card">
        <h3>지출 건수</h3>
        <p class="count">{{ expenses.length }}건</p>
      </div>
    </div>

    <div class="expense-filters">
      <input 
        v-model="searchQuery" 
        type="text" 
        placeholder="지출 내역 검색..." 
        class="search-input"
      >
      <select v-model="selectedCategory" class="category-filter">
        <option value="">모든 카테고리</option>
        <option value="식비">식비</option>
        <option value="교통비">교통비</option>
        <option value="사무용품">사무용품</option>
        <option value="마케팅">마케팅</option>
        <option value="기타">기타</option>
      </select>
    </div>

    <div class="expense-list">
      <div class="expense-table">
        <div class="table-header">
          <div class="col-date">날짜</div>
          <div class="col-category">카테고리</div>
          <div class="col-description">내용</div>
          <div class="col-department">부서</div>
          <div class="col-amount">금액</div>
        </div>
        
        <div class="table-body">
          <div 
            v-for="expense in filteredExpenses" 
            :key="expense.id" 
            class="expense-row"
          >
            <div class="col-date">{{ formatDate(expense.date) }}</div>
            <div class="col-category">
              <span class="category-tag" :class="expense.category">
                {{ expense.category }}
              </span>
            </div>
            <div class="col-description">{{ expense.description }}</div>
            <div class="col-department">{{ expense.department }}</div>
            <div class="col-amount">₩{{ expense.amount.toLocaleString() }}</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue'

export default {
  name: 'ExpenseHistory',
  setup() {
    const showAddModal = ref(false)
    const selectedPeriod = ref('this-month')
    const searchQuery = ref('')
    const selectedCategory = ref('')
    
    const expenses = ref([
      { id: 1, date: '2024-10-20', category: '식비', description: '팀 회식', department: '개발팀', amount: 150000 },
      { id: 2, date: '2024-10-19', category: '사무용품', description: '프린터 토너', department: '총무팀', amount: 85000 },
      { id: 3, date: '2024-10-18', category: '마케팅', description: '광고비', department: '마케팅팀', amount: 500000 },
      { id: 4, date: '2024-10-17', category: '교통비', description: '출장 교통비', department: '영업팀', amount: 45000 },
      { id: 5, date: '2024-10-16', category: '식비', description: '점심 식대', department: '인사팀', amount: 25000 },
      { id: 6, date: '2024-10-15', category: '기타', description: '사무실 청소', department: '총무팀', amount: 120000 },
      { id: 7, date: '2024-10-14', category: '사무용품', description: '노트북 구매', department: '개발팀', amount: 1200000 },
      { id: 8, date: '2024-10-13', category: '마케팅', description: '브로슈어 제작', department: '마케팅팀', amount: 300000 }
    ])

    const totalExpense = computed(() => 
      expenses.value.reduce((sum, expense) => sum + expense.amount, 0)
    )
    
    const avgExpense = computed(() => 
      expenses.value.length > 0 ? Math.round(totalExpense.value / expenses.value.length) : 0
    )

    const filteredExpenses = computed(() => {
      return expenses.value.filter(expense => {
        const matchesSearch = expense.description.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
                            expense.department.toLowerCase().includes(searchQuery.value.toLowerCase())
        const matchesCategory = selectedCategory.value === '' || expense.category === selectedCategory.value
        return matchesSearch && matchesCategory
      })
    })

    const formatDate = (dateString) => {
      const date = new Date(dateString)
      return date.toLocaleDateString('ko-KR', { 
        month: 'short', 
        day: 'numeric',
        weekday: 'short'
      })
    }

    return {
      showAddModal,
      selectedPeriod,
      searchQuery,
      selectedCategory,
      expenses,
      totalExpense,
      avgExpense,
      filteredExpenses,
      formatDate
    }
  }
}
</script>

<style scoped>
.expense-history {
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

.header-actions {
  display: flex;
  gap: 1rem;
  align-items: center;
  flex-wrap: wrap;
}

.period-select, .category-filter {
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  background: white;
  font-size: 0.9rem;
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
  white-space: nowrap;
}

.add-btn:hover {
  background: #1565c0;
}

.expense-summary {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.summary-card {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.summary-card h3 {
  color: #666;
  font-size: 0.9rem;
  margin: 0 0 1rem 0;
  font-weight: 500;
}

.total-amount, .avg-amount {
  font-size: 1.8rem;
  font-weight: bold;
  color: #f44336;
  margin: 0;
}

.count {
  font-size: 1.8rem;
  font-weight: bold;
  color: #1976d2;
  margin: 0;
}

.expense-filters {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
}

.search-input {
  flex: 1;
  min-width: 200px;
  padding: 12px 16px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 1rem;
}

.expense-list {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.expense-table {
  width: 100%;
}

.table-header {
  display: grid;
  grid-template-columns: 100px 100px 1fr 120px 120px;
  background: #f8f9fa;
  padding: 1rem;
  font-weight: 600;
  color: #2c3e50;
  border-bottom: 1px solid #e0e0e0;
}

.table-body {
  max-height: 500px;
  overflow-y: auto;
}

.expense-row {
  display: grid;
  grid-template-columns: 100px 100px 1fr 120px 120px;
  padding: 1rem;
  border-bottom: 1px solid #f0f0f0;
  align-items: center;
  transition: background 0.2s ease;
}

.expense-row:hover {
  background: #f8f9fa;
}

.expense-row:last-child {
  border-bottom: none;
}

.col-date {
  font-size: 0.9rem;
  color: #666;
}

.category-tag {
  display: inline-block;
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: 500;
  color: white;
}

.category-tag.식비 { background: #ff9800; }
.category-tag.교통비 { background: #2196f3; }
.category-tag.사무용품 { background: #4caf50; }
.category-tag.마케팅 { background: #9c27b0; }
.category-tag.기타 { background: #607d8b; }

.col-description {
  font-weight: 500;
}

.col-department {
  color: #666;
  font-size: 0.9rem;
}

.col-amount {
  font-weight: 600;
  color: #f44336;
  text-align: right;
}

/* PC 최적화 (1200px 이상) */
@media (min-width: 1200px) {
  .expense-summary {
    grid-template-columns: repeat(3, 1fr);
    gap: 2rem;
  }
  
  .summary-card {
    padding: 2rem;
  }
  
  .total-amount, .avg-amount, .count {
    font-size: 2rem;
  }
  
  .expense-filters {
    gap: 1.5rem;
  }
  
  .search-input {
    padding: 14px 18px;
    font-size: 1.1rem;
  }
  
  .table-header, .expense-row {
    grid-template-columns: 120px 120px 1fr 140px 140px;
    padding: 1.2rem;
  }
}

/* 태블릿 (769px - 1199px) */
@media (max-width: 1199px) and (min-width: 769px) {
  .expense-summary {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .header-actions {
    gap: 1.2rem;
  }
}

/* 모바일 (768px 이하) */
@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    align-items: stretch;
    gap: 1rem;
  }
  
  .header-actions {
    flex-direction: column;
    gap: 1rem;
  }
  
  .add-btn {
    width: 100%;
    padding: 14px 20px;
    font-size: 1.1rem;
  }
  
  .period-select, .category-filter {
    padding: 12px 16px;
    font-size: 1rem;
  }
  
  .expense-summary {
    grid-template-columns: 1fr;
    gap: 1.2rem;
  }
  
  .summary-card {
    padding: 1.5rem;
  }
  
  .expense-filters {
    flex-direction: column;
    gap: 1rem;
  }
  
  .search-input {
    padding: 14px 16px;
    font-size: 1rem;
  }
  
  .table-header {
    display: none;
  }
  
  .expense-row {
    display: block;
    padding: 1.5rem;
    border: 1px solid #e0e0e0;
    border-radius: 12px;
    margin-bottom: 1rem;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  }
  
  .expense-row > div {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.8rem;
    padding: 0.3rem 0;
  }
  
  .expense-row > div:last-child {
    margin-bottom: 0;
  }
  
  .expense-row > div:before {
    content: attr(data-label);
    font-weight: 600;
    color: #666;
    font-size: 0.9rem;
  }
  
  .col-date:before { content: '날짜'; }
  .col-category:before { content: '카테고리'; }
  .col-description:before { content: '내용'; }
  .col-department:before { content: '부서'; }
  .col-amount:before { content: '금액'; }
}

/* 소형 모바일 (480px 이하) */
@media (max-width: 480px) {
  .page-header h2 {
    font-size: 1.5rem;
  }
  
  .summary-card {
    padding: 1.2rem;
  }
  
  .total-amount, .avg-amount, .count {
    font-size: 1.5rem;
  }
  
  .expense-row {
    padding: 1.2rem;
  }
  
  .expense-row > div {
    margin-bottom: 0.6rem;
  }
  
  .category-tag {
    font-size: 0.75rem;
    padding: 3px 6px;
  }
}
</style>