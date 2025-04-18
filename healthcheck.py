import os
import time
import requests
from loguru import logger

# 환경 변수로부터 설정 불러오기
CHECK_URL = os.getenv("CHECK_URL")
PING_URL = os.getenv("PING_URL")
CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", 60))


def send_ping():
    if PING_URL:
        try:
            response = requests.get(PING_URL)
            response.raise_for_status()
        except requests.RequestException as e:
            logger.error(f"Ping 전송 실패: {e}")


def check_health():
    try:
        response = requests.get(CHECK_URL, timeout=10)
        if response.status_code != 200:
            raise Exception(f"상태 코드 {response.status_code}")
        send_ping()
    except Exception as e:
        logger.error(f"서비스 장애 감지됨: {CHECK_URL} 응답 오류 {e}")


if __name__ == "__main__":
    logger.info("Healthcheck started")
    while True:
        check_health()
        time.sleep(CHECK_INTERVAL)
