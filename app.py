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

# 현대적이고 세련된 디자인 CSS
st.markdown("""
<style>
/* 전체 앱 스타일 */
.stApp {
    background-color: #f8f9fa;
    font-family: 'Inter', 'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif;
}

/* 메인 컨테이너 */
.main .block-container {
    padding: 2rem;
    max-width: 1200px;
    background: #ffffff;
    border-radius: 12px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
    margin: 1.5rem auto;
    border: none;
}

/* 제목 스타일 */
.stTitle {
    text-align: center;
    color: #212529 !important;
    font-weight: 800;
    margin-bottom: 2.5rem;
    letter-spacing: -0.02em;
}

/* 모든 제목 태그에 적용 */
h1, .stTitle, .main h1, [data-testid="stTitle"] {
    color: #212529 !important;
    text-align: center !important;
    font-weight: 800 !important;
    letter-spacing: -0.02em !important;
}

/* 메인 컨테이너 내 모든 제목 */
.main .block-container h1 {
    color: #212529 !important;
    text-align: center !important;
    font-weight: 800 !important;
    font-size: 2.5rem !important;
}

/* Streamlit 제목 컴포넌트 */
div[data-testid="stMarkdownContainer"] h1 {
    color: #212529 !important;
    text-align: center !important;
    font-weight: 800 !important;
}

/* 사용 방법 카드 */
.stMarkdown h3 {
    color: #212529;
    border-bottom: 2px solid #4263eb;
    padding-bottom: 0.75rem;
    margin-bottom: 1.25rem;
    font-weight: 700;
    letter-spacing: -0.01em;
}

/* 일반 텍스트 색상 강화 */
.stMarkdown p, .stMarkdown li {
    color: #495057;
    font-weight: 400;
    line-height: 1.6;
    font-size: 1rem;
}

/* 입력 필드 스타일 */
.stTextInput > div > div > input {
    background: #ffffff;
    border: 1px solid #dee2e6;
    border-radius: 8px;
    padding: 0.75rem 1rem;
    font-size: 1rem;
    color: #495057;
    font-weight: 400;
    transition: all 0.2s ease;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.stTextInput > div > div > input:focus {
    border-color: #4263eb;
    box-shadow: 0 0 0 3px rgba(66, 99, 235, 0.15);
    outline: none;
}

/* 버튼 스타일 */
.stButton > button {
    background: #4263eb;
    color: white;
    border: none;
    border-radius: 8px;
    padding: 0.75rem 1.5rem;
    font-size: 0.95rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
    box-shadow: 0 2px 6px rgba(66, 99, 235, 0.2);
    letter-spacing: 0.01em;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    min-width: fit-content;
}

.stButton > button:hover {
    background: #3b5bdb;
    box-shadow: 0 4px 8px rgba(66, 99, 235, 0.3);
}

/* 폴더비우기 버튼 */
.stButton > button[kind="secondary"] {
    background: #fa5252;
    box-shadow: 0 2px 6px rgba(250, 82, 82, 0.2);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    min-width: fit-content;
}

.stButton > button[kind="secondary"]:hover {
    background: #e03131;
    box-shadow: 0 4px 8px rgba(250, 82, 82, 0.3);
}

/* 다운로드 버튼들 */
.stDownloadButton > button {
    background: #40c057;
    color: white;
    border: none;
    border-radius: 8px;
    padding: 0.6rem 1.25rem;
    font-size: 0.9rem;
    font-weight: 500;
    width: 100%;
    margin-bottom: 0.5rem;
    transition: all 0.2s ease;
    box-shadow: 0 2px 6px rgba(64, 192, 87, 0.2);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.stDownloadButton > button:hover {
    background: #37b24d;
    box-shadow: 0 4px 8px rgba(64, 192, 87, 0.3);
}

/* 사이드바 스타일 */
.css-1d391kg {
    background: #ffffff;
    border-radius: 10px;
    padding: 1.25rem;
    margin: 1rem 0;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    border: none;
}

/* 셀렉트박스 스타일 */
.stSelectbox > div > div > select {
    background: #ffffff;
    border: 1px solid #dee2e6;
    border-radius: 8px;
    padding: 0.6rem;
    font-size: 0.9rem;
    color: #495057;
    font-weight: 400;
    transition: all 0.2s ease;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

/* 알림 메시지 스타일 */
.stSuccess {
    background: #d3f9d8;
    color: #2b8a3e;
    border-radius: 8px;
    padding: 1rem;
    margin: 1rem 0;
    box-shadow: 0 2px 6px rgba(64, 192, 87, 0.15);
    border-left: 4px solid #40c057;
}

.stError {
    background: #ffe3e3;
    color: #c92a2a;
    border-radius: 8px;
    padding: 1rem;
    margin: 1rem 0;
    box-shadow: 0 2px 6px rgba(250, 82, 82, 0.15);
    border-left: 4px solid #fa5252;
}

/* 진행 바 스타일 */
.stProgress > div > div {
    background: #4263eb;
    border-radius: 6px;
    height: 8px;
}

/* 텍스트 영역 스타일 */
.stTextArea textarea {
    background: #ffffff;
    border: 1px solid #dee2e6;
    border-radius: 8px;
    padding: 1rem;
    font-size: 0.95rem;
    color: #495057;
    font-weight: 400;
}

/* 컬럼 및 컨테이너 스타일 */
.stColumn {
    min-width: 0;
    flex-shrink: 1;
}

/* 모든 텍스트 요소 줄바꿈 방지 */
.stMarkdown p, .stMarkdown div {
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

/* 체크박스 라벨 */
.stCheckbox label {
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

/* 폼 라벨 */
.stTextInput label, .stSelectbox label {
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    line-height: 1.6;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

/* 모바일 반응형 디자인 */
@media (max-width: 768px) {
    .main .block-container {
        padding: 1.25rem;
        margin: 0.75rem;
        border-radius: 10px;
    }
    
    .stTitle {
        font-size: 1.75rem;
        margin-bottom: 1.5rem;
    }
    
    .stButton > button {
        width: 100%;
        margin-bottom: 0.5rem;
        padding: 0.875rem;
        font-size: 1rem;
    }
    
    .stTextInput > div > div > input {
        font-size: 1rem;
        padding: 0.875rem;
    }
    
    /* 컬럼 스택 */
    .row-widget {
        flex-direction: column;
    }
    
    .element-container {
        margin-bottom: 1.25rem;
    }
}

/* 작은 모바일 화면 */
@media (max-width: 480px) {
    .main .block-container {
        margin: 0.5rem;
        padding: 1rem;
    }
    
    .stTitle {
        font-size: 1.5rem;
    }
    
    .stButton > button {
        padding: 0.75rem;
        font-size: 0.95rem;
    }
}

/* 애니메이션 효과 */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

.main .block-container {
    animation: fadeIn 0.4s ease-out;
}

/* 호버 효과 */
.stMarkdown:hover {
    transform: translateY(-1px);
    transition: transform 0.2s ease;
}

/* 스피너 커스텀 */
.stSpinner {
    color: #4263eb;
}

/* 폼 스타일 */
form {
    background: #ffffff;
    border-radius: 10px;
    padding: 1.5rem;
    margin: 1.25rem 0;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    border: none;
}

/* 컬럼 간격 조정 */
.row-widget.stColumns {
    gap: 1.25rem;
}

/* 레이블 텍스트 색상 강화 */
.stTextInput label, .stSelectbox label, .stTextArea label {
    color: #343a40 !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    margin-bottom: 0.5rem !important;
}

/* 사이드바 헤더 색상 강화 */
.css-1d391kg h2 {
    color: #212529 !important;
    font-weight: 700 !important;
    letter-spacing: -0.01em !important;
}

/* 터치 친화적 디자인 */
@media (hover: none) and (pointer: coarse) {
    .stButton > button {
        min-height: 44px;
        font-size: 1rem;
        padding: 0.875rem 1.25rem;
    }
    
    .stTextInput > div > div > input {
        min-height: 44px;
        font-size: 1rem;
        padding: 0.875rem;
    }
    
    .stSelectbox > div > div > select {
        min-height: 44px;
        font-size: 1rem;
        padding: 0.875rem;
    }
}

/* 로딩 스피너 개선 */
.stSpinner > div {
    border-color: #4263eb transparent transparent transparent;
}

/* 다크 모드 지원 */
@media (prefers-color-scheme: dark) {
    .main .block-container {
        background: #212529;
        color: #f8f9fa;
    }
    
    .stTextInput > div > div > input {
        background: #343a40;
        color: #f8f9fa;
        border-color: #495057;
    }
    
    .stSelectbox > div > div > select {
        background: #343a40;
        color: #f8f9fa;
        border-color: #495057;
    }
    
    .stTextArea textarea {
        background: #343a40;
        color: #f8f9fa;
        border-color: #495057;
    }
}

/* 접근성 개선 */
.stButton > button:focus {
    outline: 3px solid #4263eb;
    outline-offset: 2px;
}

.stTextInput > div > div > input:focus {
    outline: 2px solid #4263eb;
    outline-offset: 1px;
}

/* 스크롤 개선 */
::-webkit-scrollbar {
    width: 6px;
}

::-webkit-scrollbar-track {
    background: #f1f3f5;
    border-radius: 6px;
}

::-webkit-scrollbar-thumb {
    background: #adb5bd;
    border-radius: 6px;
}

::-webkit-scrollbar-thumb:hover {
    background: #868e96;
}

</style>
""", unsafe_allow_html=True)

