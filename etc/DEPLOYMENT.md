# Redis KeyVault 배포 가이드

이 문서는 Redis KeyVault 패키지를 whl 파일로 빌드하고 배포하는 방법을 설명합니다.

## 빌드 환경 준비

### 1. 필요한 패키지 설치
```bash
pip install build twine
```

### 2. 프로젝트 구조 확인
```
redis-as-kv/
├── redis_keyvault/          # 메인 패키지
│   ├── __init__.py
│   └── redis_keyvault.py
├── app/                     # 예시 애플리케이션
├── samples/                 # 샘플 설정 파일
├── pyproject.toml          # 패키지 설정
├── setup.py                # 호환성용 설정
├── MANIFEST.in             # 추가 파일 포함 설정
├── README.md               # 영어 문서
├── README-ko.md            # 한국어 문서
└── LICENSE                 # 라이선스
```

## 빌드 과정

### 1. 패키지 빌드
```bash
cd h:\git_repo\redis-as-kv
python -m build
```

### 2. 생성된 파일 확인
```bash
dir dist
```

다음 파일들이 생성됩니다:
- `redis_keyvault-1.0.0-py3-none-any.whl` - 배포용 wheel 파일
- `redis_keyvault-1.0.0.tar.gz` - 소스 배포용 tar.gz 파일

## 설치 및 테스트

### 1. 로컬 설치
```bash
pip install dist\redis_keyvault-1.0.0-py3-none-any.whl
```

### 2. CLI 명령어 테스트
```bash
redis-keyvault
```

### 3. Python 모듈 테스트
```python
import redis_keyvault
print(redis_keyvault.__version__)
```

### 4. 모듈 기능 테스트
```python
from redis_keyvault import save_info, get_info
# 사용법은 README.md 참조
```

## 배포 옵션

### 1. PyPI 업로드 (공식 패키지 저장소)
```bash
# 테스트 PyPI에 업로드
twine upload --repository testpypi dist/*

# 실제 PyPI에 업로드
twine upload dist/*
```

### 2. 프라이빗 패키지 서버
```bash
# 프라이빗 서버에 업로드
twine upload --repository-url https://your-private-pypi.com/simple/ dist/*
```

### 3. 직접 배포
- `dist/redis_keyvault-1.0.0-py3-none-any.whl` 파일을 직접 배포
- 사용자는 `pip install redis_keyvault-1.0.0-py3-none-any.whl`로 설치

## 패키지 정보

- **패키지명**: redis-keyvault
- **버전**: 1.0.0
- **Python 지원**: 3.6+
- **라이선스**: MIT
- **의존성**:
  - redis>=4.0.0
  - cryptography>=3.4.0
  - python-dotenv>=0.19.0

## CLI 명령어

설치 후 다음 명령어를 사용할 수 있습니다:

```bash
# 설정 저장
redis-keyvault save config.json

# 설정 조회
redis-keyvault get myconfig
```

## 버전 업데이트

새 버전을 배포하려면:

1. `pyproject.toml`에서 version 수정
2. `redis_keyvault/__init__.py`에서 __version__ 수정
3. 변경사항 커밋
4. 빌드 및 배포 재실행

## 주의사항

- **Redis Sentinel 클러스터 필수**: 이 패키지는 Redis Sentinel 클러스터 환경에서만 작동합니다.
- **보안**: 프로덕션 환경에서는 적절한 인증 정보를 사용하세요.
- **테스트**: 새 환경에서 설치 후 반드시 기능 테스트를 실행하세요.
