import webbrowser
from datetime import datetime
import logging
import os
import time  # 1분 대기를 위해 time 모듈 추가

def setup_logger():
    # 1. 로그 폴더 경로 설정 ('logs' 폴더)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    log_dir = os.path.join(base_dir, 'logs')

    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # 2. 오늘 날짜를 활용한 로그 파일 이름 생성 (예: 2026-03-23_opener.log)
    current_date = datetime.now().strftime("%Y-%m-%d")
    log_file_name = f"{current_date}_opener.log"
    log_file_path = os.path.join(log_dir, log_file_name)

    # 3. 로깅 설정
    logging.basicConfig(
        filename=log_file_path,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        encoding='utf-8',
        force=True 
    )

def open_website():
    # 실행 시마다 날짜를 확인하고 로거를 세팅합니다.
    setup_logger()
    
    # [디버깅 코드]
    DEBUG_MODE = False  # 디버깅 모드 활성화 여부 (True로 설정하면 5초 대기 후 웹페이지를 엽니다)
    
    if DEBUG_MODE:
        logging.info("디버깅 모드가 켜져 있습니다. 5초 뒤에 웹페이지를 실행합니다.")
        print("디버깅 모드 작동 중: 5초 뒤에 웹페이지가 열립니다...")
        
        time.sleep(5)  # 60초 → 5초로 수정
        
        url = "https://anyid.kosaf.go.kr/view/login.jsp?#/"
        try:
            webbrowser.open(url)
            logging.info("디버깅 모드: 5초 대기 후 웹페이지를 성공적으로 열었습니다.")
        except Exception as e:
            logging.error(f"디버깅 모드에서 웹페이지를 여는 중 오류 발생: {e}")
            print(f"오류 발생: {e}")
            
        return  # 디버깅 실행이 끝났으므로, 아래의 원래 스케줄 로직은 무시하고 함수를 종료합니다.
    # ---------------------------------
    
    # 요일별 퇴근 시간 설정 (0: 월, 1: 화, 2: 수, 3: 목, 4: 금)
    schedule = {
        0: 22, # 월요일
        1: 15, # 화요일
        2: 18, # 수요일
        3: 22, # 목요일
        4: 17  # 금요일
    }
    
    now = datetime.now()
    weekday = now.weekday()
    current_hour = now.hour
    
    # 스크립트가 호출되었는지 자체를 확인하기 위한 기본 로그
    logging.info(f"스크립트 실행됨 - 요일 인덱스: {weekday}, 현재 시간: {current_hour}시")
    
    # 오늘이 평일인지 먼저 확인
    if weekday in schedule:
        # 1. 현재 시간이 딕셔너리에 설정된 퇴근 시간이거나
        # 2. 혹은 무조건 실행해야 하는 22시 정각일 경우
        if current_hour == schedule[weekday] or current_hour == 22:
            url = "https://anyid.kosaf.go.kr/view/login.jsp?#/"
            
            try:
                webbrowser.open(url)
                
                # 상황에 맞게 로그 메시지 세분화
                if current_hour == schedule[weekday] and current_hour == 22:
                    logging.info("퇴근 시간(22시)이자 기본 알림 시간입니다. 웹페이지를 엽니다.")
                elif current_hour == schedule[weekday]:
                    logging.info(f"등록된 퇴근 시간({schedule[weekday]}시)입니다. 웹페이지를 엽니다.")
                elif current_hour == 22:
                    logging.info("무조건 실행되는 22시입니다. 웹페이지를 엽니다.")
                    
            except Exception as e:
                logging.error(f"웹페이지를 여는 중 오류 발생: {e}")
        else:
            logging.info(f"설정된 시간({schedule[weekday]}시 또는 22시)이 아닙니다. 그냥 종료합니다.")
    else:
        logging.info("주말이므로 실행하지 않습니다.")

if __name__ == "__main__":
    open_website()