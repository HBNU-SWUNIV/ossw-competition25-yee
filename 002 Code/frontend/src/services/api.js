// API 서비스 - 백엔드와 통신하는 함수들
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

// API 요청 헬퍼 함수
const apiRequest = async (endpoint, options = {}) => {
  const token = localStorage.getItem('access_token')

  const config = {
    headers: {
      'Content-Type': 'application/json',
      ...(token && { Authorization: `Bearer ${token}` }),
      ...options.headers
    },
    ...options
  }

  try {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, config)

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}))
      throw new Error(errorData.detail || `HTTP error! status: ${response.status}`)
    }

    return await response.json()
  } catch (error) {
    console.error('API Request Error:', error)
    throw error
  }
}

// 인증 관련 API
export const authAPI = {
  // 로그인
  login: async (email, password) => {
    const response = await apiRequest('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email, password })
    })

    // 토큰 저장
    if (response.access_token) {
      localStorage.setItem('access_token', response.access_token)
    }

    return response
  },

  // 회원가입
  register: async (userData) => {
    return await apiRequest('/auth/register', {
      method: 'POST',
      body: JSON.stringify(userData)
    })
  },

  // 현재 사용자 정보 조회
  getMe: async () => {
    return await apiRequest('/auth/me')
  },

  // 로그아웃
  logout: async () => {
    localStorage.removeItem('access_token')
    localStorage.removeItem('userInfo')
    localStorage.removeItem('isLoggedIn')
    return await apiRequest('/auth/logout', { method: 'POST' })
  }
}

// 예산 관련 API
export const budgetAPI = {
  // 예산 목록 조회
  getAll: async () => {
    return await apiRequest('/budget/')
  },

  // 예산 생성
  create: async (budgetData) => {
    return await apiRequest('/budget/', {
      method: 'POST',
      body: JSON.stringify(budgetData)
    })
  },

  // 특정 예산 조회
  getById: async (budgetId) => {
    return await apiRequest(`/budget/${budgetId}`)
  },

  // 예산 수정
  update: async (budgetId, budgetData) => {
    return await apiRequest(`/budget/${budgetId}`, {
      method: 'PUT',
      body: JSON.stringify(budgetData)
    })
  },

  // 예산 삭제
  delete: async (budgetId) => {
    return await apiRequest(`/budget/${budgetId}`, {
      method: 'DELETE'
    })
  }
}

// 지출 관련 API
export const expenseAPI = {
  // 지출 목록 조회
  getAll: async (params = {}) => {
    const queryString = new URLSearchParams(params).toString()
    const endpoint = queryString ? `/expense/?${queryString}` : '/expense/'
    return await apiRequest(endpoint)
  },

  // 지출 생성
  create: async (expenseData) => {
    return await apiRequest('/expense/', {
      method: 'POST',
      body: JSON.stringify(expenseData)
    })
  },

  // 특정 지출 조회
  getById: async (expenseId) => {
    return await apiRequest(`/expense/${expenseId}`)
  },

  // 지출 수정
  update: async (expenseId, expenseData) => {
    return await apiRequest(`/expense/${expenseId}`, {
      method: 'PUT',
      body: JSON.stringify(expenseData)
    })
  },

  // 지출 삭제
  delete: async (expenseId) => {
    return await apiRequest(`/expense/${expenseId}`, {
      method: 'DELETE'
    })
  },

  // 지출 통계 조회
  getStatistics: async (params = {}) => {
    const queryString = new URLSearchParams(params).toString()
    const endpoint = queryString ? `/expense/statistics?${queryString}` : '/expense/statistics'
    return await apiRequest(endpoint)
  },

  // 영수증별 지출 조회
  getByReceipt: async (receiptId) => {
    return await apiRequest(`/expense/by-receipt/${receiptId}`)
  },

  // PDF 다운로드
  downloadPDF: async (expenseId) => {
    const token = localStorage.getItem('access_token')

    const response = await fetch(`${API_BASE_URL}/expense/${expenseId}/pdf`, {
      method: 'GET',
      headers: {
        ...(token && { Authorization: `Bearer ${token}` })
      }
    })

    if (!response.ok) {
      throw new Error(`PDF 다운로드 실패: ${response.status}`)
    }

    return response
  },

  // 리포트 PDF 다운로드
  downloadReportPDF: async (expenseIds) => {
    const token = localStorage.getItem('access_token')

    const response = await fetch(`${API_BASE_URL}/expense/report/pdf`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...(token && { Authorization: `Bearer ${token}` })
      },
      body: JSON.stringify(expenseIds)
    })

    if (!response.ok) {
      throw new Error(`리포트 PDF 다운로드 실패: ${response.status}`)
    }

    return response
  }
}

// 영수증 관련 API (OCR)
export const receiptAPI = {
  // 영수증 업로드 및 OCR 처리
  upload: async (file) => {
    const formData = new FormData()
    formData.append('file', file)

    const token = localStorage.getItem('access_token')
    return await fetch(`${API_BASE_URL}/receipt/upload`, {
      method: 'POST',
      headers: {
        ...(token && { Authorization: `Bearer ${token}` })
      },
      body: formData
    }).then(response => {
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      return response.json()
    })
  },

  // 영수증 목록 조회
  getAll: async () => {
    return await apiRequest('/receipt/')
  },

  // 특정 영수증 조회
  getById: async (receiptId) => {
    return await apiRequest(`/receipt/${receiptId}`)
  }
}

export default {
  authAPI,
  budgetAPI,
  expenseAPI,
  receiptAPI
}