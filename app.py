from flask import Flask, render_template, Response,request,flash,redirect,url_for,abort
from forms import LoginForm,LivedataForm,SetdataForm,DeleteDateForm
from flask_sqlalchemy import SQLAlchemy
import click
import os,sys
from Hx711 import Hx711
import schedu
from camera_opencv import Camera
from servogo import Servo
app = Flask(__name__)

#下面代码判断是window系统还是linux系统，从而确定数据库URI格式
WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', prefix + os.path.join(app.root_path, 'data.db'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

app.secret_key = os.getenv('SECRET_KEY', 'secret string')
app.config['CKEDITOR_SERVE_LOCAL'] = True
app.config['CKEDITOR_FILE_UPLOADER'] = 'upload_for_ckeditor'

class Data(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    time = db.Column(db.Time)
    qulity = db.Column(db.Integer)

@app.route('/video')
def index():
     return render_template('camera.html')

@app.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        if username == 'student' and password =='123456':
            flash('Welcome home, %s!' % username)
            return redirect(url_for('index'))
        flash('账号或密码错误,请重试！')
    return render_template('login.html', form=form)

@app.route('/livefeed',methods=['GET','POST'])
def livefeed():
    form = DeleteDateForm()
    live = LivedataForm()
    ontime = SetdataForm()
    if live.validate_on_submit():
        qulity = live.qulity.data
        print(qulity)
        schedu.job(qulity=qulity+bar())
        flash('以成功投放')
    date1 = Data.query.all()
    return render_template('fedding.html', live = live, ontime=ontime,datas = date1,form=form)

@app.route('/ontimefeed',methods=['GET','POST'])
def ontimefeed():
    form = DeleteDateForm()
    live = LivedataForm()
    ontime = SetdataForm()
    if ontime.validate_on_submit():
        time = ontime.data.data
        qulity = ontime.qulity.data
        #不加.frist()相当于查询语句，返回的还是关系，故不能直接Data.query.filter(Data.time == time)来判断
        if Data.query.filter(Data.time == time).first():
            flash('此时段的喂养记录已存在，请删除后重新操作')
        else:
            data = Data(time=time,qulity=qulity)
            db.session.add(data)
            db.session.commit()

            flash('已保存数据，稍后投放')
    date2 = Data.query.all()
    return render_template('fedding.html',live = live, ontime=ontime,datas = date2,form=form)

@app.route('/delete/<int:note_id>', methods=['POST'])
def delete_date(note_id):
    form = DeleteDateForm()
    if form.validate_on_submit():
        note = Data.query.get(note_id)
        db.session.delete(note)
        db.session.commit()
        flash('所选信息已删除！')
    else:
        abort(400)
    return redirect(url_for('ontimefeed'))

@app.template_global()
def bar():
    return Hx711().send()

def getdata():
    return Data.query.all()



# os.system('mpg123 '+'./audiofile/aisay.mp3')



def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    # """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/cmd', methods=['GET', 'POST'])
def cmd():
    id = request.form.to_dict()
    Servo(id['value'])
    return "ok"

#重新初始化数据库表
@app.cli.command()
@click.option('--drop', is_flag=True, help='Create after drop.')
def initdb(drop):
    """Initialize the database."""
    if drop:
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.')

if __name__ == '__main__':
    app.run(host='192.168.137.194', port =5000, debug=True, threaded=True)#注意，host就是你的主机ip地址
 #树莓派查看ip地址为:ifconfig,电脑笔记本为:ipconfig
 #port端口树莓派用5000；笔记本用80，这与之后的内网穿透有关