# 메인 제목
st.title("🎬 유튜브 영상 변환 스튜디오")
st.markdown("<p style='text-align: center; color: #6c757d; font-size: 1.1rem; margin-bottom: 2rem;'>영상을 텍스트로, 순간을 기록으로</p>", unsafe_allow_html=True)
st.markdown("<hr style='margin: 2rem 0; border: none; height: 1px; background-color: #dee2e6;'>", unsafe_allow_html=True)

# 사용 방법
st.markdown("""
### 📋 간편한 사용 방법
1. 유튜브 URL을 입력하세요
2. 원하는 AI 모델을 선택하세요
3. 변환 시작 버튼을 클릭하세요
4. 완료 후 파일을 다운로드하세요
""")

# 사이드바 설정
with st.sidebar:
    st.header("⚙️ 변환 설정")
    st.markdown("<p style='color: #6c757d; font-size: 0.9rem; margin-bottom: 1.5rem;'>원하는 정확도와 속도에 맞게 설정하세요</p>", unsafe_allow_html=True)
    
    # 모델 선택
    model_options = {
        "tiny": "Tiny (가장 빠름, 기본 정확도)",
        "base": "Base (권장, 균형적인 성능)",
        "small": "Small (높은 정확도)",
        "medium": "Medium (매우 높은 정확도)",
        "large": "Large (최고 정확도, 느림)"
    }
    
    model_size = st.selectbox(
        "AI 모델 선택",
        options=list(model_options.keys()),
        index=1,
        format_func=lambda x: model_options[x]
    )
    
    # 영구 저장 옵션
    st.markdown("<hr style='margin: 1.5rem 0; border: none; height: 1px; background-color: #dee2e6;'>", unsafe_allow_html=True)
    st.markdown("<p style='color: #6c757d; font-size: 0.9rem; margin-bottom: 1rem;'>파일 저장 설정</p>", unsafe_allow_html=True)
    
    save_to_archive = st.checkbox(
        "영구 보관함에 저장", 
        value=True,
        help="변환된 파일을 영구 보관함(archives 폴더)에 저장합니다"
    )

