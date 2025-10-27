<template>
  <div class="settings">
    <div class="page-header">
      <h2>설정</h2>
      <button class="save-all-btn" @click="saveAllSettings">💾 모든 설정 저장</button>
    </div>

    <div class="settings-container">
      <!-- 사용자 정보 -->
      <div class="settings-section">
        <h3>👤 사용자 정보</h3>
        <div class="user-info-card">
          <div class="user-avatar">
            <span class="avatar-text">{{ userInfo?.name?.charAt(0) || 'U' }}</span>
          </div>
          <div class="user-details">
            <h4>{{ userInfo?.name || '사용자' }}</h4>
            <p class="user-email">{{ userInfo?.email || '이메일 없음' }}</p>
            <p class="user-role">{{ userInfo?.role === 'admin' ? '관리자' : '일반 사용자' }}</p>
            <p class="user-login-time">로그인 시간: {{ formatLoginTime(userInfo?.loginTime) }}</p>
          </div>
        </div>
      </div>

      <!-- 일반 설정 -->
      <div class="settings-section">
        <h3>일반 설정</h3>
        <div class="setting-item">
          <label class="setting-label">
            <span class="label-text">학교명</span>
            <input 
              v-model="settings.general.companyName" 
              type="text" 
              class="setting-input"
              placeholder="학교명을 입력하세요"
            >
          </label>
        </div>
        
        <div class="setting-item">
          <label class="setting-label">
            <span class="label-text">기본 통화</span>
            <select v-model="settings.general.currency" class="setting-select">
              <option value="KRW">원 (KRW)</option>
              <option value="USD">달러 (USD)</option>
              <option value="EUR">유로 (EUR)</option>
              <option value="JPY">엔 (JPY)</option>
            </select>
          </label>
        </div>

        <div class="setting-item">
          <label class="setting-label">
            <span class="label-text">언어</span>
            <select v-model="settings.general.language" class="setting-select">
              <option value="ko">한국어</option>
              <option value="en">English</option>
              <option value="ja">日本語</option>
            </select>
          </label>
        </div>

        <div class="setting-item">
          <label class="setting-label">
            <span class="label-text">시간대</span>
            <select v-model="settings.general.timezone" class="setting-select">
              <option value="Asia/Seoul">서울 (UTC+9)</option>
              <option value="America/New_York">뉴욕 (UTC-5)</option>
              <option value="Europe/London">런던 (UTC+0)</option>
              <option value="Asia/Tokyo">도쿄 (UTC+9)</option>
            </select>
          </label>
        </div>
      </div>

      <!-- 예산 설정 -->
      <div class="settings-section">
        <h3>예산 설정</h3>
        <div class="setting-item">
          <label class="setting-label">
            <span class="label-text">예산 승인 한도</span>
            <input 
              v-model.number="settings.budget.approvalLimit" 
              type="number" 
              class="setting-input"
              placeholder="0"
            >
          </label>
          <span class="setting-description">이 금액을 초과하는 예산은 승인이 필요합니다</span>
        </div>

        <div class="setting-item">
          <label class="setting-label">
            <span class="label-text">예산 경고 임계값 (%)</span>
            <input 
              v-model.number="settings.budget.warningThreshold" 
              type="number" 
              min="0" 
              max="100"
              class="setting-input"
              placeholder="80"
            >
          </label>
          <span class="setting-description">예산 사용률이 이 값을 초과하면 경고를 표시합니다</span>
        </div>

        <div class="setting-item">
          <div class="checkbox-group">
            <label class="checkbox-label">
              <input 
                v-model="settings.budget.autoApproval" 
                type="checkbox" 
                class="setting-checkbox"
              >
              <span class="checkmark"></span>
              <span class="checkbox-text">한도 내 자동 승인</span>
            </label>
          </div>
        </div>

        <div class="setting-item">
          <div class="checkbox-group">
            <label class="checkbox-label">
              <input 
                v-model="settings.budget.monthlyReset" 
                type="checkbox" 
                class="setting-checkbox"
              >
              <span class="checkmark"></span>
              <span class="checkbox-text">월별 예산 자동 리셋</span>
            </label>
          </div>
        </div>
      </div>

      <!-- 알림 설정 -->
      <div class="settings-section">
        <h3>알림 설정</h3>
        <div class="setting-item">
          <div class="checkbox-group">
            <label class="checkbox-label">
              <input 
                v-model="settings.notifications.email" 
                type="checkbox" 
                class="setting-checkbox"
              >
              <span class="checkmark"></span>
              <span class="checkbox-text">이메일 알림</span>
            </label>
          </div>
        </div>

        <div class="setting-item">
          <div class="checkbox-group">
            <label class="checkbox-label">
              <input 
                v-model="settings.notifications.push" 
                type="checkbox" 
                class="setting-checkbox"
              >
              <span class="checkmark"></span>
              <span class="checkbox-text">푸시 알림</span>
            </label>
          </div>
        </div>

        <div class="setting-item">
          <div class="checkbox-group">
            <label class="checkbox-label">
              <input 
                v-model="settings.notifications.budgetWarning" 
                type="checkbox" 
                class="setting-checkbox"
              >
              <span class="checkmark"></span>
              <span class="checkbox-text">예산 경고 알림</span>
            </label>
          </div>
        </div>

        <div class="setting-item">
          <div class="checkbox-group">
            <label class="checkbox-label">
              <input 
                v-model="settings.notifications.monthlyReport" 
                type="checkbox" 
                class="setting-checkbox"
              >
              <span class="checkmark"></span>
              <span class="checkbox-text">월간 리포트 알림</span>
            </label>
          </div>
        </div>
      </div>

      <!-- 보안 설정 -->
      <div class="settings-section">
        <h3>보안 설정</h3>
        <div class="setting-item">
          <label class="setting-label">
            <span class="label-text">세션 만료 시간 (분)</span>
            <input 
              v-model.number="settings.security.sessionTimeout" 
              type="number" 
              min="5" 
              max="480"
              class="setting-input"
              placeholder="30"
            >
          </label>
        </div>

        <div class="setting-item">
          <div class="checkbox-group">
            <label class="checkbox-label">
              <input 
                v-model="settings.security.twoFactorAuth" 
                type="checkbox" 
                class="setting-checkbox"
              >
              <span class="checkmark"></span>
              <span class="checkbox-text">2단계 인증 활성화</span>
            </label>
          </div>
        </div>

        <div class="setting-item">
          <div class="checkbox-group">
            <label class="checkbox-label">
              <input 
                v-model="settings.security.loginNotification" 
                type="checkbox" 
                class="setting-checkbox"
              >
              <span class="checkmark"></span>
              <span class="checkbox-text">로그인 알림</span>
            </label>
          </div>
        </div>

        <div class="setting-item">
          <button class="change-password-btn" @click="showPasswordModal = true">
            🔒 비밀번호 변경
          </button>
        </div>
      </div>

      <!-- 데이터 관리 -->
      <div class="settings-section">
        <h3>데이터 관리</h3>
        <div class="setting-item">
          <label class="setting-label">
            <span class="label-text">데이터 보관 기간 (개월)</span>
            <input 
              v-model.number="settings.data.retentionPeriod" 
              type="number" 
              min="1" 
              max="120"
              class="setting-input"
              placeholder="12"
            >
          </label>
          <span class="setting-description">이 기간이 지난 데이터는 자동으로 아카이브됩니다</span>
        </div>

        <div class="setting-item">
          <div class="data-actions">
            <button class="export-btn" @click="exportData">
              📤 데이터 내보내기
            </button>
            <button class="backup-btn" @click="backupData">
              💾 백업 생성
            </button>
          </div>
        </div>

        <div class="setting-item danger-zone">
          <h4>위험 구역</h4>
          <p class="danger-description">
            아래 작업들은 되돌릴 수 없습니다. 신중하게 진행하세요.
          </p>
          <div class="danger-actions">
            <button class="danger-btn" @click="resetSettings">
              🔄 설정 초기화
            </button>
            <button class="danger-btn" @click="clearAllData">
              🗑️ 모든 데이터 삭제
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 비밀번호 변경 모달 -->
    <div v-if="showPasswordModal" class="modal-overlay" @click="closePasswordModal">
      <div class="modal-content" @click.stop>
        <h3>비밀번호 변경</h3>
        <div class="form-group">
          <label>현재 비밀번호</label>
          <input v-model="passwordForm.current" type="password" placeholder="현재 비밀번호">
        </div>
        <div class="form-group">
          <label>새 비밀번호</label>
          <input v-model="passwordForm.new" type="password" placeholder="새 비밀번호">
        </div>
        <div class="form-group">
          <label>새 비밀번호 확인</label>
          <input v-model="passwordForm.confirm" type="password" placeholder="새 비밀번호 확인">
        </div>
        <div class="form-actions">
          <button class="cancel-btn" @click="closePasswordModal">취소</button>
          <button class="save-btn" @click="changePassword">변경</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'

