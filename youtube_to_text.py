#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
유튜브 쇼츠 영상 → 음성 → 텍스트 변환기 (CLI 버전)
간단하고 보편적인 무료 라이브러리 사용
"""

from utils import process_youtube_to_text

def main():
    """
    메인 실행 함수 (CLI 버전)
    """
    print("🎬 유튜브 쇼츠 → 텍스트 변환기 (CLI)")
    print("=" * 50)
    
    # 유튜브 URL 입력받기
    url = input("📎 유튜브 쇼츠 URL을 입력하세요: ").strip()
    
    if not url:
        print("❌ URL이 입력되지 않았습니다.")
        return
    
    # 전체 프로세스 실행
    result = process_youtube_to_text(url)
    
    if result['success']:
        # 4단계: 결과 출력 및 저장
        print("\n" + "=" * 50)
        print("📄 변환된 텍스트:")
        print("-" * 50)
        print(result['text_content'])
        print("-" * 50)
        
        print(f"\n🎉 모든 작업 완료!")
        print(f"📁 영상 파일: {result['video_file']}")
        print(f"🎵 음성 파일: {result['audio_file']}")
        print(f"📄 텍스트 파일: {result['text_file']}")
    else:
        print(f"❌ 변환 실패: {result['error']}")

if __name__ == "__main__":
    main() 