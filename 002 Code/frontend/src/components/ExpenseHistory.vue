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
        <button class="add-btn" @click="showOcrModal = true">+ 지출 등록 (OCR)</button>
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

    <!-- OCR 등록 모달 -->
    <div v-if="showOcrModal" class="modal-overlay" @click="closeOcrModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h2>
            <span class="modal-icon">📷</span>
            지출 등록 (OCR)
          </h2>
          <button class="close-modal-btn" @click="closeOcrModal">&times;</button>
        </div>

        <div class="modal-body">
          <!-- 영수증 업로드 섹션 -->
          <div class="upload-section">
            <label class="section-label">영수증 업로드</label>
            <div class="upload-area" :class="{ 'has-file': uploadedFile }">
              <input
                ref="fileInput"
                type="file"
                accept="image/*"
                @change="handleFileSelect"
                style="display: none"
              >
              <input
                ref="cameraInput"
                type="file"
                accept="image/*"
                capture="environment"
                @change="handleCameraCapture"
                style="display: none"
              >
              
              <div v-if="!uploadedFile" class="upload-placeholder">
                <span class="upload-icon">📄</span>
                <p class="upload-text">영수증 파일 선택 또는 카메라 실행</p>
              </div>
              
              <div v-if="uploadedFile" class="uploaded-preview">
                <div class="preview-info">
                  <span class="preview-icon">📷</span>
                  <span class="preview-name">{{ uploadedFile.name }}</span>
                  <button class="remove-file-btn" @click="removeFile">×</button>
                </div>
                <img v-if="imagePreview" :src="imagePreview" alt="영수증 미리보기" class="preview-image">
              </div>
              
              <div class="upload-buttons">
                <button class="upload-btn" @click="triggerFileSelect">
                  <span>📁</span> 파일 선택
                </button>
                <button class="upload-btn" @click="triggerCamera">
                  <span>📷</span> 카메라
                </button>
              </div>
            </div>
          </div>

          <!-- OCR 분석 결과 표시 -->
          <div class="ocr-result-section" v-if="ocrData">
            <label class="section-label">영수증 OCR 분석 결과</label>
            <div class="ocr-result-box">
              <div class="ocr-item">
                <span class="ocr-label">날짜:</span>
                <span class="ocr-value">{{ ocrData.date || '-' }}</span>
              </div>
              <div class="ocr-item">
                <span class="ocr-label">금액:</span>
                <span class="ocr-value">{{ ocrData.amount ? formatAmount(ocrData.amount) : '-' }}</span>
              </div>
              <div class="ocr-item">
                <span class="ocr-label">상호명:</span>
                <span class="ocr-value">{{ ocrData.merchant || '-' }}</span>
              </div>
            </div>
          </div>

          <!-- 입력 폼 -->
          <div class="form-section">
            <div class="form-row">
              <div class="form-group">
                <label>날짜</label>
                <div class="date-input-group">
                  <input
                    type="date"
                    v-model="expenseForm.date"
                    class="form-input date-input"
                    required
                  >
                  <span class="date-helper" v-if="!expenseForm.date">이 입력란을 작성하세요.</span>
                </div>
              </div>

              <div class="form-group">
                <label>금액(원)</label>
                <input
                  type="number"
                  v-model="expenseForm.amount"
                  class="form-input"
                  placeholder="금액 입력"
                  required
                >
              </div>
            </div>

            <div class="form-row">
              <div class="form-group">
                <label>상호명</label>
                <input
                  type="text"
                  v-model="expenseForm.merchant"
                  class="form-input"
                  placeholder="상호명"
                  required
                >
              </div>

              <div class="form-group">
                <label>카테고리</label>
                <select v-model="expenseForm.category" class="form-input">
                  <option value="식비">식비</option>
                  <option value="교통비">교통비</option>
                  <option value="사무용품">사무용품</option>
                  <option value="마케팅">마케팅</option>
                  <option value="기타">기타</option>
                </select>
              </div>
            </div>

            <div class="form-group">
              <label>지출 설명</label>
              <input
                type="text"
                v-model="expenseForm.description"
                class="form-input"
                placeholder="간단한 지출 목적"
                required
              >
            </div>
          </div>
        </div>

        <div class="modal-footer">
          <button class="cancel-btn" @click="closeOcrModal">취소</button>
          <button class="submit-btn" @click="registerExpense" :disabled="!isFormValid">
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

