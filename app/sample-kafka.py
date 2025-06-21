"""
Kafka 연결 및 활용 예시
Redis KeyVault에서 kafka 설정을 불러와 사용하는 샘플
"""

import sys
import os
import json
import time
from datetime import datetime

# 상위 디렉토리의 redis_keyvault 모듈 import
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from redis_keyvault import get_info

try:
    from kafka import KafkaProducer, KafkaConsumer
    from kafka.errors import KafkaError
except ImportError:
    print("kafka-python 패키지가 설치되지 않았습니다.")
    print("설치: pip install kafka-python")
    sys.exit(1)


def get_kafka_config():
    """Redis KeyVault에서 Kafka 설정을 가져오기"""
    try:
        # Redis KeyVault에서 설정 조회
        config = get_info("kafka")
        if not config:
            raise Exception("Kafka 설정을 찾을 수 없습니다.")
        
        print(f"Kafka 연결 정보:")
        print(f"- 브로커: {config['hostname']}:{config['port']}")
        print(f"- 토픽: {config['topic']}")
        print(f"- 그룹 ID: {config['group_id']}")
        print(f"- 프로토콜: {config['protocol']}")
        
        return config
        
    except Exception as e:
        print(f"Kafka 설정 로드 실패: {e}")
        return None


def create_kafka_producer():
    """Kafka Producer 생성"""
    config = get_kafka_config()
    if not config:
        return None
        
    try:
        # SSL 설정이 있는 경우
        kafka_config = {
            'bootstrap_servers': [f"{config['hostname']}:{config['port']}"],
            'value_serializer': lambda v: json.dumps(v).encode('utf-8'),
            'key_serializer': lambda v: str(v).encode('utf-8') if v else None
        }
        
        # SSL 및 인증 설정
        if config.get('ssl', False):
            kafka_config.update({
                'security_protocol': config.get('protocol', 'SASL_SSL'),
                'sasl_mechanism': 'PLAIN',
                'sasl_plain_username': config['username'],
                'sasl_plain_password': config['password']
            })
        
        producer = KafkaProducer(**kafka_config)
        return producer, config
        
    except Exception as e:
        print(f"Kafka Producer 생성 실패: {e}")
        return None, None


def create_kafka_consumer():
    """Kafka Consumer 생성"""
    config = get_kafka_config()
    if not config:
        return None
        
    try:
        # SSL 설정이 있는 경우
        kafka_config = {
            'bootstrap_servers': [f"{config['hostname']}:{config['port']}"],
            'group_id': config['group_id'],
            'value_deserializer': lambda v: json.loads(v.decode('utf-8')),
            'key_deserializer': lambda v: v.decode('utf-8') if v else None,
            'auto_offset_reset': 'latest',
            'consumer_timeout_ms': 10000  # 10초 타임아웃
        }
        
        # SSL 및 인증 설정
        if config.get('ssl', False):
            kafka_config.update({
                'security_protocol': config.get('protocol', 'SASL_SSL'),
                'sasl_mechanism': 'PLAIN',
                'sasl_plain_username': config['username'],
                'sasl_plain_password': config['password']
            })
        
        consumer = KafkaConsumer(config['topic'], **kafka_config)
        return consumer, config
        
    except Exception as e:
        print(f"Kafka Consumer 생성 실패: {e}")
        return None, None


def test_kafka_connection():
    """Kafka 연결 테스트"""
    producer, config = create_kafka_producer()
    if not producer:
        return False
        
    try:
        # 간단한 테스트 메시지 전송
        test_message = {
            'type': 'connection_test',
            'timestamp': datetime.now().isoformat(),
            'message': 'Redis KeyVault Kafka connection test'
        }
        
        future = producer.send(config['topic'], value=test_message, key='test')
        result = future.get(timeout=10)  # 10초 타임아웃
        
        print(f"\n연결 테스트 성공:")
        print(f"- 파티션: {result.partition}")
        print(f"- 오프셋: {result.offset}")
        
        producer.close()
        return True
        
    except KafkaError as e:
        print(f"Kafka 연결 테스트 실패: {e}")
        return False
    except Exception as e:
        print(f"연결 테스트 중 오류: {e}")
        return False
    finally:
        if producer:
            producer.close()


def sample_producer_operations():
    """Kafka Producer 샘플 동작"""
    producer, config = create_kafka_producer()
    if not producer:
        return
        
    try:
        print(f"\n=== Producer 샘플 메시지 전송 ===")
        
        # 샘플 메시지들 전송
        sample_messages = [
            {
                'event_type': 'user_login',
                'user_id': 'user123',
                'timestamp': datetime.now().isoformat(),
                'ip': '192.168.1.100',
                'source': 'redis-keyvault-demo'
            },
            {
                'event_type': 'data_update',
                'table': 'users',
                'action': 'UPDATE',
                'timestamp': datetime.now().isoformat(),
                'source': 'redis-keyvault-demo'
            },
            {
                'event_type': 'system_alert',
                'level': 'INFO',
                'message': 'Redis KeyVault demo completed successfully',
                'timestamp': datetime.now().isoformat(),
                'source': 'redis-keyvault-demo'
            }
        ]
        
        for i, message in enumerate(sample_messages, 1):
            future = producer.send(
                config['topic'], 
                value=message, 
                key=f"demo_key_{i}"
            )
            result = future.get(timeout=10)
            print(f"메시지 {i} 전송 완료 - 파티션: {result.partition}, 오프셋: {result.offset}")
            time.sleep(1)  # 1초 간격
        
        producer.flush()  # 모든 메시지 전송 완료 대기
        print(f"\n총 {len(sample_messages)}개 메시지 전송 완료")
        
    except Exception as e:
        print(f"Producer 동작 실패: {e}")
    finally:
        if producer:
            producer.close()


def sample_consumer_operations():
    """Kafka Consumer 샘플 동작"""
    consumer, config = create_kafka_consumer()
    if not consumer:
        return
        
    try:
        print(f"\n=== Consumer 메시지 수신 대기 ===")
        print("10초간 메시지를 수신합니다...")
        
        message_count = 0
        for message in consumer:
            message_count += 1
            print(f"\n메시지 {message_count} 수신:")
            print(f"- 키: {message.key}")
            print(f"- 파티션: {message.partition}")
            print(f"- 오프셋: {message.offset}")
            print(f"- 내용: {message.value}")
            
            # 최대 5개 메시지만 처리
            if message_count >= 5:
                break
        
        if message_count == 0:
            print("수신된 메시지가 없습니다.")
        else:
            print(f"\n총 {message_count}개 메시지 처리 완료")
        
    except Exception as e:
        print(f"Consumer 동작 실패: {e}")
    finally:
        if consumer:
            consumer.close()


if __name__ == "__main__":
    print("=== Kafka 연결 예시 ===")
    print("Redis KeyVault에서 설정을 불러와 Kafka에 연결합니다.\n")
    
    # 연결 테스트
    if test_kafka_connection():
        print("\n=== Producer 예시 ===")
        sample_producer_operations()
        
        print("\n=== Consumer 예시 ===")
        sample_consumer_operations()
    else:
        print("Kafka 연결에 실패했습니다.")
        print("\n확인사항:")
        print("1. Redis KeyVault에 kafka 설정이 저장되어 있는지 확인")
        print("2. Kafka 브로커가 실행 중인지 확인")
        print("3. 네트워크 연결 및 인증 정보 확인")
        print("4. 토픽이 존재하는지 확인")
