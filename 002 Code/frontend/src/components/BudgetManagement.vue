<template>
  <div class="space-y-8 max-w-6xl mx-auto">
    <!-- 페이지 헤더 -->
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
      <h2 class="text-2xl sm:text-3xl font-bold text-gray-900">예산 관리</h2>
      <div class="flex gap-2 w-full sm:w-auto">
        <button class="btn-secondary flex items-center gap-2" @click="migrateToOrganization" v-if="budgets.length > 0">
          🔄 조직 공유로 전환
        </button>
        <button class="btn-primary flex items-center gap-2" @click="showAddModal = true">
          <span class="text-lg">+</span>
          새 예산 추가
        </button>
      </div>
    </div>

    <!-- 통계 카드 -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
      <div
        class="bg-white rounded-2xl p-6 border border-gray-100 hover:border-blue-200 hover:shadow-lg transition-all duration-200">
        <div class="mb-4">
          <p class="text-xs font-medium text-gray-500 uppercase tracking-wide mb-2">총 예산</p>
          <p class="text-xl font-bold text-gray-900">₩{{ totalBudget.toLocaleString() }}</p>
        </div>
      </div>

      <div
        class="bg-white rounded-2xl p-6 border border-gray-100 hover:border-red-200 hover:shadow-lg transition-all duration-200">
        <div class="mb-4">
          <p class="text-xs font-medium text-gray-500 uppercase tracking-wide mb-2">사용된 예산</p>
          <p class="text-xl font-bold text-red-600">₩{{ usedBudget.toLocaleString() }}</p>
        </div>
      </div>

      <div
        class="bg-white rounded-2xl p-6 border border-gray-100 hover:border-green-200 hover:shadow-lg transition-all duration-200">
        <div class="mb-4">
          <p class="text-xs font-medium text-gray-500 uppercase tracking-wide mb-2">남은 예산</p>
          <p class="text-xl font-bold text-green-600">₩{{ remainingBudget.toLocaleString() }}</p>
        </div>
      </div>
    </div>

    <!-- 부서별 예산 현황 -->
    <div class="bg-white rounded-2xl p-6 border border-gray-100">
      <h3 class="text-xl font-bold text-gray-900 mb-6">부서별 예산 현황</h3>

      <!-- 예산 목록이 비어있을 때 -->
      <div v-if="budgets.length === 0 && !isLoading" class="text-center py-16">

        <h4 class="text-lg font-semibold text-gray-900 mb-2">예산을 등록해보세요</h4>
        <p class="text-gray-500 mb-6">첫 번째 예산을 등록하여 관리를 시작하세요</p>
        <button class="btn-primary" @click="showAddModal = true">
          예산 추가하기
        </button>
      </div>

      <!-- 예산 목록 -->
      <div v-else class="space-y-4">
        <div v-for="budget in budgets" :key="budget.id"
          class="border border-gray-200 rounded-2xl p-6 hover:border-blue-300 hover:shadow-md transition-all duration-200">
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
              <div class="flex gap-2">
                <button @click="editBudget(budget)"
                  class="px-3 py-1 text-sm bg-blue-100 text-blue-700 rounded hover:bg-blue-200">
                  수정
                </button>
                <button @click="deleteBudget(budget.id)"
                  class="px-3 py-1 text-sm bg-red-100 text-red-700 rounded hover:bg-red-200">
                  삭제
                </button>
              </div>
            </div>
          </div>
          <div class="w-full bg-gray-200 rounded-full h-2">
            <div class="h-2 rounded-full transition-all duration-300" :class="{
              'bg-green-500': (budget.spent / budget.amount) < 0.7,
              'bg-yellow-500': (budget.spent / budget.amount) >= 0.7 && (budget.spent / budget.amount) < 0.9,
              'bg-red-500': (budget.spent / budget.amount) >= 0.9
            }" :style="{ width: Math.min((budget.spent / budget.amount * 100), 100) + '%' }"></div>
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

    <!-- 예산 추가/수정 모달 -->
    <div v-if="showAddModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div class="bg-white rounded-3xl p-8 max-w-md w-full shadow-strong">
        <h3 class="text-xl font-bold text-gray-900 mb-6">
          {{ editingBudget ? '예산 수정' : '새 예산 추가' }}
        </h3>
        <form @submit.prevent="saveBudget" class="space-y-4">
          <div>
            <label class="block text-sm font-semibold text-gray-900 mb-2">예산 이름</label>
            <input v-model="budgetForm.name" type="text" required class="input-field" placeholder="예: 마케팅 부서, IT 부서" />
          </div>
          <div>
            <label class="block text-sm font-semibold text-gray-900 mb-2">카테고리</label>
            <select v-model="budgetForm.category" class="input-field">
              <option value="전체">전체</option>
              <option value="식비">식비</option>
              <option value="교통비">교통비</option>
              <option value="사무용품">사무용품</option>
              <option value="마케팅">마케팅</option>
              <option value="회식">회식</option>
              <option value="기타">기타</option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-semibold text-gray-900 mb-2">예산 금액 (원)</label>
            <input v-model.number="budgetForm.amount" type="number" required min="1" class="input-field"
              placeholder="1000000" />
          </div>
          <div class="flex gap-3 mt-6">
            <button type="submit" class="btn-primary flex-1">
              {{ editingBudget ? '수정' : '추가' }}
            </button>
            <button type="button" @click="closeModal" class="btn-secondary flex-1">
              취소
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, reactive } from 'vue'
import { budgetAPI } from '../api/budget'

