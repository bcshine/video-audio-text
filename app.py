#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎬 유튜브 쇼츠 → mp4, mp3, text 변환기 🎬
Streamlit 기반 간단한 GUI
"""

import streamlit as st
import shutil
import time
from pathlib import Path
from utils import process_youtube_to_text

# 페이지 설정
st.set_page_config(
    page_title="🎬 유튜브 쇼츠 → mp4, mp3, text 변환기",
    page_icon="🎬",
    layout="wide"
)

# 메인 제목
st.title("🎬 유튜브 쇼츠 → mp4, mp3, text 변환기")
st.markdown("---")

# 사용 방법
st.markdown("""
### 📋 사용 방법
1. 유튜브 URL을 입력하세요
2. AI 모델을 선택하세요 (빠름 ↔ 정확함)
3. 변환 시작 버튼을 클릭하세요
4. MP4, MP3, TXT 파일을 다운로드하세요
""")

# 사이드바 설정
with st.sidebar:
    st.header("⚙️ 설정")
    
    # 모델 선택
    model_options = {
        "tiny": "Tiny (빠름)",
        "base": "Base (권장)",
        "small": "Small (정확함)",
        "medium": "Medium (매우 정확함)",
        "large": "Large (최고 정확함)"
    }
    
    model_size = st.selectbox(
        "AI 모델 크기",
        options=list(model_options.keys()),
        index=1,
        format_func=lambda x: model_options[x]
    )

# 메인 인터페이스
col1, col2 = st.columns([3, 1])

with col2:
    # 폴더 정리 버튼
    if st.button("🧹 폴더 정리"):
        try:
            downloads_path = Path("downloads")
            if downloads_path.exists():
                shutil.rmtree(downloads_path)
                st.success("✅ 폴더 정리 완료!")
            else:
                st.info("📁 폴더가 비어있습니다.")
        except Exception as e:
            st.error(f"❌ 오류: {e}")

# 세션 상태 초기화
if 'is_processing' not in st.session_state:
    st.session_state.is_processing = False

# 변환 폼 (안정적인 버튼 처리)
with st.form("conversion_form"):
    col1, col2 = st.columns([4, 1])
    
    with col1:
        # URL 입력
        youtube_url = st.text_input(
            "유튜브 URL 입력:",
            placeholder="https://youtube.com/shorts/xxxxxxxx"
        )
    
    with col2:
        # 빈 공간 (정렬용)
        st.write("")
        st.write("")
        
        # 변환 시작 버튼 (상태에 따라 텍스트 변경)
        if st.session_state.is_processing:
            start_button = st.form_submit_button(
                "⏳ 변환 중...", 
                type="secondary",
                use_container_width=True,
                disabled=True
            )
        else:
            start_button = st.form_submit_button(
                "🚀 변환 시작", 
                type="primary",
                use_container_width=True
            )

# 변환 프로세스
if start_button:
    if not youtube_url.strip():
        st.error("❌ 유튜브 URL을 입력해주세요!")
        st.stop()
    
    # URL 유효성 간단 검사
    if not ("youtube.com" in youtube_url or "youtu.be" in youtube_url):
        st.error("❌ 올바른 유튜브 URL을 입력해주세요!")
        st.stop()
    
    # 처리 시작 - 상태 변경
    st.session_state.is_processing = True
    
    # 진행 상황 표시
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # 변환 중 표시
    with st.spinner("🎬 변환 처리 중입니다..."):
        try:
            # 단계별 진행 상황 업데이트
            progress_bar.progress(0.25)
            status_text.text("🔄 영상 다운로드 중...")
            
            # 변환 실행
            result = process_youtube_to_text(
                url=youtube_url.strip(),
                output_path="downloads",
                model_size=model_size
            )
            
            # 결과 처리
            if result['success']:
                progress_bar.progress(1.0)
                status_text.text("✅ 완료!")
                
                st.success("🎉 변환이 완료되었습니다!")
                
                # 결과 표시
                st.markdown("### 📁 결과 다운로드")
                
                # 다운로드 버튼들
                col1, col2, col3 = st.columns(3)
                
                # MP4 다운로드
                if result['video_file'] and Path(result['video_file']).exists():
                    with col1:
                        with open(result['video_file'], 'rb') as f:
                            st.download_button(
                                "📹 MP4 다운로드",
                                f.read(),
                                file_name=Path(result['video_file']).name,
                                mime="video/mp4"
                            )
                
                # MP3 다운로드
                if result['audio_file'] and Path(result['audio_file']).exists():
                    with col2:
                        with open(result['audio_file'], 'rb') as f:
                            st.download_button(
                                "🎵 MP3 다운로드",
                                f.read(),
                                file_name=Path(result['audio_file']).name,
                                mime="audio/mpeg"
                            )
                
                # TXT 다운로드
                if result['text_file'] and Path(result['text_file']).exists():
                    with col3:
                        st.download_button(
                            "📄 TXT 다운로드",
                            result['text_content'],
                            file_name=Path(result['text_file']).name,
                            mime="text/plain"
                        )
                
                # 텍스트 미리보기
                if result['text_content']:
                    st.markdown("### 📄 텍스트 미리보기")
                    st.text_area(
                        "변환된 텍스트:",
                        result['text_content'],
                        height=200
                    )
            
            else:
                # 오류 처리
                progress_bar.progress(0)
                status_text.text("❌ 실패")
                st.error(f"변환 실패: {result['error']}")
                
        except Exception as e:
            progress_bar.progress(0)
            status_text.text("❌ 오류")
            st.error(f"오류 발생: {str(e)}")
        
        finally:
            # 처리 완료 - 상태 재설정
            st.session_state.is_processing = False 