export default {
  name: 'Settings',
  setup() {
    const showPasswordModal = ref(false)
    
    // 사용자 정보 가져오기
    const userInfo = ref(null)
    
    // 로컬 스토리지에서 사용자 정보 로드
    const loadUserInfo = () => {
      const storedUserInfo = localStorage.getItem('userInfo')
      if (storedUserInfo) {
        userInfo.value = JSON.parse(storedUserInfo)
      }
    }
    
    // 로그인 시간 포맷팅
    const formatLoginTime = (loginTime) => {
      if (!loginTime) return '알 수 없음'
      const date = new Date(loginTime)
      return date.toLocaleString('ko-KR', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
      })
    }
    
    // 컴포넌트 마운트 시 사용자 정보 로드
    loadUserInfo()
    
    const settings = ref({
      general: {
        companyName: '우리학교',
        currency: 'KRW',
        language: 'ko',
        timezone: 'Asia/Seoul'
      },
      budget: {
        approvalLimit: 1000000,
        warningThreshold: 80,
        autoApproval: true,
        monthlyReset: true
      },
      notifications: {
        email: true,
        push: true,
        budgetWarning: true,
        monthlyReport: true
      },
      security: {
        sessionTimeout: 30,
        twoFactorAuth: false,
        loginNotification: true
      },
      data: {
        retentionPeriod: 12
      }
    })

    const passwordForm = ref({
      current: '',
      new: '',
      confirm: ''
    })

    const saveAllSettings = () => {
      // 실제로는 API 호출
      alert('모든 설정이 저장되었습니다.')
    }

    const closePasswordModal = () => {
      showPasswordModal.value = false
      passwordForm.value = {
        current: '',
        new: '',
        confirm: ''
      }
    }

    const changePassword = () => {
      if (passwordForm.value.new !== passwordForm.value.confirm) {
        alert('새 비밀번호가 일치하지 않습니다.')
        return
      }
      // 실제로는 API 호출
      alert('비밀번호가 변경되었습니다.')
      closePasswordModal()
    }

    const exportData = () => {
      alert('데이터 내보내기를 시작합니다.')
    }

    const backupData = () => {
      alert('백업을 생성합니다.')
    }

    const resetSettings = () => {
      if (confirm('정말로 모든 설정을 초기화하시겠습니까?')) {
        alert('설정이 초기화되었습니다.')
      }
    }

    const clearAllData = () => {
      if (confirm('정말로 모든 데이터를 삭제하시겠습니까? 이 작업은 되돌릴 수 없습니다.')) {
        alert('모든 데이터가 삭제되었습니다.')
      }
    }

    return {
      showPasswordModal,
      userInfo,
      formatLoginTime,
      settings,
      passwordForm,
      saveAllSettings,
      closePasswordModal,
      changePassword,
      exportData,
      backupData,
      resetSettings,
      clearAllData
    }
  }
}
</script>

