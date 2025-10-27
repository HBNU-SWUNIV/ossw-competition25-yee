// Firebase 설정 파일 (백엔드 개발자가 연결할 예정)
// TODO: Firebase 프로젝트 설정 후 활성화

/*
import { initializeApp } from 'firebase/app'
import { getAuth } from 'firebase/auth'
import { getFirestore } from 'firebase/firestore'

// Firebase 설정 (환경 변수로 관리 예정)
const firebaseConfig = {
  apiKey: process.env.VUE_APP_FIREBASE_API_KEY,
  authDomain: process.env.VUE_APP_FIREBASE_AUTH_DOMAIN,
  projectId: process.env.VUE_APP_FIREBASE_PROJECT_ID,
  storageBucket: process.env.VUE_APP_FIREBASE_STORAGE_BUCKET,
  messagingSenderId: process.env.VUE_APP_FIREBASE_MESSAGING_SENDER_ID,
  appId: process.env.VUE_APP_FIREBASE_APP_ID
}

// Firebase 초기화
const app = initializeApp(firebaseConfig)

// 인증 및 데이터베이스 인스턴스
export const auth = getAuth(app)
export const db = getFirestore(app)

export default app
*/

// 임시 설정 (Firebase 연결 전)
export const auth = null
export const db = null
