"""
MariaDB 연결 및 활용 예시
Redis KeyVault에서 mariadb 설정을 불러와 사용하는 샘플
"""

import sys
import os

# 상위 디렉토리의 redis_keyvault 모듈 import
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from redis_keyvault import get_info

try:
    import mysql.connector
    from mysql.connector import Error
except ImportError:
    print("mysql-connector-python 패키지가 설치되지 않았습니다.")
    print("설치: pip install mysql-connector-python")
    sys.exit(1)


def get_mariadb_connection():
    """Redis KeyVault에서 MariaDB 설정을 가져와 연결 생성"""
    try:
        # Redis KeyVault에서 설정 조회
        config = get_info("mariadb")
        if not config:
            raise Exception("MariaDB 설정을 찾을 수 없습니다.")
        
        print(f"MariaDB 연결 정보:")
        print(f"- 호스트: {config['hostname']}:{config['port']}")
        print(f"- 데이터베이스: {config['database']}")
        print(f"- 사용자: {config['username']}")
        print(f"- SSL: {config['ssl']}")
        
        # MariaDB 연결 생성
        connection = mysql.connector.connect(
            host=config['hostname'],
            port=config['port'],
            database=config['database'],
            user=config['username'],
            password=config['password'],
            charset=config['charset'],
            #use_ssl=config['ssl'],
            connection_timeout=config['timeout']
        )
        
        return connection, config
        
    except Error as e:
        print(f"MariaDB 연결 실패: {e}")
        return None, None
    except Exception as e:
        print(f"설정 로드 실패: {e}")
        return None, None


def test_mariadb_connection():
    """MariaDB 연결 테스트"""
    connection, config = get_mariadb_connection()
    if not connection:
        return False
        
    try:
        cursor = connection.cursor()
        
        # 서버 정보 조회
        cursor.execute("SELECT VERSION()")
        version = cursor.fetchone()
        print(f"\nMariaDB 버전: {version[0]}")
        
        # 현재 데이터베이스 확인
        cursor.execute("SELECT DATABASE()")
        database = cursor.fetchone()
        print(f"현재 데이터베이스: {database[0]}")
        
        # 연결 상태 확인
        if connection.is_connected():
            print("연결 상태: 정상")
            return True
        else:
            print("연결 상태: 비정상")
            return False
            
    except Error as e:
        print(f"MariaDB 연결 테스트 실패: {e}")
        return False
    finally:
        if cursor:
            cursor.close()


def sample_database_operations():
    """데이터베이스 조작 샘플"""
    connection, config = get_mariadb_connection()
    if not connection:
        return
        
    cursor = None
    try:
        cursor = connection.cursor()
        
        # 샘플 테이블 생성
        create_table_query = """
        CREATE TABLE IF NOT EXISTS redis_keyvault_demo (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        cursor.execute(create_table_query)
        print("\n샘플 테이블 생성 완료")
        
        # 샘플 데이터 삽입
        insert_query = """
        INSERT INTO redis_keyvault_demo (name, email) 
        VALUES (%s, %s)
        """
        sample_data = [
            ("Redis KeyVault User", "user@example.com"),
            ("Demo User", "demo@example.com")
        ]
        
        cursor.executemany(insert_query, sample_data)
        connection.commit()
        print(f"샘플 데이터 {cursor.rowcount}개 삽입 완료")
        
        # 데이터 조회
        select_query = "SELECT * FROM redis_keyvault_demo ORDER BY id DESC LIMIT 5"
        cursor.execute(select_query)
        results = cursor.fetchall()
        
        print("\n최근 데이터 조회 결과:")
        for row in results:
            print(f"- ID: {row[0]}, 이름: {row[1]}, 이메일: {row[2]}, 생성일: {row[3]}")
        
        # 테이블 정보 조회
        cursor.execute("SHOW TABLE STATUS LIKE 'redis_keyvault_demo'")
        table_info = cursor.fetchone()
        if table_info:
            print(f"\n테이블 정보:")
            print(f"- 레코드 수: {table_info[4]}")
            print(f"- 데이터 크기: {table_info[6]} bytes")
        
    except Error as e:
        print(f"데이터베이스 조작 실패: {e}")
        if connection:
            connection.rollback()
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()


def cleanup_demo_data():
    """데모 데이터 정리"""
    connection, config = get_mariadb_connection()
    if not connection:
        return
        
    cursor = None
    try:
        cursor = connection.cursor()
        
        # 데모 테이블 삭제
        cursor.execute("DROP TABLE IF EXISTS redis_keyvault_demo")
        connection.commit()
        print("\n데모 테이블 정리 완료")
        
    except Error as e:
        print(f"데이터 정리 실패: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()


if __name__ == "__main__":
    print("=== MariaDB 연결 예시 ===")
    print("Redis KeyVault에서 설정을 불러와 MariaDB에 연결합니다.\n")
    
    # 연결 테스트
    if test_mariadb_connection():
        print("\n=== 데이터베이스 조작 예시 ===")
        sample_database_operations()
        
        # 정리 여부 확인
        cleanup = input("\n데모 데이터를 정리하시겠습니까? (y/N): ").lower()
        if cleanup == 'y':
            cleanup_demo_data()
    else:
        print("MariaDB 연결에 실패했습니다.")
        print("\n확인사항:")
        print("1. Redis KeyVault에 mariadb 설정이 저장되어 있는지 확인")
        print("2. MariaDB 서버가 실행 중인지 확인")
        print("3. 네트워크 연결 및 인증 정보 확인")
