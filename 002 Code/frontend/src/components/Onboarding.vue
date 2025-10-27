<template>
    <div class="fixed inset-0 bg-white z-50 overflow-hidden">
        <!-- 시작화면 -->
        <div v-if="currentStep === 0"
            class="h-full bg-gradient-to-br from-blue-600 to-blue-700 flex flex-col items-center justify-center px-8">
            <div class="text-center">
                <h1 class="text-6xl font-bold text-white mb-6">Budgetly</h1>
                <p class="text-xl text-blue-100 mb-2">카드로 시작하는</p>
                <p class="text-xl text-blue-100">재밌는 뇌 건강 습관</p>
            </div>
        </div>

        <!-- 온보딩 1 -->
        <div v-if="currentStep === 1" class="h-full flex flex-col items-center justify-between px-8 py-16">
            <div class="flex-1 flex flex-col items-center justify-center">
                <div class="w-32 h-32 mb-8 flex items-center justify-center">
                    <div class="text-8xl">🧠</div>
                </div>
                <h2 class="text-2xl font-bold text-gray-900 mb-4">Budgetly와</h2>
                <h2 class="text-2xl font-bold text-blue-600 mb-6">시작하는 뇌 건강</h2>
                <p class="text-gray-600 text-center leading-relaxed">
                    매일의 작은 기억들로 만이<br>
                    건강한 뇌를 만들어가요
                </p>
            </div>

            <!-- 인디케이터 -->
            <div class="flex gap-2 mb-8">
                <div class="w-2 h-2 rounded-full bg-blue-600"></div>
                <div class="w-2 h-2 rounded-full bg-gray-300"></div>
                <div class="w-2 h-2 rounded-full bg-gray-300"></div>
            </div>

            <button @click="nextStep" class="w-full py-4 bg-blue-600 text-white font-semibold rounded-xl">
                다음으로
            </button>
        </div>

        <!-- 온보딩 2 -->
        <div v-if="currentStep === 2" class="h-full flex flex-col items-center justify-between px-8 py-16">
            <div class="flex-1 flex flex-col items-center justify-center">
                <div class="w-32 h-32 mb-8 flex items-center justify-center">
                    <div class="text-8xl">🎯</div>
                </div>
                <h2 class="text-2xl font-bold text-gray-900 mb-4">Budgetly가</h2>
                <h2 class="text-2xl font-bold text-blue-600 mb-6">늘 곁에서 도와드릴게요</h2>
                <p class="text-gray-600 text-center leading-relaxed">
                    맞춤형 추천과 상세한 분석까지<br>
                    체계적으로 관리하도록 돕겠습니다
                </p>
            </div>

            <!-- 인디케이터 -->
            <div class="flex gap-2 mb-8">
                <div class="w-2 h-2 rounded-full bg-gray-300"></div>
                <div class="w-2 h-2 rounded-full bg-blue-600"></div>
                <div class="w-2 h-2 rounded-full bg-gray-300"></div>
            </div>

            <button @click="nextStep" class="w-full py-4 bg-blue-600 text-white font-semibold rounded-xl">
                다음으로
            </button>
        </div>

        <!-- 온보딩 3 -->
        <div v-if="currentStep === 3" class="h-full flex flex-col items-center justify-between px-8 py-16">
            <div class="flex-1 flex flex-col items-center justify-center">
                <div class="w-32 h-32 mb-8 flex items-center justify-center">
                    <div class="text-8xl">💍</div>
                </div>
                <h2 class="text-2xl font-bold text-gray-900 mb-4">함께 만드는</h2>
                <h2 class="text-2xl font-bold text-blue-600 mb-6">건강한 내일을 위해</h2>
                <p class="text-gray-600 text-center leading-relaxed">
                    매일 조금씩 함께하며<br>
                    더 건강한 습관을 만들어볼까요?
                </p>
            </div>

            <!-- 인디케이터 -->
            <div class="flex gap-2 mb-8">
                <div class="w-2 h-2 rounded-full bg-gray-300"></div>
                <div class="w-2 h-2 rounded-full bg-gray-300"></div>
                <div class="w-2 h-2 rounded-full bg-blue-600"></div>
            </div>

            <div class="w-full space-y-3">
                <button @click="completeOnboarding" class="w-full py-4 bg-blue-600 text-white font-semibold rounded-xl">
                    확인/저장
                </button>
                <button @click="completeOnboarding" class="w-full text-gray-500 text-sm">
                    이미 계정이 있으신가요? <span class="text-blue-600 font-semibold">로그인</span>
                </button>
            </div>
        </div>
    </div>
</template>

<script>
import { ref, onMounted } from 'vue'

export default {
    name: 'Onboarding',
    emits: ['complete'],
    setup(props, { emit }) {
        const currentStep = ref(0)

        onMounted(() => {
            // 시작 화면 2초 후 자동으로 온보딩 1로 이동
            setTimeout(() => {
                currentStep.value = 1
            }, 2000)
        })

        const nextStep = () => {
            if (currentStep.value < 3) {
                currentStep.value++
            }
        }

        const completeOnboarding = () => {
            // 온보딩 완료 상태 저장
            localStorage.setItem('onboardingCompleted', 'true')
            emit('complete')
        }

        return {
            currentStep,
            nextStep,
            completeOnboarding
        }
    }
}
</script>
