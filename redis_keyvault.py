import os
import sys
import json
from dotenv import load_dotenv, set_key
from cryptography.fernet import Fernet
from redis.sentinel import Sentinel
from pathlib import Path

def create_new_env():
    """새로운 .env 파일 생성을 위한 사용자 입력 처리"""
    print("\n=== Redis Sentinel 설정 정보 입력 ===")
    
    while True:
        try:
            node_count = int(input("\nSentinel 노드 수를 입력하세요 (최소 3개, 홀수): "))
            if node_count < 3 or node_count % 2 == 0:
                print("Sentinel 노드는 최소 3개 이상의 홀수여야 합니다.")
                continue
            break
        except ValueError:
            print("올바른 숫자를 입력하세요.")
    
    try:
        # 공통 설정 정보 입력
        master_name = input("\nSentinel master 이름 (예: redismaster): ").strip()
        socket_timeout = float(input("Socket timeout 값 (예: 1.0): ").strip())
        redis_password = input("Redis 비밀번호: ").strip()
        
        # DB 번호 입력
        while True:
            try:
                redis_db = int(input("Redis DB 번호 (0-15): ").strip())
                if 0 <= redis_db <= 15:
                    break
                print("DB 번호는 0에서 15 사이의 값이어야 합니다.")
            except ValueError:
                print("올바른 숫자를 입력하세요.")
        
        # Fernet 키 생성
        hash_key = Fernet.generate_key()
        cipher = Fernet(hash_key)
        
        # 기본 환경 변수 설정
        env_content = {
            'HASH_KEY': hash_key.decode(),
            'REDIS_SENTINEL_NODE_COUNT': str(node_count),
            'REDIS_SENTINEL_MASTER_NAME': cipher.encrypt(master_name.encode()).decode(),
            'REDIS_SENTINEL_TIMEOUT': cipher.encrypt(str(socket_timeout).encode()).decode(),
            'REDIS_PASSWORD': cipher.encrypt(redis_password.encode()).decode(),
            'REDIS_DB': cipher.encrypt(str(redis_db).encode()).decode()
        }
        
        # 각 노드 정보 개별 저장
        for i in range(node_count):
            print(f"\n=== Sentinel 노드 {i+1} 정보 입력 ===")
            node_info = {
                'hostname': input("Sentinel 호스트명(예: L4, node1): ").strip(),
                'port': int(input("Sentinel 포트 번호: ").strip())
            }
            node_json = json.dumps(node_info)
            encrypted_node = cipher.encrypt(node_json.encode()).decode()
            env_content[f'REDIS_SENTINEL_NODE_{i+1}'] = encrypted_node
        
        # .env 파일 생성
        current_dir = os.path.dirname(os.path.abspath(__file__))
        dotenv_path = os.path.join(current_dir, '.env')
        Path(dotenv_path).touch(exist_ok=True)
        
        for key, value in env_content.items():
            set_key(dotenv_path, key, value)
        
        print("\n.env 파일이 성공적으로 생성되었습니다.")
        return True
        
    except Exception as e:
        print(f"설정 파일 생성 중 오류 발생: {e}")
        return False

def initialize_redis():
    """Redis 연결 초기화"""
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        dotenv_path = os.path.join(current_dir, '.env')
        
        if not os.path.exists(dotenv_path):
            if not create_new_env():
                raise Exception(".env 파일 생성에 실패했습니다.")
        
        load_dotenv(dotenv_path)
        
        hash_key = os.getenv('HASH_KEY')
        if not hash_key:
            raise Exception("암호화 키가 없습니다.")
            
        cipher = Fernet(hash_key.encode())
        
        # 기본 설정 복호화
        node_count = int(os.getenv('REDIS_SENTINEL_NODE_COUNT'))
        master_name = cipher.decrypt(os.getenv('REDIS_SENTINEL_MASTER_NAME').encode()).decode()
        socket_timeout = float(cipher.decrypt(os.getenv('REDIS_SENTINEL_TIMEOUT').encode()).decode())
        redis_password = cipher.decrypt(os.getenv('REDIS_PASSWORD').encode()).decode()
        redis_db = int(cipher.decrypt(os.getenv('REDIS_DB').encode()).decode())
        
        # 각 노드 정보 복호화
        sentinel_hosts = []
        for i in range(1, node_count + 1):
            encrypted_node = os.getenv(f'REDIS_SENTINEL_NODE_{i}')
            if not encrypted_node:
                raise Exception(f"Sentinel 노드 {i} 정보가 없습니다.")
            node_info = json.loads(cipher.decrypt(encrypted_node.encode()).decode())
            sentinel_hosts.append((node_info['hostname'], node_info['port']))
        
        sentinel = Sentinel(sentinel_hosts, socket_timeout=socket_timeout)
        master = sentinel.master_for(
            master_name,
            socket_timeout=socket_timeout,
            password=redis_password,
            db=redis_db
        )
        
        master.ping()
        return cipher, master, redis_db
        
    except Exception as e:
        raise Exception(f"Redis Sentinel 연결 실패: {e}")

