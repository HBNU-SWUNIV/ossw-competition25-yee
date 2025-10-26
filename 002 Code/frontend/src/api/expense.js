import apiClient from './client'

/**
 * 지출 관련 API
 */
export const expenseAPI = {
  /**
   * 지출 목록 조회
   * @param {Object} params - 쿼리 파라미터 (category, start_date, end_date, limit)
   * @returns {Promise} 지출 목록
   */
  async getExpenses(params = {}) {
    try {
      const response = await apiClient.get('/api/expense/', { params })
      return {
        success: true,
        data: response.data
      }
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.detail || '지출 목록 조회에 실패했습니다.'
      }
    }
  },

  /**
   * 특정 지출 조회
   * @param {string} expenseId - 지출 ID
   * @returns {Promise} 지출 정보
   */
  async getExpense(expenseId) {
    try {
      const response = await apiClient.get(`/api/expense/${expenseId}`)
      return {
        success: true,
        data: response.data
      }
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.detail || '지출 조회에 실패했습니다.'
      }
    }
  },

  /**
   * 지출 생성
   * @param {Object} expenseData - 지출 정보
   * @returns {Promise} 생성된 지출 정보
   */
  async createExpense(expenseData) {
    try {
      const response = await apiClient.post('/api/expense/', expenseData)
      return {
        success: true,
        data: response.data
      }
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.detail || '지출 생성에 실패했습니다.'
      }
    }
  },

  /**
   * 지출 수정
   * @param {string} expenseId - 지출 ID
   * @param {Object} expenseData - 수정할 지출 정보
   * @returns {Promise} 수정된 지출 정보
   */
  async updateExpense(expenseId, expenseData) {
    try {
      const response = await apiClient.put(`/api/expense/${expenseId}`, expenseData)
      return {
        success: true,
        data: response.data
      }
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.detail || '지출 수정에 실패했습니다.'
      }
    }
  },

  /**
   * 지출 삭제
   * @param {string} expenseId - 지출 ID
   * @returns {Promise}
   */
  async deleteExpense(expenseId) {
    try {
      const response = await apiClient.delete(`/api/expense/${expenseId}`)
      return {
        success: true,
        data: response.data
      }
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.detail || '지출 삭제에 실패했습니다.'
      }
    }
  },

  /**
   * 지출 통계 조회
   * @param {Object} params - 쿼리 파라미터 (start_date, end_date)
   * @returns {Promise} 지출 통계
   */
  async getStatistics(params = {}) {
    try {
      const response = await apiClient.get('/api/expense/statistics', { params })
      return {
        success: true,
        data: response.data
      }
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.detail || '지출 통계 조회에 실패했습니다.'
      }
    }
  },

  /**
   * 영수증별 지출 조회
   * @param {string} receiptId - 영수증 ID
   * @returns {Promise} 지출 목록
   */
  async getExpensesByReceipt(receiptId) {
    try {
      const response = await apiClient.get(`/api/expense/by-receipt/${receiptId}`)
      return {
        success: true,
        data: response.data
      }
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.detail || '영수증 지출 조회에 실패했습니다.'
      }
    }
  }
}
