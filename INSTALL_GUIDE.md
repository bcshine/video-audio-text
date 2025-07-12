# 🚀 고속 다운로드를 위한 aria2c 설치 가이드

YouTube 비디오를 더 빠르게 다운로드하려면 `aria2c`를 설치하세요. 일반 모드보다 2-5배 빠른 속도를 제공합니다.

## 🖥️ Windows

### 방법 1: 직접 다운로드
1. [aria2 공식 릴리즈 페이지](https://github.com/aria2/aria2/releases)에서 Windows 버전 다운로드
2. 압축 해제 후 `aria2c.exe`를 PATH에 추가
3. 명령 프롬프트에서 `aria2c --version`으로 설치 확인

### 방법 2: Chocolatey (권장)
```powershell
choco install aria2
```

### 방법 3: Scoop
```powershell
scoop install aria2
```

## 🍎 macOS

### 방법 1: Homebrew (권장)
```bash
brew install aria2
```

### 방법 2: MacPorts
```bash
sudo port install aria2
```

## 🐧 Linux

### Ubuntu/Debian
```bash
sudo apt update
sudo apt install aria2
```

### CentOS/RHEL
```bash
sudo yum install aria2
```

### Fedora
```bash
sudo dnf install aria2
```

### Arch Linux
```bash
sudo pacman -S aria2
```

## ✅ 설치 확인

설치가 완료되면 터미널/명령 프롬프트에서 다음 명령어로 확인:

```bash
aria2c --version
```

버전 정보가 표시되면 성공적으로 설치된 것입니다!

## 🎯 사용 방법

1. 앱을 실행하고 사이드바에서 "🚀 고속 다운로드 모드 (aria2c)" 옵션을 체크
2. 평소와 같이 YouTube URL을 입력하고 변환 시작
3. 더 빠른 다운로드 속도를 경험하세요!

## 📊 성능 차이

| 모드 | 속도 | 특징 |
|------|------|------|
| 일반 모드 | 기본 | 안정적, 호환성 좋음 |
| 고속 모드 | 2-5배 빠름 | 멀티스레드, 병렬 다운로드 |

## 🔧 문제 해결

### aria2c가 인식되지 않는 경우
- Windows: PATH 환경변수에 aria2c.exe 경로 추가
- macOS/Linux: `which aria2c` 명령어로 설치 위치 확인
- 터미널/명령 프롬프트를 다시 시작해보세요

### 다운로드 오류가 발생하는 경우
- 일반 모드로 전환하여 다시 시도
- 인터넷 연결 상태 확인
- 방화벽 설정 확인

## 💡 팁

- aria2c는 대용량 파일 다운로드에 특히 효과적입니다
- 네트워크 환경이 좋을수록 속도 향상 효과가 큽니다
- 첫 번째 다운로드는 설정 최적화로 약간의 지연이 있을 수 있습니다 