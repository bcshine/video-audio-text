#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
유튜브 쇼츠 → mp4, mp3, text 변환기 (CLI 버전)
"""

from utils import process_youtube_to_text

def main():
    """CLI 버전 메인 함수"""
    print("🎬 유튜브 쇼츠 → mp4, mp3, text 변환기 (CLI)")
    print("=" * 50)
    
    # URL 입력
    url = input("📎 유튜브 URL 입력: ").strip()
    
    if not url:
        print("❌ URL이 입력되지 않았습니다.")
        return
    
    # 변환 실행
    result = process_youtube_to_text(url)
    
    if result['success']:
        print("\n" + "=" * 50)
        print("📄 변환된 텍스트:")
        print("-" * 50)
        print(result['text_content'])
        print("-" * 50)
        
        print(f"\n🎉 모든 작업 완료!")
        print(f"📁 영상: {result['video_file']}")
        print(f"🎵 음성: {result['audio_file']}")
        print(f"📄 텍스트: {result['text_file']}")
    else:
        print(f"❌ 변환 실패: {result['error']}")

if __name__ == "__main__":
    main() 