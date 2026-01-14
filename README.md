# 공유 캘린더

## 필요한 라이브러리 (Python)

- flask
- flask-bcrypt
- flask-login
- flask-sqlalchemy
- python-dotenv

## 로컬 서버 실행 방법

1. cmd에서 루트 디렉토리로 이동
2. `py -m flask run` 실행

## URL별 기능

- /: 홈페이지
- /register: 회원가입
- /login: 로그인
- /logout: 로그아웃 (/으로 리다이렉트)
- /group/1: 1번 그룹 (다른 수도 가능)
- /create: 그룹 생성
- /my: 마이 페이지 (소속된 그룹 보여줌)
