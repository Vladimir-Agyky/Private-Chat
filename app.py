from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, send
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'secret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

socketio = SocketIO(app)
db = SQLAlchemy(app)

# 메시지 모델 정의
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    message = db.Column(db.String(200), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# 로그인 시간 기록을 위한 모델 정의
class UserLogin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    login_time = db.Column(db.DateTime, default=datetime.utcnow)

# 비밀번호와 닉네임 설정
users = {
    "1234": "Test", #Set Password, Username
    "1111": "Admin" #If you want to add, just add a line with a comma
}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        password = request.form['password']
        if password in users:
            session['username'] = users[password]
            if password == '1111': #Set Admin by password
                session['admin'] = True
            else:
                session['admin'] = False

            # 로그인 시간 기록
            new_login = UserLogin(username=session['username'])
            db.session.add(new_login)
            db.session.commit()

            return redirect(url_for('chat'))
        else:
            return "비밀번호가 잘못되었습니다."
    return render_template('index.html')

@app.route('/chat')
def chat():
    if 'username' not in session:
        return redirect(url_for('index'))

    # DB에서 모든 메시지 불러오기
    messages = Message.query.all()

    return render_template('chat.html', username=session['username'], admin=session.get('admin', False), messages=messages)

@app.route('/loginhistory')
def loginhistory():
    if 'username' not in session or not session.get('admin', False):
        return redirect(url_for('index'))

    # DB에서 모든 로그인 기록 불러오기
    logins = UserLogin.query.all()

    return render_template('loginhistory.html', logins=logins)

@app.route('/delete_all', methods=['POST'])
def delete_all():
    if 'username' not in session or not session.get('admin', False):
        return redirect(url_for('index'))

    # DB의 모든 메시지와 로그인 기록 삭제
    Message.query.delete()
    UserLogin.query.delete()
    db.session.commit()

    return redirect(url_for('index'))

@socketio.on('message')
def handleMessage(msg):
    username = session['username']
    timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M')

    # 메시지를 DB에 저장
    new_message = Message(username=username, message=msg, timestamp=datetime.utcnow())
    db.session.add(new_message)
    db.session.commit()

    # 모든 사용자에게 메시지 브로드캐스트
    send({'message': msg, 'username': username, 'timestamp': timestamp}, broadcast=True)

if __name__ == '__main__':
    # 앱 컨텍스트 내에서 DB 테이블 생성
    with app.app_context():
        db.create_all()

    # 소켓 서버 실행
    socketio.run(app, host='0.0.0.0', port=80)