export default {
  name: 'BudgetManagement',
  setup() {
    const showAddModal = ref(false)
    const budgets = ref([])
    const isLoading = ref(false)
    const editingBudget = ref(null)

    const budgetForm = reactive({
      name: '',
      category: '전체',
      amount: ''
    })

    // 예산 목록 조회
    const fetchBudgets = async () => {
      isLoading.value = true
      try {
        const result = await budgetAPI.getBudgets()
        if (result.success) {
          budgets.value = result.data
        } else {
          console.error('예산 목록 조회 실패:', result.error)
          alert('예산 목록 조회에 실패했습니다.')
        }
      } catch (error) {
        console.error('예산 목록 조회 중 오류:', error)
        alert('예산 목록 조회 중 오류가 발생했습니다.')
      } finally {
        isLoading.value = false
      }
    }

    // 예산 저장 (추가/수정)
    const saveBudget = async () => {
      try {
        const budgetData = {
          name: budgetForm.name,
          category: budgetForm.category,
          amount: parseFloat(budgetForm.amount)
        }

        let result
        if (editingBudget.value) {
          // 수정
          result = await budgetAPI.updateBudget(editingBudget.value.id, budgetData)
        } else {
          // 추가
          result = await budgetAPI.createBudget(budgetData)
        }

        if (result.success) {
          alert(editingBudget.value ? '예산이 수정되었습니다.' : '예산이 추가되었습니다.')
          await fetchBudgets()
          closeModal()
        } else {
          alert('예산 저장 실패: ' + result.error)
        }
      } catch (error) {
        console.error('예산 저장 중 오류:', error)
        alert('예산 저장 중 오류가 발생했습니다.')
      }
    }

    // 예산 수정
    const editBudget = (budget) => {
      editingBudget.value = budget
      budgetForm.name = budget.name
      budgetForm.category = budget.category
      budgetForm.amount = budget.amount
      showAddModal.value = true
    }

    // 예산 삭제
    const deleteBudget = async (budgetId) => {
      if (!confirm('정말 이 예산을 삭제하시겠습니까?')) {
        return
      }

      try {
        const result = await budgetAPI.deleteBudget(budgetId)
        if (result.success) {
          alert('예산이 삭제되었습니다.')
          await fetchBudgets()
        } else {
          alert('예산 삭제 실패: ' + result.error)
        }
      } catch (error) {
        console.error('예산 삭제 중 오류:', error)
        alert('예산 삭제 중 오류가 발생했습니다.')
      }
    }

    // 조직 공유로 전환
    const migrateToOrganization = async () => {
      if (!confirm('기존 개인 예산을 조직 예산으로 전환하시겠습니까? 조직 멤버들과 공유됩니다.')) {
        return
      }

      try {
        const result = await budgetAPI.migrateToOrganization()
        if (result.success) {
          alert(`총 ${result.data.updated}개의 예산이 조직 공유 예산으로 전환되었습니다.`)
          await fetchBudgets()
        } else {
          alert('조직 공유 전환 실패: ' + result.error)
        }
      } catch (error) {
        console.error('조직 공유 전환 중 오류:', error)
        alert('조직 공유 전환 중 오류가 발생했습니다.')
      }
    }

    // 모달 닫기
    const closeModal = () => {
      showAddModal.value = false
      editingBudget.value = null
      budgetForm.name = ''
      budgetForm.category = '전체'
      budgetForm.amount = ''
    }

    // 총 예산
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
      editingBudget,
      budgetForm,
      totalBudget,
      usedBudget,
      remainingBudget,
      fetchBudgets,
      saveBudget,
      editBudget,
      deleteBudget,
      migrateToOrganization,
      closeModal
    }
  }
}
</script>
