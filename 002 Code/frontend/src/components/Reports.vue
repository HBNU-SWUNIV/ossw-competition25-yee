<template>
  <div class="reports">
    <div class="page-header">
      <h2>리포트</h2>
      <div class="header-actions">
        <select v-model="selectedReportType" class="report-select">
          <option value="monthly">월간 리포트</option>
          <option value="quarterly">분기 리포트</option>
          <option value="yearly">연간 리포트</option>
        </select>
        <button class="export-btn">📊 내보내기</button>
      </div>
    </div>

    <div class="report-overview">
      <div class="overview-card trend-up">
        <div class="card-icon">📈</div>
        <div class="card-content">
          <h3>예산 효율성</h3>
          <p class="percentage">+15.3%</p>
          <span class="trend">전월 대비 개선</span>
        </div>
      </div>
      
      <div class="overview-card trend-down">
        <div class="card-icon">💸</div>
        <div class="card-content">
          <h3>지출 증가율</h3>
          <p class="percentage">-8.2%</p>
          <span class="trend">전월 대비 감소</span>
        </div>
      </div>
      
      <div class="overview-card">
        <div class="card-icon">🎯</div>
        <div class="card-content">
          <h3>목표 달성률</h3>
          <p class="percentage">87.5%</p>
          <span class="trend">목표 대비</span>
        </div>
      </div>
    </div>

    <div class="charts-section">
      <div class="chart-container">
        <h3>부서별 예산 사용률</h3>
        <div class="chart-placeholder">
          <div class="department-chart">
            <div v-for="dept in departmentData" :key="dept.name" class="dept-bar">
              <div class="dept-info">
                <span class="dept-name">{{ dept.name }}</span>
                <span class="dept-percentage">{{ dept.usage }}%</span>
              </div>
              <div class="progress-bar">
                <div 
                  class="progress" 
                  :style="{ width: dept.usage + '%' }"
                  :class="{ 'over-budget': dept.usage > 90 }"
                ></div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="chart-container">
        <h3>월별 지출 추이</h3>
        <div class="chart-placeholder">
          <div class="monthly-chart">
            <div class="chart-bars">
              <div 
                v-for="month in monthlyData" 
                :key="month.month" 
                class="month-bar"
              >
                <div 
                  class="bar" 
                  :style="{ height: (month.amount / maxAmount * 100) + '%' }"
                ></div>
                <span class="month-label">{{ month.month }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="detailed-reports">
      <div class="report-section">
        <h3>카테고리별 지출 분석</h3>
        <div class="category-analysis">
          <div v-for="category in categoryData" :key="category.name" class="category-item">
            <div class="category-header">
              <span class="category-name">{{ category.name }}</span>
              <span class="category-amount">₩{{ category.amount.toLocaleString() }}</span>
            </div>
            <div class="category-details">
              <div class="progress-bar">
                <div 
                  class="progress" 
                  :style="{ width: (category.amount / totalCategoryAmount * 100) + '%' }"
                ></div>
              </div>
              <span class="percentage">{{ Math.round(category.amount / totalCategoryAmount * 100) }}%</span>
            </div>
          </div>
        </div>
      </div>

      <div class="report-section">
        <h3>주요 지표</h3>
        <div class="metrics-grid">
          <div class="metric-card">
            <h4>평균 일일 지출</h4>
            <p class="metric-value">₩{{ dailyAverage.toLocaleString() }}</p>
          </div>
          <div class="metric-card">
            <h4>최대 지출 부서</h4>
            <p class="metric-value">{{ topSpendingDept }}</p>
          </div>
          <div class="metric-card">
            <h4>예산 준수율</h4>
            <p class="metric-value">{{ budgetCompliance }}%</p>
          </div>
          <div class="metric-card">
            <h4>절약 금액</h4>
            <p class="metric-value savings">₩{{ savedAmount.toLocaleString() }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue'

export default {
  name: 'Reports',
  setup() {
    const selectedReportType = ref('monthly')
    
    const departmentData = ref([
      { name: '개발팀', usage: 75 },
      { name: '마케팅팀', usage: 92 },
      { name: '영업팀', usage: 68 },
      { name: '인사팀', usage: 45 },
      { name: '총무팀', usage: 83 }
    ])

    const monthlyData = ref([
      { month: '6월', amount: 3200000 },
      { month: '7월', amount: 2800000 },
      { month: '8월', amount: 3500000 },
      { month: '9월', amount: 2900000 },
      { month: '10월', amount: 3100000 }
    ])

    const categoryData = ref([
      { name: '사무용품', amount: 1200000 },
      { name: '마케팅', amount: 2100000 },
      { name: '식비', amount: 800000 },
      { name: '교통비', amount: 450000 },
      { name: '기타', amount: 650000 }
    ])

    const maxAmount = computed(() => 
      Math.max(...monthlyData.value.map(m => m.amount))
    )

    const totalCategoryAmount = computed(() => 
      categoryData.value.reduce((sum, cat) => sum + cat.amount, 0)
    )

    const dailyAverage = computed(() => 
      Math.round(totalCategoryAmount.value / 30)
    )

    const topSpendingDept = computed(() => 
      departmentData.value.reduce((max, dept) => 
        dept.usage > max.usage ? dept : max
      ).name
    )

    const budgetCompliance = ref(87)
    const savedAmount = ref(2450000)

    return {
      selectedReportType,
      departmentData,
      monthlyData,
      categoryData,
      maxAmount,
      totalCategoryAmount,
      dailyAverage,
      topSpendingDept,
      budgetCompliance,
      savedAmount
    }
  }
}
</script>

<style scoped>
.reports {
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

.report-select {
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  background: white;
  font-size: 0.9rem;
}

.export-btn {
  background: #4caf50;
  color: white;
  border: none;
  padding: 12px 20px;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  transition: background 0.3s ease;
}

.export-btn:hover {
  background: #45a049;
}

.report-overview {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.overview-card {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  transition: transform 0.2s ease;
}

.overview-card:hover {
  transform: translateY(-2px);
}

.card-icon {
  font-size: 2.5rem;
  margin-right: 1rem;
}

.card-content h3 {
  color: #666;
  font-size: 0.9rem;
  margin: 0 0 0.5rem 0;
  font-weight: 500;
}

.percentage {
  font-size: 1.8rem;
  font-weight: bold;
  margin: 0 0 0.25rem 0;
}

.trend-up .percentage {
  color: #4caf50;
}

.trend-down .percentage {
  color: #f44336;
}

.overview-card:not(.trend-up):not(.trend-down) .percentage {
  color: #1976d2;
}

.trend {
  font-size: 0.8rem;
  color: #666;
}

.charts-section {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 2rem;
  margin-bottom: 2rem;
}

.chart-container {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.chart-container h3 {
  color: #2c3e50;
  margin: 0 0 1.5rem 0;
  font-size: 1.2rem;
}

.department-chart {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.dept-bar {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.dept-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.dept-name {
  font-weight: 500;
  color: #2c3e50;
}

.dept-percentage {
  font-weight: 600;
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
  background: #1976d2;
  transition: width 0.3s ease;
}

.progress.over-budget {
  background: #f44336;
}

.monthly-chart {
  height: 200px;
  display: flex;
  align-items: end;
}

.chart-bars {
  display: flex;
  align-items: end;
  justify-content: space-between;
  width: 100%;
  height: 100%;
  gap: 1rem;
}

.month-bar {
  display: flex;
  flex-direction: column;
  align-items: center;
  flex: 1;
  height: 100%;
}

.bar {
  width: 100%;
  max-width: 40px;
  background: linear-gradient(to top, #1976d2, #42a5f5);
  border-radius: 4px 4px 0 0;
  margin-bottom: 0.5rem;
  transition: height 0.3s ease;
}

.month-label {
  font-size: 0.8rem;
  color: #666;
  font-weight: 500;
}

.detailed-reports {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 2rem;
}

.report-section {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.report-section h3 {
  color: #2c3e50;
  margin: 0 0 1.5rem 0;
  font-size: 1.2rem;
}

.category-analysis {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.category-item {
  padding: 1rem;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
}

.category-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.category-name {
  font-weight: 500;
  color: #2c3e50;
}

.category-amount {
  font-weight: 600;
  color: #f44336;
}

.category-details {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.category-details .progress-bar {
  flex: 1;
}

.category-details .percentage {
  font-size: 0.9rem;
  color: #666;
  font-weight: 500;
  min-width: 40px;
}

.metrics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 1rem;
}

.metric-card {
  text-align: center;
  padding: 1rem;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
}

.metric-card h4 {
  color: #666;
  font-size: 0.8rem;
  margin: 0 0 0.5rem 0;
  font-weight: 500;
}

.metric-value {
  font-size: 1.2rem;
  font-weight: bold;
  color: #2c3e50;
  margin: 0;
}

.metric-value.savings {
  color: #4caf50;
}

/* PC 최적화 (1200px 이상) */
@media (min-width: 1200px) {
  .report-overview {
    grid-template-columns: repeat(3, 1fr);
    gap: 2rem;
  }
  
  .overview-card {
    padding: 2rem;
  }
  
  .card-icon {
    font-size: 3rem;
  }
  
  .percentage {
    font-size: 2.2rem;
  }
  
  .charts-section {
    grid-template-columns: repeat(2, 1fr);
    gap: 2.5rem;
  }
  
  .chart-container {
    padding: 2rem;
  }
  
  .detailed-reports {
    grid-template-columns: repeat(2, 1fr);
    gap: 2.5rem;
  }
  
  .metrics-grid {
    grid-template-columns: repeat(4, 1fr);
    gap: 1.5rem;
  }
  
  .metric-card {
    padding: 1.5rem;
  }
  
  .metric-value {
    font-size: 1.4rem;
  }
}

/* 태블릿 (769px - 1199px) */
@media (max-width: 1199px) and (min-width: 769px) {
  .report-overview {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .charts-section {
    grid-template-columns: 1fr;
    gap: 2rem;
  }
  
  .detailed-reports {
    grid-template-columns: 1fr;
    gap: 2rem;
  }
  
  .metrics-grid {
    grid-template-columns: repeat(2, 1fr);
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
  
  .export-btn {
    width: 100%;
    padding: 14px 20px;
    font-size: 1.1rem;
  }
  
  .report-select {
    padding: 12px 16px;
    font-size: 1rem;
  }
  
  .report-overview {
    grid-template-columns: 1fr;
    gap: 1.2rem;
  }
  
  .overview-card {
    padding: 1.5rem;
    flex-direction: row;
  }
  
  .card-icon {
    font-size: 2.2rem;
  }
  
  .percentage {
    font-size: 1.6rem;
  }
  
  .charts-section {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }
  
  .chart-container {
    padding: 1.5rem;
  }
  
  .detailed-reports {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }
  
  .metrics-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 1rem;
  }
  
  .metric-card {
    padding: 1.2rem;
  }
  
  .monthly-chart {
    height: 180px;
  }
}

/* 소형 모바일 (480px 이하) */
@media (max-width: 480px) {
  .page-header h2 {
    font-size: 1.5rem;
  }
  
  .overview-card {
    flex-direction: column;
    text-align: center;
    padding: 1.2rem;
  }
  
  .card-icon {
    margin: 0 0 1rem 0;
    font-size: 2.5rem;
  }
  
  .chart-container {
    padding: 1rem;
  }
  
  .metrics-grid {
    grid-template-columns: 1fr;
  }
  
  .metric-card {
    padding: 1rem;
  }
  
  .monthly-chart {
    height: 150px;
  }
  
  .dept-bar, .category-item {
    padding: 0.8rem;
  }
}
</style>