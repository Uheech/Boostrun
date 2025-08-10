''' 
HTTP
: 파이썬을 이용해 네트워크 자원에 접근하는 방법
- 전송계층: 우리가 속한 계층
- 양방향 프로토콜: 한 컴퓨터가 소켓에 말하면 다른 컴퓨터가 응답
- 소켓: 데이터 전화
- 어떤 서비스/프로세스에 접근할 껀지 
'''
# 소켓 라이브러리 호출
import socket
# 소켓 생성중(바깥쪽으로 연결될 수 있지만 아직 연결되지 않은 상태)
# socket.AF_INET: 소켓을 만들거라고 선언, 인터넷을 통해 나간단 의미
# socket.SOCK_STREAM: 데이터가 블럭 형태로 다뤄지는 게 아니라 연속된 문자의 흐름으로 다뤄짐 
mysock=socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
# 소켓 객체를 가져와서 인터넷을 통해 연결을 만드는 것.
# 인터넷 연결하고 이 호스트에 연결, 포트번호는 80
# host: 전화번호, port: 내선번호 느낌
mysock.connect(('data.pr4e.org', 80))


#2. HTTP를 이용해 서버에 요청 보내기 
'''
각 프로토콜은 하위에서 소켓을 사용, 그 위에 하이퍼텍스트 웹페이지를 위한 도로를 만듬 
- 프로토콜: 전화와서 먼저 이야기하는 사람
> 우리의 역할: 양쪽다 받아들일 수 있게 규칙을 만들어야 함.
ex) URL: 프로토콜을 암호화해 포함하기 시작
'''
'''
<서버로부터 데이터 받기>
1) 사용자가 href=값 을 가지고 있는 앵커 태그를 클릭
2) 새로운 페이지로 이동할 때마다 브라우저는 웹 서버와 연결을 만듬
3) get 요청을 실행해 페이지 URL에 나타난 값을 수신
: 웹서버를 통해 80번 포트로 연결 요청 
4) 서버는 문서를 포맷팅하고 유저에게 보여주는 HTML 문서를 리턴
'''

#3. 파이썬을 이용해 웹브라우저 만들기 

import socket
# 소켓 가져오고 만들기(Stream 기반: 인터넷을 통한 통신에 적합)
mysock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 전화를 거는 것과 비슷함, 해당 호스트의 80번 포트에 연결함
# 소켓을 내보내고 웹서버에 연결함, 여기에서 소프트웨어가 작동하고 있어야함.
mysock.connect(('data.pr4e.org',80))
# 우리가 요청을 보내는 거임
# encode: 인터넷을 통해 나갈 데이터를 준비 (유니코드 >UTF-8)
cmd='GET http://data.pr4e.org/romeo.txt HTTP/1.0\n\n'.encode()
mysock.send(cmd)

while True:
  # 문자 512개를 먼저 받는 것임(매 반복마다)
  data =mysock.reev(512)
  # 문자가 0개 들어오면, 스트리이 끝났단 이야기 
  if (len(data)<1):
    break
  # 데이터는 외부에서 오기 때문에 출력 전에 복호화 필수(UTF-8>유니코드)
  print(data.decode())
  # 소켓 종료 
mysock.close()

'''
Telnet이랑 하는 것과 결과의 차이가 없다. 
'''


# 문자를 표현하는 방법 및 인코딩/디코딩
'''
ASCII: 라틴 문자의 집합
각 문자는 0~256 사이의 숫자로 대응되어 저장됨, 이는 메모리에서 8비트를 차지
8bit=1byte
'''
# ord(): ASCII 문자에 대응되는 숫자를 리턴
# 정렬도 여기서 생김 
print(ord('H')) #72
print(ord('e')) #101

'''
하지만 시대가 변하고 사용하는 문자가 많아지면서 한계에 부딪힘
> 유니코드로까지 진화하게 됨, 유니코드엔 빈공간이 많아 다양한 문자를 포함, 자리 주는 게 가능.
But, 유니코드를 네트워크로 전송할 때 용량이 과도하게 큼 
UTF-32의 경우, 한 글자당 4 byte를 할당함.
> 이걸 압축할 수 있음. UTF-16, UTF-8 같은 걸로
ASCII: 1Byte
UTF-16: 2Byte
UTF-32: 4Byte
UTF-8: 동적으로 1~4Byte로 변환가능.
이제는 거의 UTF-8쓰고 권장됨, UTF-32의 역할도 할 수 있고 압축할 수도 있기 때문 
'''

# 파이썬 내 문자열의 종류
'''
1) python 2: ascii 문자열(Byte와 문자열이 같음)
- 유니코드 쓰고 싶으면 다른 종류의 객체 사용 
- 영어만 알아들음 
2) python 3: 문자열을 유니코드와 같게 만듬
- 파일에서 데이터를 가져와 파이썬에서 작업하는 경우 그냥 작동함
- 하지만 소켓을 통해 네트워크로 데이터를 전송하거나 DB와 연결하는 경우 데이터를 Byte<-> 문자열로 인코딩/디코딩해야함. 
'''

# urllib를 이용해 웹 데이터 읽어오기
'''
이전에는 10줄 정도로 http를 이용해서 웹 브라우저를 만들었지만
urllib을 사용하면 더 간단해짐 
> 연결 만들고 겟 요청 전송, 헤더를 처리하는 등 모든걸 다 함 
'''
# urllib: 파이썬에서 소켓 통신과 http 통신을 편하게 하기 위한 라이브러리
import urllib.request, urllib.parse, urllib.error
# 자동으로 인코딩, get 요청, 연결도 만들고, 응답도 받음.
fhand=urllib.request.urlopen('http://data.pr43.org/romeo.text')
# header 는 볼 수 없음, 원하면 부를 수 있음 
for line in fhand:
  print(line.decode().strip())

# 파일에서 데이터를 읽어왔던 걸 인터넷에서도 데이터를 읽어올 수 있음.
import urllib.request, urllib.parse, urllib.error

fhand = urllib.request.urlopen('http://data.pr4e.org/romeo.txt')

counts = dict()
for line in fhand:
    words = line.decode().split()
    for word in words:
        counts[word] = counts.get(word, 0) + 1
print(counts)

