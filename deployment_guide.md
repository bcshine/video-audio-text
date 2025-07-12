# 📦 배포 가이드

## 🌟 방법 1: Streamlit Cloud (무료, 추천)

### 단계별 과정:

1. **GitHub 저장소 생성**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/사용자명/youtube-to-text.git
   git push -u origin main
   ```

2. **Streamlit Cloud 배포**
   - [share.streamlit.io](https://share.streamlit.io) 접속
   - GitHub 계정으로 로그인
   - "New app" 클릭
   - 저장소 선택: `사용자명/youtube-to-text`
   - Main file path: `app.py`
   - Deploy! 클릭

3. **결과**
   - 자동으로 URL 생성: `https://사용자명-youtube-to-text-app-xyz.streamlit.app`
   - 코드 변경 시 자동 업데이트

### 주의사항:
- 무료 계정: 1GB 메모리 제한
- 대용량 영상 처리에 제한이 있을 수 있음
- 첫 실행 시 AI 모델 다운로드로 시간 소요

---

## 🐳 방법 2: Docker 배포

### 로컬 Docker 실행:
```bash
# Docker 이미지 빌드
docker build -t youtube-to-text .

# 컨테이너 실행
docker run -p 8501:8501 youtube-to-text
```

### 클라우드 배포 (예: Google Cloud Run):
```bash
# 이미지 빌드 및 푸시
docker build -t gcr.io/프로젝트-id/youtube-to-text .
docker push gcr.io/프로젝트-id/youtube-to-text

# Cloud Run 배포
gcloud run deploy youtube-to-text \
    --image gcr.io/프로젝트-id/youtube-to-text \
    --platform managed \
    --region asia-northeast1 \
    --allow-unauthenticated
```

---

## 🖥️ 방법 3: 실행 파일 생성 (PyInstaller)

### 설치 및 생성:
```bash
# PyInstaller 설치
pip install pyinstaller

# 실행 파일 생성 (단일 파일)
pyinstaller --onefile --noconsole app.py

# 실행 파일 생성 (폴더 포함)
pyinstaller --onedir app.py
```

### 주의사항:
- FFmpeg가 별도로 필요
- 파일 크기가 매우 클 수 있음 (수백MB)
- Windows/Mac/Linux 각각 다른 실행 파일 필요

---

## 🌍 방법 4: Replit 배포

### 단계:
1. [replit.com](https://replit.com) 접속
2. "Create Repl" → "Import from GitHub"
3. 저장소 URL 입력
4. `.replit` 파일 생성:
   ```
   run = "streamlit run app.py"
   
   [nix]
   channel = "stable-22_11"
   
   [nix.packages]
   ffmpeg = "latest"
   ```

---

## 🛠️ 방법 5: 개인 서버 배포

### Nginx + 도메인 연결:
```bash
# 서버에서 실행
git clone https://github.com/사용자명/youtube-to-text.git
cd youtube-to-text
pip install -r requirements.txt
nohup streamlit run app.py --server.port=8501 &
```

### Nginx 설정:
```nginx
server {
    listen 80;
    server_name yourdomain.com;
    
    location / {
        proxy_pass http://localhost:8501;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## 📊 배포 방법 비교

| 방법 | 난이도 | 비용 | 성능 | 제어권 |
|------|--------|------|------|--------|
| Streamlit Cloud | ⭐ | 무료 | 보통 | 낮음 |
| Docker | ⭐⭐⭐ | 유료 | 높음 | 높음 |
| 실행 파일 | ⭐⭐ | 무료 | 높음 | 높음 |
| Replit | ⭐ | 무료/유료 | 보통 | 보통 |
| 개인 서버 | ⭐⭐⭐⭐ | 유료 | 최고 | 최고 |

---

## 🎯 추천 배포 전략

### 1. **개인/테스트용**: Streamlit Cloud
- 무료이고 간단
- 빠른 배포 가능

### 2. **소규모 사용자**: Docker + Google Cloud Run
- 안정적이고 확장 가능
- 사용한 만큼 과금

### 3. **대규모 사용자**: 개인 서버
- 최고 성능
- 완전한 제어권

---

## 🔧 배포 후 최적화

### 성능 향상:
- Whisper 모델 크기 조정
- 메모리 사용량 모니터링
- 동시 접속자 수 제한

### 보안 강화:
- HTTPS 적용
- 사용량 제한
- 로그 모니터링

---

## 📞 지원 및 문의

배포 관련 문제가 있으시면:
- GitHub Issues에 문의
- 이메일: [이메일 주소]
- 문서: [상세 문서 링크] 