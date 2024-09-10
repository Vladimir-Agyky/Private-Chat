# Korean & English
Used module : Flask, flask_socketio, flask_sqlalchemy
사용된 모듈 : Flask, flask_socketio, flask_sqlalchemy

# Instruction / 사용법
1. Install modules
1. 모듈을 설치하세요
```
pip install MODULE_NAME
```
<img width="1355" alt="스크린샷 2024-09-10 오전 8 26 26" src="https://github.com/user-attachments/assets/e389bd05-5f93-4704-ab63-cfd579fa5fb0">
2. Edit account infromation "PASSWORD": "USERNAME" <br/>
2. 계정정보 수정 "비밀번호": "닉네임" <br/>
<br/>
3. Set admin <br/>
3. 관리자 설정 <br/>

# In website
<img width="1792" alt="스크린샷 2024-09-10 오전 8 33 52" src="https://github.com/user-attachments/assets/93de78ae-d05e-4172-b07b-c96255fd5b8e">

Only entering "채팅방입장" will let you enter the chatting room

"채팅방입장"을 입력해야만 채팅방으로 넘어갑니다

# Other
Admin can delete all the DB for one click<br/>
관리자는 클릭 한번으로 모든 DB를 삭제할 수 있습니다.<br/>
<br/>
What's in DB : Chatting log(Message, Messaged UTC time, Logged in history(Username, UTC Time)<br/>
DB에 저장되는 목록 : 채팅로그(Message, Messaged UTC time, 로그인 기록(Username, UTC Time)<br/>
<br/>
Making new algorithm to encrypt the db with AES256<br/>
AES256으로 암호화되는 DB 알고리즘 적용중
