import apiClient from './client'

/**
 * 영수증 관련 API
 */
export const receiptAPI = {
  /**
   * OCR 처리만 수행 (Expense 생성 안함)
   * @param {File} file - 영수증 이미지 파일
   * @returns {Promise} OCR 처리 결과
   */
  async performOCR(file) {
    try {
      const formData = new FormData()
      formData.append('file', file)

      const response = await apiClient.post('/receipt/ocr', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })

      console.log('[receiptAPI] OCR 백엔드 응답:', response.data)

      if (response.data && response.data.status === 'success') {
        return {
          success: true,
          data: response.data.data
        }
      } else {
        return {
          success: false,
          error: response.data?.message || 'OCR 처리에 실패했습니다.'
        }
      }
    } catch (error) {
      console.error('[receiptAPI] OCR 에러:', error)

      if (error.code === 'ECONNABORTED' || error.message.includes('timeout')) {
        return {
          success: false,
          error: 'OCR 처리 시간이 초과되었습니다. 이미지 크기를 줄이거나 다시 시도해주세요.'
        }
      }

      return {
        success: false,
        error: error.response?.data?.detail || 'OCR 처리에 실패했습니다.'
      }
    }
  },

  /**
   * 영수증 업로드 및 전체 처리 (OCR + Expense 자동 생성)
   * @param {File} file - 영수증 이미지 파일
   * @returns {Promise} OCR 처리 결과 및 영수증 정보
   */
  async uploadReceipt(file) {
    try {
      const formData = new FormData()
      formData.append('file', file)

      const response = await apiClient.post('/receipt/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })

      console.log('[receiptAPI] 백엔드 응답:', response.data)

      // 백엔드가 status: "success"를 반환하므로 확인
      if (response.data && response.data.status === 'success') {
        return {
          success: true,
          data: response.data
        }
      } else {
        return {
          success: false,
          error: response.data?.message || '영수증 업로드에 실패했습니다.'
        }
      }
    } catch (error) {
      console.error('[receiptAPI] 에러:', error)

      // 타임아웃 에러 처리
      if (error.code === 'ECONNABORTED' || error.message.includes('timeout')) {
        return {
          success: false,
          error: 'OCR 처리 시간이 초과되었습니다. 이미지 크기를 줄이거나 다시 시도해주세요.'
        }
      }

      return {
        success: false,
        error: error.response?.data?.detail || '영수증 업로드에 실패했습니다.'
      }
    }
  },

  /**
   * 영수증 목록 조회
   * @param {Object} params - 쿼리 파라미터 (start_date, end_date, limit)
   * @returns {Promise} 영수증 목록
   */
  async getReceipts(params = {}) {
    try {
      const response = await apiClient.get('/receipt/', { params })
      return {
        success: true,
        data: response.data
      }
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.detail || '영수증 목록 조회에 실패했습니다.'
      }
    }
  },

  /**
   * 특정 영수증 조회
   * @param {string} receiptId - 영수증 ID
   * @param {boolean} includeExpenses - 관련 지출 내역 포함 여부
   * @returns {Promise} 영수증 정보
   */
  async getReceipt(receiptId, includeExpenses = false) {
    try {
      const response = await apiClient.get(`/receipt/${receiptId}`, {
        params: { include_expenses: includeExpenses }
      })
      return {
        success: true,
        data: response.data
      }
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.detail || '영수증 조회에 실패했습니다.'
      }
    }
  },

  /**
   * 영수증 삭제
   * @param {string} receiptId - 영수증 ID
   * @param {boolean} deleteExpenses - 관련 지출 내역도 삭제 여부
   * @returns {Promise}
   */
  async deleteReceipt(receiptId, deleteExpenses = true) {
    try {
      const response = await apiClient.delete(`/receipt/${receiptId}`, {
        params: { delete_expenses: deleteExpenses }
      })
      return {
        success: true,
        data: response.data
      }
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.detail || '영수증 삭제에 실패했습니다.'
      }
    }
  }
}
