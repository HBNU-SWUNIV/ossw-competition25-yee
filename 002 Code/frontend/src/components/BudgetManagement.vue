<template>
  <div class="space-y-8">
    <!-- 페이지 헤더 -->
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
      <h2 class="text-2xl sm:text-3xl font-bold text-gray-900">예산 관리</h2>
      <button 
        class="btn-primary flex items-center gap-2 w-full sm:w-auto"
        @click="showAddModal = true"
      >
        <span class="text-lg">+</span>
        새 예산 추가
      </button>
    </div>

    <!-- 통계 카드 -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div class="card p-6 hover:shadow-medium transition-shadow duration-200">
        <div class="flex items-center gap-4">
          <div class="text-4xl">💰</div>
          <div>
            <h3 class="text-sm font-medium text-gray-600 mb-1">총 예산</h3>
            <p class="text-2xl font-bold text-gray-900">₩{{ totalBudget.toLocaleString() }}</p>
          </div>
        </div>
      </div>
      
      <div class="card p-6 hover:shadow-medium transition-shadow duration-200">
        <div class="flex items-center gap-4">
          <div class="text-4xl">📊</div>
          <div>
            <h3 class="text-sm font-medium text-gray-600 mb-1">사용된 예산</h3>
            <p class="text-2xl font-bold text-red-600">₩{{ usedBudget.toLocaleString() }}</p>
          </div>
        </div>
      </div>
      
      <div class="card p-6 hover:shadow-medium transition-shadow duration-200">
        <div class="flex items-center gap-4">
          <div class="text-4xl">💳</div>
          <div>
            <h3 class="text-sm font-medium text-gray-600 mb-1">남은 예산</h3>
            <p class="text-2xl font-bold text-green-600">₩{{ remainingBudget.toLocaleString() }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- 부서별 예산 현황 -->
    <div class="card p-6">
      <h3 class="text-xl font-semibold text-gray-900 mb-6">부서별 예산 현황</h3>
      <div class="space-y-4">
        <div 
          v-for="budget in budgets" 
          :key="budget.id" 
          class="border border-gray-200 rounded-lg p-6 hover:border-primary-300 hover:shadow-soft transition-all duration-200"
        >
          <div class="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4 mb-4">
            <div class="flex-1">
              <h4 class="text-lg font-semibold text-gray-900 mb-1">{{ budget.name }}</h4>
              <p class="text-sm text-gray-600">{{ budget.category }}</p>
            </div>
            <div class="flex flex-col sm:flex-row gap-4 lg:gap-8">
              <div class="text-center">
                <span class="text-sm text-gray-600 block">배정</span>
                <span class="text-lg font-semibold text-gray-900">₩{{ budget.amount.toLocaleString() }}</span>
              </div>
              <div class="text-center">
                <span class="text-sm text-gray-600 block">사용</span>
                <span class="text-lg font-semibold text-red-600">₩{{ budget.spent.toLocaleString() }}</span>
              </div>
            </div>
          </div>
          <div class="w-full bg-gray-200 rounded-full h-2">
            <div
              class="h-2 rounded-full transition-all duration-300"
              :class="{
                'bg-green-500': (budget.spent / budget.amount) < 0.7,
                'bg-yellow-500': (budget.spent / budget.amount) >= 0.7 && (budget.spent / budget.amount) < 0.9,
                'bg-red-500': (budget.spent / budget.amount) >= 0.9
              }"
              :style="{ width: Math.min((budget.spent / budget.amount * 100), 100) + '%' }"
            ></div>
          </div>
          <div class="flex justify-between items-center mt-2">
            <span class="text-sm text-gray-600">
              사용률: {{ Math.round((budget.spent / budget.amount) * 100) }}%
            </span>
            <span class="text-sm font-medium text-gray-900">
              남은 예산: ₩{{ budget.remaining.toLocaleString() }}
            </span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { budgetAPI } from '../api/budget'

export default {
  name: 'BudgetManagement',
  setup() {
    const showAddModal = ref(false)
    const budgets = ref([])
    const isLoading = ref(false)

    // 예산 목록 조회
    const fetchBudgets = async () => {
      isLoading.value = true
      try {
        const result = await budgetAPI.getBudgets()
        if (result.success) {
          budgets.value = result.data
        } else {
          console.error('예산 목록 조회 실패:', result.error)
        }
      } catch (error) {
        console.error('예산 목록 조회 중 오류:', error)
      } finally {
        isLoading.value = false
      }
    }

    // 총 예산 (백엔드의 amount 필드 사용)
    const totalBudget = computed(() =>
      budgets.value.reduce((sum, budget) => sum + budget.amount, 0)
    )

    // 사용된 예산
    const usedBudget = computed(() =>
      budgets.value.reduce((sum, budget) => sum + budget.spent, 0)
    )

    // 남은 예산
    const remainingBudget = computed(() =>
      budgets.value.reduce((sum, budget) => sum + budget.remaining, 0)
    )

    // 컴포넌트 마운트 시 예산 목록 조회
    onMounted(() => {
      fetchBudgets()
    })

    return {
      showAddModal,
      budgets,
      isLoading,
      totalBudget,
      usedBudget,
      remainingBudget,
      fetchBudgets
    }
  }
}
</script>
