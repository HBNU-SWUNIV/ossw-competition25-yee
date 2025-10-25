<template>
  <div class="space-y-8">
    <!-- 페이지 헤더 -->
    <div class="flex flex-col lg:flex-row lg:items-start lg:justify-between gap-6">
      <h2 class="text-2xl sm:text-3xl font-bold text-gray-900">리포트</h2>
      <div class="flex flex-col xl:flex-row gap-4">
        <!-- 날짜 필터 -->
        <div class="flex flex-col sm:flex-row gap-3">
          <select v-model="selectedYear" @change="onYearChange" class="input-field w-full sm:w-32">
            <option value="">연도 선택</option>
            <option v-for="year in availableYears" :key="year" :value="year">{{ year }}년</option>
          </select>
          <select v-model="selectedMonth" @change="onMonthChange" class="input-field w-full sm:w-32" :disabled="!selectedYear">
            <option value="">월 선택</option>
            <option v-for="month in availableMonths" :key="month.value" :value="month.value">{{ month.label }}</option>
          </select>
          <select v-model="selectedDay" @change="onDayChange" class="input-field w-full sm:w-32" :disabled="!selectedMonth">
            <option value="">일 선택</option>
            <option v-for="day in availableDays" :key="day" :value="day">{{ day }}일</option>
          </select>
        </div>

        <!-- 카테고리 필터 -->
        <select v-model="selectedCategory" @change="onCategoryChange" class="input-field w-full sm:w-48">
          <option value="">전체 카테고리</option>
          <option v-for="category in availableCategories" :key="category" :value="category">{{ category }}</option>
        </select>

        <!-- 내보내기 드롭다운 -->
        <div class="relative" :class="{ 'z-50': showExportMenu }">
          <button 
            class="btn-primary flex items-center gap-2 w-full sm:w-auto"
            @click="toggleExportMenu"
          >
            <span class="text-lg">📊</span>
            {{ getExportButtonText() }}
            <span class="text-sm transition-transform duration-200" :class="{ 'rotate-180': showExportMenu }">▼</span>
          </button>

          <div v-if="showExportMenu" class="absolute top-full left-0 right-0 mt-2 bg-white border-2 border-primary-500 rounded-lg shadow-strong overflow-hidden">
            <div class="p-2 space-y-1">
              <button 
                class="w-full flex items-center gap-3 p-3 hover:bg-gray-50 rounded-lg transition-colors duration-200"
                @click="exportAsPDF"
              >
                <span class="text-xl">📄</span>
                <div class="text-left">
                  <div class="font-semibold text-gray-900">PDF 리포트</div>
                  <div class="text-sm text-gray-600">완전한 시각적 리포트</div>
                </div>
              </button>

              <button 
                class="w-full flex items-center gap-3 p-3 hover:bg-gray-50 rounded-lg transition-colors duration-200"
                @click="exportAsExcelCSV"
              >
                <span class="text-xl">📊</span>
                <div class="text-left">
                  <div class="font-semibold text-gray-900">Excel 호환 CSV</div>
                  <div class="text-sm text-gray-600">Excel에서 한글 깨짐 없음</div>
                </div>
              </button>

              <button 
                class="w-full flex items-center gap-3 p-3 hover:bg-gray-50 rounded-lg transition-colors duration-200"
                @click="exportAsCSV"
              >
                <span class="text-xl">📋</span>
                <div class="text-left">
                  <div class="font-semibold text-gray-900">일반 CSV</div>
                  <div class="text-sm text-gray-600">범용적인 데이터 형식</div>
                </div>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 리포트 정보 -->
    <div class="card p-6">
      <div class="text-center">
        <h3 class="text-xl font-semibold text-gray-900 mb-2">{{ getCurrentPeriodTitle() }}</h3>
        <p class="text-gray-600">{{ getPeriodDescription() }}</p>
      </div>
    </div>

    <!-- 요약 카드 -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      <div class="card p-6 hover:shadow-medium transition-shadow duration-200">
        <div class="flex items-center gap-4">
          <div class="text-4xl">💰</div>
          <div class="flex-1">
            <h3 class="text-sm font-medium text-gray-600 mb-1">총 지출</h3>
            <p class="text-2xl font-bold text-gray-900">₩{{ currentData.totalExpense.toLocaleString() }}</p>
            <span 
              class="text-sm"
              :class="{ 
                'text-red-600': currentData.expenseChange > 0, 
                'text-green-600': currentData.expenseChange < 0,
                'text-gray-600': currentData.expenseChange === 0
              }"
            >
              {{ currentData.expenseChange > 0 ? '+' : '' }}{{ currentData.expenseChange }}% {{ getPreviousPeriodText() }} 대비
            </span>
          </div>
        </div>
      </div>

      <div class="card p-6 hover:shadow-medium transition-shadow duration-200">
        <div class="flex items-center gap-4">
          <div class="text-4xl">📊</div>
          <div class="flex-1">
            <h3 class="text-sm font-medium text-gray-600 mb-1">평균 {{ getAverageText() }}</h3>
            <p class="text-2xl font-bold text-gray-900">₩{{ currentData.averageExpense.toLocaleString() }}</p>
            <span class="text-sm text-gray-600">{{ getAverageDescription() }}</span>
          </div>
        </div>
      </div>

      <div class="card p-6 hover:shadow-medium transition-shadow duration-200">
        <div class="flex items-center gap-4">
          <div class="text-4xl">📈</div>
          <div class="flex-1">
            <h3 class="text-sm font-medium text-gray-600 mb-1">지출 건수</h3>
            <p class="text-2xl font-bold text-gray-900">{{ currentData.transactionCount }}건</p>
            <span class="text-sm text-gray-600">{{ getTransactionDescription() }}</span>
          </div>
        </div>
      </div>

      <div class="card p-6 hover:shadow-medium transition-shadow duration-200">
        <div class="flex items-center gap-4">
          <div class="text-4xl">🎯</div>
          <div class="flex-1">
            <h3 class="text-sm font-medium text-gray-600 mb-1">예산 대비</h3>
            <p class="text-2xl font-bold text-gray-900">{{ currentData.budgetUsage }}%</p>
            <span 
              class="text-sm"
              :class="{ 
                'text-red-600': currentData.budgetUsage > 80, 
                'text-green-600': currentData.budgetUsage < 50,
                'text-gray-600': currentData.budgetUsage >= 50 && currentData.budgetUsage <= 80
              }"
            >
              {{ getBudgetStatusText() }}
            </span>
          </div>
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
import { ref, computed, onMounted, onUnmounted } from 'vue'
import jsPDF from 'jspdf'

