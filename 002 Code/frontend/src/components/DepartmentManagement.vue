<template>
  <div class="autonomous-management max-w-6xl mx-auto">
    <!-- 페이지 헤더 -->
    <div class="page-header">
      <h2 class="page-title">자치기구 관리</h2>
    </div>

    <!-- 사용자 자치기구 정보 -->
    <div v-if="!userInfo?.organizationName" class="empty-state">
      <div class="empty-icon">🏛️</div>
      <h3>자치기구 정보가 없습니다</h3>
      <p>회원가입 시 자치기구 정보를 입력해주세요.</p>
    </div>

    <template v-else>
      <!-- 내 자치기구 정보 -->
      <div class="my-org-section">
        <h3 class="section-header">내 자치기구</h3>
        <div class="organization-card my-org-card">
        <!-- 카드 헤더 -->
        <div class="card-header">
          <div class="org-main-info">
            <div class="org-details">
                <h3 class="org-name">{{ userInfo.organizationName }}</h3>
                <p class="org-subtitle">{{ getSubtitle() }}</p>
            </div>
          </div>
            <div class="budget-status">
              <span class="status-badge">소속</span>
          </div>
        </div>

          <!-- 조직 정보 -->
          <div class="org-info-section">
            <div class="info-grid">
              <div class="info-item">
                <span class="info-label">조직 유형</span>
                <span class="info-value">{{ userInfo.organizationType || '-' }}</span>
            </div>
              <div class="info-item" v-if="userInfo.organizationSubType">
                <span class="info-label">세부 유형</span>
                <span class="info-value">{{ userInfo.organizationSubType }}</span>
            </div>
              <div class="info-item">
                <span class="info-label">학교</span>
                <span class="info-value">{{ userInfo.school || '-' }}</span>
          </div>
              <div class="info-item">
                <span class="info-label">학과</span>
                <span class="info-value">{{ userInfo.department || '-' }}</span>
            </div>
              <div class="info-item">
                <span class="info-label">내 직책</span>
                <span class="info-value">{{ userInfo.position || '-' }}</span>
            </div>
          </div>
        </div>

        <!-- 임원 정보 -->
        <div class="officers-section">
          <h4 class="section-title">임원 정보</h4>
            <div class="officers-list" v-if="myOrgOfficers.length > 0">
              <div v-for="officer in myOrgOfficers" :key="officer.id" class="officer-item">
              <span class="officer-name">{{ officer.name }}</span>
                <span class="officer-role">{{ officer.position || '직책 없음' }}</span>
            </div>
          </div>
            <div v-else class="loading-text">로딩 중...</div>
        </div>

          <!-- 월 선택 + PDF 내보내기 -->
          <div class="p-4 flex flex-col sm:flex-row gap-3 sm:items-center">
            <div class="flex gap-2 items-center">
              <select v-model="selectedYear" class="input-field w-28">
                <option v-for="y in [new Date().getFullYear(), new Date().getFullYear()-1, new Date().getFullYear()-2]" :key="y" :value="y">{{ y }}년</option>
              </select>
              <select v-model="selectedMonth" class="input-field w-24">
                <option v-for="m in 12" :key="m" :value="m">{{ m }}월</option>
              </select>
              <button class="btn-secondary" @click="openExpensePreview">조회</button>
            </div>
            <div class="flex gap-2">
              <button class="btn-primary" @click="createShareQR" v-if="!readOnly">🔗 QR 공유</button>
            </div>
        </div>
      </div>
    </div>

      <!-- 다른 자치기구 목록 -->
      <div class="other-orgs-section">
        <h3 class="section-header">다른 자치기구</h3>
        <div v-if="otherOrganizations.length > 0" class="organizations-grid">
          <div v-for="org in otherOrganizations" :key="org.name" class="organization-card">
            <div class="card-header">
              <div class="org-main-info">
                <div class="org-details">
                  <h3 class="org-name">{{ org.name }}</h3>
                  <p class="org-subtitle">{{ org.school }} {{ org.department }}</p>
        </div>
            </div>
            </div>

            <div class="org-info-section">
              <div class="info-grid">
                <div class="info-item">
                  <span class="info-label">조직 유형</span>
                  <span class="info-value">{{ org.organizationType || '-' }}</span>
                </div>
                <div class="info-item" v-if="org.organizationSubType">
                  <span class="info-label">세부 유형</span>
                  <span class="info-value">{{ org.organizationSubType }}</span>
                </div>
            </div>
          </div>

            <!-- 임원 정보 -->
            <div class="officers-section">
              <h4 class="section-title">임원 정보</h4>
              <div class="officers-list" v-if="org.officers && org.officers.length > 0">
                <div v-for="officer in org.officers" :key="officer.id" class="officer-item">
                  <span class="officer-name">{{ officer.name }}</span>
                  <span class="officer-role">{{ officer.position || '직책 없음' }}</span>
            </div>
            </div>
              <div v-else class="empty-officers">임원 정보 없음</div>
          </div>
        </div>
      </div>
        <div v-else class="empty-state">
          <p>다른 자치기구가 없습니다.</p>
    </div>
      </div>
    </template>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { authAPI } from '../services/api.js'

