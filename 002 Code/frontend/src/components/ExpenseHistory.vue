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
        <button class="btn-primary flex items-center gap-2 w-full sm:w-auto" @click="showOcrModal = true">
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
      <input v-model="searchQuery" type="text" placeholder="지출 내역 검색..." class="input-field flex-1">
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
        <div class="grid grid-cols-7 gap-4 p-4 bg-gray-50 font-semibold text-gray-700 border-b">
          <div>날짜</div>
          <div>카테고리</div>
          <div>내용</div>
          <div>상점명</div>
          <div>주소</div>
          <div>연락처</div>
          <div class="text-right">금액</div>
        </div>
        <div class="divide-y divide-gray-200">
          <div v-for="expense in filteredExpenses" :key="expense.id"
            class="grid grid-cols-7 gap-4 p-4 hover:bg-gray-50 transition-colors duration-200">
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
            <div class="font-medium">{{ expense.description || expense.store_name }}</div>
            <div class="text-sm font-medium text-gray-900">{{ expense.store_name }}</div>
            <div class="text-sm text-gray-600">{{ expense.store_address || '-' }}</div>
            <div class="text-sm text-gray-600">{{ expense.store_phone_number || '-' }}</div>
            <div class="text-right font-semibold text-red-600">₩{{ expense.amount.toLocaleString() }}</div>
            <div class="text-right">
              <div class="flex gap-2 justify-end">
                <button @click="openEditModal(expense)"
                  class="px-3 py-1 bg-blue-500 hover:bg-blue-600 text-white text-sm rounded-lg transition-colors duration-200"
                  title="수정">
                  ✏️ 수정
                </button>
                <button @click="deleteExpense(expense.id)"
                  class="px-3 py-1 bg-red-500 hover:bg-red-600 text-white text-sm rounded-lg transition-colors duration-200"
                  title="삭제">
                  🗑️ 삭제
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 모바일 카드 -->
      <div class="lg:hidden space-y-4 p-4">
        <div v-for="expense in filteredExpenses" :key="expense.id"
          class="border border-gray-200 rounded-lg p-4 hover:shadow-soft transition-shadow duration-200">
          <div class="flex justify-between items-start mb-3">
            <div>
              <h4 class="font-semibold text-gray-900">{{ expense.description || expense.store_name }}</h4>
              <p class="text-sm text-gray-700">{{ expense.store_name }}</p>
              <p v-if="expense.store_address" class="text-xs text-gray-500 mt-1">{{ expense.store_address }}</p>
              <p v-if="expense.store_phone_number" class="text-xs text-gray-500">{{ expense.store_phone_number }}</p>
            </div>
            <span class="text-lg font-bold text-red-600">₩{{ expense.amount.toLocaleString() }}</span>
          </div>
          <div class="flex justify-between items-center">
            <span class="text-sm text-gray-600">{{ formatDate(expense.date) }}</span>
            <div class="flex items-center gap-2">
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
              <button @click="openEditModal(expense)"
                class="px-3 py-1 bg-blue-500 hover:bg-blue-600 text-white text-xs rounded-lg transition-colors duration-200"
                title="수정">
                ✏️
              </button>
              <button @click="deleteExpense(expense.id)"
                class="px-3 py-1 bg-red-500 hover:bg-red-600 text-white text-xs rounded-lg transition-colors duration-200"
                title="삭제">
                🗑️
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- OCR 등록 모달 -->
    <div v-if="showOcrModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4"
      @click.self="closeOcrModal">
      <div class="bg-white rounded-2xl w-full max-w-2xl max-h-[90vh] overflow-y-auto shadow-strong">
        <!-- 모달 헤더 -->
        <div class="flex items-center justify-between p-6 border-b border-gray-200 bg-gray-50 rounded-t-2xl">
          <h2 class="flex items-center gap-3 text-xl font-semibold text-gray-900">
            <span class="text-2xl">📷</span>
            지출 등록 (OCR)
          </h2>
          <button
            class="w-8 h-8 flex items-center justify-center rounded-full hover:bg-gray-200 transition-colors duration-200"
            @click="closeOcrModal">
            <span class="text-xl">&times;</span>
          </button>
        </div>

        <div class="p-6 space-y-6">
          <!-- 영수증 업로드 섹션 -->
          <div>
            <label class="block text-lg font-semibold text-gray-900 mb-3">영수증 업로드</label>
            <div
              class="relative border-2 border-dashed border-gray-300 rounded-xl p-8 text-center transition-all duration-300"
              :class="{ 'border-primary-500 bg-primary-50': uploadedFile }">
              <!-- OCR 처리 중 로딩 오버레이 -->
              <div v-if="isLoading"
                class="absolute inset-0 bg-white bg-opacity-95 rounded-xl flex items-center justify-center z-10">
                <div class="text-center space-y-4">
                  <div
                    class="inline-block animate-spin rounded-full h-16 w-16 border-4 border-primary-500 border-t-transparent">
                  </div>
                  <div>
                    <p class="text-lg font-semibold text-gray-900">OCR 처리 중...</p>
                    <p class="text-sm text-gray-600 mt-2">영수증을 분석하고 있습니다</p>
                    <p class="text-xs text-gray-500 mt-1">잠시만 기다려주세요 (약 5-10초)</p>
                  </div>
                </div>
              </div>

              <input ref="fileInput" type="file" accept="image/*" @change="handleFileSelect" class="hidden">
              <input ref="cameraInput" type="file" accept="image/*" capture="environment" @change="handleCameraCapture"
                class="hidden">

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
                    @click="removeFile">
                    ×
                  </button>
                </div>
                <img v-if="imagePreview" :src="imagePreview" alt="영수증 미리보기"
                  class="max-w-full max-h-64 mx-auto rounded-lg shadow-soft">
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
              <div class="flex justify-between items-center py-2 border-b border-gray-200">
                <span class="font-semibold text-gray-700">상호명:</span>
                <span class="font-medium text-gray-900">{{ ocrData.merchant || '-' }}</span>
              </div>
              <div class="flex justify-between items-center py-2 border-b border-gray-200">
                <span class="font-semibold text-gray-700">주소:</span>
                <span class="font-medium text-gray-900">{{ ocrData.address || '정보 없음' }}</span>
              </div>
              <div class="flex justify-between items-center py-2">
                <span class="font-semibold text-gray-700">전화번호:</span>
                <span class="font-medium text-gray-900">{{ ocrData.phone || '정보 없음' }}</span>
              </div>
            </div>
          </div>

          <!-- 입력 폼 -->
          <div class="space-y-6">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-semibold text-gray-900 mb-2">날짜</label>
                <input type="date" v-model="expenseForm.date" class="input-field" required>
              </div>
              <div>
                <label class="block text-sm font-semibold text-gray-900 mb-2">금액(원)</label>
                <input type="number" v-model="expenseForm.amount" class="input-field" placeholder="금액 입력" required>
              </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-semibold text-gray-900 mb-2">상호명</label>
                <input type="text" v-model="expenseForm.merchant" class="input-field" placeholder="상호명" required>
              </div>
              <div>
                <label class="block text-sm font-semibold text-gray-900 mb-2">카테고리</label>
                <select v-model="expenseForm.category" class="input-field">
                  <option value="식비">식비</option>
                  <option value="교통비">교통비</option>
                  <option value="사무용품">사무용품</option>
                  <option value="회식">회식</option>
                  <option value="공과금">공과금</option>
                  <option value="유흥">유흥</option>
                  <option value="교육">교육</option>
                  <option value="의료">의료</option>
                  <option value="기타">기타</option>
                </select>
              </div>
            </div>

            <div>
              <label class="block text-sm font-semibold text-gray-900 mb-2">주소</label>
              <input type="text" v-model="expenseForm.address" class="input-field" placeholder="주소 (OCR 또는 수동 입력)">
            </div>

            <div>
              <label class="block text-sm font-semibold text-gray-900 mb-2">전화번호</label>
              <input type="text" v-model="expenseForm.phone" class="input-field" placeholder="전화번호 (OCR 또는 수동 입력)">
            </div>

            <div>
              <label class="block text-sm font-semibold text-gray-900 mb-2">지출 설명</label>
              <input type="text" v-model="expenseForm.description" class="input-field" placeholder="간단한 지출 목적" required>
            </div>
          </div>
        </div>

        <!-- 모달 푸터 -->
        <div class="flex justify-end gap-3 p-6 border-t border-gray-200 bg-gray-50 rounded-b-2xl">
          <button class="btn-secondary" @click="closeOcrModal">취소</button>
          <button class="btn-primary" @click="registerExpense" :disabled="!isFormValid"
            :class="{ 'opacity-50 cursor-not-allowed': !isFormValid }">
            등록하기
          </button>
        </div>
      </div>
    </div>

    <!-- 지출 수정 모달 -->
    <div v-if="showEditModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4"
      @click.self="closeEditModal">
      <div class="bg-white rounded-2xl w-full max-w-2xl max-h-[90vh] overflow-y-auto shadow-strong">
        <!-- 모달 헤더 -->
        <div class="flex items-center justify-between p-6 border-b border-gray-200 bg-gray-50 rounded-t-2xl">
          <h2 class="flex items-center gap-3 text-xl font-semibold text-gray-900">
            <span class="text-2xl">✏️</span>
            지출 내역 수정
          </h2>
          <button
            class="w-8 h-8 flex items-center justify-center rounded-full hover:bg-gray-200 transition-colors duration-200"
            @click="closeEditModal">
            <span class="text-xl">&times;</span>
          </button>
        </div>

        <div class="p-6 space-y-6">
          <!-- 입력 폼 -->
          <div class="space-y-6">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-semibold text-gray-900 mb-2">날짜</label>
                <input type="date" v-model="editForm.date" class="input-field" required>
              </div>
              <div>
                <label class="block text-sm font-semibold text-gray-900 mb-2">금액(원)</label>
                <input type="number" v-model="editForm.amount" class="input-field" placeholder="금액 입력" required>
              </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-semibold text-gray-900 mb-2">상호명</label>
                <input type="text" v-model="editForm.store_name" class="input-field" placeholder="상호명" required>
              </div>
              <div>
                <label class="block text-sm font-semibold text-gray-900 mb-2">카테고리</label>
                <select v-model="editForm.category" class="input-field">
                  <option value="식비">식비</option>
                  <option value="교통비">교통비</option>
                  <option value="사무용품">사무용품</option>
                  <option value="회식">회식</option>
                  <option value="공과금">공과금</option>
                  <option value="유흥">유흥</option>
                  <option value="교육">교육</option>
                  <option value="의료">의료</option>
                  <option value="기타">기타</option>
                </select>
              </div>
            </div>

            <div>
              <label class="block text-sm font-semibold text-gray-900 mb-2">주소</label>
              <input type="text" v-model="editForm.store_address" class="input-field" placeholder="주소 (선택)">
            </div>

            <div>
              <label class="block text-sm font-semibold text-gray-900 mb-2">전화번호</label>
              <input type="text" v-model="editForm.store_phone_number" class="input-field" placeholder="전화번호 (선택)">
            </div>

            <div>
              <label class="block text-sm font-semibold text-gray-900 mb-2">지출 설명</label>
              <input type="text" v-model="editForm.description" class="input-field" placeholder="간단한 지출 목적" required>
            </div>
          </div>
        </div>

        <!-- 모달 푸터 -->
        <div class="flex justify-end gap-3 p-6 border-t border-gray-200 bg-gray-50 rounded-b-2xl">
          <button class="btn-secondary" @click="closeEditModal">취소</button>
          <button class="btn-primary" @click="updateExpense" :disabled="!isEditFormValid"
            :class="{ 'opacity-50 cursor-not-allowed': !isEditFormValid }">
            수정하기
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { expenseAPI } from '../api/expense'
import { receiptAPI } from '../api/receipt'

