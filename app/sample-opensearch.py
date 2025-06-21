"""
OpenSearch 연결 및 활용 예시
Redis KeyVault에서 opensearch 설정을 불러와 사용하는 샘플
"""

import sys
import os

# 상위 디렉토리의 redis_keyvault 모듈 import
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from redis_keyvault import get_info

try:
    from opensearchpy import OpenSearch
except ImportError:
    print("opensearch-py 패키지가 설치되지 않았습니다.")
    print("설치: pip install opensearch-py")
    sys.exit(1)


def get_opensearch_client():
    """Redis KeyVault에서 OpenSearch 설정을 가져와 클라이언트 생성"""
    try:
        # Redis KeyVault에서 설정 조회
        config = get_info("opensearch")
        if not config:
            raise Exception("OpenSearch 설정을 찾을 수 없습니다.")
        
        print(f"OpenSearch 연결 정보:")
        print(f"- 호스트: {config['hostname']}:{config['port']}")
        print(f"- 인덱스: {config['index']}")
        print(f"- SSL: {config['ssl']}")
        
        # OpenSearch 클라이언트 생성
        client = OpenSearch(
            hosts=[{'host': config['hostname'], 'port': config['port']}],
            http_auth=(config['username'], config['password']),
            use_ssl=config['ssl'],
            verify_certs=False,  # 개발환경용
            timeout=config['timeout']
        )
        
        return client, config
        
    except Exception as e:
        print(f"OpenSearch 클라이언트 생성 실패: {e}")
        return None, None


def test_opensearch_connection():
    """OpenSearch 연결 테스트"""
    client, config = get_opensearch_client()
    if not client:
        return False
        
    try:
        # 클러스터 정보 조회
        info = client.info()
        print(f"\n클러스터 정보:")
        print(f"- 클러스터명: {info['cluster_name']}")
        print(f"- 버전: {info['version']['number']}")
        
        # 클러스터 상태 확인
        health = client.cluster.health()
        print(f"- 상태: {health['status']}")
        print(f"- 노드 수: {health['number_of_nodes']}")
        
        return True
        
    except Exception as e:
        print(f"OpenSearch 연결 테스트 실패: {e}")
        return False


def sample_index_operations():
    """인덱스 조작 샘플"""
    client, config = get_opensearch_client()
    if not client:
        return
        
    index_name = config['index']
    
    try:
        # 샘플 문서 색인
        sample_doc = {
            'timestamp': '2024-01-01T10:00:00',
            'level': 'INFO',
            'message': 'Sample log message from Redis KeyVault demo',
            'application': 'redis-keyvault-demo',
            'host': 'demo-server'
        }
        
        response = client.index(
            index=index_name,
            body=sample_doc
        )
        print(f"\n문서 색인 성공: {response['_id']}")
        
        # 문서 검색
        search_body = {
            'query': {
                'match': {
                    'application': 'redis-keyvault-demo'
                }
            }
        }
        
        search_response = client.search(
            index=index_name,
            body=search_body
        )
        
        print(f"검색 결과: {search_response['hits']['total']['value']}개 문서 발견")
        
        for hit in search_response['hits']['hits']:
            print(f"- 문서 ID: {hit['_id']}")
            print(f"  메시지: {hit['_source']['message']}")
        
    except Exception as e:
        print(f"인덱스 조작 실패: {e}")


if __name__ == "__main__":
    print("=== OpenSearch 연결 예시 ===")
    print("Redis KeyVault에서 설정을 불러와 OpenSearch에 연결합니다.\n")
    
    # 연결 테스트
    if test_opensearch_connection():
        print("\n=== 인덱스 조작 예시 ===")
        sample_index_operations()
    else:
        print("OpenSearch 연결에 실패했습니다.")
        print("\n확인사항:")
        print("1. Redis KeyVault에 opensearch 설정이 저장되어 있는지 확인")
        print("2. OpenSearch 서버가 실행 중인지 확인")
        print("3. 네트워크 연결 확인")
