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

    <!-- 차트 섹션 -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- 부서별 지출 차트 -->
      <div class="card p-6">
        <h3 class="text-xl font-semibold text-gray-900 mb-6">{{ getChartTitle('department') }}</h3>
        <div class="space-y-4">
          <div 
            v-for="(dept, index) in departmentData" 
            :key="index"
            class="space-y-2"
          >
            <div class="flex justify-between items-center">
              <span class="font-medium text-gray-900">{{ dept.name }}</span>
              <span class="font-semibold text-primary-600">₩{{ dept.amount.toLocaleString() }}</span>
              </div>
            <div class="w-full bg-gray-200 rounded-full h-2">
              <div 
                class="h-2 rounded-full bg-primary-600 transition-all duration-300"
                :style="{ width: Math.min((dept.amount / Math.max(...departmentData.map(d => d.amount)) * 100), 100) + '%' }"
              ></div>
            </div>
          </div>
        </div>
      </div>

      <!-- 트렌드 차트 -->
      <div class="card p-6">
        <h3 class="text-xl font-semibold text-gray-900 mb-6">{{ getChartTitle('trend') }}</h3>
        <div class="h-48 flex items-end justify-between gap-2">
          <div 
            v-for="(period, index) in trendData" 
            :key="index"
            class="flex flex-col items-center flex-1"
          >
            <div 
              class="w-full bg-gradient-to-t from-primary-600 to-primary-400 rounded-t transition-all duration-300 min-h-4"
              :style="{ height: (period.amount / Math.max(...trendData.map(p => p.amount)) * 100) + '%' }"
            ></div>
            <div class="text-xs text-gray-600 mt-2 text-center">
              <div class="font-medium">{{ period.label }}</div>
              <div class="text-gray-500">₩{{ period.amount.toLocaleString() }}</div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 상세 리포트 -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- 카테고리 분석 -->
      <div class="card p-6">
        <h3 class="text-xl font-semibold text-gray-900 mb-6">카테고리별 분석</h3>
        <div class="space-y-4">
          <div 
            v-for="(category, index) in categoryData" 
            :key="index"
            class="border border-gray-200 rounded-lg p-4"
          >
            <div class="flex justify-between items-center mb-2">
              <span class="font-medium text-gray-900">{{ category.name }}</span>
              <span class="font-semibold text-red-600">₩{{ category.amount.toLocaleString() }}</span>
            </div>
            <div class="flex items-center gap-4 mb-2">
              <div class="flex-1 bg-gray-200 rounded-full h-2">
                <div 
                  class="h-2 rounded-full bg-primary-600 transition-all duration-300"
                  :style="{ width: Math.min((category.amount / Math.max(...categoryData.map(c => c.amount)) * 100), 100) + '%' }"
                ></div>
                </div>
              <span class="text-sm font-medium text-gray-600">{{ Math.round((category.amount / categoryData.reduce((sum, c) => sum + c.amount, 0)) * 100) }}%</span>
              </div>
            <div class="text-right">
              <span 
                class="text-sm font-medium"
                :class="{ 
                  'text-red-600': category.trend > 0, 
                  'text-green-600': category.trend < 0,
                  'text-gray-600': category.trend === 0
                }"
              >
                {{ category.trend > 0 ? '+' : '' }}{{ category.trend }}%
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- 상세 내역 -->
      <div class="card p-6">
        <h3 class="text-xl font-semibold text-gray-900 mb-6">상세 내역</h3>
        <div class="max-h-96 overflow-y-auto">
          <!-- 데스크톱 테이블 -->
          <div class="hidden lg:block">
            <div class="grid grid-cols-5 gap-4 p-4 bg-gray-50 font-semibold text-gray-700 border-b">
              <div>날짜</div>
              <div>카테고리</div>
              <div>내용</div>
              <div>부서</div>
              <div class="text-right">금액</div>
            </div>
            <div class="divide-y divide-gray-200">
              <div 
                v-for="(expense, index) in detailedData" 
                :key="index"
                class="grid grid-cols-5 gap-4 p-4 hover:bg-gray-50 transition-colors duration-200"
              >
                <div class="text-sm text-gray-600">{{ formatDate(expense.date) }}</div>
                <div>
                  <span 
                    class="inline-block px-3 py-1 rounded-full text-xs font-medium text-white"
                    :class="{
                      'bg-orange-500': expense.category === '식비',
                      'bg-blue-500': expense.category === '교통비',
                      'bg-green-500': expense.category === '사무용품',
                      'bg-purple-500': expense.category === '마케팅',
                      'bg-red-500': expense.category === '인건비',
                      'bg-yellow-600': expense.category === '임대료',
                      'bg-gray-500': expense.category === '기타'
                    }"
                  >
                    {{ expense.category }}
                  </span>
            </div>
                <div class="font-medium">{{ expense.description }}</div>
                <div class="text-sm text-gray-600">{{ expense.department }}</div>
                <div class="text-right font-semibold text-red-600">₩{{ expense.amount.toLocaleString() }}</div>
          </div>
        </div>
      </div>

          <!-- 모바일 카드 -->
          <div class="lg:hidden space-y-4">
            <div 
              v-for="(expense, index) in detailedData" 
              :key="index"
              class="border border-gray-200 rounded-lg p-4 hover:shadow-soft transition-shadow duration-200"
            >
              <div class="flex justify-between items-start mb-3">
                <div>
                  <h4 class="font-semibold text-gray-900">{{ expense.description }}</h4>
                  <p class="text-sm text-gray-600">{{ expense.department }}</p>
          </div>
                <span class="text-lg font-bold text-red-600">₩{{ expense.amount.toLocaleString() }}</span>
              </div>
              <div class="flex justify-between items-center">
                <span class="text-sm text-gray-600">{{ formatDate(expense.date) }}</span>
                <span 
                  class="inline-block px-3 py-1 rounded-full text-xs font-medium text-white"
                  :class="{
                    'bg-orange-500': expense.category === '식비',
                    'bg-blue-500': expense.category === '교통비',
                    'bg-green-500': expense.category === '사무용품',
                    'bg-purple-500': expense.category === '마케팅',
                    'bg-red-500': expense.category === '인건비',
                    'bg-yellow-600': expense.category === '임대료',
                    'bg-gray-500': expense.category === '기타'
                  }"
                >
                  {{ expense.category }}
              </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import jsPDF from 'jspdf'
