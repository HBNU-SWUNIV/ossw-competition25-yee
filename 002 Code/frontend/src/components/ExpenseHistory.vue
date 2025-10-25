<template>
  <div class="space-y-8">
    <!-- 페이지 헤더 -->
    <div class="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
      <h2 class="text-2xl sm:text-3xl font-bold text-gray-900">지출 내역</h2>
      <div class="flex flex-col sm:flex-row gap-4">
        <select v-model="selectedPeriod" class="input-field w-full sm:w-auto">
          <option value="this-month">이번 달</option>
          <option value="last-month">지난 달</option>
          <option value="this-year">올해</option>
        </select>
        <button 
          class="btn-primary flex items-center gap-2 w-full sm:w-auto"
          @click="showOcrModal = true"
        >
          <span class="text-lg">+</span>
          지출 등록 (OCR)
        </button>
      </div>
    </div>

    <!-- 요약 카드 -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <div class="card p-6 text-center">
        <h3 class="text-sm font-medium text-gray-600 mb-2">총 지출</h3>
        <p class="text-3xl font-bold text-red-600">₩{{ totalExpense.toLocaleString() }}</p>
      </div>
      <div class="card p-6 text-center">
        <h3 class="text-sm font-medium text-gray-600 mb-2">평균 지출</h3>
        <p class="text-3xl font-bold text-blue-600">₩{{ avgExpense.toLocaleString() }}</p>
      </div>
      <div class="card p-6 text-center">
        <h3 class="text-sm font-medium text-gray-600 mb-2">지출 건수</h3>
        <p class="text-3xl font-bold text-green-600">{{ expenses.length }}건</p>
      </div>
    </div>

    <!-- 필터 -->
    <div class="flex flex-col sm:flex-row gap-4">
      <input 
        v-model="searchQuery" 
        type="text" 
        placeholder="지출 내역 검색..." 
        class="input-field flex-1"
      >
      <select v-model="selectedCategory" class="input-field w-full sm:w-48">
        <option value="">모든 카테고리</option>
        <option value="식비">식비</option>
        <option value="교통비">교통비</option>
        <option value="사무용품">사무용품</option>
        <option value="마케팅">마케팅</option>
        <option value="기타">기타</option>
      </select>
    </div>

    <!-- 지출 목록 -->
    <div class="card overflow-hidden">
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
            v-for="expense in filteredExpenses" 
            :key="expense.id" 
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
      <div class="lg:hidden space-y-4 p-4">
        <div 
          v-for="expense in filteredExpenses" 
          :key="expense.id" 
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
                'bg-gray-500': expense.category === '기타'
              }"
            >
              {{ expense.category }}
            </span>
          </div>
        </div>
      </div>
    </div>

    <!-- OCR 등록 모달 -->
    <div v-if="showOcrModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4" @click="closeOcrModal">
      <div class="bg-white rounded-2xl w-full max-w-2xl max-h-[90vh] overflow-y-auto shadow-strong" @click.stop>
        <!-- 모달 헤더 -->
        <div class="flex items-center justify-between p-6 border-b border-gray-200 bg-gray-50 rounded-t-2xl">
          <h2 class="flex items-center gap-3 text-xl font-semibold text-gray-900">
            <span class="text-2xl">📷</span>
            지출 등록 (OCR)
          </h2>
          <button 
            class="w-8 h-8 flex items-center justify-center rounded-full hover:bg-gray-200 transition-colors duration-200"
            @click="closeOcrModal"
          >
            <span class="text-xl">&times;</span>
          </button>
        </div>

        <div class="p-6 space-y-6">
          <!-- 영수증 업로드 섹션 -->
          <div>
            <label class="block text-lg font-semibold text-gray-900 mb-3">영수증 업로드</label>
            <div 
              class="border-2 border-dashed border-gray-300 rounded-xl p-8 text-center transition-all duration-300"
              :class="{ 'border-primary-500 bg-primary-50': uploadedFile }"
            >
              <input
                ref="fileInput"
                type="file"
                accept="image/*"
                @change="handleFileSelect"
                class="hidden"
              >
              <input
                ref="cameraInput"
                type="file"
                accept="image/*"
                capture="environment"
                @change="handleCameraCapture"
                class="hidden"
              >
              
              <div v-if="!uploadedFile" class="space-y-4">
                <div class="text-5xl">📄</div>
                <p class="text-gray-600">영수증 파일 선택 또는 카메라 실행</p>
              </div>
              
              <div v-if="uploadedFile" class="space-y-4">
                <div class="flex items-center justify-center gap-3 p-3 bg-white rounded-lg">
                  <span class="text-2xl">📷</span>
                  <span class="font-medium text-gray-900 flex-1">{{ uploadedFile.name }}</span>
                  <button 
                    class="w-7 h-7 bg-red-500 text-white rounded-full flex items-center justify-center hover:bg-red-600 transition-colors duration-200"
                    @click="removeFile"
                  >
                    ×
                  </button>
                </div>
                <img v-if="imagePreview" :src="imagePreview" alt="영수증 미리보기" class="max-w-full max-h-64 mx-auto rounded-lg shadow-soft">
              </div>
              
              <div class="flex flex-col sm:flex-row gap-3 justify-center mt-6">
                <button class="btn-primary flex items-center gap-2" @click="triggerFileSelect">
                  <span class="text-lg">📁</span> 파일 선택
                </button>
                <button class="btn-secondary flex items-center gap-2" @click="triggerCamera">
                  <span class="text-lg">📷</span> 카메라
                </button>
              </div>
            </div>
          </div>

          <!-- OCR 분석 결과 표시 -->
          <div v-if="ocrData" class="space-y-3">
            <label class="block text-lg font-semibold text-gray-900">영수증 OCR 분석 결과</label>
            <div class="bg-gray-50 rounded-xl p-4 space-y-3">
              <div class="flex justify-between items-center py-2 border-b border-gray-200">
                <span class="font-semibold text-gray-700">날짜:</span>
                <span class="font-medium text-gray-900">{{ ocrData.date || '-' }}</span>
              </div>
              <div class="flex justify-between items-center py-2 border-b border-gray-200">
                <span class="font-semibold text-gray-700">금액:</span>
                <span class="font-medium text-gray-900">{{ ocrData.amount ? formatAmount(ocrData.amount) : '-' }}</span>
              </div>
              <div class="flex justify-between items-center py-2">
                <span class="font-semibold text-gray-700">상호명:</span>
                <span class="font-medium text-gray-900">{{ ocrData.merchant || '-' }}</span>
              </div>
            </div>
          </div>

          <!-- 입력 폼 -->
          <div class="space-y-6">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-semibold text-gray-900 mb-2">날짜</label>
                <input
                  type="date"
                  v-model="expenseForm.date"
                  class="input-field"
                  required
                >
              </div>
              <div>
                <label class="block text-sm font-semibold text-gray-900 mb-2">금액(원)</label>
                <input
                  type="number"
                  v-model="expenseForm.amount"
                  class="input-field"
                  placeholder="금액 입력"
                  required
                >
              </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-semibold text-gray-900 mb-2">상호명</label>
                <input
                  type="text"
                  v-model="expenseForm.merchant"
                  class="input-field"
                  placeholder="상호명"
                  required
                >
              </div>
              <div>
                <label class="block text-sm font-semibold text-gray-900 mb-2">카테고리</label>
                <select v-model="expenseForm.category" class="input-field">
                  <option value="식비">식비</option>
                  <option value="교통비">교통비</option>
                  <option value="사무용품">사무용품</option>
                  <option value="마케팅">마케팅</option>
                  <option value="기타">기타</option>
                </select>
              </div>
            </div>

            <div>
              <label class="block text-sm font-semibold text-gray-900 mb-2">지출 설명</label>
              <input
                type="text"
                v-model="expenseForm.description"
                class="input-field"
                placeholder="간단한 지출 목적"
                required
              >
            </div>
          </div>
        </div>

        <!-- 모달 푸터 -->
        <div class="flex justify-end gap-3 p-6 border-t border-gray-200 bg-gray-50 rounded-b-2xl">
          <button class="btn-secondary" @click="closeOcrModal">취소</button>
          <button 
            class="btn-primary" 
            @click="registerExpense" 
            :disabled="!isFormValid"
            :class="{ 'opacity-50 cursor-not-allowed': !isFormValid }"
          >
            등록하기 (Firestore addDoc)
          </button>
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
    const showOcrModal = ref(false)
    const selectedPeriod = ref('this-month')
    const searchQuery = ref('')
    const selectedCategory = ref('')
    
    // OCR 관련 state
    const uploadedFile = ref(null)
    const imagePreview = ref(null)
    const ocrData = ref(null)
    const fileInput = ref(null)
    const cameraInput = ref(null)
    
    // 폼 데이터
    const expenseForm = ref({
      date: '',
      amount: '',
      merchant: '',
      category: '식비',
      description: ''
    })
    
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

    const isFormValid = computed(() => {
      return expenseForm.value.date && 
             expenseForm.value.amount && 
             expenseForm.value.merchant && 
             expenseForm.value.description
    })

    // 파일 선택
    const handleFileSelect = (event) => {
      const file = event.target.files[0]
      if (file) {
        uploadedFile.value = file
        const reader = new FileReader()
        reader.onload = (e) => {
          imagePreview.value = e.target.result
        }
        reader.readAsDataURL(file)
        // TODO: 백엔드 OCR API 호출
        performOcrAnalysis(file)
      }
    }

    // 카메라 캡처
    const handleCameraCapture = (event) => {
      handleFileSelect(event)
    }

    // 파일 선택 트리거
    const triggerFileSelect = () => {
      fileInput.value?.click()
    }

    // 카메라 트리거
    const triggerCamera = () => {
      cameraInput.value?.click()
    }

    // 파일 제거
    const removeFile = () => {
      uploadedFile.value = null
      imagePreview.value = null
      ocrData.value = null
      if (fileInput.value) fileInput.value.value = ''
      if (cameraInput.value) cameraInput.value.value = ''
    }

    // OCR 분석 수행 (백엔드 API 호출)
    const performOcrAnalysis = async (file) => {
      // TODO: 백엔드 개발자가 API 연동 후 수정
      // const formData = new FormData()
      // formData.append('file', file)
      // const response = await fetch('/api/ocr', {
      //   method: 'POST',
      //   body: formData
      // })
      // const data = await response.json()
      
      // 임시 mock 데이터
      setTimeout(() => {
        ocrData.value = {
          date: '2024-10-20',
          amount: 15000,
          merchant: '스타벅스 강남점'
        }
        
        // OCR 결과를 폼에 자동 입력
        if (ocrData.value) {
          expenseForm.value.date = ocrData.value.date || ''
          expenseForm.value.amount = ocrData.value.amount || ''
          expenseForm.value.merchant = ocrData.value.merchant || ''
        }
      }, 1000)
    }

    // 금액 포맷팅
    const formatAmount = (amount) => {
      return `₩${amount?.toLocaleString() || '0'}`
    }

    // 모달 닫기
    const closeOcrModal = () => {
      showOcrModal.value = false
      removeFile()
      expenseForm.value = {
        date: '',
        amount: '',
        merchant: '',
        category: '식비',
        description: ''
      }
      ocrData.value = null
    }

    // 지출 등록
    const registerExpense = () => {
      if (!isFormValid.value) {
        alert('모든 필드를 입력해주세요.')
        return
      }

      // TODO: Firestore에 데이터 저장
      // await addDoc(collection(db, 'expenses'), {
      //   date: expenseForm.value.date,
      //   amount: parseInt(expenseForm.value.amount),
      //   merchant: expenseForm.value.merchant,
      //   category: expenseForm.value.category,
      //   description: expenseForm.value.description,
      //   createdAt: new Date()
      // })

      // 임시로 expenses 배열에 추가
      expenses.value.push({
        id: expenses.value.length + 1,
        date: expenseForm.value.date,
        category: expenseForm.value.category,
        description: expenseForm.value.description,
        department: '개발팀',
        amount: parseInt(expenseForm.value.amount)
      })

      alert('지출 내역이 등록되었습니다.')
      closeOcrModal()
    }

    const formatDate = (dateString) => {
      const date = new Date(dateString)
      return date.toLocaleDateString('ko-KR', { 
        month: 'short', 
        day: 'numeric',
        weekday: 'short'
      })
    }

    return {
      showOcrModal,
      selectedPeriod,
      searchQuery,
      selectedCategory,
      expenses,
      totalExpense,
      avgExpense,
      filteredExpenses,
      formatDate,
      uploadedFile,
      imagePreview,
      ocrData,
      fileInput,
      cameraInput,
      expenseForm,
      handleFileSelect,
      handleCameraCapture,
      triggerFileSelect,
      triggerCamera,
      removeFile,
      formatAmount,
      closeOcrModal,
      registerExpense,
      isFormValid
    }
  }
}
</script>
