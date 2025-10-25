<template>
  <div class="reports">
    <div class="page-header">
      <h2>리포트</h2>
      <div class="header-actions">
        <div class="date-filters">
          <select v-model="selectedYear" @change="onYearChange" class="date-select">
            <option value="">연도 선택</option>
            <option v-for="year in availableYears" :key="year" :value="year">{{ year }}년</option>
          </select>

          <select v-model="selectedMonth" @change="onMonthChange" class="date-select" :disabled="!selectedYear">
            <option value="">월 선택</option>
            <option v-for="month in availableMonths" :key="month.value" :value="month.value">{{ month.label }}</option>
          </select>

          <select v-model="selectedDay" @change="onDayChange" class="date-select" :disabled="!selectedMonth">
            <option value="">일 선택</option>
            <option v-for="day in availableDays" :key="day" :value="day">{{ day }}일</option>
          </select>
        </div>

        <div class="category-filter">
          <select v-model="selectedCategory" @change="onCategoryChange" class="category-select">
            <option value="">전체 카테고리</option>
            <option v-for="category in availableCategories" :key="category" :value="category">{{ category }}</option>
          </select>
        </div>

        <button class="export-btn" @click="exportAsCSV">📊 {{ getExportButtonText() }}</button>
      </div>
    </div>

    <div class="report-info">
      <div class="current-period">
        <h3>{{ getCurrentPeriodTitle() }}</h3>
        <p class="period-description">{{ getPeriodDescription() }}</p>
      </div>
    </div>

    <div class="report-overview">
      <div class="overview-card">
        <div class="card-icon">💰</div>
        <div class="card-content">
          <h3>총 지출</h3>
          <p class="amount">₩{{ currentData.totalExpense.toLocaleString() }}</p>
          <span class="trend"
            :class="{ 'trend-up': currentData.expenseChange > 0, 'trend-down': currentData.expenseChange < 0 }">
            {{ currentData.expenseChange > 0 ? '+' : '' }}{{ currentData.expenseChange }}% {{ getPreviousPeriodText() }}
            대비
          </span>
        </div>
      </div>

      <div class="overview-card">
        <div class="card-icon">📊</div>
        <div class="card-content">
          <h3>평균 {{ getAverageText() }}</h3>
          <p class="amount">₩{{ currentData.averageExpense.toLocaleString() }}</p>
          <span class="trend">{{ getAverageDescription() }}</span>
        </div>
      </div>

      <div class="overview-card">
        <div class="card-icon">📈</div>
        <div class="card-content">
          <h3>지출 건수</h3>
          <p class="amount">{{ currentData.transactionCount }}건</p>
          <span class="trend">{{ getTransactionDescription() }}</span>
        </div>
      </div>

      <div class="overview-card">
        <div class="card-icon">🎯</div>
        <div class="card-content">
          <h3>예산 대비</h3>
          <p class="amount">{{ currentData.budgetUsage }}%</p>
          <span class="trend"
            :class="{ 'trend-up': currentData.budgetUsage > 80, 'trend-down': currentData.budgetUsage < 50 }">
            {{ getBudgetStatusText() }}
          </span>
        </div>
      </div>
    </div>

    <div class="charts-section">
      <div class="chart-container">
        <h3>{{ getChartTitle('department') }}</h3>
        <div class="chart-placeholder">
          <div class="department-chart">
            <div v-for="dept in filteredDepartmentData" :key="dept.name" class="dept-bar">
              <div class="dept-info">
                <span class="dept-name">{{ dept.name }}</span>
                <span class="dept-amount">₩{{ dept.amount.toLocaleString() }}</span>
              </div>
              <div class="progress-bar">
                <div class="progress" :style="{ width: (dept.amount / maxDepartmentAmount * 100) + '%' }"></div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="chart-container">
        <h3>{{ getChartTitle('trend') }}</h3>
        <div class="chart-placeholder">
          <div class="trend-chart">
            <div class="chart-bars">
              <div v-for="item in filteredTrendData" :key="item.period" class="trend-bar">
                <div class="bar" :style="{ height: (item.amount / maxTrendAmount * 100) + '%' }"></div>
                <span class="period-label">{{ item.period }}</span>
                <span class="amount-label">₩{{ (item.amount / 1000).toFixed(0) }}K</span>
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
          <div v-for="category in filteredCategoryData" :key="category.name" class="category-item">
            <div class="category-header">
              <span class="category-name">{{ category.name }}</span>
              <span class="category-amount">₩{{ category.amount.toLocaleString() }}</span>
            </div>
            <div class="category-details">
              <div class="progress-bar">
                <div class="progress" :style="{ width: (category.amount / totalFilteredCategoryAmount * 100) + '%' }">
                </div>
              </div>
              <span class="percentage">{{ Math.round(category.amount / totalFilteredCategoryAmount * 100) }}%</span>
            </div>
            <div class="category-trend">
              <span class="trend-indicator"
                :class="{ 'trend-up': category.change > 0, 'trend-down': category.change < 0 }">
                {{ category.change > 0 ? '↗' : category.change < 0 ? '↘' : '→' }} {{ Math.abs(category.change) }}%
                  </span>
            </div>
          </div>
        </div>
      </div>

      <div class="report-section">
        <h3>상세 내역 (최신순)</h3>
        <div class="detail-list">
          <div class="detail-header">
            <span class="col-date">날짜</span>
            <span class="col-category">카테고리</span>
            <span class="col-department">부서</span>
            <span class="col-description">내용</span>
            <span class="col-amount">금액</span>
          </div>
          <div class="detail-body">
            <div v-for="item in filteredDetailData" :key="item.id" class="detail-row">
              <span class="col-date">{{ formatDate(item.date) }}</span>
              <span class="col-category">
                <span class="category-tag" :class="item.category">{{ item.category }}</span>
              </span>
              <span class="col-department">{{ item.department }}</span>
              <span class="col-description">{{ item.description }}</span>
              <span class="col-amount">₩{{ item.amount.toLocaleString() }}</span>
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
  name: 'Reports',
  setup() {
    // 날짜 선택 상태
    const selectedYear = ref('')
    const selectedMonth = ref('')
    const selectedDay = ref('')
    const selectedCategory = ref('')



    // 사용 가능한 날짜 옵션들 (최신순)
    const availableYears = ref([2024, 2023, 2022])

    const availableMonths = ref([
      { value: '12', label: '12월' }, { value: '11', label: '11월' }, { value: '10', label: '10월' },
      { value: '09', label: '9월' }, { value: '08', label: '8월' }, { value: '07', label: '7월' },
      { value: '06', label: '6월' }, { value: '05', label: '5월' }, { value: '04', label: '4월' },
      { value: '03', label: '3월' }, { value: '02', label: '2월' }, { value: '01', label: '1월' }
    ])

    const availableDays = computed(() => {
      if (!selectedYear.value || !selectedMonth.value) return []
      const daysInMonth = new Date(selectedYear.value, selectedMonth.value, 0).getDate()
      return Array.from({ length: daysInMonth }, (_, i) => String(daysInMonth - i).padStart(2, '0'))
    })

    const availableCategories = ref(['사무용품', '마케팅', '식비', '교통비', '인건비', '임대료', '기타'])

    // 샘플 데이터 (실제로는 API에서 가져올 데이터)
    const allExpenseData = ref([
      // 2024년 10월 데이터
      { id: 1, date: '2024-10-25', category: '마케팅', department: '마케팅팀', description: '온라인 광고비', amount: 850000 },
      { id: 2, date: '2024-10-24', category: '사무용품', department: '총무팀', description: '프린터 토너', amount: 120000 },
      { id: 3, date: '2024-10-23', category: '식비', department: '개발팀', description: '팀 회식', amount: 180000 },
      { id: 4, date: '2024-10-22', category: '교통비', department: '영업팀', description: '출장비', amount: 95000 },
      { id: 5, date: '2024-10-21', category: '인건비', department: '인사팀', description: '외부 강사비', amount: 300000 },
      { id: 6, date: '2024-10-20', category: '마케팅', department: '마케팅팀', description: '브로슈어 제작', amount: 450000 },
      { id: 7, date: '2024-10-19', category: '사무용품', department: '개발팀', description: '노트북 구매', amount: 1200000 },
      { id: 8, date: '2024-10-18', category: '임대료', department: '총무팀', description: '사무실 임대료', amount: 2500000 },
      { id: 9, date: '2024-10-17', category: '식비', department: '전체', description: '회사 워크샵', amount: 320000 },
      { id: 10, date: '2024-10-16', category: '교통비', department: '영업팀', description: '고객 미팅', amount: 150000 },

      // 2024년 9월 데이터
      { id: 11, date: '2024-09-30', category: '마케팅', department: '마케팅팀', description: '전시회 참가비', amount: 750000 },
      { id: 12, date: '2024-09-25', category: '식비', department: '전체', description: '회사 워크샵', amount: 320000 },
      { id: 13, date: '2024-09-20', category: '사무용품', department: '총무팀', description: '사무용 가구', amount: 680000 },
      { id: 14, date: '2024-09-15', category: '교통비', department: '영업팀', description: '고객 미팅', amount: 150000 },

      // 2024년 8월 데이터
      { id: 15, date: '2024-08-30', category: '인건비', department: '인사팀', description: '교육비', amount: 400000 },
      { id: 16, date: '2024-08-25', category: '마케팅', department: '마케팅팀', description: '소셜미디어 광고', amount: 300000 },
      { id: 17, date: '2024-08-20', category: '사무용품', department: '개발팀', description: '개발 장비', amount: 1500000 },

      // 2023년 데이터
      { id: 18, date: '2023-12-20', category: '마케팅', department: '마케팅팀', description: '연말 이벤트', amount: 900000 },
      { id: 19, date: '2023-11-15', category: '인건비', department: '인사팀', description: '교육비', amount: 400000 },
      { id: 20, date: '2023-10-25', category: '사무용품', department: '개발팀', description: '개발 장비', amount: 1500000 }
    ])

    // 현재 선택된 기간에 따른 데이터 필터링
    const filteredDetailData = computed(() => {
      let filtered = allExpenseData.value

      // 카테고리 필터
      if (selectedCategory.value) {
        filtered = filtered.filter(item => item.category === selectedCategory.value)
      }

      // 날짜 필터
      if (selectedYear.value) {
        filtered = filtered.filter(item => item.date.startsWith(selectedYear.value))

        if (selectedMonth.value) {
          filtered = filtered.filter(item => item.date.includes(`-${selectedMonth.value}-`))

          if (selectedDay.value) {
            filtered = filtered.filter(item => item.date.endsWith(`-${selectedDay.value}`))
          }
        }
      }

      // 최신 날짜순으로 정렬
      return filtered.sort((a, b) => new Date(b.date) - new Date(a.date))
    })

    // 현재 데이터 통계
    const currentData = computed(() => {
      const data = filteredDetailData.value
      const totalExpense = data.reduce((sum, item) => sum + item.amount, 0)
      const transactionCount = data.length

      let averageExpense = 0
      if (selectedDay.value) {
        averageExpense = totalExpense // 일별은 그 날의 총액
      } else if (selectedMonth.value) {
        const daysInMonth = new Date(selectedYear.value, selectedMonth.value, 0).getDate()
        averageExpense = Math.round(totalExpense / daysInMonth)
      } else if (selectedYear.value) {
        averageExpense = Math.round(totalExpense / 12)
      } else {
        averageExpense = Math.round(totalExpense / (transactionCount || 1))
      }

      return {
        totalExpense,
        averageExpense,
        transactionCount,
        expenseChange: Math.round((Math.random() - 0.5) * 30), // 임시 변화율
        budgetUsage: Math.round((totalExpense / 10000000) * 100) // 가정된 예산 대비
      }
    })

    // 부서별 데이터
    const filteredDepartmentData = computed(() => {
      const deptMap = new Map()

      filteredDetailData.value.forEach(item => {
        const current = deptMap.get(item.department) || 0
        deptMap.set(item.department, current + item.amount)
      })

      return Array.from(deptMap.entries())
        .map(([name, amount]) => ({ name, amount }))
        .sort((a, b) => b.amount - a.amount)
    })

    const maxDepartmentAmount = computed(() =>
      Math.max(...filteredDepartmentData.value.map(d => d.amount), 1)
    )

    // 카테고리별 데이터
    const filteredCategoryData = computed(() => {
      const catMap = new Map()

      filteredDetailData.value.forEach(item => {
        const current = catMap.get(item.category) || 0
        catMap.set(item.category, current + item.amount)
      })

      return Array.from(catMap.entries())
        .map(([name, amount]) => ({
          name,
          amount,
          change: Math.round((Math.random() - 0.5) * 40) // 임시 변화율
        }))
        .sort((a, b) => b.amount - a.amount)
    })

    const totalFilteredCategoryAmount = computed(() =>
      filteredCategoryData.value.reduce((sum, cat) => sum + cat.amount, 0)
    )

    // 트렌드 데이터 (기간에 따라 다르게 표시)
    const filteredTrendData = computed(() => {
      if (selectedDay.value) {
        // 일별 선택시 - 해당 월의 일별 데이터 (최근 10일)
        const monthData = allExpenseData.value.filter(item =>
          item.date.startsWith(`${selectedYear.value}-${selectedMonth.value}`)
        )

        const dayMap = new Map()
        monthData.forEach(item => {
          const day = item.date.split('-')[2]
          const current = dayMap.get(day) || 0
          dayMap.set(day, current + item.amount)
        })

        return Array.from(dayMap.entries())
          .map(([day, amount]) => ({ period: `${day}일`, amount }))
          .sort((a, b) => parseInt(b.period) - parseInt(a.period))
          .slice(0, 10)

      } else if (selectedMonth.value) {
        // 월별 선택시 - 해당 연도의 월별 데이터 (최신순)
        const yearData = allExpenseData.value.filter(item =>
          item.date.startsWith(selectedYear.value)
        )

        const monthMap = new Map()
        yearData.forEach(item => {
          const month = item.date.split('-')[1]
          const current = monthMap.get(month) || 0
          monthMap.set(month, current + item.amount)
        })

        return Array.from(monthMap.entries())
          .map(([month, amount]) => ({ period: `${parseInt(month)}월`, amount }))
          .sort((a, b) => parseInt(b.period) - parseInt(a.period))

      } else if (selectedYear.value) {
        // 연도별 선택시 - 연도별 데이터 (최신순)
        const yearMap = new Map()
        allExpenseData.value.forEach(item => {
          const year = item.date.split('-')[0]
          const current = yearMap.get(year) || 0
          yearMap.set(year, current + item.amount)
        })

        return Array.from(yearMap.entries())
          .map(([year, amount]) => ({ period: `${year}년`, amount }))
          .sort((a, b) => parseInt(b.period) - parseInt(a.period))
      }

      return []
    })

    const maxTrendAmount = computed(() =>
      Math.max(...filteredTrendData.value.map(d => d.amount), 1)
    )

    // 이벤트 핸들러
    const onYearChange = () => {
      selectedMonth.value = ''
      selectedDay.value = ''
    }

    const onMonthChange = () => {
      selectedDay.value = ''
    }

    const onDayChange = () => {
      // 일 변경시 추가 로직 필요시 구현
    }

    const onCategoryChange = () => {
      // 카테고리 변경시 추가 로직 필요시 구현
    }

    // 헬퍼 함수들
    const getCurrentPeriodTitle = () => {
      if (selectedDay.value) {
        return `${selectedYear.value}년 ${parseInt(selectedMonth.value)}월 ${parseInt(selectedDay.value)}일 리포트`
      } else if (selectedMonth.value) {
        return `${selectedYear.value}년 ${parseInt(selectedMonth.value)}월 리포트`
      } else if (selectedYear.value) {
        return `${selectedYear.value}년 리포트`
      }
      return '전체 리포트'
    }

    const getPeriodDescription = () => {
      const count = filteredDetailData.value.length
      if (selectedDay.value) {
        return `선택한 날짜의 지출 내역 ${count}건`
      } else if (selectedMonth.value) {
        return `선택한 월의 지출 내역 ${count}건`
      } else if (selectedYear.value) {
        return `선택한 연도의 지출 내역 ${count}건`
      }
      return `전체 지출 내역 ${count}건`
    }

    const getExportButtonText = () => {
      if (selectedDay.value) return '일별 리포트 CSV 내보내기'
      if (selectedMonth.value) return '월별 리포트 CSV 내보내기'
      if (selectedYear.value) return '연간 리포트 CSV 내보내기'
      return '전체 리포트 CSV 내보내기'
    }

    const getPreviousPeriodText = () => {
      if (selectedDay.value) return '전일'
      if (selectedMonth.value) return '전월'
      if (selectedYear.value) return '전년'
      return '이전 기간'
    }

    const getAverageText = () => {
      if (selectedDay.value) return '일일 지출'
      if (selectedMonth.value) return '일일 지출'
      if (selectedYear.value) return '월별 지출'
      return '지출'
    }

    const getAverageDescription = () => {
      if (selectedDay.value) return '해당 일의 총 지출'
      if (selectedMonth.value) return '해당 월의 일평균'
      if (selectedYear.value) return '해당 연도의 월평균'
      return '전체 평균'
    }

    const getTransactionDescription = () => {
      if (selectedDay.value) return '해당 일의 거래'
      if (selectedMonth.value) return '해당 월의 거래'
      if (selectedYear.value) return '해당 연도의 거래'
      return '전체 거래'
    }

    const getBudgetStatusText = () => {
      const usage = currentData.value.budgetUsage
      if (usage > 90) return '예산 초과 위험'
      if (usage > 80) return '예산 사용 주의'
      if (usage < 50) return '예산 여유'
      return '정상 범위'
    }

    const getChartTitle = (type) => {
      const period = selectedDay.value ? '일별' : selectedMonth.value ? '월별' : selectedYear.value ? '연간' : '전체'
      if (type === 'department') {
        return `${period} 부서별 지출 현황`
      } else if (type === 'trend') {
        if (selectedDay.value) return '해당 월 일별 지출 추이'
        if (selectedMonth.value) return '해당 연도 월별 지출 추이'
        if (selectedYear.value) return '연도별 지출 추이'
        return '전체 지출 추이'
      }
      return ''
    }

    const formatDate = (dateString) => {
      const date = new Date(dateString)
      return date.toLocaleDateString('ko-KR', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        weekday: 'short'
      })
    }

    const exportAsCSV = () => {
      const reportType = selectedDay.value ? '일별' : selectedMonth.value ? '월별' : selectedYear.value ? '연간' : '전체'
      const period = getCurrentPeriodTitle()

      const csvContent = generateExcelCSV() // Excel 호환 CSV 사용 (한글 깨짐 방지)
      downloadExcelCSV(csvContent, `${reportType}_리포트_${period}.csv`)

      setTimeout(() => {
        alert(`${reportType} CSV 리포트를 내보냈습니다.`)
      }, 500)
    }



    const generateExcelCSV = () => {
      // Excel에서 한글이 깨지지 않도록 특별히 처리
      const headers = ['날짜', '카테고리', '부서', '내용', '금액(원)']

      // 리포트 정보 추가
      const reportInfo = [
        [`리포트 생성일: ${new Date().toLocaleDateString('ko-KR')}`],
        [`리포트 유형: ${selectedDay.value ? '일별' : selectedMonth.value ? '월별' : selectedYear.value ? '연간' : '전체'}`],
        [`대상 기간: ${getCurrentPeriodTitle()}`],
        [`총 지출: ₩${currentData.value.totalExpense.toLocaleString()}`],
        [`거래 건수: ${currentData.value.transactionCount}건`],
        [''], // 빈 줄
        headers
      ]

      const rows = filteredDetailData.value.map(item => [
        item.date,
        item.category,
        item.department,
        item.description.replace(/"/g, '""'), // 따옴표 이스케이프
        `₩${item.amount.toLocaleString()}`
      ])

      const allRows = [...reportInfo, ...rows]
      return allRows.map(row =>
        row.map(cell => `"${cell}"`).join(',')
      ).join('\r\n')
    }

    const downloadCSV = (content, filename) => {
      // UTF-8 BOM 추가로 한글 깨짐 방지
      const BOM = '\uFEFF'
      const blob = new Blob([BOM + content], {
        type: 'text/csv;charset=utf-8;'
      })

      const link = document.createElement('a')
      const url = URL.createObjectURL(blob)
      link.setAttribute('href', url)
      link.setAttribute('download', filename)
      link.style.visibility = 'hidden'
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      URL.revokeObjectURL(url)
    }

    const downloadExcelCSV = (content, filename) => {
      // Excel 전용 UTF-8 BOM과 인코딩
      const BOM = '\uFEFF'
      const blob = new Blob([BOM + content], {
        type: 'application/vnd.ms-excel;charset=utf-8;'
      })

      const link = document.createElement('a')
      const url = URL.createObjectURL(blob)
      link.setAttribute('href', url)
      link.setAttribute('download', filename)
      link.style.visibility = 'hidden'
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      URL.revokeObjectURL(url)
    }



    return {
      selectedYear,
      selectedMonth,
      selectedDay,
      selectedCategory,
      availableYears,
      availableMonths,
      availableDays,
      availableCategories,
      filteredDetailData,
      currentData,
      filteredDepartmentData,
      maxDepartmentAmount,
      filteredCategoryData,
      totalFilteredCategoryAmount,
      filteredTrendData,
      maxTrendAmount,
      onYearChange,
      onMonthChange,
      onDayChange,
      onCategoryChange,
      getCurrentPeriodTitle,
      getPeriodDescription,
      getExportButtonText,
      getPreviousPeriodText,
      getAverageText,
      getAverageDescription,
      getTransactionDescription,
      getBudgetStatusText,
      getChartTitle,
      formatDate,
      exportAsCSV
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
  align-items: flex-start;
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
  flex-direction: column;
  gap: 1.2rem;
  align-items: flex-end;
}

.date-filters {
  display: flex;
  gap: 0.8rem;
  flex-wrap: wrap;
  align-items: center;
}

.date-filters::before {
  content: '📅';
  font-size: 1.2rem;
  margin-right: 0.5rem;
}

.date-select,
.category-select {
  padding: 10px 14px;
  border: 2px solid #ddd;
  border-radius: 8px;
  background: white;
  color: #2c3e50;
  font-size: 1rem;
  font-weight: 500;
  min-width: 140px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.date-select:hover,
.category-select:hover {
  border-color: #1976d2;
  box-shadow: 0 2px 4px rgba(25, 118, 210, 0.1);
}

.date-select:focus,
.category-select:focus {
  outline: none;
  border-color: #1976d2;
  box-shadow: 0 0 0 3px rgba(25, 118, 210, 0.1);
}

.date-select:disabled {
  background: #f8f9fa;
  color: #6c757d;
  border-color: #e9ecef;
  cursor: not-allowed;
}

.date-select option,
.category-select option {
  color: #2c3e50;
  background: white;
  padding: 8px;
}

.category-filter {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.category-filter::before {
  content: '🏷️';
  font-size: 1.2rem;
}

.export-btn {
  background: #4caf50;
  color: white;
  border: none;
  padding: 12px 20px;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s ease;
  white-space: nowrap;
}

.export-btn:hover {
  background: #45a049;
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(76, 175, 80, 0.3);
}

.report-info {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  margin-bottom: 2rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.current-period h3 {
  color: #2c3e50;
  margin: 0 0 0.5rem 0;
  font-size: 1.3rem;
}

.period-description {
  color: #666;
  margin: 0;
  font-size: 1rem;
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

.amount {
  font-size: 1.8rem;
  font-weight: bold;
  margin: 0 0 0.25rem 0;
  color: #2c3e50;
}

.trend {
  font-size: 0.8rem;
  color: #666;
}

.trend.trend-up {
  color: #f44336;
}

.trend.trend-down {
  color: #4caf50;
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

.dept-amount {
  font-weight: 600;
  color: #1976d2;
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

.trend-chart {
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
  gap: 0.5rem;
}

.trend-bar {
  display: flex;
  flex-direction: column;
  align-items: center;
  flex: 1;
  height: 100%;
  max-width: 60px;
}

.bar {
  width: 100%;
  background: linear-gradient(to top, #1976d2, #42a5f5);
  border-radius: 4px 4px 0 0;
  margin-bottom: 0.5rem;
  transition: height 0.3s ease;
  min-height: 4px;
}

.period-label {
  font-size: 0.8rem;
  color: #666;
  font-weight: 500;
  margin-bottom: 0.25rem;
}

.amount-label {
  font-size: 0.7rem;
  color: #999;
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
  margin-bottom: 0.5rem;
}

.category-details .progress-bar {
  flex: 1;
}

.percentage {
  font-size: 0.9rem;
  color: #666;
  font-weight: 500;
  min-width: 40px;
}

.category-trend {
  text-align: right;
}

.trend-indicator {
  font-size: 0.8rem;
  font-weight: 600;
}

.trend-indicator.trend-up {
  color: #f44336;
}

.trend-indicator.trend-down {
  color: #4caf50;
}

.detail-list {
  max-height: 400px;
  overflow-y: auto;
}

.detail-header {
  display: grid;
  grid-template-columns: 100px 100px 120px 1fr 120px;
  gap: 1rem;
  padding: 1rem;
  background: #f8f9fa;
  font-weight: 600;
  color: #2c3e50;
  border-bottom: 1px solid #e0e0e0;
  position: sticky;
  top: 0;
}

.detail-body {
  display: flex;
  flex-direction: column;
}

.detail-row {
  display: grid;
  grid-template-columns: 100px 100px 120px 1fr 120px;
  gap: 1rem;
  padding: 1rem;
  border-bottom: 1px solid #f0f0f0;
  align-items: center;
  transition: background 0.2s ease;
}

.detail-row:hover {
  background: #f8f9fa;
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

.category-tag.식비 {
  background: #ff9800;
}

.category-tag.교통비 {
  background: #2196f3;
}

.category-tag.사무용품 {
  background: #4caf50;
}

.category-tag.마케팅 {
  background: #9c27b0;
}

.category-tag.인건비 {
  background: #f44336;
}

.category-tag.임대료 {
  background: #795548;
}

.category-tag.기타 {
  background: #607d8b;
}

.col-department {
  color: #666;
  font-size: 0.9rem;
}

.col-description {
  font-weight: 500;
}

.col-amount {
  font-weight: 600;
  color: #f44336;
  text-align: right;
}

/* 반응형 디자인 */
@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    align-items: stretch;
  }

  .header-actions {
    align-items: stretch;
  }

  .date-filters {
    flex-direction: column;
    align-items: stretch;
  }

  .date-filters::before {
    align-self: flex-start;
    margin-bottom: 0.5rem;
  }

  .date-select,
  .category-select {
    width: 100%;
    padding: 12px 16px;
    font-size: 1.1rem;
  }

  .export-dropdown {
    width: 100%;
  }

  .export-btn {
    width: 100%;
    min-width: auto;
  }

  .export-menu {
    position: fixed;
    top: auto;
    left: 15px;
    right: 15px;
    width: auto;
    border-radius: 8px;
    border: 2px solid #4caf50;
  }

  .export-dropdown.active .export-btn {
    border-radius: 8px;
  }

  .report-overview {
    grid-template-columns: 1fr;
  }

  .charts-section {
    grid-template-columns: 1fr;
  }

  .detailed-reports {
    grid-template-columns: 1fr;
  }

  .detail-header {
    display: none;
  }

  .detail-row {
    display: block;
    padding: 1rem;
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    margin-bottom: 0.5rem;
  }

  .detail-row>span {
    display: block;
    margin-bottom: 0.5rem;
  }

  .detail-row>span:before {
    content: attr(class);
    font-weight: 600;
    color: #666;
    font-size: 0.8rem;
    display: inline-block;
    width: 80px;
  }

  .col-date:before {
    content: '날짜: ';
  }

  .col-category:before {
    content: '카테고리: ';
  }

  .col-department:before {
    content: '부서: ';
  }

  .col-description:before {
    content: '내용: ';
  }

  .col-amount:before {
    content: '금액: ';
  }
}

@media (max-width: 480px) {
  .overview-card {
    flex-direction: column;
    text-align: center;
  }

  .card-icon {
    margin: 0 0 1rem 0;
  }

  .chart-container {
    padding: 1rem;
  }

  .trend-chart {
    height: 150px;
  }
}
</style>