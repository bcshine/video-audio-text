#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
유튜브 → 텍스트 변환 유틸리티 함수들
"""

import os
import subprocess
from pathlib import Path
import time
import yt_dlp
import whisper

def download_youtube_video(url, output_path="downloads"):
    """유튜브 영상 다운로드"""
    try:
        # 비디오 ID 추출
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            info = ydl.extract_info(url, download=False)
            video_id = info.get('id', '')
    except Exception as e:
        print(f"❌ 영상 정보 추출 실패: {e}")
        return None
    
    # 각 영상마다 별도 폴더 생성
    unique_folder = os.path.join(output_path, f"video_{video_id}")
    os.makedirs(unique_folder, exist_ok=True)
    
    # 타임스탬프 기반 파일명
    timestamp = int(time.time())
    
    # yt-dlp 설정
    ydl_opts = {
        'format': 'best[height<=720]',
        'outtmpl': f'{unique_folder}/{timestamp}_%(id)s.%(ext)s',
        'restrictfilenames': True,
        'ignoreerrors': False,
        'cachedir': None,
        'noplaylist': True,
        'quiet': True,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            
            # 다운로드된 파일 찾기
            download_dir = Path(unique_folder)
            video_files = list(download_dir.glob("*.mp4")) + list(download_dir.glob("*.webm")) + list(download_dir.glob("*.mkv"))
            
            if video_files:
                latest_file = max(video_files, key=lambda f: f.stat().st_mtime)
                return str(latest_file)
            else:
                return None
                    
    except Exception as e:
        print(f"❌ 다운로드 실패: {e}")
        return None

def extract_audio_to_mp3(video_path, audio_path=None):
    """영상에서 음성 추출"""
    if not audio_path:
        audio_path = Path(video_path).with_suffix('.mp3')
    
    try:
        command = [
            'ffmpeg', '-i', video_path, '-vn', '-acodec', 'mp3',
            '-ab', '192k', '-ar', '44100', '-y', str(audio_path)
        ]
        
        result = subprocess.run(command, capture_output=True, text=True)
        
        if result.returncode == 0:
            return str(audio_path)
        else:
            print(f"❌ 음성 추출 실패: {result.stderr}")
            return None
            
    except Exception as e:
        print(f"❌ 음성 추출 중 오류: {e}")
        return None

def convert_audio_to_text(audio_path, model_size="base"):
    """음성을 텍스트로 변환"""
    try:
        model = whisper.load_model(model_size)
        result = model.transcribe(audio_path)
        return result["text"].strip()
        
    except Exception as e:
        print(f"❌ 텍스트 변환 실패: {e}")
        return None

def save_text_to_file(text, file_path):
    """텍스트를 파일로 저장"""
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(text)
        return str(file_path)
    except Exception as e:
        print(f"❌ 파일 저장 실패: {e}")
        return None

def process_youtube_to_text(url, output_path="downloads", model_size="base"):
    """
    전체 프로세스: 유튜브 URL → 영상 → 음성 → 텍스트
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
        # 1. 영상 다운로드
        video_file = download_youtube_video(url, output_path)
        if not video_file:
            result['error'] = "영상 다운로드 실패"
            return result
        result['video_file'] = video_file
        
        # 2. 음성 추출
        audio_file = extract_audio_to_mp3(video_file)
        if not audio_file:
            result['error'] = "음성 추출 실패"
            return result
        result['audio_file'] = audio_file
        
        # 3. 텍스트 변환
        text = convert_audio_to_text(audio_file, model_size)
        if not text:
            result['error'] = "텍스트 변환 실패"
            return result
        result['text_content'] = text
        
        # 4. 텍스트 파일 저장
        text_file = Path(audio_file).with_suffix('.txt')
        saved_text_file = save_text_to_file(text, text_file)
        if not saved_text_file:
            result['error'] = "텍스트 파일 저장 실패"
            return result
        result['text_file'] = saved_text_file
        
        result['success'] = True
        
    except Exception as e:
        result['error'] = f"처리 중 오류: {str(e)}"
    
    return result 