export default {
  name: 'Reports',
  setup() {
    // 날짜 선택 상태
    const selectedYear = ref('')
    const selectedMonth = ref('')
    const selectedDay = ref('')
    const selectedCategory = ref('')

    // 내보내기 메뉴 상태
    const showExportMenu = ref(false)

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
      if (selectedDay.value) return '일별 리포트 내보내기 (PDF/CSV)'
      if (selectedMonth.value) return '월별 리포트 내보내기 (PDF/CSV)'
      if (selectedYear.value) return '연간 리포트 내보내기 (PDF/CSV)'
      return '전체 리포트 내보내기 (PDF/CSV)'
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

    const toggleExportMenu = () => {
      showExportMenu.value = !showExportMenu.value
    }

    const closeExportMenu = () => {
      showExportMenu.value = false
    }

    // 외부 클릭 시 메뉴 닫기
    const handleClickOutside = (event) => {
      const exportDropdown = event.target.closest('.export-dropdown')
      if (!exportDropdown && showExportMenu.value) {
        closeExportMenu()
      }
    }

    onMounted(() => {
      document.addEventListener('click', handleClickOutside)
    })

    onUnmounted(() => {
      document.removeEventListener('click', handleClickOutside)
    })

    const exportAsPDF = () => {
      const reportType = selectedDay.value ? '일별' : selectedMonth.value ? '월별' : selectedYear.value ? '연간' : '전체'
      const period = getCurrentPeriodTitle()

      generatePDF(reportType, period)
      closeExportMenu()

      setTimeout(() => {
        alert(`${reportType} PDF 리포트를 내보냈습니다.`)
      }, 500)
    }

    const exportAsExcelCSV = () => {
      const reportType = selectedDay.value ? '일별' : selectedMonth.value ? '월별' : selectedYear.value ? '연간' : '전체'
      const period = getCurrentPeriodTitle()

      const excelContent = generateExcelCSV()
      downloadExcelCSV(excelContent, `${reportType}_리포트_${period}.csv`)
      closeExportMenu()

      setTimeout(() => {
        alert(`${reportType} Excel 호환 CSV를 내보냈습니다.`)
      }, 500)
    }

    const exportAsCSV = () => {
      const reportType = selectedDay.value ? '일별' : selectedMonth.value ? '월별' : selectedYear.value ? '연간' : '전체'
      const period = getCurrentPeriodTitle()

      const csvContent = generateCSV()
      downloadCSV(csvContent, `${reportType}_리포트_${period}.csv`)
      closeExportMenu()

      setTimeout(() => {
        alert(`${reportType} 일반 CSV를 내보냈습니다.`)
      }, 500)
    }

    const generateCSV = () => {
      const headers = ['날짜', '카테고리', '부서', '내용', '금액']
      const rows = filteredDetailData.value.map(item => [
        item.date,
        item.category,
        item.department,
        `"${item.description}"`, // 쉼표가 포함된 내용을 위해 따옴표 추가
        item.amount.toLocaleString()
      ])

      return [headers, ...rows].map(row => row.join(',')).join('\n')
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

    const generatePDF = (reportType, period) => {
      try {
        // jsPDF 인스턴스 생성 (A4 세로)
        const doc = new jsPDF('p', 'mm', 'a4')

        let yPosition = 20
        const pageWidth = doc.internal.pageSize.getWidth()
        const margin = 20

        // 한글을 영문으로 변환하는 함수
        const translateToEnglish = (koreanText) => {
          const translations = {
            '일별': 'Daily',
            '월별': 'Monthly',
            '연간': 'Annual',
            '전체': 'Total',
            '리포트': 'Report',
            '생성일': 'Generated',
            '대상 기간': 'Period',
            '총 지출': 'Total Expense',
            '거래 건수': 'Transactions',
            '요약 통계': 'Summary Statistics',
            '평균': 'Average',
            '일일 지출': 'Daily Expense',
            '월별 지출': 'Monthly Expense',
            '예산 사용률': 'Budget Usage',
            '전일': 'Previous Day',
            '전월': 'Previous Month',
            '전년': 'Previous Year',
            '대비': 'vs',
            '부서별 지출 현황': 'Expense by Department',
            '카테고리별 지출 분석': 'Expense by Category',
            '상세 내역': 'Detailed Records',
            '최신': 'Latest',
            '건': 'items',
            '날짜': 'Date',
            '카테고리': 'Category',
            '부서': 'Department',
            '내용': 'Description',
            '금액': 'Amount',
            '마케팅팀': 'Marketing Team',
            '개발팀': 'Development Team',
            '영업팀': 'Sales Team',
            '인사팀': 'HR Team',
            '총무팀': 'General Affairs Team',
            '전체': 'All',
            '마케팅': 'Marketing',
            '사무용품': 'Office Supplies',
            '식비': 'Meals',
            '교통비': 'Transportation',
            '인건비': 'Personnel',
            '임대료': 'Rent',
            '기타': 'Others',
            '온라인 광고비': 'Online Advertising',
            '프린터 토너': 'Printer Toner',
            '팀 회식': 'Team Dinner',
            '출장비': 'Business Trip',
            '외부 강사비': 'External Instructor',
            '브로슈어 제작': 'Brochure Production',
            '노트북 구매': 'Laptop Purchase',
            '사무실 임대료': 'Office Rent',
            '회사 워크샵': 'Company Workshop',
            '고객 미팅': 'Client Meeting',
            '전시회 참가비': 'Exhibition Fee',
            '사무용 가구': 'Office Furniture',
            '교육비': 'Training Fee',
            '소셜미디어 광고': 'Social Media Ads',
            '개발 장비': 'Development Equipment',
            '연말 이벤트': 'Year-end Event'
          }

          let result = koreanText
          Object.keys(translations).forEach(korean => {
            result = result.replace(new RegExp(korean, 'g'), translations[korean])
          })
          return result
        }

        // 제목
        doc.setFontSize(20)
        doc.setFont('helvetica', 'bold')
        const title = translateToEnglish(`${reportType} 리포트`)
        const titleWidth = doc.getTextWidth(title)
        doc.text(title, (pageWidth - titleWidth) / 2, yPosition)

        yPosition += 15

        // 리포트 정보
        doc.setFontSize(12)
        doc.setFont('helvetica', 'normal')
        doc.text(translateToEnglish(`생성일: ${new Date().toLocaleDateString('en-US')}`), margin, yPosition)
        yPosition += 7
        doc.text(translateToEnglish(`대상 기간: ${period}`), margin, yPosition)
        yPosition += 7
        doc.text(`Total Expense: $${Math.round(currentData.value.totalExpense / 1300).toLocaleString()}`, margin, yPosition)
        yPosition += 7
        doc.text(`Transactions: ${currentData.value.transactionCount} items`, margin, yPosition)
        yPosition += 15

        // 구분선
        doc.setLineWidth(0.5)
        doc.line(margin, yPosition, pageWidth - margin, yPosition)
        yPosition += 10

        // 요약 통계
        doc.setFontSize(14)
        doc.setFont('helvetica', 'bold')
        doc.text('Summary Statistics', margin, yPosition)
        yPosition += 10

        doc.setFontSize(10)
        doc.setFont('helvetica', 'normal')

        const stats = [
          `Average ${translateToEnglish(getAverageText())}: $${Math.round(currentData.value.averageExpense / 1300).toLocaleString()}`,
          `Budget Usage: ${currentData.value.budgetUsage}%`,
          `vs ${translateToEnglish(getPreviousPeriodText())}: ${currentData.value.expenseChange > 0 ? '+' : ''}${currentData.value.expenseChange}%`
        ]

        stats.forEach(stat => {
          doc.text(stat, margin, yPosition)
          yPosition += 6
        })

        yPosition += 10

        // 부서별 지출 현황
        if (filteredDepartmentData.value.length > 0) {
          doc.setFontSize(14)
          doc.setFont('helvetica', 'bold')
          doc.text('Expense by Department', margin, yPosition)
          yPosition += 10

          doc.setFontSize(10)
          doc.setFont('helvetica', 'normal')

          filteredDepartmentData.value.slice(0, 10).forEach(dept => {
            const percentage = Math.round((dept.amount / maxDepartmentAmount.value) * 100)
            const translatedDept = translateToEnglish(dept.name)
            doc.text(`${translatedDept}: $${Math.round(dept.amount / 1300).toLocaleString()} (${percentage}%)`, margin, yPosition)
            yPosition += 6

            // 페이지 넘김 체크
            if (yPosition > 250) {
              doc.addPage()
              yPosition = 20
            }
          })

          yPosition += 10
        }

        // 카테고리별 지출 분석
        if (filteredCategoryData.value.length > 0) {
          // 페이지 넘김 체크
          if (yPosition > 200) {
            doc.addPage()
            yPosition = 20
          }

          doc.setFontSize(14)
          doc.setFont('helvetica', 'bold')
          doc.text('Expense by Category', margin, yPosition)
          yPosition += 10

          doc.setFontSize(10)
          doc.setFont('helvetica', 'normal')

          filteredCategoryData.value.forEach(category => {
            const percentage = Math.round((category.amount / totalFilteredCategoryAmount.value) * 100)
            const changeText = category.change > 0 ? `+${category.change}%` : category.change < 0 ? `${category.change}%` : '0%'
            const translatedCategory = translateToEnglish(category.name)
            doc.text(`${translatedCategory}: $${Math.round(category.amount / 1300).toLocaleString()} (${percentage}%) ${changeText}`, margin, yPosition)
            yPosition += 6

            // 페이지 넘김 체크
            if (yPosition > 250) {
              doc.addPage()
              yPosition = 20
            }
          })

          yPosition += 10
        }

        // 상세 내역 (최대 20건)
        if (filteredDetailData.value.length > 0) {
          // 페이지 넘김 체크
          if (yPosition > 180) {
            doc.addPage()
            yPosition = 20
          }

          doc.setFontSize(14)
          doc.setFont('helvetica', 'bold')
          doc.text('Detailed Records (Latest 20 items)', margin, yPosition)
          yPosition += 10

          // 테이블 헤더
          doc.setFontSize(9)
          doc.setFont('helvetica', 'bold')
          doc.text('Date', margin, yPosition)
          doc.text('Category', margin + 25, yPosition)
          doc.text('Department', margin + 55, yPosition)
          doc.text('Description', margin + 90, yPosition)
          doc.text('Amount($)', margin + 140, yPosition)
          yPosition += 5

          // 구분선
          doc.setLineWidth(0.3)
          doc.line(margin, yPosition, pageWidth - margin, yPosition)
          yPosition += 5

          doc.setFont('helvetica', 'normal')

          filteredDetailData.value.slice(0, 20).forEach(item => {
            const date = item.date.substring(5) // MM-DD 형식
            let description = translateToEnglish(item.description)
            if (description.length > 20) {
              description = description.substring(0, 20) + '...'
            }

            doc.text(date, margin, yPosition)
            doc.text(translateToEnglish(item.category), margin + 25, yPosition)
            doc.text(translateToEnglish(item.department), margin + 55, yPosition)
            doc.text(description, margin + 90, yPosition)
            doc.text(`$${Math.round(item.amount / 1300).toLocaleString()}`, margin + 140, yPosition)
            yPosition += 5

            // 페이지 넘김 체크
            if (yPosition > 270) {
              doc.addPage()
              yPosition = 20
            }
          })
        }

        // 페이지 번호 추가
        const pageCount = doc.internal.getNumberOfPages()
        for (let i = 1; i <= pageCount; i++) {
          doc.setPage(i)
          doc.setFontSize(8)
          doc.setFont('helvetica', 'normal')
          doc.text(`${i} / ${pageCount}`, pageWidth - 30, 285)
        }

        // PDF 다운로드
        const filename = `${translateToEnglish(reportType)}_Report_${new Date().toISOString().split('T')[0]}.pdf`
        doc.save(filename)

      } catch (error) {
        console.error('PDF generation error:', error)
        alert('PDF 생성 중 오류가 발생했습니다. 다시 시도해주세요.')
      }
    }

    return {
      selectedYear,
      selectedMonth,
      selectedDay,
      selectedCategory,
      showExportMenu,
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
      toggleExportMenu,
      closeExportMenu,
      exportAsPDF,
      exportAsExcelCSV,
      exportAsCSV
    }
  }
}
</script>
