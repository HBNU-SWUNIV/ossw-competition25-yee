import apiClient from './client'

/**
 * 인증 관련 API
 */
export const authAPI = {
  /**
   * 로그인
   * @param {string} email - 사용자 이메일
   * @param {string} password - 비밀번호
   * @returns {Promise} 토큰 정보
   */
  async login(email, password) {
    try {
      const response = await apiClient.post('/api/auth/login', {
        email,
        password
      })
      return {
        success: true,
        data: response.data
      }
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.detail || '로그인에 실패했습니다.'
      }
    }
  },

  /**
   * 회원가입
   * @param {Object} userData - 사용자 정보 (email, password, name)
   * @returns {Promise} 사용자 정보
   */
  async register(userData) {
    try {
      const response = await apiClient.post('/api/auth/register', userData)
      return {
        success: true,
        data: response.data
      }
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.detail || '회원가입에 실패했습니다.'
      }
    }
  },

  /**
   * 로그아웃
   * @returns {Promise}
   */
  async logout() {
    try {
      await apiClient.post('/api/auth/logout')
      // 로컬 스토리지 정리
      localStorage.removeItem('accessToken')
      localStorage.removeItem('userInfo')
      localStorage.removeItem('isLoggedIn')
      return {
        success: true
      }
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.detail || '로그아웃에 실패했습니다.'
      }
    }
  },

  /**
   * 현재 사용자 정보 조회
   * @returns {Promise} 사용자 정보
   */
  async getCurrentUser() {
    try {
      const response = await apiClient.get('/api/auth/me')
      return {
        success: true,
        data: response.data
      }
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.detail || '사용자 정보 조회에 실패했습니다.'
      }
    }
  }
}