def get_redis_connection():
    """Redis 연결 객체 반환"""
    try:
        _, master, _ = initialize_redis()
        return master
    except Exception as e:
        raise Exception(f"Redis connection failed: {e}")

def save_info(key, data):
    """정보 저장"""
    try:
        cipher, master, _ = initialize_redis()
        json_data = json.dumps(data)
        encrypted_data = cipher.encrypt(json_data.encode())
        master.set(f"info:{key}", encrypted_data)
        print(f"데이터가 성공적으로 저장되었습니다. (키: info:{key})")
        return True
    except Exception as e:
        print(f"데이터 저장 실패: {e}")
        sys.exit(1)

def get_info(key):
    """저장된 정보 조회"""
    try:
        cipher, master, _ = initialize_redis()
        encrypted_data = master.get(f"info:{key}")
        if encrypted_data:
            decrypted_data = cipher.decrypt(encrypted_data).decode()
            return json.loads(decrypted_data)
        print(f"키에 해당하는 데이터를 찾을 수 없습니다: info:{key}")
        return None
    except Exception as e:
        print(f"데이터 조회 실패: {e}")
        return None

if __name__ == "__main__":
    # 스크립트가 직접 실행될 때만 실행
    current_dir = os.path.dirname(os.path.abspath(__file__))
    dotenv_path = os.path.join(current_dir, '.env')
    
    # .env 파일이 없는 경우
    if not os.path.exists(dotenv_path):
        print("\n.env 파일이 존재하지 않습니다.")
        if create_new_env():
            print("\n이제 아래 명령어를 사용할 수 있습니다:")
            print("  python redis_keyvault.py save <json_파일>")
            print("  python redis_keyvault.py get <키>")
        sys.exit(0)
    
    # 명령행 인수 처리
    if len(sys.argv) != 3:
        print("사용법: python redis_keyvault.py <명령어> <키_또는_파일>")
        print("명령어:")
        print("  save <json_파일> : JSON 파일에서 연결 정보 저장")
        print("  get <키>        : 키로 연결 정보 조회 (예: maxscale-sqlmgr)")
        sys.exit(1)

    command = sys.argv[1].lower()
    argument = sys.argv[2]

    if command == "save":
        if not os.path.exists(argument):
            print(f"오류: 파일이 존재하지 않습니다 '{argument}'")
            sys.exit(1)

        try:
            with open(argument, 'r') as f:
                data = json.load(f)
            key_name = os.path.splitext(os.path.basename(argument))[0]
            save_info(key_name, data)
        except json.JSONDecodeError as e:
            print(f"JSON 파일 파싱 오류: {e}")
            sys.exit(1)
        except Exception as e:
            print(f"데이터 저장 중 오류 발생: {e}")
            sys.exit(1)

    elif command == "get":
        try:
            data = get_info(argument)
            if data:
                print(json.dumps(data, indent=4, ensure_ascii=False))
                sys.exit(0)
        except Exception as e:
            print(f"데이터 조회 중 오류 발생: {e}")
            sys.exit(1)

    else:
        print("잘못된 명령어입니다. 'save' 또는 'get'을 사용하세요.")
        sys.exit(1)