# 메인 인터페이스
col1, col2 = st.columns([4, 1])

with col2:
    # 저장 파일 보기 버튼들
    col_btn1, col_btn2 = st.columns(2)
    
    with col_btn1:
        # 임시 파일 폴더 열기
        if st.button("📂 파일 보기", help="탐색기로 임시 저장 폴더를 엽니다"):
            import os
            import subprocess
            
            downloads_path = Path("downloads").absolute()
            
            if downloads_path.exists():
                abs_path = os.path.abspath(str(downloads_path))
                
                try:
                    # Windows에서 탐색기 열기
                    os.startfile(abs_path)
                except:
                    try:
                        subprocess.run(["explorer", abs_path], check=False)
                    except:
                        subprocess.run(["cmd", "/c", "start", abs_path], check=False)
            else:
                # 폴더가 없으면 생성 후 열기
                downloads_path.mkdir(exist_ok=True)
                abs_path = os.path.abspath(str(downloads_path))
                try:
                    os.startfile(abs_path)
                except:
                    try:
                        subprocess.run(["explorer", abs_path], check=False)
                    except:
                        subprocess.run(["cmd", "/c", "start", abs_path], check=False)
    
    with col_btn2:
        # 영구 보관함 폴더 열기
        if st.button("📚 보관함보기", help="탐색기로 영구 보관함 폴더를 엽니다"):
            import os
            import subprocess
            
            archives_path = Path("archives").absolute()
            
            if archives_path.exists():
                abs_path = os.path.abspath(str(archives_path))
                
                try:
                    # Windows에서 탐색기 열기
                    os.startfile(abs_path)
                except:
                    try:
                        subprocess.run(["explorer", abs_path], check=False)
                    except:
                        subprocess.run(["cmd", "/c", "start", abs_path], check=False)
            else:
                # 폴더가 없으면 생성 후 열기
                archives_path.mkdir(exist_ok=True)
                abs_path = os.path.abspath(str(archives_path))
                try:
                    os.startfile(abs_path)
                except:
                    try:
                        subprocess.run(["explorer", abs_path], check=False)
                    except:
                        subprocess.run(["cmd", "/c", "start", abs_path], check=False)
    
    # 폴더 관리 버튼들
    col1, col2 = st.columns(2)
    
    with col1:
        # 임시 파일 정리 버튼
        if st.button("🗑️ 파일 정리", help="다운로드된 모든 임시 파일을 삭제합니다", type="secondary"):
            try:
                downloads_path = Path("downloads")
                if downloads_path.exists():
                    shutil.rmtree(downloads_path)
                    st.success("✅ 임시 파일 정리 완료!")
                else:
                    st.info("📁 정리할 임시 파일이 없습니다.")
            except Exception as e:
                st.error(f"❌ 오류: {e}")
    
    with col2:
        # 영구 보관함 관리 버튼
        if st.button("⚙️ 보관함관리", help="영구 보관함 관리 옵션을 표시합니다"):
            archives_path = Path("archives")
            if archives_path.exists() and any(archives_path.iterdir()):
                # 관리 옵션 표시
                st.success("📚 영구 보관함 관리")
                
                # 비디오 폴더 목록 가져오기
                video_folders = [f for f in archives_path.iterdir() if f.is_dir() and f.name.startswith("video_")]
                
                if video_folders:
                    # 삭제할 비디오 선택
                    options = {folder.name.replace("video_", ""): folder.name for folder in video_folders}
                    selected_video = st.selectbox("삭제할 비디오 선택", options=list(options.keys()), format_func=lambda x: f"비디오 ID: {x}")
                    
                    if st.button("🗑️ 선택한 비디오 삭제", type="secondary"):
                        try:
                            folder_to_delete = archives_path / options[selected_video]
                            if folder_to_delete.exists():
                                shutil.rmtree(folder_to_delete)
                                st.success(f"✅ 비디오 ID: {selected_video} 삭제 완료!")
                                st.rerun()  # 페이지 새로고침
                        except Exception as e:
                            st.error(f"❌ 삭제 오류: {e}")
                    
                    # 전체 삭제 버튼
                    if st.button("🗑️ 모든 보관 파일 삭제", type="secondary"):
                        try:
                            shutil.rmtree(archives_path)
                            st.success("✅ 모든 보관 파일 삭제 완료!")
                            st.rerun()  # 페이지 새로고침
                        except Exception as e:
                            st.error(f"❌ 삭제 오류: {e}")
                else:
                    st.info("보관된 비디오가 없습니다.")
            else:
                st.info("📁 보관된 파일이 없습니다.")

