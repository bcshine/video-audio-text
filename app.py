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

# 현대적이고 반응형 디자인 CSS
st.markdown("""
<style>
/* 전체 앱 스타일 */
.stApp {
    background: linear-gradient(135deg, #f7f3e9 0%, #e6d7c3 50%, #f4e4bc 100%);
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* 메인 컨테이너 */
.main .block-container {
    padding: 1rem;
    max-width: 1200px;
    background: rgba(255, 255, 255, 0.98);
    border-radius: 20px;
    box-shadow: 0 15px 35px rgba(0, 0, 0, 0.15);
    backdrop-filter: blur(10px);
    margin: 1rem auto;
    border: 1px solid rgba(255, 255, 255, 0.3);
}

/* 제목 스타일 - 더 강력한 규칙 */
.stTitle {
    text-align: center;
    color: #000000 !important;
    font-weight: 700;
    margin-bottom: 2rem;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
}

/* 모든 제목 태그에 적용 */
h1, .stTitle, .main h1, [data-testid="stTitle"] {
    color: #000000 !important;
    text-align: center !important;
    font-weight: 700 !important;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.3) !important;
}

/* 메인 컨테이너 내 모든 제목 */
.main .block-container h1 {
    color: #000000 !important;
    text-align: center !important;
    font-weight: 700 !important;
}

/* Streamlit 제목 컴포넌트 */
div[data-testid="stMarkdownContainer"] h1 {
    color: #000000 !important;
    text-align: center !important;
    font-weight: 700 !important;
}

/* 사용 방법 카드 */
.stMarkdown h3 {
    color: #000000;
    border-bottom: 3px solid #3498db;
    padding-bottom: 0.5rem;
    margin-bottom: 1rem;
    font-weight: 600;
    text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
}

/* 일반 텍스트 색상 강화 */
.stMarkdown p, .stMarkdown li {
    color: #2c2c2c;
    font-weight: 500;
}

/* 입력 필드 스타일 */
.stTextInput > div > div > input {
    background: rgba(255, 255, 255, 1);
    border: 2px solid #bdc3c7;
    border-radius: 15px;
    padding: 0.75rem 1rem;
    font-size: 1rem;
    color: #2c2c2c;
    font-weight: 500;
    transition: all 0.3s ease;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.stTextInput > div > div > input:focus {
    border-color: #3498db;
    box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.2);
    outline: none;
}

/* 버튼 스타일 */
.stButton > button {
    background: linear-gradient(45deg, #3498db, #2980b9);
    color: white;
    border: none;
    border-radius: 25px;
    padding: 0.75rem 2rem;
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 6px 12px rgba(52, 152, 219, 0.3);
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 16px rgba(52, 152, 219, 0.4);
    background: linear-gradient(45deg, #2980b9, #3498db);
}

/* 폴더비우기 버튼 */
.stButton > button[kind="secondary"] {
    background: linear-gradient(45deg, #e74c3c, #c0392b);
    box-shadow: 0 6px 12px rgba(231, 76, 60, 0.3);
}

.stButton > button[kind="secondary"]:hover {
    background: linear-gradient(45deg, #c0392b, #e74c3c);
    box-shadow: 0 8px 16px rgba(231, 76, 60, 0.4);
}

/* 다운로드 버튼들 */
.stDownloadButton > button {
    background: linear-gradient(45deg, #27ae60, #2ecc71);
    color: white;
    border: none;
    border-radius: 20px;
    padding: 0.6rem 1.5rem;
    font-size: 0.9rem;
    font-weight: 500;
    width: 100%;
    margin-bottom: 0.5rem;
    transition: all 0.3s ease;
    box-shadow: 0 4px 8px rgba(39, 174, 96, 0.3);
}

.stDownloadButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 6px 12px rgba(39, 174, 96, 0.4);
}

/* 사이드바 스타일 */
.css-1d391kg {
    background: rgba(255, 255, 255, 0.98);
    border-radius: 15px;
    padding: 1rem;
    margin: 1rem 0;
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.15);
    border: 1px solid rgba(255, 255, 255, 0.5);
}

/* 셀렉트박스 스타일 */
.stSelectbox > div > div > select {
    background: rgba(255, 255, 255, 1);
    border: 2px solid #bdc3c7;
    border-radius: 15px;
    padding: 0.5rem;
    font-size: 0.9rem;
    color: #2c2c2c;
    font-weight: 500;
    transition: all 0.3s ease;
}

/* 알림 메시지 스타일 */
.stSuccess {
    background: linear-gradient(45deg, #2ecc71, #27ae60);
    color: white;
    border-radius: 15px;
    padding: 1rem;
    margin: 1rem 0;
    box-shadow: 0 4px 8px rgba(46, 204, 113, 0.3);
}

.stError {
    background: linear-gradient(45deg, #e74c3c, #c0392b);
    color: white;
    border-radius: 15px;
    padding: 1rem;
    margin: 1rem 0;
    box-shadow: 0 4px 8px rgba(231, 76, 60, 0.3);
}

/* 진행 바 스타일 */
.stProgress > div > div {
    background: linear-gradient(45deg, #3498db, #2980b9);
    border-radius: 10px;
    height: 10px;
}

/* 텍스트 영역 스타일 */
.stTextArea textarea {
    background: rgba(255, 255, 255, 1);
    border: 2px solid #bdc3c7;
    border-radius: 15px;
    padding: 1rem;
    font-size: 0.9rem;
    color: #2c2c2c;
    font-weight: 500;
    line-height: 1.6;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

/* 모바일 반응형 디자인 */
@media (max-width: 768px) {
    .main .block-container {
        padding: 0.5rem;
        margin: 0.5rem;
        border-radius: 15px;
    }
    
    .stTitle {
        font-size: 1.5rem;
        margin-bottom: 1rem;
    }
    
    .stButton > button {
        width: 100%;
        margin-bottom: 0.5rem;
        padding: 1rem;
        font-size: 1.1rem;
    }
    
    .stTextInput > div > div > input {
        font-size: 1rem;
        padding: 1rem;
    }
    
    /* 컬럼 스택 */
    .row-widget {
        flex-direction: column;
    }
    
    .element-container {
        margin-bottom: 1rem;
    }
}

/* 작은 모바일 화면 */
@media (max-width: 480px) {
    .main .block-container {
        margin: 0.25rem;
        padding: 0.75rem;
    }
    
    .stTitle {
        font-size: 1.3rem;
    }
    
    .stButton > button {
        padding: 0.875rem;
        font-size: 1rem;
    }
}

/* 애니메이션 효과 */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

.main .block-container {
    animation: fadeIn 0.6s ease-out;
}

/* 호버 효과 */
.stMarkdown:hover {
    transform: translateY(-2px);
    transition: transform 0.3s ease;
}

/* 스피너 커스텀 */
.stSpinner {
    color: #3498db;
}

/* 폼 스타일 */
form {
    background: rgba(255, 255, 255, 0.95);
    border-radius: 20px;
    padding: 1.5rem;
    margin: 1rem 0;
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.15);
    backdrop-filter: blur(5px);
    border: 1px solid rgba(255, 255, 255, 0.6);
}

/* 컬럼 간격 조정 */
.row-widget.stColumns {
    gap: 1rem;
}

/* 레이블 텍스트 색상 강화 */
.stTextInput label, .stSelectbox label, .stTextArea label {
    color: #2c2c2c !important;
    font-weight: 600 !important;
}

/* 사이드바 헤더 색상 강화 */
.css-1d391kg h2 {
    color: #1a1a1a !important;
    font-weight: 700 !important;
}

/* 터치 친화적 디자인 */
@media (hover: none) and (pointer: coarse) {
    .stButton > button {
        min-height: 48px;
        font-size: 1.1rem;
        padding: 1rem 1.5rem;
    }
    
    .stTextInput > div > div > input {
        min-height: 48px;
        font-size: 1rem;
        padding: 1rem;
    }
    
    .stSelectbox > div > div > select {
        min-height: 48px;
        font-size: 1rem;
        padding: 1rem;
    }
}

/* 로딩 스피너 개선 */
.stSpinner > div {
    border-color: #3498db transparent transparent transparent;
}

/* 다크 모드 지원 */
@media (prefers-color-scheme: dark) {
    .main .block-container {
        background: rgba(30, 30, 30, 0.95);
        color: #f0f0f0;
    }
    
    .stTextInput > div > div > input {
        background: rgba(50, 50, 50, 0.9);
        color: #f0f0f0;
        border-color: #555;
    }
    
    .stSelectbox > div > div > select {
        background: rgba(50, 50, 50, 0.9);
        color: #f0f0f0;
        border-color: #555;
    }
    
    .stTextArea textarea {
        background: rgba(50, 50, 50, 0.9);
        color: #f0f0f0;
        border-color: #555;
    }
}

/* 접근성 개선 */
.stButton > button:focus {
    outline: 3px solid #3498db;
    outline-offset: 2px;
}

.stTextInput > div > div > input:focus {
    outline: 2px solid #3498db;
    outline-offset: 1px;
}

/* 스크롤 개선 */
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: rgba(0, 0, 0, 0.1);
    border-radius: 10px;
}

::-webkit-scrollbar-thumb {
    background: linear-gradient(45deg, #3498db, #2980b9);
    border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(45deg, #2980b9, #3498db);
}

</style>
""", unsafe_allow_html=True)

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
    if st.button("🗑️ 폴더비우기", help="다운로드 폴더의 모든 파일을 삭제합니다", type="secondary"):
        try:
            downloads_path = Path("downloads")
            if downloads_path.exists():
                shutil.rmtree(downloads_path)
                st.success("✅ 폴더 비우기 완료!")
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