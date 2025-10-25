// Firebase Authentication 유틸리티 함수
// TODO: Firebase 연결 후 활성화

/*
import { 
  signInWithEmailAndPassword,
  signOut,
  onAuthStateChanged,
  createUserWithEmailAndPassword,
  updateProfile
} from 'firebase/auth'
import { auth } from './config'

// 로그인 함수
export const loginUser = async (email, password) => {
  try {
    const userCredential = await signInWithEmailAndPassword(auth, email, password)
    return {
      success: true,
      user: userCredential.user
    }
  } catch (error) {
    return {
      success: false,
      error: error.message
    }
  }
}

// 로그아웃 함수
export const logoutUser = async () => {
  try {
    await signOut(auth)
    return { success: true }
  } catch (error) {
    return {
      success: false,
      error: error.message
    }
  }
}

// 사용자 상태 변경 감지
export const onAuthStateChange = (callback) => {
  return onAuthStateChanged(auth, callback)
}

// 회원가입 함수
export const registerUser = async (email, password, displayName) => {
  try {
    const userCredential = await createUserWithEmailAndPassword(auth, email, password)
    await updateProfile(userCredential.user, {
      displayName: displayName
    })
    return {
      success: true,
      user: userCredential.user
    }
  } catch (error) {
    return {
      success: false,
      error: error.message
    }
  }
}
*/

// 임시 함수들 (Firebase 연결 전)
export const loginUser = async (email, password) => {
  // 임시 로그인 로직
  if (email === 'user' && password === '1234') {
    return {
      success: true,
      user: {
        uid: 'temp-user-id',
        email: 'user@company.com',
        displayName: '사용자'
      }
    }
  }
  return {
    success: false,
    error: '사용자명 또는 비밀번호가 올바르지 않습니다.'
  }
}

export const logoutUser = async () => {
  return { success: true }
}

export const onAuthStateChange = (callback) => {
  // 임시 상태 변경 감지
  return () => {}
}

export const registerUser = async (email, password, displayName) => {
  return {
    success: false,
    error: 'Firebase 연결 후 회원가입 기능이 활성화됩니다.'
  }
}
