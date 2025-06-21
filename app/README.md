# 애플리케이션 예시

이 폴더에는 Redis KeyVault에서 저장된 설정을 불러와 각 서비스에 연결하는 실제 사용 예시가 포함되어 있습니다.

## 포함된 예시들

### 1. OpenSearch 연결 예시 (`sample-opensearch.py`)
- Redis KeyVault에서 opensearch 설정을 불러와 OpenSearch 클라이언트 생성
- 클러스터 정보 조회 및 연결 테스트
- 문서 색인 및 검색 예시

**필요한 패키지:**
```bash
pip install opensearch-py
```

### 2. MariaDB 연결 예시 (`sample-mariadb.py`)
- Redis KeyVault에서 mariadb 설정을 불러와 데이터베이스 연결
- 연결 상태 확인 및 서버 정보 조회
- 테이블 생성, 데이터 삽입/조회 예시

**필요한 패키지:**
```bash
pip install mysql-connector-python
```

### 3. Kafka 연결 예시 (`sample-kafka.py`)
- Redis KeyVault에서 kafka 설정을 불러와 Producer/Consumer 생성
- 연결 테스트 및 메시지 전송/수신 예시
- SSL/SASL 인증 지원

**필요한 패키지:**
```bash
pip install kafka-python
```

## 사용 방법

### 1. 설정 저장
먼저 samples 폴더의 설정 파일들을 Redis KeyVault에 저장해야 합니다:

```bash
# 설정 파일들을 실제 환경에 맞게 수정 후
python redis_keyvault.py save samples/opensearch.json
python redis_keyvault.py save samples/mariadb.json
python redis_keyvault.py save samples/kafka.json
```

### 2. 예시 실행

각 서비스별 예시를 실행합니다:

```bash
# OpenSearch 예시 실행
python app/sample-opensearch.py

# MariaDB 예시 실행
python app/sample-mariadb.py

# Kafka 예시 실행
python app/sample-kafka.py
```

## 예시별 기능

### OpenSearch 예시
- **연결 테스트**: 클러스터 정보 및 상태 확인
- **문서 색인**: 샘플 로그 문서를 인덱스에 저장
- **문서 검색**: 저장된 문서를 검색하여 조회

### MariaDB 예시
- **연결 테스트**: 서버 버전 및 데이터베이스 정보 확인
- **테이블 조작**: 샘플 테이블 생성 및 데이터 삽입
- **데이터 조회**: 저장된 데이터 조회 및 테이블 정보 확인
- **정리 기능**: 데모 데이터 정리 옵션

### Kafka 예시
- **연결 테스트**: 브로커 연결 및 테스트 메시지 전송
- **Producer**: 다양한 유형의 샘플 메시지 전송
- **Consumer**: 메시지 수신 및 처리 예시
- **SSL/SASL**: 보안 연결 지원

## 주의사항

1. **패키지 설치**: 각 예시를 실행하기 전에 필요한 패키지를 설치하세요.
2. **설정 확인**: Redis KeyVault에 올바른 설정이 저장되어 있는지 확인하세요.
3. **서비스 상태**: 각 서비스(OpenSearch, MariaDB, Kafka)가 실행 중인지 확인하세요.
4. **네트워크**: 방화벽 및 네트워크 연결 상태를 확인하세요.
5. **권한**: 각 서비스에 대한 적절한 접근 권한이 있는지 확인하세요.

## 트러블슈팅

### 공통 문제
- `ModuleNotFoundError`: 필요한 패키지를 설치하세요
- 설정을 찾을 수 없음: Redis KeyVault에 설정이 저장되어 있는지 확인
- 연결 실패: 서비스 상태 및 네트워크 연결 확인

### 서비스별 문제
- **OpenSearch**: SSL 인증서 문제 시 `verify_certs=False` 설정 확인
- **MariaDB**: 데이터베이스 권한 및 방화벽 설정 확인
- **Kafka**: 토픽 존재 여부 및 보안 설정 확인
