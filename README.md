# kosaf-auto-opener

평일 요일별 지정된 퇴근 시간 및 22시 정각에 한국장학재단 출근 페이지를 자동으로 띄워주는 Mac용 파이썬 스크립트입니다. 지정된 퇴근 시간 외에도 22시에는 무조건 한 번 더 알림 창을 띄워 출근부 작성을 잊지 않도록 이중으로 방지합니다.

---

## ⚙️ 사전 준비: macOS 전체 디스크 접근 권한 설정

macOS의 보안 정책으로 인해, 터미널(Terminal)과 스케줄러(cron)가 백그라운드에서 정상적으로 웹 브라우저를 팝업 하려면 권한 허용이 필수입니다.

1. `시스템 설정` → `개인정보 보호 및 보안` → `전체 디스크 접근 권한`으로 이동합니다.
2. 목록에서 **터미널.app(Terminal)**을 찾아 우측 스위치를 파란색(켬)으로 활성화합니다.
3. 만약 터미널이 목록에 없다면 하단의 `+` 버튼을 눌러 `응용 프로그램` → `유틸리티` → `터미널`을 직접 찾아 추가해 줍니다.

## 🚀 Step 1. 파이썬 코드 설정

본인의 요일별 퇴근 시간에 맞춰 스크립트 내부의 시간을 세팅합니다.

1. 파일을 다운로드하거나 레포지토리를 클론하여 맥북 내 원하는 경로에 배치합니다.
* 기본 예시 경로: `/Users/jinius36/Documents/GitHub/kosaf-auto-opener/open_kosaf.py`


2. 텍스트 편집기나 IDE로 `open_kosaf.py` 파일을 열고, `schedule` 딕셔너리의 숫자를 본인의 실제 퇴근 시간(시)에 맞게 수정합니다.

```python
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
    
    # 오늘이 평일인지 확인
    if weekday in schedule:
        # 1. 현재 시간이 딕셔너리에 설정된 퇴근 시간이거나
        # 2. 무조건 실행해야 하는 22시 정각일 경우
        if current_hour == schedule[weekday] or current_hour == 22:
            url = "https://anyid.kosaf.go.kr/view/login.jsp?#/"
            webbrowser.open(url)
            
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

```

## ⏰ Step 2. 스케줄러(crontab) 설정

월요일 → 금요일 10시부터 22시 사이의 **매시간 정각(0분)**에 파이썬 코드가 깨어나 조건을 확인합니다.

1. 맥북에서 **터미널(Terminal)** 앱을 실행합니다.
2. 기존에 잘못 등록된 스케줄을 초기화하고 싶다면 `crontab -r`을 입력하여 삭제합니다.
3. 터미널에 `crontab -e`를 입력하고 엔터를 칩니다. (Vim 에디터가 열립니다.)
4. 키보드에서 영문 `i` 키를 누릅니다. (화면 하단에 `-- INSERT --`라고 표시되며 입력 모드로 바뀝니다.)
5. 아래 내용을 복사하여 붙여넣습니다.
*(주의: `/Users/jinius36/...` 부분은 실제 파이썬 파일이 저장된 본인의 절대 경로로 수정해야 합니다!)*
```bash
0 10-22 * * 1-5 /usr/bin/python3 /Users/jinius36/Documents/GitHub/kosaf-auto-opener/open_kosaf.py

```


* **의미:** `0`(매 정각 0분) `10-22`(10시부터 22시 사이) `*`(매일) `*`(매월) `1-5`(월요일 → 금요일)에 파이썬 스크립트를 실행하라는 뜻입니다.


6. 작성이 끝났으면 `esc` 키를 눌러 입력 모드를 종료합니다.
7. `:wq`를 입력하고 엔터를 치면 설정이 저장되고 에디터에서 빠져나옵니다. 설정 완료!

---