export default {
  name: 'ExpenseHistory',
  setup() {
    const showOcrModal = ref(false)
    const showEditModal = ref(false)
    const selectedPeriod = ref('this-month')
    const searchQuery = ref('')
    const selectedCategory = ref('')
    const isLoading = ref(false)

    // OCR 관련 state
    const uploadedFile = ref(null)
    const imagePreview = ref(null)
    const ocrData = ref(null)
    const fileInput = ref(null)
    const cameraInput = ref(null)

    // 수정용 state
    const editingExpenseId = ref(null)

    // 폼 데이터
    const expenseForm = ref({
      date: '',
      amount: '',
      merchant: '',
      category: '식비',
      description: '',
      receipt_id: '',
      address: '',
      phone: ''
    })

    const editForm = ref({
      date: '',
      amount: '',
      store_name: '',
      store_address: '',
      store_phone_number: '',
      category: '식비',
      description: ''
    })

    const expenses = ref([])

    // 지출 목록 조회
    const fetchExpenses = async () => {
      isLoading.value = true
      try {
        const result = await expenseAPI.getExpenses()
        if (result.success) {
          expenses.value = result.data
        } else {
          console.error('지출 목록 조회 실패:', result.error)
        }
      } catch (error) {
        console.error('지출 목록 조회 중 오류:', error)
      } finally {
        isLoading.value = false
      }
    }

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

    const isEditFormValid = computed(() => {
      return editForm.value.date &&
        editForm.value.amount &&
        editForm.value.store_name &&
        editForm.value.description
    })

    // 파일 선택
    const handleFileSelect = async (event) => {
      const file = event.target.files[0]
      if (file) {
        uploadedFile.value = file

        // OCR 처리는 즉시 시작 (이미지 미리보기와 병렬 처리)
        performOcrAnalysis(file)

        // 이미지 미리보기는 비동기로 처리 (OCR 처리를 방해하지 않음)
        const reader = new FileReader()
        reader.onload = (e) => {
          imagePreview.value = e.target.result
        }
        reader.readAsDataURL(file)
      }
    }

    // 이미지 압축 함수
    const compressImage = (file, maxSize = 800, quality = 0.8) => {
      return new Promise((resolve) => {
        const reader = new FileReader()
        reader.onload = (e) => {
          const img = new Image()
          img.onload = () => {
            const canvas = document.createElement('canvas')
            let width = img.width
            let height = img.height

            // 비율 유지하면서 리사이즈
            if (width > height) {
              if (width > maxSize) {
                height = (height * maxSize) / width
                width = maxSize
              }
            } else {
              if (height > maxSize) {
                width = (width * maxSize) / height
                height = maxSize
              }
            }

            canvas.width = width
            canvas.height = height
            const ctx = canvas.getContext('2d')
            ctx.drawImage(img, 0, 0, width, height)

            // Canvas를 Blob으로 변환 (JPEG, 품질 0.8)
            canvas.toBlob(
              (blob) => {
                const compressedFile = new File([blob], file.name, {
                  type: 'image/jpeg',
                  lastModified: Date.now()
                })
                console.log('[이미지 압축] 원본:', (file.size / 1024).toFixed(2), 'KB -> 압축:', (compressedFile.size / 1024).toFixed(2), 'KB')
                resolve(compressedFile)
              },
              'image/jpeg',
              quality
            )
          }
          img.src = e.target.result
        }
        reader.readAsDataURL(file)
      })
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

    // OCR 분석 수행 (백엔드 API 호출 - Expense 생성 안함)
    const performOcrAnalysis = async (file) => {
      try {
        isLoading.value = true
        console.log('[OCR] 파일 업로드 시작:', file.name)

        // 백엔드 OCR API 호출 (OCR만 수행, Expense 생성 안함)
        const result = await receiptAPI.performOCR(file)

        console.log('[OCR] API 응답:', result)

        if (result.success) {
          console.log('[OCR] 성공:', result.data)

          // OCR 결과 저장
          ocrData.value = {
            date: result.data.date || new Date().toISOString().split('T')[0],
            amount: result.data.total_amount,
            merchant: result.data.store_name,
            address: result.data.store_address || '',
            phone: result.data.store_phone_number || ''
          }

          // OCR 결과를 폼에 자동 입력
          expenseForm.value.date = ocrData.value.date || ''
          expenseForm.value.amount = ocrData.value.amount || ''
          expenseForm.value.merchant = ocrData.value.merchant || ''
          expenseForm.value.address = ocrData.value.address || ''
          expenseForm.value.phone = ocrData.value.phone || ''

          alert(`OCR 처리 완료!\n상호명: ${ocrData.value.merchant}\n주소: ${ocrData.value.address || '정보 없음'}\n전화번호: ${ocrData.value.phone || '정보 없음'}\n금액: ${ocrData.value.amount}원\n\n"등록" 버튼을 눌러 지출 내역을 저장하세요.`)
        } else {
          console.error('[OCR] 실패:', result.error)
          alert('OCR 처리 실패: ' + result.error)
        }
      } catch (error) {
        console.error('[OCR] 처리 중 오류:', error)
        alert('OCR 처리 중 오류가 발생했습니다: ' + error.message)
      } finally {
        isLoading.value = false
      }
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
        description: '',
        receipt_id: '',
        address: '',
        phone: ''
      }
      ocrData.value = null
    }

    // 지출 등록
    const registerExpense = async () => {
      if (!isFormValid.value) {
        alert('모든 필드를 입력해주세요.')
        return
      }

      try {
        // 날짜를 ISO 형식으로 변환 (백엔드 datetime 형식)
        const dateObj = new Date(expenseForm.value.date)
        const isoDate = dateObj.toISOString()

        // 백엔드 API를 통해 지출 등록
        const expenseData = {
          receipt_id: 'manual-' + Date.now(),
          store_name: expenseForm.value.merchant,
          store_address: expenseForm.value.address || '',
          store_phone_number: expenseForm.value.phone || '',
          amount: parseFloat(expenseForm.value.amount),
          date: isoDate,  // ISO 형식으로 변환
          item_name: '',
          category: expenseForm.value.category,
          description: expenseForm.value.description || `${expenseForm.value.merchant}에서 구매`
        }

        console.log('[registerExpense] 전송 데이터:', expenseData)

        const result = await expenseAPI.createExpense(expenseData)

        if (result.success) {
          alert('지출 내역이 등록되었습니다.')
          // 지출 목록 다시 조회
          await fetchExpenses()
          closeOcrModal()
        } else {
          alert('지출 등록 실패: ' + result.error)
        }
      } catch (error) {
        console.error('지출 등록 중 오류:', error)
        alert('지출 등록 중 오류가 발생했습니다.')
      }
    }

    const formatDate = (dateString) => {
      const date = new Date(dateString)
      return date.toLocaleDateString('ko-KR', {
        month: 'short',
        day: 'numeric',
        weekday: 'short'
      })
    }

    // 지출 삭제
    const deleteExpense = async (expenseId) => {
      if (!confirm('이 지출 내역을 삭제하시겠습니까?')) {
        return
      }

      try {
        const result = await expenseAPI.deleteExpense(expenseId)
        if (result.success) {
          alert('지출 내역이 삭제되었습니다.')
          // 목록 새로고침
          await fetchExpenses()
        } else {
          alert('삭제 실패: ' + result.error)
        }
      } catch (error) {
        console.error('[삭제] 오류:', error)
        alert('삭제 중 오류가 발생했습니다.')
      }
    }

    // 수정 모달 열기
    const openEditModal = (expense) => {
      editingExpenseId.value = expense.id

      // 날짜를 YYYY-MM-DD 형식으로 변환
      const dateObj = new Date(expense.date)
      const year = dateObj.getFullYear()
      const month = String(dateObj.getMonth() + 1).padStart(2, '0')
      const day = String(dateObj.getDate()).padStart(2, '0')
      const formattedDate = `${year}-${month}-${day}`

      editForm.value = {
        date: formattedDate,
        amount: expense.amount,
        store_name: expense.store_name || '',
        store_address: expense.store_address || '',
        store_phone_number: expense.store_phone_number || '',
        category: expense.category,
        description: expense.description || ''
      }

      showEditModal.value = true
    }

    // 수정 모달 닫기
    const closeEditModal = () => {
      showEditModal.value = false
      editingExpenseId.value = null
      editForm.value = {
        date: '',
        amount: '',
        store_name: '',
        store_address: '',
        store_phone_number: '',
        category: '식비',
        description: ''
      }
    }

    // 지출 수정
    const updateExpense = async () => {
      if (!isEditFormValid.value) {
        alert('모든 필수 필드를 입력해주세요.')
        return
      }

      try {
        // 날짜를 ISO 형식으로 변환
        const dateObj = new Date(editForm.value.date)
        const isoDate = dateObj.toISOString()

        const updateData = {
          date: isoDate,
          amount: parseFloat(editForm.value.amount),
          store_name: editForm.value.store_name,
          store_address: editForm.value.store_address,
          store_phone_number: editForm.value.store_phone_number,
          category: editForm.value.category,
          description: editForm.value.description
        }

        console.log('[updateExpense] 수정 데이터:', updateData)

        const result = await expenseAPI.updateExpense(editingExpenseId.value, updateData)

        if (result.success) {
          alert('지출 내역이 수정되었습니다.')
          await fetchExpenses()
          closeEditModal()
        } else {
          alert('수정 실패: ' + result.error)
        }
      } catch (error) {
        console.error('[수정] 오류:', error)
        alert('수정 중 오류가 발생했습니다.')
      }
    }



    // 컴포넌트 마운트 시 지출 목록 조회
    onMounted(() => {
      fetchExpenses()
    })

    return {
      showOcrModal,
      showEditModal,
      selectedPeriod,
      searchQuery,
      selectedCategory,
      expenses,
      isLoading,
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
      editForm,
      handleFileSelect,
      handleCameraCapture,
      triggerFileSelect,
      triggerCamera,
      removeFile,
      formatAmount,
      closeOcrModal,
      registerExpense,
      isFormValid,
      isEditFormValid,
      fetchExpenses,
      deleteExpense,
      openEditModal,
      closeEditModal,
      updateExpense
    }
  }
}
</script>
