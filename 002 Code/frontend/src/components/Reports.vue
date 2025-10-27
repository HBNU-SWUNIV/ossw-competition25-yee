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
          <select v-model="selectedMonth" @change="onMonthChange" class="input-field w-full sm:w-32"
            :disabled="!selectedYear">
            <option value="">월 선택</option>
            <option v-for="month in availableMonths" :key="month.value" :value="month.value">{{ month.label }}</option>
          </select>
          <select v-model="selectedDay" @change="onDayChange" class="input-field w-full sm:w-32"
            :disabled="!selectedMonth">
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
          <button class="btn-primary flex items-center gap-2 w-full sm:w-auto" @click="toggleExportMenu">
            {{ getExportButtonText() }}
            <span class="text-sm transition-transform duration-200" :class="{ 'rotate-180': showExportMenu }">▼</span>
          </button>

          <div v-if="showExportMenu"
            class="absolute top-full left-0 right-0 mt-2 bg-white border-2 border-primary-500 rounded-lg shadow-strong overflow-hidden">
            <div class="p-2 space-y-1">
              <button
                class="w-full flex items-center gap-3 p-3 hover:bg-gray-50 rounded-lg transition-colors duration-200"
                @click="exportSelectedAsExcelCSV">
                <div
                  class="w-8 h-8 bg-blue-100 rounded-lg flex items-center justify-center text-blue-600 font-bold text-sm">
                  CSV
                </div>
                <div class="text-left">
                  <div class="font-semibold text-gray-900">선택 항목 Excel CSV</div>
                  <div class="text-sm text-gray-600">선택한 항목만 내보내기</div>
                </div>
              </button>

              <button
                class="w-full flex items-center gap-3 p-3 hover:bg-gray-50 rounded-lg transition-colors duration-200"
                @click="exportSelectedAsPDF">
                <div
                  class="w-8 h-8 bg-red-100 rounded-lg flex items-center justify-center text-red-600 font-bold text-sm">
                  PDF
                </div>
                <div class="text-left">
                  <div class="font-semibold text-gray-900">선택 항목 PDF</div>
                  <div class="text-sm text-gray-600">선택한 항목만 PDF로</div>
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
        <div>
          <h3 class="text-sm font-medium text-gray-600 mb-1">총 지출</h3>
          <p class="text-2xl font-bold text-gray-900">₩{{ currentData.totalExpense.toLocaleString() }}</p>
          <span class="text-sm" :class="{
            'text-red-600': currentData.expenseChange > 0,
            'text-green-600': currentData.expenseChange < 0,
            'text-gray-600': currentData.expenseChange === 0
          }">
            {{ currentData.expenseChange > 0 ? '+' : '' }}{{ currentData.expenseChange }}% {{ getPreviousPeriodText()
            }} 대비
          </span>
        </div>
      </div>

      <div class="card p-6 hover:shadow-medium transition-shadow duration-200">
        <div>
          <h3 class="text-sm font-medium text-gray-600 mb-1">평균 {{ getAverageText() }}</h3>
          <p class="text-2xl font-bold text-gray-900">₩{{ currentData.averageExpense.toLocaleString() }}</p>
          <span class="text-sm text-gray-600">{{ getAverageDescription() }}</span>
        </div>
      </div>
    </div>

    <div class="card p-6 hover:shadow-medium transition-shadow duration-200">
      <div>
        <h3 class="text-sm font-medium text-gray-600 mb-1">지출 건수</h3>
        <p class="text-2xl font-bold text-gray-900">{{ currentData.transactionCount }}건</p>
        <span class="text-sm text-gray-600">{{ getTransactionDescription() }}</span>
      </div>
    </div>

    <div class="card p-6 hover:shadow-medium transition-shadow duration-200">
      <div>
        <h3 class="text-sm font-medium text-gray-600 mb-1">예산 대비</h3>
        <p class="text-2xl font-bold text-gray-900">{{ currentData.budgetUsage }}%</p>
        <span class="text-sm" :class="{
          'text-red-600': currentData.budgetUsage > 80,
          'text-green-600': currentData.budgetUsage < 50,
          'text-gray-600': currentData.budgetUsage >= 50 && currentData.budgetUsage <= 80
        }">
          {{ getBudgetStatusText() }}
        </span>
      </div>
    </div>
  </div>

  <!-- 차트 섹션 -->
  <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
    <!-- 부서별 지출 차트 -->
    <div class="card p-6">
      <h3 class="text-xl font-semibold text-gray-900 mb-6">{{ getChartTitle('department') }}</h3>
      <div class="space-y-4">
        <div v-for="(dept, index) in departmentData" :key="index" class="space-y-2">
          <div class="flex justify-between items-center">
            <span class="font-medium text-gray-900">{{ dept.name }}</span>
            <span class="font-semibold text-primary-600">₩{{ dept.amount.toLocaleString() }}</span>
          </div>
          <div class="w-full bg-gray-200 rounded-full h-2">
            <div class="h-2 rounded-full bg-primary-600 transition-all duration-300"
              :style="{ width: Math.min((dept.amount / Math.max(...departmentData.map(d => d.amount)) * 100), 100) + '%' }">
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 트렌드 차트 -->
    <div class="card p-6">
      <h3 class="text-xl font-semibold text-gray-900 mb-6">{{ getChartTitle('trend') }}</h3>
      <div class="h-48 flex items-end justify-between gap-2">
        <div v-for="(period, index) in trendData" :key="index" class="flex flex-col items-center flex-1">
          <div
            class="w-full bg-gradient-to-t from-primary-600 to-primary-400 rounded-t transition-all duration-300 min-h-4"
            :style="{ height: (period.amount / Math.max(...trendData.map(p => p.amount)) * 100) + '%' }"></div>
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
        <div v-for="(category, index) in categoryData" :key="index" class="border border-gray-200 rounded-lg p-4">
          <div class="flex justify-between items-center mb-2">
            <span class="font-medium text-gray-900">{{ category.name }}</span>
            <span class="font-semibold text-red-600">₩{{ category.amount.toLocaleString() }}</span>
          </div>
          <div class="flex items-center gap-4 mb-2">
            <div class="flex-1 bg-gray-200 rounded-full h-2">
              <div class="h-2 rounded-full bg-primary-600 transition-all duration-300"
                :style="{ width: Math.min((category.amount / Math.max(...categoryData.map(c => c.amount)) * 100), 100) + '%' }">
              </div>
            </div>
            <span class="text-sm font-medium text-gray-600">{{Math.round((category.amount / categoryData.reduce((sum,
              c) => sum + c.amount, 0)) * 100)}}%</span>
          </div>
          <div class="text-right">
            <span class="text-sm font-medium" :class="{
              'text-red-600': category.trend > 0,
              'text-green-600': category.trend < 0,
              'text-gray-600': category.trend === 0
            }">
              {{ category.trend > 0 ? '+' : '' }}{{ category.trend }}%
            </span>
          </div>
        </div>
      </div>
    </div>

    <!-- 상세 내역 -->
    <div class="card p-6">
      <div class="flex justify-between items-center mb-6">
        <h3 class="text-xl font-semibold text-gray-900">상세 내역</h3>
        <div class="text-sm text-gray-600">
          선택: {{ selectedExpenses.length }}개
        </div>
      </div>
      <div class="max-h-96 overflow-y-auto">
        <!-- 데스크톱 테이블 -->
        <div class="hidden lg:block">
          <div class="grid grid-cols-7 gap-4 p-4 bg-gray-50 font-semibold text-gray-700 border-b">
            <div>
              <input type="checkbox" @change="toggleSelectAll" :checked="isAllSelected" class="rounded" />
            </div>
            <div>날짜</div>
            <div>카테고리</div>
            <div>내용</div>
            <div>상점명</div>
            <div>연락처</div>
            <div class="text-right">금액</div>
          </div>
          <div class="divide-y divide-gray-200">
            <div v-for="(expense, index) in detailedData" :key="index"
              class="grid grid-cols-7 gap-4 p-4 hover:bg-gray-50 transition-colors duration-200">
              <div>
                <input type="checkbox" v-model="selectedExpenses" :value="expense" class="rounded" />
              </div>
              <div class="text-sm text-gray-600">{{ formatDate(expense.date) }}</div>
              <div>
                <span class="inline-block px-3 py-1 rounded-full text-xs font-medium text-white" :class="{
                  'bg-orange-500': expense.category === '식비',
                  'bg-blue-500': expense.category === '교통비',
                  'bg-green-500': expense.category === '사무용품',
                  'bg-purple-500': expense.category === '회식',
                  'bg-red-500': expense.category === '공과금',
                  'bg-yellow-600': expense.category === '유흥',
                  'bg-indigo-500': expense.category === '교육',
                  'bg-pink-500': expense.category === '의료',
                  'bg-gray-500': expense.category === '기타'
                }">
                  {{ expense.category }}
                </span>
              </div>
              <div class="font-medium">{{ expense.description }}</div>
              <div class="text-sm">
                <div class="font-medium text-gray-900">{{ expense.department }}</div>
                <div v-if="expense.store_address" class="text-xs text-gray-500">{{ expense.store_address }}</div>
              </div>
              <div class="text-sm text-gray-600">{{ expense.store_phone_number || '-' }}</div>
              <div class="text-right font-semibold text-red-600">₩{{ expense.amount.toLocaleString() }}</div>
            </div>
          </div>
        </div>

        <!-- 모바일 카드 -->
        <div class="lg:hidden space-y-4">
          <div v-for="(expense, index) in detailedData" :key="index"
            class="border border-gray-200 rounded-lg p-4 hover:shadow-soft transition-shadow duration-200">
            <div class="flex justify-between items-start mb-3">
              <div class="flex items-start gap-3 flex-1">
                <input type="checkbox" v-model="selectedExpenses" :value="expense" class="rounded mt-1" />
                <div class="flex-1">
                  <h4 class="font-semibold text-gray-900">{{ expense.description }}</h4>
                  <p class="text-sm text-gray-700">{{ expense.department }}</p>
                  <p v-if="expense.store_address" class="text-xs text-gray-500 mt-1">{{ expense.store_address }}</p>
                  <p v-if="expense.store_phone_number" class="text-xs text-gray-500">{{ expense.store_phone_number }}
                  </p>
                </div>
              </div>
              <span class="text-lg font-bold text-red-600">₩{{ expense.amount.toLocaleString() }}</span>
            </div>
            <div class="flex justify-between items-center">
              <span class="text-sm text-gray-600">{{ formatDate(expense.date) }}</span>
              <span class="inline-block px-3 py-1 rounded-full text-xs font-medium text-white" :class="{
                'bg-orange-500': expense.category === '식비',
                'bg-blue-500': expense.category === '교통비',
                'bg-green-500': expense.category === '사무용품',
                'bg-purple-500': expense.category === '회식',
                'bg-red-500': expense.category === '공과금',
                'bg-yellow-600': expense.category === '유흥',
                'bg-indigo-500': expense.category === '교육',
                'bg-pink-500': expense.category === '의료',
                'bg-gray-500': expense.category === '기타'
              }">
                {{ expense.category }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, watch } from 'vue'