# 세션 상태 초기화
if 'is_processing' not in st.session_state:
    st.session_state.is_processing = False

# 미디어 보기 상태 초기화
if 'show_video' not in st.session_state:
    st.session_state.show_video = False
if 'show_audio' not in st.session_state:
    st.session_state.show_audio = False
if 'show_text' not in st.session_state:
    st.session_state.show_text = False

# 변환 폼 (안정적인 버튼 처리)
with st.form("conversion_form"):
    st.markdown("<p style='color: #495057; font-weight: 500; margin-bottom: 1rem;'>변환할 유튜브 영상 URL을 입력하세요</p>", unsafe_allow_html=True)
    col1, col2 = st.columns([5, 1])
    
    with col1:
        # URL 입력
        youtube_url = st.text_input(
            "유튜브 URL",
            placeholder="https://youtube.com/watch?v=xxxx 또는 https://youtu.be/xxxx"
        )
    
    with col2:
        # 빈 공간 (정렬용)
        st.write("")
        
        # 변환 시작 버튼 (상태에 따라 텍스트 변경)
        if st.session_state.is_processing:
            start_button = st.form_submit_button(
                "⏳ 처리 중...", 
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
    
    # 미디어 보기 상태 초기화
    st.session_state.show_video = False
    st.session_state.show_audio = False
    st.session_state.show_text = False
    
    # URL 유효성 간단 검사
    if not ("youtube.com" in youtube_url or "youtu.be" in youtube_url):
        st.error("❌ 올바른 유튜브 URL을 입력해주세요!")
        st.stop()
    
    # 처리 시작 - 상태 변경
    st.session_state.is_processing = True
    
    # 진행 상황 표시
    progress_container = st.container()
    with progress_container:
        progress_bar = st.progress(0)
        status_text = st.empty()
    
    # 변환 중 표시
    with st.spinner("🎬 영상 처리 중입니다..."):
        try:
            # 단계별 진행 상황 업데이트
            progress_bar.progress(0.25)
            status_text.markdown("<p style='color: #495057; font-size: 0.9rem;'>🔄 영상 다운로드 중...</p>", unsafe_allow_html=True)
            
            # 변환 실행
            result = process_youtube_to_text(
                url=youtube_url.strip(),
                output_path="downloads",
                model_size=model_size,
                save_to_archive=save_to_archive
            )
            
            # 결과 처리
            if result['success']:
                progress_bar.progress(1.0)
                status_text.markdown("<p style='color: #2b8a3e; font-size: 0.9rem; font-weight: 500;'>✅ 변환 완료!</p>", unsafe_allow_html=True)
                
                # 성공 메시지 (영구 저장 여부에 따라 다르게 표시)
                if save_to_archive and result.get('archived_files'):
                    st.success("🎉 모든 파일이 성공적으로 변환되었고 영구 보관함에 저장되었습니다!")
                else:
                    st.success("🎉 모든 파일이 성공적으로 변환되었습니다!")
                
                # 결과 표시
                st.markdown("### 📁 변환 결과")
                st.markdown("<p style='color: #495057; margin-bottom: 1.5rem;'>다음 파일들이 성공적으로 생성되었습니다</p>", unsafe_allow_html=True)
                
                # 다운로드 버튼들
                col1, col2, col3 = st.columns(3)
                
                # MP4 다운로드 및 보기
                if result['video_file'] and Path(result['video_file']).exists():
                    with col1:
                        # 다운로드 버튼
                        with open(result['video_file'], 'rb') as f:
                            video_data = f.read()
                            st.download_button(
                                "📹 영상 다운로드",
                                video_data,
                                file_name=Path(result['video_file']).name,
                                mime="video/mp4"
                            )
                        # 영상 보기 버튼
                        if st.button("🎬 영상보기", key="view_video"):
                            st.session_state.show_video = True
                
                # MP3 다운로드 및 듣기
                if result['audio_file'] and Path(result['audio_file']).exists():
                    with col2:
                        # 다운로드 버튼
                        with open(result['audio_file'], 'rb') as f:
                            audio_data = f.read()
                            st.download_button(
                                "🎵 오디오 다운로드",
                                audio_data,
                                file_name=Path(result['audio_file']).name,
                                mime="audio/mpeg"
                            )
                        # 오디오 듣기 버튼
                        if st.button("🔊 음성듣기", key="listen_audio"):
                            st.session_state.show_audio = True
                
                # TXT 다운로드 및 보기
                if result['text_file'] and Path(result['text_file']).exists():
                    with col3:
                        # 다운로드 버튼
                        st.download_button(
                            "📄 텍스트 다운로드",
                            result['text_content'],
                            file_name=Path(result['text_file']).name,
                            mime="text/plain"
                        )
                        # 텍스트 보기 버튼
                        if st.button("📝 텍스트보기", key="view_text"):
                            st.session_state.show_text = True
                
                # 미디어 표시 섹션
                st.markdown("<hr style='margin: 2rem 0; border: none; height: 1px; background-color: #dee2e6;'>", unsafe_allow_html=True)
                st.markdown("### 🎬 미디어 보기")
                
                # 영상 보기
                if st.session_state.show_video and result['video_file'] and Path(result['video_file']).exists():
                    st.markdown("#### 📹 영상")
                    st.video(result['video_file'])
                
                # 오디오 듣기
                if st.session_state.show_audio and result['audio_file'] and Path(result['audio_file']).exists():
                    st.markdown("#### 🔊 오디오")
                    st.audio(result['audio_file'])
                
                # 텍스트 미리보기
                if (st.session_state.show_text or result['text_content']) and result['text_file'] and Path(result['text_file']).exists():
                    st.markdown("<h4 id='text_preview'>📄 텍스트 미리보기</h4>", unsafe_allow_html=True)
                    st.markdown("<p style='color: #495057; margin-bottom: 1rem;'>AI가 변환한 텍스트 내용입니다</p>", unsafe_allow_html=True)
                    st.text_area(
                        "변환 결과",
                        result['text_content'],
                        height=200
                    )
            
            else:
                # 오류 처리
                progress_bar.progress(0)
                status_text.markdown("<p style='color: #c92a2a; font-size: 0.9rem; font-weight: 500;'>❌ 변환 실패</p>", unsafe_allow_html=True)
                st.error(f"변환에 실패했습니다: {result['error']}")
                st.markdown("<p style='color: #495057; font-size: 0.9rem; margin-top: 1rem;'>다른 URL을 시도하거나 나중에 다시 시도해보세요.</p>", unsafe_allow_html=True)
                
        except Exception as e:
            progress_bar.progress(0)
            status_text.markdown("<p style='color: #c92a2a; font-size: 0.9rem; font-weight: 500;'>❌ 오류 발생</p>", unsafe_allow_html=True)
            st.error(f"처리 중 오류가 발생했습니다: {str(e)}")
            st.markdown("<p style='color: #495057; font-size: 0.9rem; margin-top: 1rem;'>URL이 올바른지 확인하고 다시 시도해보세요.</p>", unsafe_allow_html=True)
        
        finally:
            # 처리 완료 - 상태 재설정
            st.session_state.is_processing = False