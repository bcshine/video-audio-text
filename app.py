#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎬 유튜브 쇼츠 → 텍스트 변환기 웹 인터페이스
Streamlit 기반 사용자 친화적 GUI
"""

import streamlit as st
import os
from pathlib import Path
import time
from utils import process_youtube_to_text

# 페이지 설정
st.set_page_config(
    page_title="🎬 유튜브 쇼츠 → 텍스트 변환기",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 메인 제목
st.title("🎬 유튜브 쇼츠 → 텍스트 변환기")
st.markdown("---")

# 설명 섹션
with st.container():
    st.markdown("""
    ### 📋 사용 방법
    1. **유튜브 쇼츠 URL**을 입력하세요
    2. **AI 모델 크기**를 선택하세요 (빠름 ↔ 정확함)
    3. **변환 시작** 버튼을 클릭하세요
    4. 완료 후 **결과물을 다운로드**하세요
    """)

# 사이드바 설정
with st.sidebar:
    st.header("⚙️ 설정")
    
    # Whisper 모델 크기 선택
    model_options = {
        "tiny": "Tiny (가장 빠름, 낮은 정확도)",
        "base": "Base (권장, 균형잡힌 성능)",
        "small": "Small (느림, 높은 정확도)", 
        "medium": "Medium (매우 느림, 매우 높은 정확도)",
        "large": "Large (가장 느림, 최고 정확도)"
    }
    
    selected_model = st.selectbox(
        "🤖 AI 모델 크기",
        options=list(model_options.keys()),
        index=1,  # 기본값: base
        format_func=lambda x: model_options[x]
    )
    
    st.markdown("---")
    st.markdown("""
    ### 💡 팁
    - **Tiny**: 빠른 테스트용
    - **Base**: 일반적 사용 권장  
    - **Small 이상**: 고품질 필요시
    
    ### 📁 출력 파일
    - 📹 **MP4**: 원본 영상
    - 🎵 **MP3**: 추출된 음성
    - 📄 **TXT**: 변환된 텍스트
    """)

# 메인 인터페이스
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📎 유튜브 URL 입력")
    
    # URL 입력
    youtube_url = st.text_input(
        "유튜브 쇼츠 URL을 입력하세요:",
        placeholder="https://youtube.com/shorts/xxxxxxxx",
        help="유튜브 쇼츠 또는 일반 영상 URL을 입력하세요"
    )
    
    # 변환 시작 버튼
    col_start, col_clean = st.columns([3, 1])
    
    with col_start:
        start_button = st.button(
            "🚀 변환 시작", 
            type="primary",
            use_container_width=True,
            disabled=not youtube_url.strip()
        )
    
    with col_clean:
        clean_button = st.button(
            "🧹 폴더 정리",
            help="이전 다운로드 파일들을 정리합니다",
            use_container_width=True
        )

with col2:
    st.subheader("📊 진행 상황")
    progress_container = st.container()

# 결과 표시 영역
results_container = st.container()

# 폴더 정리 기능
if clean_button:
    import shutil
    try:
        downloads_path = Path("downloads")
        if downloads_path.exists():
            # 기존 다운로드 폴더 백업
            backup_path = Path(f"downloads_backup_{int(time.time())}")
            shutil.move(str(downloads_path), str(backup_path))
            st.success(f"✅ 기존 파일들을 {backup_path}로 백업했습니다!")
            
            # 새로운 다운로드 폴더 생성
            downloads_path.mkdir(exist_ok=True)
            st.info("🆕 새로운 다운로드 폴더가 생성되었습니다!")
        else:
            st.info("📁 다운로드 폴더가 비어있습니다.")
    except Exception as e:
        st.error(f"❌ 폴더 정리 중 오류: {str(e)}")

# 변환 프로세스 실행
if start_button and youtube_url.strip():
    
    # 세션 상태 초기화 및 URL 변경 감지
    if 'processing' not in st.session_state:
        st.session_state.processing = False
    
    # URL 변경 감지를 위한 세션 상태 관리
    if 'last_url' not in st.session_state:
        st.session_state.last_url = ""
    
    # 새로운 URL인지 확인
    current_url = youtube_url.strip()
    if st.session_state.last_url != current_url:
        st.session_state.last_url = current_url
        print(f"🔄 새로운 URL 감지: {current_url}")
        # 기존 결과 초기화
        if 'last_result' in st.session_state:
            del st.session_state.last_result
    
    # 진행 상황 표시
    with progress_container:
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # 단계별 진행 상황 업데이트
        def update_progress(step, total, message):
            progress = step / total
            progress_bar.progress(progress)
            status_text.text(f"🔄 {message}")
            time.sleep(0.5)  # 사용자가 진행 상황을 볼 수 있게 약간의 지연
    
    try:
        # 1단계: 다운로드 시작
        update_progress(1, 4, "유튜브 영상 다운로드 중...")
        
        # 디버깅 정보 표시
        with st.expander("🔍 디버깅 정보 (문제 해결용)", expanded=False):
            st.write(f"**처리 중인 URL:** {current_url}")
            st.write(f"**선택된 모델:** {selected_model}")
            st.write(f"**타임스탬프:** {time.strftime('%Y-%m-%d %H:%M:%S')}")
            debug_container = st.empty()
        
        # 실제 변환 프로세스 실행
        with st.spinner("🎬 영상 다운로드 중..."):
            result = process_youtube_to_text(
                url=current_url,
                output_path="downloads",
                model_size=selected_model
            )
        
        # 진행 상황 업데이트
        if result['video_file']:
            update_progress(2, 4, "음성 추출 중...")
        if result['audio_file']:
            update_progress(3, 4, "AI 텍스트 변환 중...")
        if result['text_file']:
            update_progress(4, 4, "완료!")
        
        # 결과 처리
        if result['success']:
            progress_bar.progress(1.0)
            status_text.text("✅ 모든 작업 완료!")
            
            # 성공 메시지
            st.success("🎉 변환이 성공적으로 완료되었습니다!")
            
            # 결과 표시
            with results_container:
                st.markdown("---")
                st.subheader("📁 결과물 다운로드")
                
                # 처리된 파일 정보 표시
                if result.get('video_file'):
                    video_filename = Path(result['video_file']).name
                    st.info(f"🎬 **처리된 영상:** {video_filename}")
                    
                    # 디버깅 정보 업데이트
                    with st.expander("🔍 디버깅 정보 (문제 해결용)", expanded=False):
                        st.write(f"**처리 중인 URL:** {current_url}")
                        st.write(f"**선택된 모델:** {selected_model}")
                        st.write(f"**타임스탬프:** {time.strftime('%Y-%m-%d %H:%M:%S')}")
                        st.write(f"**처리된 비디오 파일:** {result['video_file']}")
                        st.write(f"**처리된 오디오 파일:** {result['audio_file']}")
                        st.write(f"**처리된 텍스트 파일:** {result['text_file']}")
                        if result.get('text_content'):
                            st.write(f"**텍스트 길이:** {len(result['text_content'])} 글자")
                
                # 다운로드 버튼들을 3개 컬럼으로 배치
                download_col1, download_col2, download_col3 = st.columns(3)
                
                # MP4 다운로드
                if result['video_file'] and Path(result['video_file']).exists():
                    with download_col1:
                        with open(result['video_file'], 'rb') as video_file:
                            file_name = Path(result['video_file']).name
                            st.download_button(
                                label="📹 MP4 다운로드",
                                data=video_file.read(),
                                file_name=file_name,
                                mime="video/mp4",
                                use_container_width=True
                            )
                
                # MP3 다운로드  
                if result['audio_file'] and Path(result['audio_file']).exists():
                    with download_col2:
                        with open(result['audio_file'], 'rb') as audio_file:
                            file_name = Path(result['audio_file']).name
                            st.download_button(
                                label="🎵 MP3 다운로드",
                                data=audio_file.read(),
                                file_name=file_name,
                                mime="audio/mpeg",
                                use_container_width=True
                            )
                
                # TXT 다운로드
                if result['text_file'] and Path(result['text_file']).exists():
                    with download_col3:
                        file_name = Path(result['text_file']).name
                        st.download_button(
                            label="📄 TXT 다운로드",
                            data=result['text_content'],
                            file_name=file_name,
                            mime="text/plain",
                            use_container_width=True
                        )
                
                # 텍스트 내용 표시
                st.markdown("---")
                st.subheader("📄 변환된 텍스트")
                
                # 텍스트를 읽기 좋게 표시
                if result['text_content']:
                    st.text_area(
                        "변환 결과:",
                        value=result['text_content'],
                        height=200,
                        help="텍스트를 복사하려면 Ctrl+A 후 Ctrl+C를 사용하세요"
                    )
                    
                    # 통계 정보
                    text_stats_col1, text_stats_col2, text_stats_col3 = st.columns(3)
                    
                    with text_stats_col1:
                        st.metric("📊 글자 수", len(result['text_content']))
                    
                    with text_stats_col2:
                        word_count = len(result['text_content'].split())
                        st.metric("📝 단어 수", word_count)
                    
                    with text_stats_col3:
                        if result['audio_file'] and Path(result['audio_file']).exists():
                            file_size = Path(result['audio_file']).stat().st_size / (1024*1024)
                            st.metric("🎵 음성 크기", f"{file_size:.1f} MB")
        
        else:
            # 실패 처리
            progress_bar.progress(0.0)
            status_text.text("❌ 작업 실패")
            st.error(f"❌ 변환 실패: {result.get('error', '알 수 없는 오류')}")
    
    except Exception as e:
        st.error(f"❌ 처리 중 오류가 발생했습니다: {str(e)}")
        progress_bar.progress(0.0)
        status_text.text("❌ 오류 발생")

# 하단 정보
st.markdown("---")
with st.expander("ℹ️ 프로그램 정보"):
    st.markdown("""
    ### 🛠️ 사용된 기술
    - **yt-dlp**: 유튜브 영상 다운로드
    - **FFmpeg**: 음성 추출 
    - **OpenAI Whisper**: AI 음성→텍스트 변환
    - **Streamlit**: 웹 인터페이스
    
    ### 📝 참고사항
    - 첫 실행 시 AI 모델이 자동으로 다운로드됩니다
    - 인터넷 연결이 필요합니다 (영상 다운로드용)
    - 변환 속도는 모델 크기와 음성 길이에 따라 달라집니다
    - 모든 처리는 로컬에서 이루어집니다 (개인정보 안전)
    """)

# 실행 방법 안내
if not youtube_url.strip():
    st.info("💡 위의 입력창에 유튜브 쇼츠 URL을 입력하고 변환을 시작해보세요!") 