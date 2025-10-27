import apiClient from './client'

/**
 * 예산 관련 API
 */
export const budgetAPI = {
  /**
   * 예산 목록 조회
   * @returns {Promise} 예산 목록
   */
  async getBudgets() {
    try {
      const response = await apiClient.get('/budget/')
      return {
        success: true,
        data: response.data
      }
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.detail || '예산 목록 조회에 실패했습니다.'
      }
    }
  },

  /**
   * 특정 예산 조회
   * @param {string} budgetId - 예산 ID
   * @returns {Promise} 예산 정보
   */
  async getBudget(budgetId) {
    try {
      const response = await apiClient.get(`/budget/${budgetId}`)
      return {
        success: true,
        data: response.data
      }
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.detail || '예산 조회에 실패했습니다.'
      }
    }
  },

  /**
   * 예산 생성
   * @param {Object} budgetData - 예산 정보 (name, amount, category)
   * @returns {Promise} 생성된 예산 정보
   */
  async createBudget(budgetData) {
    try {
      const response = await apiClient.post('/budget/', budgetData)
      return {
        success: true,
        data: response.data
      }
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.detail || '예산 생성에 실패했습니다.'
      }
    }
  },

  /**
   * 예산 수정
   * @param {string} budgetId - 예산 ID
   * @param {Object} budgetData - 수정할 예산 정보
   * @returns {Promise} 수정된 예산 정보
   */
  async updateBudget(budgetId, budgetData) {
    try {
      const response = await apiClient.put(`/budget/${budgetId}`, budgetData)
      return {
        success: true,
        data: response.data
      }
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.detail || '예산 수정에 실패했습니다.'
      }
    }
  },

  /**
   * 예산 삭제
   * @param {string} budgetId - 예산 ID
   * @returns {Promise}
   */
  async deleteBudget(budgetId) {
    try {
      const response = await apiClient.delete(`/budget/${budgetId}`)
      return {
        success: true,
        data: response.data
      }
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.detail || '예산 삭제에 실패했습니다.'
      }
    }
  }
}