export default {
  name: 'DepartmentManagement',
  props: {
    userInfo: {
      type: Object,
      default: null
    }
  },
  setup(props) {
    const myOrgOfficers = ref([])
    const otherOrganizations = ref([])
    const isLoading = ref(true)
    const expensePreviewRef = ref(null)
    const now = new Date()
    const selectedYear = ref(now.getFullYear())
    const selectedMonth = ref(now.getMonth()+1)
    const selectedOrgExpenses = ref([])
    // 공유 링크로 접근 시 읽기 전용 모드
    const shareToken = new URLSearchParams(window.location.search).get('share')
    const hasAccessToken = !!localStorage.getItem('access_token')
    const readOnly = ref(!hasAccessToken && !!shareToken)

    const getSubtitle = () => {
      if (!props.userInfo) return ''
      const parts = []
      if (props.userInfo.school) parts.push(props.userInfo.school)
      if (props.userInfo.organizationName) {
        return `${props.userInfo.organizationName}`
      }
      return parts.join(' ')
    }

    const loadMyOrgOfficers = async () => {
      if (!props.userInfo?.organizationName) return

      try {
        const users = await authAPI.getUsersByOrganization(props.userInfo.organizationName)
        myOrgOfficers.value = users.map(user => ({
          id: user.id,
          name: user.name,
          position: user.position,
          email: user.email
        }))
      } catch (error) {
        console.error('내 조직 임원 조회 실패:', error)
      }
    }

    const loadOtherOrganizations = async () => {
      try {
        const orgs = await authAPI.getAllOrganizations()
        // 내 조직 제외
        otherOrganizations.value = orgs.filter(org => 
          org.name !== props.userInfo?.organizationName
        )
      } catch (error) {
        console.error('다른 자치기구 조회 실패:', error)
      } finally {
        isLoading.value = false
      }
    }

    onMounted(async () => {
      await Promise.all([
        loadMyOrgOfficers(),
        loadOtherOrganizations()
      ])
      await fetchMonthlyExpenses()
    })

    const fetchMonthlyExpenses = async () => {
      try {
        // 공유 모드에서는 토큰 없이 공개 API 사용
        const start = new Date(selectedYear.value, selectedMonth.value-1, 1)
        const end = new Date(selectedYear.value, selectedMonth.value, 0, 23, 59, 59)
        // FastAPI datetime 타입을 위해 ISO 8601 형식으로 전달 (URL 인코딩 하지 않음)
        const startStr = start.toISOString()
        const endStr = end.toISOString()

        const token = localStorage.getItem('access_token')
        const apiBase = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

        if (readOnly.value) {
          // 공유 모드
          const url = `${apiBase}/public/expenses?token=${encodeURIComponent(shareToken)}&start_date=${startStr}&end_date=${endStr}&limit=10000`
          const res = await fetch(url)
          if (!res.ok) throw new Error('조회 실패')
          const arr = await res.json()
          selectedOrgExpenses.value = Array.isArray(arr) ? arr : []
        } else {
          // 로그인 모드
          if (!props.userInfo?.organizationName) { selectedOrgExpenses.value = []; return }
          const url = `${apiBase}/expense/?start_date=${startStr}&end_date=${endStr}&limit=10000`
          const res = await fetch(url, {
            headers: {
              ...(token ? { Authorization: `Bearer ${token}` } : {})
            }
          })
          if (!res.ok) {
            const errorText = await res.text()
            console.error('API 에러 응답:', errorText)
            throw new Error(`조회 실패: ${res.status}`)
          }
          const expenses = await res.json()
          selectedOrgExpenses.value = Array.isArray(expenses) ? expenses : []
        }
      } catch (e) {
        console.error('월별 지출 조회 실패:', e)
        selectedOrgExpenses.value = []
      }
    }

    const openExpensePreview = async () => {
      try {
        await fetchMonthlyExpenses()

        if (selectedOrgExpenses.value.length === 0) {
          alert('해당 월에 지출 내역이 없습니다.')
          return
        }

        // 백엔드 API를 사용하여 영수증 이미지 포함 PDF 생성
        const expenseIds = selectedOrgExpenses.value.map(e => e.id).filter(Boolean)
        if (expenseIds.length === 0) {
          alert('유효한 지출 내역이 없습니다.')
          return
        }

        const token = localStorage.getItem('access_token')
        const apiBase = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

        const res = await fetch(`${apiBase}/expense/report/pdf`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            ...(token ? { Authorization: `Bearer ${token}` } : {})
          },
          body: JSON.stringify(expenseIds)
        })

        if (!res.ok) {
          throw new Error('PDF 생성 실패')
        }

        // PDF blob을 받아서 새 탭에서 열기
        const blob = await res.blob()
        const blobUrl = URL.createObjectURL(blob)
        window.open(blobUrl, '_blank')

      } catch (e) {
        console.error('PDF 미리보기 실패:', e)
        alert('PDF 미리보기에 실패했습니다.')
      }
    }

    const createShareQR = async () => {
      try {
        const apiBase = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
        const token = localStorage.getItem('access_token')
        const res = await fetch(`${apiBase}/public/share/create`, {
          method: 'POST',
          headers: { ...(token ? { Authorization: `Bearer ${token}` } : {}) }
        })
        if (!res.ok) throw new Error('공유 링크 생성 실패')
        const data = await res.json()
        const share = data.token
        const shareUrl = `${window.location.origin}${window.location.pathname}?share=${encodeURIComponent(share)}`
        const qrUrl = `https://api.qrserver.com/v1/create-qr-code/?size=240x240&data=${encodeURIComponent(shareUrl)}`
        const w = window.open('', '_blank')
        if (w) {
          w.document.write(`<div style="font-family:sans-serif;text-align:center;padding:20px">
            <h3>자치기구관리 QR 공유</h3>
            <p><a href="${shareUrl}" target="_blank">링크 열기</a></p>
            <img src="${qrUrl}" alt="QR Code" />
            <p style="margin-top:10px;font-size:12px;color:#666">URL: ${shareUrl}</p>
          </div>`)
          w.document.close()
        }
      } catch (e) {
        console.error('QR 생성 실패:', e)
        alert('QR 생성에 실패했습니다.')
      }
    }

    return {
      myOrgOfficers,
      otherOrganizations,
      isLoading,
      getSubtitle,
      expensePreviewRef,
      selectedYear,
      selectedMonth,
      selectedOrgExpenses,
      fetchMonthlyExpenses,
      openExpensePreview,
      createShareQR,
      readOnly
    }
  }
}
</script>

