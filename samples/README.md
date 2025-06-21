# 샘플 설정 파일들

이 폴더에는 `redis_keyvault.py`를 사용하여 저장할 수 있는 다양한 서비스의 연결 정보 샘플이 포함되어 있습니다.

## 포함된 샘플들

### 1. OpenSearch (`opensearch.json`)
- 기본 연결 정보 (hostname, port, username, password)
- 인덱스 및 SSL 설정
- 클러스터 정보

### 2. MariaDB (`mariadb.json`)
- 데이터베이스 연결 정보
- SSL 설정
- 기본 옵션

### 3. Kafka (`kafka.json`)
- 브로커 연결 정보
- SASL/SSL 보안 설정
- 토픽 및 그룹 설정

### 4. ProxySQL (`sample-proxysql.json`)
- ProxySQL 연결 정보
- 외부 접속 정보
- MariaDB 프록시 설정

## 사용 방법

### 1. 샘플 파일 수정
각 JSON 파일을 실제 환경에 맞게 수정합니다:

```bash
# 파일 편집
notepad opensearch.json
notepad mariadb.json
notepad kafka.json
notepad sample-proxysql.json
```

### 2. Redis KeyVault에 저장
수정된 설정을 Redis에 저장합니다:

```bash
# 각 서비스 설정 저장
python redis_keyvault.py save samples/opensearch.json
python redis_keyvault.py save samples/mariadb.json
python redis_keyvault.py save samples/kafka.json
python redis_keyvault.py save samples/sample-proxysql.json
```

### 3. 저장된 설정 조회
저장된 설정을 확인합니다:

```bash
# 각 서비스 설정 조회
python redis_keyvault.py get opensearch
python redis_keyvault.py get mariadb
python redis_keyvault.py get kafka
python redis_keyvault.py get sample-proxysql
```

## 주의사항

- **실제 비밀번호 사용 금지**: 샘플 파일의 비밀번호는 예시용입니다. 실제 환경에서는 반드시 실제 인증 정보로 변경하세요.
- **네트워크 설정**: 호스트명과 포트는 실제 서비스 환경에 맞게 변경하세요.
- **보안 설정**: 프로덕션 환경에서는 적절한 보안 설정을 적용하세요.

## 추가 샘플

다른 서비스의 설정 샘플이 필요하다면 기존 샘플을 참고하여 유사한 구조로 작성할 수 있습니다.