/* 모달 스타일 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
}

.modal-content {
  background: white;
  border-radius: 16px;
  width: 100%;
  max-width: 800px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24px 32px;
  border-bottom: 1px solid #e0e0e0;
  background: #f8f9fa;
  border-radius: 16px 16px 0 0;
}

.modal-header h2 {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 1.5rem;
  color: #2c3e50;
  margin: 0;
}

.modal-icon {
  font-size: 1.8rem;
}

.close-modal-btn {
  background: none;
  border: none;
  font-size: 32px;
  color: #666;
  cursor: pointer;
  padding: 0;
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: all 0.2s;
}

.close-modal-btn:hover {
  background: #e0e0e0;
  color: #333;
}

.modal-body {
  padding: 32px;
}

.section-label {
  display: block;
  font-size: 1.1rem;
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 12px;
}

/* 업로드 섹션 */
.upload-area {
  border: 2px dashed #ccc;
  border-radius: 12px;
  padding: 40px;
  text-align: center;
  background: #fafafa;
  transition: all 0.3s;
}

.upload-area.has-file {
  border-color: #1976d2;
  background: #f0f7ff;
}

.upload-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  margin-bottom: 24px;
}

.upload-icon {
  font-size: 48px;
}

.upload-text {
  color: #666;
  font-size: 1rem;
  margin: 0;
}

.uploaded-preview {
  margin-bottom: 24px;
}

.preview-info {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  padding: 12px;
  background: white;
  border-radius: 8px;
  margin-bottom: 12px;
}

.preview-icon {
  font-size: 24px;
}

.preview-name {
  flex: 1;
  font-weight: 500;
  color: #333;
}

.remove-file-btn {
  background: #f44336;
  color: white;
  border: none;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  cursor: pointer;
  font-size: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.2s;
}

.remove-file-btn:hover {
  background: #d32f2f;
}

.preview-image {
  max-width: 100%;
  max-height: 300px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.upload-buttons {
  display: flex;
  gap: 12px;
  justify-content: center;
}

.upload-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  background: #1976d2;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 500;
  transition: background 0.2s;
}

.upload-btn:hover {
  background: #1565c0;
}

.upload-btn span {
  font-size: 1.2rem;
}

/* OCR 결과 섹션 */
.ocr-result-section {
  margin-top: 32px;
}

.ocr-result-box {
  background: #f5f5f5;
  border-radius: 12px;
  padding: 20px;
  border: 1px solid #e0e0e0;
}

.ocr-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 0;
  border-bottom: 1px solid #e0e0e0;
}

.ocr-item:last-child {
  border-bottom: none;
}

.ocr-label {
  font-weight: 600;
  color: #666;
}

.ocr-value {
  font-weight: 500;
  color: #2c3e50;
}

/* 폼 섹션 */
.form-section {
  margin-top: 32px;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-bottom: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group label {
  font-weight: 500;
  color: #2c3e50;
  margin-bottom: 8px;
}

.form-input {
  padding: 12px 16px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.2s;
}

.form-input:focus {
  outline: none;
  border-color: #1976d2;
}

.date-input-group {
  position: relative;
}

.date-helper {
  position: absolute;
  top: 100%;
  left: 0;
  margin-top: 4px;
  font-size: 0.875rem;
  color: #666;
}

.form-group:has(.form-input:required:invalid) .date-helper {
  color: #f44336;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  padding: 24px 32px;
  border-top: 1px solid #e0e0e0;
  background: #f8f9fa;
  border-radius: 0 0 16px 16px;
}

.cancel-btn,
.submit-btn {
  padding: 12px 24px;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.cancel-btn {
  background: #e0e0e0;
  color: #666;
}

.cancel-btn:hover {
  background: #d0d0d0;
}

.submit-btn {
  background: #1976d2;
  color: white;
}

.submit-btn:hover:not(:disabled) {
  background: #1565c0;
}

.submit-btn:disabled {
  background: #ccc;
  cursor: not-allowed;
}

/* 모바일 반응형 */
@media (max-width: 768px) {
  .modal-content {
    max-width: 100%;
    max-height: 95vh;
    border-radius: 12px;
  }

  .modal-header {
    padding: 20px;
  }

  .modal-header h2 {
    font-size: 1.3rem;
  }

  .modal-body {
    padding: 24px;
  }

  .upload-area {
    padding: 24px 16px;
  }

  .upload-buttons {
    flex-direction: column;
  }

  .upload-btn {
    width: 100%;
    justify-content: center;
  }

  .form-row {
    grid-template-columns: 1fr;
    gap: 16px;
  }

  .modal-footer {
    padding: 20px;
    flex-direction: column-reverse;
  }

  .cancel-btn,
  .submit-btn {
    width: 100%;
  }
}
</style>