import html2canvas from 'html2canvas'

export default {
  name: 'Reports',
  setup() {
    // 반응형 데이터
    const selectedYear = ref('')
    const selectedMonth = ref('')
    const selectedDay = ref('')
    const selectedCategory = ref('')
    const showExportMenu = ref(false)

    // 사용 가능한 옵션들
    const availableYears = ref([2024, 2023, 2022])
    const availableMonths = ref([
      { value: 1, label: '1월' },
      { value: 2, label: '2월' },
      { value: 3, label: '3월' },
      { value: 4, label: '4월' },
      { value: 5, label: '5월' },
      { value: 6, label: '6월' },
      { value: 7, label: '7월' },
      { value: 8, label: '8월' },
      { value: 9, label: '9월' },
      { value: 10, label: '10월' },
      { value: 11, label: '11월' },
      { value: 12, label: '12월' }
    ])
    const availableDays = ref([])
    const availableCategories = ref(['식비', '교통비', '사무용품', '마케팅', '인건비', '임대료', '기타'])

    // 현재 데이터 (실제로는 API에서 가져올 데이터)
    const currentData = ref({
      totalExpense: 12500000,
      averageExpense: 1250000,
      transactionCount: 45,
      budgetUsage: 75,
      expenseChange: 12
    })

    // 차트 데이터
    const departmentData = ref([
      { name: '개발팀', amount: 4500000 },
      { name: '마케팅팀', amount: 3200000 },
      { name: '영업팀', amount: 2800000 },
      { name: '인사팀', amount: 2000000 }
    ])

    const trendData = ref([
      { label: '1월', amount: 1200000 },
      { label: '2월', amount: 1500000 },
      { label: '3월', amount: 1100000 },
      { label: '4월', amount: 1800000 },
      { label: '5월', amount: 1600000 },
      { label: '6월', amount: 1900000 }
    ])

    const categoryData = ref([
      { name: '식비', amount: 3500000, trend: 5 },
      { name: '교통비', amount: 2800000, trend: -2 },
      { name: '사무용품', amount: 2200000, trend: 8 },
      { name: '마케팅', amount: 4000000, trend: 15 }
    ])

    const detailedData = ref([
      { date: '2024-01-15', category: '식비', description: '팀 회식비', department: '개발팀', amount: 150000 },
      { date: '2024-01-14', category: '교통비', description: '택시비', department: '마케팅팀', amount: 25000 },
      { date: '2024-01-13', category: '사무용품', description: '문구류 구매', department: '인사팀', amount: 80000 },
      { date: '2024-01-12', category: '마케팅', description: '광고비', department: '마케팅팀', amount: 500000 }
    ])

    // 계산된 속성들
    const getCurrentPeriodTitle = () => {
      if (selectedYear.value && selectedMonth.value && selectedDay.value) {
        return `${selectedYear.value}년 ${selectedMonth.value}월 ${selectedDay.value}일 리포트`
      } else if (selectedYear.value && selectedMonth.value) {
        return `${selectedYear.value}년 ${selectedMonth.value}월 리포트`
      } else if (selectedYear.value) {
        return `${selectedYear.value}년 리포트`
      }
      return '전체 기간 리포트'
    }

    const getPeriodDescription = () => {
      if (selectedYear.value && selectedMonth.value && selectedDay.value) {
        return '선택된 날짜의 상세 지출 내역을 확인하세요.'
      } else if (selectedYear.value && selectedMonth.value) {
        return '선택된 월의 지출 현황과 트렌드를 분석합니다.'
      } else if (selectedYear.value) {
        return '선택된 연도의 전체 지출 현황을 종합 분석합니다.'
      }
      return '모든 기간의 지출 데이터를 종합적으로 분석합니다.'
    }

    const getAverageText = () => {
      if (selectedYear.value && selectedMonth.value && selectedDay.value) {
        return '일일 평균'
      } else if (selectedYear.value && selectedMonth.value) {
        return '일일 평균'
      } else if (selectedYear.value) {
        return '월 평균'
      }
      return '월 평균'
    }

    const getAverageDescription = () => {
      if (selectedYear.value && selectedMonth.value && selectedDay.value) {
        return '해당 날짜 기준'
      } else if (selectedYear.value && selectedMonth.value) {
        return '해당 월 기준'
      } else if (selectedYear.value) {
        return '해당 연도 기준'
      }
      return '전체 기간 기준'
    }

    const getTransactionDescription = () => {
      if (selectedYear.value && selectedMonth.value && selectedDay.value) {
        return '해당 날짜 거래'
      } else if (selectedYear.value && selectedMonth.value) {
        return '해당 월 거래'
      } else if (selectedYear.value) {
        return '해당 연도 거래'
      }
      return '전체 거래'
    }

    const getPreviousPeriodText = () => {
      if (selectedYear.value && selectedMonth.value && selectedDay.value) {
        return '전일'
      } else if (selectedYear.value && selectedMonth.value) {
        return '전월'
      } else if (selectedYear.value) {
        return '전년'
      }
      return '전기'
    }

    const getBudgetStatusText = () => {
      const usage = currentData.value.budgetUsage
      if (usage > 90) return '예산 초과 위험'
      if (usage > 80) return '예산 부족 경고'
      if (usage > 50) return '적정 수준'
      return '여유 있음'
    }

    const getChartTitle = (type) => {
      if (type === 'department') {
        return '부서별 지출 현황'
      } else if (type === 'trend') {
        return '지출 트렌드'
      }
      return '차트'
    }

    const getExportButtonText = () => {
      return '리포트 내보내기'
    }

    // 이벤트 핸들러들
    const onYearChange = () => {
      selectedMonth.value = ''
      selectedDay.value = ''
      updateAvailableDays()
    }

    const onMonthChange = () => {
      selectedDay.value = ''
      updateAvailableDays()
    }

    const onDayChange = () => {
      // 일 변경 시 처리
    }

    const onCategoryChange = () => {
      // 카테고리 변경 시 처리
    }

    const toggleExportMenu = () => {
      showExportMenu.value = !showExportMenu.value
    }

    const updateAvailableDays = () => {
      if (selectedYear.value && selectedMonth.value) {
        const daysInMonth = new Date(selectedYear.value, selectedMonth.value, 0).getDate()
        availableDays.value = Array.from({ length: daysInMonth }, (_, i) => i + 1)
      } else {
        availableDays.value = []
      }
    }

    const formatDate = (dateString) => {
      const date = new Date(dateString)
      return date.toLocaleDateString('ko-KR')
    }

    // 내보내기 함수들
    const exportAsPDF = async () => {
      try {
        const element = document.querySelector('.space-y-8')
        const canvas = await html2canvas(element)
        const imgData = canvas.toDataURL('image/png')
        
        const pdf = new jsPDF()
        const imgWidth = 210
        const pageHeight = 295
        const imgHeight = (canvas.height * imgWidth) / canvas.width
        let heightLeft = imgHeight

        let position = 0

        pdf.addImage(imgData, 'PNG', 0, position, imgWidth, imgHeight)
        heightLeft -= pageHeight

        while (heightLeft >= 0) {
          position = heightLeft - imgHeight
          pdf.addPage()
          pdf.addImage(imgData, 'PNG', 0, position, imgWidth, imgHeight)
          heightLeft -= pageHeight
        }

        pdf.save('expense-report.pdf')
        showExportMenu.value = false
      } catch (error) {
        console.error('PDF 생성 중 오류:', error)
        alert('PDF 생성 중 오류가 발생했습니다.')
      }
    }

    const exportAsExcelCSV = () => {
      const csvContent = generateCSVContent()
      const blob = new Blob(['\ufeff' + csvContent], { type: 'text/csv;charset=utf-8;' })
      const link = document.createElement('a')
      link.href = URL.createObjectURL(blob)
      link.download = 'expense-report-excel.csv'
      link.click()
      showExportMenu.value = false
    }

    const exportAsCSV = () => {
      const csvContent = generateCSVContent()
      const blob = new Blob([csvContent], { type: 'text/csv' })
      const link = document.createElement('a')
      link.href = URL.createObjectURL(blob)
      link.download = 'expense-report.csv'
      link.click()
      showExportMenu.value = false
    }

    const generateCSVContent = () => {
      const headers = ['날짜', '카테고리', '내용', '부서', '금액']
      const rows = detailedData.value.map(expense => [
        expense.date,
        expense.category,
        expense.description,
        expense.department,
        expense.amount
      ])
      
      return [headers, ...rows].map(row => row.join(',')).join('\n')
    }

    // 컴포넌트 마운트 시 초기화
    onMounted(() => {
      const now = new Date()
      selectedYear.value = now.getFullYear().toString()
      selectedMonth.value = (now.getMonth() + 1).toString()
      updateAvailableDays()
    })

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
      currentData,
      departmentData,
      trendData,
      categoryData,
      detailedData,
      getCurrentPeriodTitle,
      getPeriodDescription,
      getAverageText,
      getAverageDescription,
      getTransactionDescription,
      getPreviousPeriodText,
      getBudgetStatusText,
      getChartTitle,
      getExportButtonText,
      onYearChange,
      onMonthChange,
      onDayChange,
      onCategoryChange,
      toggleExportMenu,
      formatDate,
      exportAsPDF,
      exportAsExcelCSV,
      exportAsCSV
    }
  }
}
</script>