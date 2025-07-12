#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
유튜브 → 텍스트 변환 유틸리티 함수들
"""

import os
import subprocess
import shutil
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
    
    # 기본 downloads 폴더 생성
    os.makedirs(output_path, exist_ok=True)
    
    # 각 영상마다 별도 폴더 생성
    unique_folder = os.path.join(output_path, f"video_{video_id}")
    os.makedirs(unique_folder, exist_ok=True)
    
    print(f"📁 폴더 생성: {unique_folder}")
    
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
                print(f"✅ 영상 다운로드 완료: {latest_file.name}")
                return str(latest_file)
            else:
                print("❌ 다운로드된 파일을 찾을 수 없습니다.")
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

def process_youtube_to_text(url, output_path="downloads", model_size="base", save_to_archive=False):
    """
    전체 프로세스: 유튜브 URL → 영상 → 음성 → 텍스트
    
    Parameters:
    - url: 유튜브 URL
    - output_path: 임시 출력 경로
    - model_size: Whisper 모델 크기
    - save_to_archive: 영구 보관소에 저장 여부
    """
    result = {
        'video_file': None,
        'audio_file': None, 
        'text_file': None,
        'text_content': None,
        'archived_files': [],
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
        
        # 5. 영구 보관소에 파일 복사 (선택적)
        if save_to_archive:
            archive_path = Path("archives")
            archive_path.mkdir(exist_ok=True)
            
            # 비디오 ID 추출
            video_path = Path(video_file)
            video_id = video_path.parent.name.replace("video_", "")
            
            # 타임스탬프 추출
            timestamp = video_path.stem.split("_")[0]
            
            # 아카이브 폴더 생성
            archive_video_path = archive_path / f"video_{video_id}"
            archive_video_path.mkdir(exist_ok=True)
            
            # 파일 복사
            archived_files = []
            
            # 비디오 파일 복사
            video_dest = archive_video_path / video_path.name
            if not video_dest.exists():
                shutil.copy2(video_file, video_dest)
                archived_files.append(str(video_dest))
            
            # 오디오 파일 복사
            audio_path = Path(audio_file)
            audio_dest = archive_video_path / audio_path.name
            if not audio_dest.exists():
                shutil.copy2(audio_file, audio_dest)
                archived_files.append(str(audio_dest))
            
            # 텍스트 파일 복사
            text_path = Path(text_file)
            text_dest = archive_video_path / text_path.name
            if not text_dest.exists():
                shutil.copy2(text_file, text_dest)
                archived_files.append(str(text_dest))
            
            result['archived_files'] = archived_files
        
        result['success'] = True
        
    except Exception as e:
        result['error'] = f"처리 중 오류: {str(e)}"
    
    return result