import jsPDF from 'jspdf'
import html2canvas from 'html2canvas'
import { expenseAPI } from '../services/api'

export default {
  name: 'Reports',
  setup() {
    // 반응형 데이터
    const selectedYear = ref('')
    const selectedMonth = ref('')
    const selectedDay = ref('')
    const selectedCategory = ref('')
    const showExportMenu = ref(false)
    const loading = ref(false)
    const selectedExpenses = ref([])
    const isAllSelected = ref(false)

    // 사용 가능한 옵션들
    const now = new Date()
    const availableYears = ref([now.getFullYear(), now.getFullYear() - 1, now.getFullYear() - 2])
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
    const availableCategories = ref(['식비', '사무용품', '회식', '교통비', '공과금', '유흥', '교육', '의료', '기타'])

    // API에서 가져온 데이터
    const statistics = ref(null)
    const expenses = ref([])
    const previousStatistics = ref(null)

    // 현재 데이터 (계산됨)
    const currentData = ref({
      totalExpense: 0,
      averageExpense: 0,
      transactionCount: 0,
      budgetUsage: 0,
      expenseChange: 0
    })

    // 차트 데이터 (계산됨)
    const departmentData = ref([])
    const trendData = ref([])
    const categoryData = ref([])
    const detailedData = ref([])

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
    // API 데이터 로드 함수
    const loadData = async () => {
      loading.value = true
      try {
        // 날짜 범위 계산
        const { start_date, end_date } = getDateRange()

        // 통계 데이터 가져오기
        const statsResult = await expenseAPI.getStatistics({
          start_date: start_date?.toISOString(),
          end_date: end_date?.toISOString()
        })

        statistics.value = statsResult

        // 카테고리 데이터 업데이트
        categoryData.value = statistics.value.by_category.map(cat => ({
          name: cat.category,
          amount: cat.total_amount,
          trend: 0 // 트렌드는 이전 기간 데이터와 비교해서 계산 필요
        }))

        // 현재 데이터 업데이트
        currentData.value = {
          totalExpense: statistics.value.total_amount || 0,
          averageExpense: calculateAverage(statistics.value.total_amount),
          transactionCount: statistics.value.total_count || 0,
          budgetUsage: 75, // TODO: 예산 기능 구현 시 실제 값으로 대체
          expenseChange: 0 // TODO: 이전 기간과 비교
        }

        // 상세 내역 가져오기
        const params = {
          start_date: start_date?.toISOString(),
          end_date: end_date?.toISOString(),
          limit: 1000
        }

        // category가 있을 때만 추가
        if (selectedCategory.value) {
          params.category = selectedCategory.value
        }

        const expensesResult = await expenseAPI.getAll(params)

        console.log('[Reports] expensesResult:', expensesResult)
        console.log('[Reports] expensesResult type:', typeof expensesResult, Array.isArray(expensesResult))

        expenses.value = expensesResult
        console.log('[Reports] expenses.value:', expenses.value)

        detailedData.value = expenses.value.map(exp => ({
          id: exp.id,
          date: exp.date,
          category: exp.category,
          description: exp.description || exp.item_name || exp.store_name,
          department: exp.store_name, // 부서 대신 상점명 사용
          amount: exp.amount,
          store_name: exp.store_name,
          store_address: exp.store_address || '',
          store_phone_number: exp.store_phone_number || ''
        }))

        // 부서별 데이터 계산 (임시로 상점명 기준으로 그룹화)
        if (expenses.value.length > 0) {
          const deptMap = {}
          expenses.value.forEach(exp => {
            const dept = exp.store_name || '기타'
            if (!deptMap[dept]) {
              deptMap[dept] = 0
            }
            deptMap[dept] += exp.amount
          })
          departmentData.value = Object.entries(deptMap).map(([name, amount]) => ({
            name,
            amount
          })).sort((a, b) => b.amount - a.amount)
        } else {
          departmentData.value = []
        }

        // 트렌드 데이터 계산 (임시 데이터)
        if (expenses.value.length > 0) {
          const dates = expenses.value.map(exp => new Date(exp.date))
          const validDates = dates.filter(d => !isNaN(d.getTime()))

          if (validDates.length > 0) {
            // 월별로 그룹화
            const trendMap = {}
            expenses.value.forEach(exp => {
              const date = new Date(exp.date)
              if (!isNaN(date.getTime())) {
                const key = `${date.getFullYear()}-${date.getMonth() + 1}`
                if (!trendMap[key]) {
                  trendMap[key] = 0
                }
                trendMap[key] += exp.amount
              }
            })

            trendData.value = Object.entries(trendMap).map(([key, amount]) => {
              const [year, month] = key.split('-')
              return {
                label: `${year}-${month.padStart(2, '0')}`,
                amount
              }
            }).sort((a, b) => a.label.localeCompare(b.label))
          } else {
            trendData.value = []
          }
        } else {
          trendData.value = []
        }
      } catch (error) {
        console.error('데이터 로드 실패:', error)
        alert('데이터를 불러오는데 실패했습니다.')
      } finally {
        loading.value = false
      }
    }

    const getDateRange = () => {
      if (!selectedYear.value) {
        // 전체 기간
        return { start_date: null, end_date: null }
      }

      const year = parseInt(selectedYear.value)

      if (selectedDay.value && selectedMonth.value) {
        // 특정 일
        const month = parseInt(selectedMonth.value)
        const day = parseInt(selectedDay.value)
        const start_date = new Date(year, month - 1, day, 0, 0, 0)
        const end_date = new Date(year, month - 1, day, 23, 59, 59)
        return { start_date, end_date }
      } else if (selectedMonth.value) {
        // 특정 월
        const month = parseInt(selectedMonth.value)
        const start_date = new Date(year, month - 1, 1)
        const end_date = new Date(year, month, 0, 23, 59, 59)
        return { start_date, end_date }
      } else {
        // 특정 년도
        const start_date = new Date(year, 0, 1)
        const end_date = new Date(year, 11, 31, 23, 59, 59)
        return { start_date, end_date }
      }
    }

    const calculateAverage = (total) => {
      if (!selectedYear.value) {
        // 전체 기간: 월 평균
        const months = 12 // TODO: 실제 데이터가 있는 월 수로 계산
        return Math.round(total / months)
      }

      if (selectedDay.value && selectedMonth.value) {
        // 특정 일: 해당 일 금액
        return total
      } else if (selectedMonth.value) {
        // 특정 월: 일 평균
        const year = parseInt(selectedYear.value)
        const month = parseInt(selectedMonth.value)
        const daysInMonth = new Date(year, month, 0).getDate()
        return Math.round(total / daysInMonth)
      } else {
        // 특정 년도: 월 평균
        return Math.round(total / 12)
      }
    }

    const onYearChange = () => {
      selectedMonth.value = ''
      selectedDay.value = ''
      updateAvailableDays()
      loadData()
    }

    const onMonthChange = () => {
      selectedDay.value = ''
      updateAvailableDays()
      loadData()
    }

    const onDayChange = () => {
      loadData()
    }

    const onCategoryChange = () => {
      loadData()
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

    const exportSelectedAsExcelCSV = () => {
      if (selectedExpenses.value.length === 0) {
        alert('선택한 항목이 없습니다.')
        return
      }
      const csvContent = generateSelectedCSVContent()
      const blob = new Blob(['\ufeff' + csvContent], { type: 'text/csv;charset=utf-8;' })
      const link = document.createElement('a')
      link.href = URL.createObjectURL(blob)
      link.download = 'selected-expense-report-excel.csv'
      link.click()
      showExportMenu.value = false
    }

    const exportSelectedAsPDF = async () => {
      if (selectedExpenses.value.length === 0) {
        alert('선택한 항목이 없습니다.')
        return
      }

      try {
        showExportMenu.value = false

        // 선택된 지출 내역의 ID 배열 생성
        const expenseIds = selectedExpenses.value
          .filter(expense => expense.id)
          .map(expense => expense.id)

        if (expenseIds.length === 0) {
          alert('유효한 지출 내역이 없습니다.')
          return
        }

        console.log('[PDF] 리포트 다운로드 시작:', expenseIds)

        // 리포트 PDF 다운로드
        const response = await expenseAPI.downloadReportPDF(expenseIds)

        // PDF 파일 다운로드
        const blob = await response.blob()
        const url = window.URL.createObjectURL(blob)

        // 파일명 생성
        const today = new Date().toISOString().split('T')[0].replace(/-/g, '')
        let filename = `expense_report_${today}.pdf`

        const contentDisposition = response.headers.get('Content-Disposition')
        if (contentDisposition) {
          const filenameMatch = contentDisposition.match(/filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/)
          if (filenameMatch) {
            filename = filenameMatch[1].replace(/['"]/g, '')
          }
        }

        // 다운로드 링크 생성 및 클릭
        const link = document.createElement('a')
        link.href = url
        link.download = filename
        document.body.appendChild(link)
        link.click()

        // 정리
        document.body.removeChild(link)
        window.URL.revokeObjectURL(url)

        console.log('[PDF] 리포트 다운로드 완료:', filename)
        alert(`선택한 ${selectedExpenses.value.length}개 항목의 리포트 PDF가 다운로드되었습니다.`)

      } catch (error) {
        console.error('[PDF] 리포트 다운로드 실패:', error)
        alert('PDF 다운로드에 실패했습니다: ' + error.message)
      }
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

    const toggleSelectAll = () => {
      if (isAllSelected.value) {
        selectedExpenses.value = []
      } else {
        selectedExpenses.value = [...detailedData.value]
      }
      isAllSelected.value = !isAllSelected.value
    }

    // CSV 값 이스케이프 처리 (쉼표, 줄바꿈, 따옴표 처리)
    const escapeCSVValue = (value) => {
      if (value == null) return ''
      const stringValue = String(value)
      // 쉼표, 줄바꿈, 따옴표가 있으면 따옴표로 감싸고, 내부 따옴표는 두 개로 변경
      if (stringValue.includes(',') || stringValue.includes('\n') || stringValue.includes('"')) {
        return `"${stringValue.replace(/"/g, '""')}"`
      }
      return stringValue
    }

    const generateSelectedCSVContent = () => {
      const headers = ['날짜', '카테고리', '내용', '상점명', '주소', '전화번호', '금액']
      const rows = selectedExpenses.value.map(expense => [
        escapeCSVValue(expense.date),
        escapeCSVValue(expense.category),
        escapeCSVValue(expense.description),
        escapeCSVValue(expense.department),
        escapeCSVValue(expense.store_address || ''),
        escapeCSVValue(expense.store_phone_number || ''),
        escapeCSVValue(expense.amount)
      ])

      return [headers, ...rows].map(row => row.join(',')).join('\n')
    }

    const generateCSVContent = () => {
      const headers = ['날짜', '카테고리', '내용', '상점명', '주소', '전화번호', '금액']
      const rows = detailedData.value.map(expense => [
        escapeCSVValue(expense.date),
        escapeCSVValue(expense.category),
        escapeCSVValue(expense.description),
        escapeCSVValue(expense.department),
        escapeCSVValue(expense.store_address || ''),
        escapeCSVValue(expense.store_phone_number || ''),
        escapeCSVValue(expense.amount)
      ])

      return [headers, ...rows].map(row => row.join(',')).join('\n')
    }

    // 컴포넌트 마운트 시 초기화
    onMounted(async () => {
      const now = new Date()
      selectedYear.value = now.getFullYear().toString()
      selectedMonth.value = (now.getMonth() + 1).toString()
      updateAvailableDays()
      await loadData()
    })

    return {
      selectedYear,
      selectedMonth,
      selectedDay,
      selectedCategory,
      showExportMenu,
      loading,
      availableYears,
      availableMonths,
      availableDays,
      availableCategories,
      currentData,
      departmentData,
      trendData,
      categoryData,
      detailedData,
      selectedExpenses,
      isAllSelected,
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
      exportAsCSV,
      exportSelectedAsExcelCSV,
      exportSelectedAsPDF,
      toggleSelectAll,
      loadData
    }
  }
}
</script>