<style scoped>
.autonomous-management {
  padding: 2rem;
}

/* 페이지 헤더 */
.page-header {
  margin-bottom: 2rem;
}

.page-title {
  color: #2c3e50;
  font-size: 2rem;
  font-weight: 700;
  margin: 0;
}

.section-header {
  color: #2c3e50;
  font-size: 1.3rem;
  font-weight: 600;
  margin-bottom: 1rem;
}

/* 섹션 */
.my-org-section, .other-orgs-section {
  margin-bottom: 3rem;
}

/* 빈 상태 */
.empty-state {
  text-align: center;
  padding: 4rem 2rem;
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
}

.empty-state h3 {
  color: #2c3e50;
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
}

.empty-state p {
  color: #64748b;
  font-size: 1rem;
}

/* 조직 카드 */
.organization-card {
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  overflow: hidden;
  border: 2px solid transparent;
}

.my-org-card {
  border: 2px solid #667eea;
}

/* 카드 헤더 */
.card-header {
  padding: 1.5rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.org-main-info {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.org-details h3 {
  margin: 0 0 0.25rem 0;
  font-size: 1.4rem;
  font-weight: 700;
}

.org-subtitle {
  margin: 0;
  font-size: 0.9rem;
  opacity: 0.9;
}

.budget-status {
  display: flex;
  align-items: center;
}

.status-badge {
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 600;
  background: rgba(255, 255, 255, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.3);
}

/* 조직 정보 섹션 */
.org-info-section {
  padding: 1.5rem;
  border-bottom: 1px solid #f1f5f9;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.info-label {
  font-size: 0.85rem;
  color: #64748b;
  font-weight: 500;
}

.info-value {
  font-size: 1.1rem;
  font-weight: 700;
  color: #1e293b;
}

/* 임원 섹션 */
.officers-section {
  padding: 1rem 1.5rem;
}

.section-title {
  margin: 0 0 1rem 0;
  font-size: 1rem;
  font-weight: 600;
  color: #374151;
}

.officers-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.officer-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem 0;
}

.officer-name {
  font-weight: 500;
  color: #1e293b;
}

.officer-role {
  font-size: 0.85rem;
  color: #64748b;
  background: #f1f5f9;
  padding: 2px 8px;
  border-radius: 12px;
}

.loading-text, .empty-officers {
  color: #64748b;
  font-size: 0.9rem;
  text-align: center;
  padding: 1rem 0;
}

/* 그리드 */
.organizations-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 1.5rem;
}

/* 반응형 디자인 */
@media (max-width: 768px) {
  .autonomous-management {
    padding: 1rem;
  }

  .page-title {
    font-size: 1.5rem;
  }

  .info-grid {
    grid-template-columns: 1fr;
  }

  .card-header {
    flex-direction: column;
    gap: 1rem;
    align-items: stretch;
  }

  .org-main-info {
    justify-content: space-between;
  }

  .organizations-grid {
    grid-template-columns: 1fr;
  }
}
</style>