<style scoped>
.settings {
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

.save-all-btn {
  background: #4caf50;
  color: white;
  border: none;
  padding: 12px 20px;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  transition: background 0.3s ease;
}

.save-all-btn:hover {
  background: #45a049;
}

.settings-container {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.settings-section {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.settings-section h3 {
  color: #2c3e50;
  margin: 0 0 1.5rem 0;
  font-size: 1.3rem;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid #e3f2fd;
}

/* 사용자 정보 카드 스타일 */
.user-info-card {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  padding: 1.5rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 12px;
  color: white;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
}

.user-avatar {
  width: 60px;
  height: 60px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  font-weight: bold;
  backdrop-filter: blur(10px);
}

.avatar-text {
  color: white;
  font-size: 1.5rem;
  font-weight: bold;
}

.user-details h4 {
  margin: 0 0 0.5rem 0;
  font-size: 1.2rem;
  font-weight: 600;
}

.user-details p {
  margin: 0.25rem 0;
  font-size: 0.9rem;
  opacity: 0.9;
}

.user-email {
  font-weight: 500;
}

.user-role {
  background: rgba(255, 255, 255, 0.2);
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  display: inline-block;
  font-size: 0.8rem;
  font-weight: 500;
}

.user-login-time {
  font-size: 0.8rem;
  opacity: 0.8;
}

.setting-item {
  margin-bottom: 1.5rem;
}

.setting-item:last-child {
  margin-bottom: 0;
}

.setting-label {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.label-text {
  color: #2c3e50;
  font-weight: 500;
  font-size: 0.95rem;
}

.setting-input, .setting-select {
  padding: 12px 16px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.3s ease;
}

.setting-input:focus, .setting-select:focus {
  outline: none;
  border-color: #1976d2;
}

.setting-description {
  font-size: 0.85rem;
  color: #666;
  margin-top: 0.25rem;
}

.checkbox-group {
  display: flex;
  align-items: center;
}

.checkbox-label {
  display: flex;
  align-items: center;
  cursor: pointer;
  position: relative;
}

.setting-checkbox {
  position: absolute;
  opacity: 0;
  cursor: pointer;
}

.checkmark {
  width: 20px;
  height: 20px;
  background: #f0f0f0;
  border: 2px solid #ddd;
  border-radius: 4px;
  margin-right: 12px;
  position: relative;
  transition: all 0.3s ease;
}

.setting-checkbox:checked + .checkmark {
  background: #1976d2;
  border-color: #1976d2;
}

.setting-checkbox:checked + .checkmark:after {
  content: '';
  position: absolute;
  left: 6px;
  top: 2px;
  width: 6px;
  height: 10px;
  border: solid white;
  border-width: 0 2px 2px 0;
  transform: rotate(45deg);
}

.checkbox-text {
  color: #2c3e50;
  font-weight: 500;
}

.change-password-btn {
  background: #ff9800;
  color: white;
  border: none;
  padding: 12px 20px;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  transition: background 0.3s ease;
}

.change-password-btn:hover {
  background: #f57c00;
}

.data-actions {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.export-btn, .backup-btn {
  background: #1976d2;
  color: white;
  border: none;
  padding: 12px 20px;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  transition: background 0.3s ease;
}

.export-btn:hover, .backup-btn:hover {
  background: #1565c0;
}

.danger-zone {
  border: 2px solid #ffebee;
  border-radius: 8px;
  padding: 1.5rem;
  background: #fafafa;
}

.danger-zone h4 {
  color: #f44336;
  margin: 0 0 0.5rem 0;
  font-size: 1.1rem;
}

.danger-description {
  color: #666;
  margin: 0 0 1rem 0;
  font-size: 0.9rem;
}

.danger-actions {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.danger-btn {
  background: #f44336;
  color: white;
  border: none;
  padding: 10px 16px;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
  font-size: 0.9rem;
  transition: background 0.3s ease;
}

.danger-btn:hover {
  background: #d32f2f;
}

/* 모달 스타일 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  width: 90%;
  max-width: 400px;
}

.modal-content h3 {
  color: #2c3e50;
  margin: 0 0 1.5rem 0;
  font-size: 1.5rem;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  color: #2c3e50;
  font-weight: 500;
}

.form-group input {
  width: 100%;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 1rem;
}

.form-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  margin-top: 2rem;
}

.cancel-btn, .save-btn {
  padding: 12px 24px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
  transition: background 0.3s ease;
}

.cancel-btn {
  background: #f5f5f5;
  color: #666;
}

.cancel-btn:hover {
  background: #e0e0e0;
}

.save-btn {
  background: #1976d2;
  color: white;
}

.save-btn:hover {
  background: #1565c0;
}

/* PC 최적화 (1200px 이상) */
@media (min-width: 1200px) {
  .settings-container {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 2.5rem;
  }
  
  .settings-section {
    padding: 2.5rem;
  }
  
  .settings-section h3 {
    font-size: 1.4rem;
    margin-bottom: 2rem;
  }
  
  .setting-item {
    margin-bottom: 2rem;
  }
  
  .setting-input, .setting-select {
    padding: 14px 18px;
    font-size: 1.1rem;
  }
  
  .data-actions {
    gap: 1.5rem;
  }
  
  .export-btn, .backup-btn, .change-password-btn {
    padding: 14px 24px;
    font-size: 1.1rem;
  }
}

/* 태블릿 (769px - 1199px) */
@media (max-width: 1199px) and (min-width: 769px) {
  .settings-container {
    gap: 2rem;
  }
  
  .settings-section {
    padding: 2rem;
  }
}

/* 모바일 (768px 이하) */
@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    align-items: stretch;
    gap: 1rem;
  }
  
  .save-all-btn {
    width: 100%;
    padding: 14px 20px;
    font-size: 1.1rem;
  }
  
  .settings-container {
    gap: 1.5rem;
  }
  
  .settings-section {
    padding: 1.8rem;
  }
  
  .settings-section h3 {
    font-size: 1.2rem;
  }
  
  .setting-item {
    margin-bottom: 1.8rem;
  }
  
  .setting-input, .setting-select {
    padding: 14px 16px;
    font-size: 1rem;
  }
  
  .checkbox-label {
    padding: 0.5rem 0;
  }
  
  .checkmark {
    width: 22px;
    height: 22px;
    margin-right: 15px;
  }
  
  .checkbox-text {
    font-size: 1rem;
  }
  
  .change-password-btn {
    width: 100%;
    padding: 14px 20px;
    font-size: 1.1rem;
  }
  
  .data-actions {
    flex-direction: column;
    gap: 1rem;
  }
  
  .export-btn, .backup-btn {
    width: 100%;
    padding: 14px 20px;
    font-size: 1.1rem;
  }
  
  .danger-actions {
    flex-direction: column;
    gap: 1rem;
  }
  
  .danger-btn {
    width: 100%;
    padding: 12px 16px;
    font-size: 1rem;
  }
}

/* 소형 모바일 (480px 이하) */
@media (max-width: 480px) {
  .page-header h2 {
    font-size: 1.5rem;
  }
  
  .settings-section {
    padding: 1.2rem;
  }
  
  .settings-section h3 {
    font-size: 1.1rem;
  }
  
  .setting-item {
    margin-bottom: 1.5rem;
  }
  
  .label-text {
    font-size: 0.9rem;
  }
  
  .setting-description {
    font-size: 0.8rem;
  }
  
  .danger-zone {
    padding: 1.2rem;
  }
  
  .danger-zone h4 {
    font-size: 1rem;
  }
  
  .modal-content {
    padding: 1.5rem;
    margin: 1rem;
  }
  
  .form-group {
    margin-bottom: 1.2rem;
  }
  
  .form-group input {
    padding: 14px 16px;
    font-size: 1rem;
  }
  
  .form-actions {
    flex-direction: column;
    gap: 0.8rem;
  }
  
  .cancel-btn, .save-btn {
    width: 100%;
    padding: 14px 20px;
  }
}
</style>