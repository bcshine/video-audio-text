#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
유튜브 → 텍스트 변환 유틸리티 함수들
웹 인터페이스와 CLI에서 공통으로 사용
"""

import os
import subprocess
from pathlib import Path
import time
import yt_dlp
import whisper

def download_youtube_video(url, output_path="downloads"):
    """
    유튜브 영상을 다운로드하는 함수
    
    Args:
        url (str): 유튜브 영상 URL
        output_path (str): 다운로드할 폴더 경로
    
    Returns:
        str: 다운로드된 파일 경로 또는 None
    """
    print(f"📥 유튜브 영상 다운로드 시작: {url}")
    
    # 먼저 비디오 ID 추출
    try:
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            info = ydl.extract_info(url, download=False)
            video_id = info.get('id', '')
            video_title = info.get('title', '')
    except Exception as e:
        print(f"❌ 영상 정보 추출 실패: {e}")
        return None
    
    # 각 영상마다 별도의 폴더 생성 (비디오 ID 기반)
    unique_folder = os.path.join(output_path, f"video_{video_id}")
    os.makedirs(unique_folder, exist_ok=True)
    
    print(f"📁 다운로드 폴더: {unique_folder}")
    
    # 타임스탬프 생성 (파일명 중복 방지)
    timestamp = int(time.time())
    
    # yt-dlp 설정
    ydl_opts = {
        'format': 'best[height<=720]',  # 720p 이하 최고 화질 (쇼츠용)
        'outtmpl': f'{unique_folder}/{timestamp}_%(id)s_%(title)s.%(ext)s',  # 각 영상별 폴더에 저장
        'restrictfilenames': True,  # 파일명 안전하게 변경
        'no_warnings': False,  # 경고 메시지 표시
        'ignoreerrors': False,  # 에러 시 중단
        'force_json': False,  # JSON 출력 비활성화
        'cachedir': None,  # 캐시 디렉토리 비활성화
        'rm_cachedir': True,  # 캐시 디렉토리 삭제
        'writeinfojson': False,  # JSON 정보 파일 생성 안함
        'writedescription': False,  # 설명 파일 생성 안함
        'writesubtitles': False,  # 자막 파일 생성 안함
        'writeautomaticsub': False,  # 자동 자막 생성 안함
        'overwrites': True,  # 기존 파일 덮어쓰기
        'noplaylist': True,  # 플레이리스트 무시
    }
    
    try:
        # 다운로드 시작 시간 기록
        download_start_time = time.time()
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"📋 영상 정보:")
            print(f"   - ID: {video_id}")
            print(f"   - 제목: {video_title}")
            
            # 영상 다운로드
            print(f"⬇️ 영상 다운로드 시작...")
            ydl.download([url])
            print(f"✅ 다운로드 완료!")
            
            # 해당 영상의 폴더에서 파일 검색 (매우 단순화)
            download_dir = Path(unique_folder)
            video_files = list(download_dir.glob("*.mp4")) + list(download_dir.glob("*.webm")) + list(download_dir.glob("*.mkv"))
            
            print(f"🔍 파일 검색 결과 (폴더: {unique_folder}):")
            print(f"   - 비디오 파일: {len(video_files)}개")
            for i, f in enumerate(video_files):
                print(f"   - {i+1}. {f.name}")
            
            if video_files:
                # 가장 최근 파일 선택 (해당 폴더에는 해당 영상 파일만 있음)
                latest_file = max(video_files, key=lambda f: f.stat().st_mtime)
                print(f"✅ 다운로드 완료: {latest_file}")
                return str(latest_file)
            else:
                print(f"❌ 다운로드된 파일을 찾을 수 없습니다.")
                return None
                    
    except Exception as e:
        print(f"❌ 다운로드 실패: {e}")
        return None

def extract_audio_to_mp3(video_path, audio_path=None):
    """
    영상 파일에서 음성을 추출하여 MP3로 저장
    
    Args:
        video_path (str): 원본 영상 파일 경로
        audio_path (str): 저장할 음성 파일 경로 (옵션)
    
    Returns:
        str: 추출된 MP3 파일 경로 또는 None
    """
    print(f"🎵 음성 추출 시작: {video_path}")
    
    if not audio_path:
        # 영상 파일과 같은 이름으로 mp3 파일 생성
        video_file = Path(video_path)
        audio_path = video_file.with_suffix('.mp3')
    
    try:
        # ffmpeg 명령어로 음성 추출
        command = [
            'ffmpeg',
            '-i', video_path,  # 입력 파일
            '-vn',  # 비디오 제거
            '-acodec', 'mp3',  # MP3 코덱 사용
            '-ab', '192k',  # 192kbps 비트레이트
            '-ar', '44100',  # 44.1kHz 샘플링 레이트
            '-y',  # 기존 파일 덮어쓰기
            str(audio_path)
        ]
        
        # ffmpeg 실행
        result = subprocess.run(command, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ 음성 추출 완료: {audio_path}")
            return str(audio_path)
        else:
            print(f"❌ 음성 추출 실패: {result.stderr}")
            return None
            
    except Exception as e:
        print(f"❌ 음성 추출 중 오류: {e}")
        return None

def convert_audio_to_text(audio_path, model_size="base"):
    """
    음성 파일을 텍스트로 변환 (OpenAI Whisper 사용)
    
    Args:
        audio_path (str): 음성 파일 경로
        model_size (str): Whisper 모델 크기 (tiny, base, small, medium, large)
    
    Returns:
        str: 변환된 텍스트 또는 None
    """
    print(f"📝 음성을 텍스트로 변환 시작: {audio_path}")
    print(f"🤖 Whisper 모델 크기: {model_size}")
    
    try:
        # Whisper 모델 로드
        model = whisper.load_model(model_size)
        
        # 음성 파일 텍스트 변환
        result = model.transcribe(audio_path)
        
        # 변환된 텍스트
        text = result["text"].strip()
        
        print(f"✅ 텍스트 변환 완료!")
        print(f"📄 변환된 텍스트 길이: {len(text)} 글자")
        
        return text
        
    except Exception as e:
        print(f"❌ 텍스트 변환 실패: {e}")
        return None

def save_text_to_file(text, file_path):
    """
    텍스트를 파일로 저장
    
    Args:
        text (str): 저장할 텍스트
        file_path (str): 저장할 파일 경로
    
    Returns:
        str: 저장된 파일 경로 또는 None
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(text)
        print(f"💾 텍스트 파일 저장 완료: {file_path}")
        return str(file_path)
    except Exception as e:
        print(f"❌ 파일 저장 실패: {e}")
        return None

