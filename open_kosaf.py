import webbrowser
from datetime import datetime

def open_website():
    # 요일별 퇴근 시간 설정 (0: 월, 1: 화, 2: 수, 3: 목, 4: 금)
    schedule = {
        0: 22, # 월요일 22시
        1: 20, # 화요일 20시
        2: 18, # 수요일 18시
        3: 22, # 목요일 22시
        4: 17  # 금요일 17시
    }
    
    now = datetime.now()
    weekday = now.weekday()
    current_hour = now.hour
    
    # 오늘이 평일인지 먼저 확인
    if weekday in schedule:
        # 1. 현재 시간이 딕셔너리에 설정된 퇴근 시간이거나
        # 2. 혹은 무조건 실행해야 하는 22시 정각일 경우
        if current_hour == schedule[weekday] or current_hour == 22:
            url = "https://anyid.kosaf.go.kr/view/login.jsp?#/"
            webbrowser.open(url)
            
            # 상황에 맞게 터미널 출력 메시지 세분화
            if current_hour == schedule[weekday] and current_hour == 22:
                print(f"[{now}] 퇴근 시간(22시)이자 기본 알림 시간입니다. 웹페이지를 엽니다.")
            elif current_hour == schedule[weekday]:
                print(f"[{now}] 등록된 퇴근 시간({schedule[weekday]}시)입니다. 웹페이지를 엽니다.")
            elif current_hour == 22:
                print(f"[{now}] 무조건 실행되는 22시입니다. 웹페이지를 엽니다.")
        else:
            print(f"[{now}] 설정된 시간({schedule[weekday]}시 또는 22시)이 아닙니다. 그냥 종료합니다.")
    else:
        print(f"[{now}] 주말이므로 실행하지 않습니다.")

if __name__ == "__main__":
    open_website()