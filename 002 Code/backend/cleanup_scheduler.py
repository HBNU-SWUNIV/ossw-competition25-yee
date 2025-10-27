"""영수증 자동 정리 스케줄러"""
import asyncio
import schedule
import time
import sys
import os
from datetime import datetime

# 프로젝트 루트를 Python 경로에 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.services.receipt_cleanup_service import cleanup_service


async def daily_cleanup():
    """매일 실행되는 정리 작업"""
    print(f"[{datetime.now()}] 일일 영수증 정리 작업 시작...")
    
    try:
        # 1. 실패한 영수증 정리 (7일 이상)
        failed_result = await cleanup_service.cleanup_failed_receipts(days_old=7)
        print(f"실패한 영수증 정리: {failed_result['deleted_failed_receipts']}개 삭제")
        
        # 2. Storage 사용량 확인
        stats = await cleanup_service.get_storage_usage_stats()
        print(f"현재 Storage 사용량: {stats.get('total_storage_mb', 0)}MB")
        print(f"예상 월 비용: ${stats.get('estimated_monthly_cost_usd', 0)}")
        
        # 3. 정리 권장 여부 확인
        if stats.get('total_receipts', 0) > 1000:
            print("⚠️  영수증이 1000개를 초과했습니다. 수동 정리를 고려하세요.")
            
    except Exception as e:
        print(f"❌ 일일 정리 작업 실패: {e}")


async def weekly_cleanup():
    """주간 정리 작업"""
    print(f"[{datetime.now()}] 주간 영수증 정리 작업 시작...")
    
    try:
        # 90일 이상 된 실패한 영수증들 정리
        result = await cleanup_service.cleanup_old_receipts(
            days_to_keep=90,
            keep_successful_only=True,
            dry_run=False  # 실제 삭제
        )
        
        print(f"주간 정리 완료:")
        print(f"- 삭제된 영수증: {result['deleted_count']}개")
        print(f"- 확보된 Storage: {result['storage_freed_mb']}MB")
        
        if result['errors']:
            print(f"- 오류: {len(result['errors'])}개")
            
    except Exception as e:
        print(f"❌ 주간 정리 작업 실패: {e}")


def run_daily_cleanup():
    """스케줄러에서 호출할 동기 함수"""
    asyncio.run(daily_cleanup())


def run_weekly_cleanup():
    """스케줄러에서 호출할 동기 함수"""
    asyncio.run(weekly_cleanup())


def main():
    """스케줄러 메인 함수"""
    print("🤖 영수증 자동 정리 스케줄러 시작")
    print("- 매일 오전 2시: 실패한 영수증 정리")
    print("- 매주 일요일 오전 3시: 오래된 영수증 정리")
    
    # 스케줄 등록
    schedule.every().day.at("02:00").do(run_daily_cleanup)
    schedule.every().sunday.at("03:00").do(run_weekly_cleanup)
    
    # 즉시 한 번 실행 (테스트용)
    print("\n🔧 초기 정리 작업 실행...")
    run_daily_cleanup()
    
    # 스케줄러 실행
    while True:
        schedule.run_pending()
        time.sleep(60)  # 1분마다 체크


if __name__ == "__main__":
    main()