def process_youtube_to_text(url, output_path="downloads", model_size="base"):
    """
    전체 프로세스 실행: 유튜브 URL → 영상 → 음성 → 텍스트
    
    Args:
        url (str): 유튜브 URL
        output_path (str): 출력 폴더 경로
        model_size (str): Whisper 모델 크기
    
    Returns:
        dict: 결과 파일들의 경로 정보
        {
            'video_file': str,
            'audio_file': str, 
            'text_file': str,
            'text_content': str,
            'success': bool,
            'error': str
        }
    """
    result = {
        'video_file': None,
        'audio_file': None, 
        'text_file': None,
        'text_content': None,
        'success': False,
        'error': None
    }
    
    try:
        # 1단계: 영상 다운로드
        video_file = download_youtube_video(url, output_path)
        if not video_file:
            result['error'] = "영상 다운로드에 실패했습니다."
            return result
        result['video_file'] = video_file
        
        # 2단계: 음성 추출
        audio_file = extract_audio_to_mp3(video_file)
        if not audio_file:
            result['error'] = "음성 추출에 실패했습니다."
            return result
        result['audio_file'] = audio_file
        
        # 3단계: 텍스트 변환
        text = convert_audio_to_text(audio_file, model_size)
        if not text:
            result['error'] = "텍스트 변환에 실패했습니다."
            return result
        result['text_content'] = text
        
        # 4단계: 텍스트 파일 저장
        text_file = Path(audio_file).with_suffix('.txt')
        saved_text_file = save_text_to_file(text, text_file)
        if not saved_text_file:
            result['error'] = "텍스트 파일 저장에 실패했습니다."
            return result
        result['text_file'] = saved_text_file
        
        result['success'] = True
        print(f"🎉 모든 작업 완료!")
        
    except Exception as e:
        result['error'] = f"처리 중 오류 발생: {str(e)}"
        print(f"❌ {result['error']}")
    
    return result 