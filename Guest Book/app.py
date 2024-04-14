from flask import Flask,render_template,request,session
from pymongo import MongoClient
import boto3

comp = boto3.client('comprehend')

cluster=MongoClient('mongodb+srv://Siva:paruocd05@cluster0.6niahge.mongodb.net/')
db=cluster['guestbook']
coll=db['users']
feedbacks=db['feedbacks']
hotels=db['hotels']
app=Flask(__name__) 
app.secret_key='50000'

@app.route('/')
def home():
    return render_template('mainpage.html')

@app.route('/userreg')
def loadReg():
    return render_template('userRegister.html')

@app.route('/hotreg')
def loadReg1():
    return render_template('hotelregister.html')

@app.route('/userlog')
def log():
    return render_template('userLogin.html')

@app.route('/hotlog')
def hlog():
    return render_template('hotellogin.html')

@app.route('/register',methods=['post','get'])
def register():
    username=request.form['username']
    mail=request.form['email']
    password=request.form['password']
    confirmpass=request.form['cpassword']
    k={}
    k['username']=username
    k['email']=mail
    k['password']=password
    k['confirmpass']=confirmpass 
    res=coll.find()
    for data in res:
        x=dict(data)
        if(x['username']==username):
            return render_template('userRegister.html',res='Username already exists')
        if(x['email']==mail):
         return render_template('userRegister.html',res='Email already exists')
        if(password!=confirmpass):
            return render_template('userRegister.html',res='Passwords do not match')
        if(len(password)<8):
            return render_template('userRegister.html',res='Password should have atlest 8 characters')           
    else:
        coll.insert_one(k)
        return render_template('userRegister.html',res='Registration successful')
    
@app.route('/hotregister',methods=['post','get'])
def hotregister():
    username=request.form['username']
    mail=request.form['email']
    password=request.form['password']
    confirmpass=request.form['cpassword']
    k={}
    k['username']=username
    k['email']=mail
    k['password']=password
    k['confirmpass']=confirmpass 
    res=hotels.find()
    for data in res:
        x=dict(data)
        if(x['username']==username):
            return render_template('hotelregister.html',res='Username already exists')
        if(x['email']==mail):
         return render_template('hotelregister.html',res='Email already exists')
        if(password!=confirmpass):
            return render_template('hotelregister.html',res='Passwords do not match')
        if(len(password)<8):
            return render_template('hotelregister.html',res='Password should have atlest 8 characters')           
    else:
        hotels.insert_one(k)
        return render_template('hotelregister.html',res='Registration successful')

@app.route('/login',methods=['post'])
def login():
    username=request.form['username']
    password=request.form['password']
    session['name']=username
    data=coll.find_one({'username':username})
    if data and data['password']==password:
        return render_template('indexes.html')
    else:
        return render_template('userLogin.html',res="User does not exist or Incorrect credentials")
    
    
@app.route('/hotlogin',methods=['post'])
def hlogin():
    username=request.form['username']
    password=request.form['password']
    session['hotel']=username
    data=hotels.find_one({'username':username})
    if data and data['password']==password:
        return render_template('index.html')
    else:
        return render_template('hotellogin.html',status="User does not exist or Incorrect credentials")


@app.route('/feedback',methods=['get','post'])
def feedback():
    hotel=request.form['hotel']
    text = request.form['feedback']
    res = comp.detect_sentiment(Text=text,LanguageCode='en')
    sentiment = res['Sentiment']
    data=hotels.find()
    feedbacks.insert_one({"hotelname":hotel,"text":text,"result":sentiment,"by":session['name']})
    return render_template('feedback.html',status="Feedback submitted successfully",hotels=data)


@app.route('/userfeedbacks')
def userfed():
    data=feedbacks.find({"by":session['name']})
    return render_template('userfeedbacks.html',data=data)

@app.route('/hotelfeedbacks')
def hotfed():
    data=feedbacks.find({"hotelname":session['hotel']})
    if data:
        print("hii")
    return render_template('hotelfeedbacks.html',data=data)
@app.route('/fed')
def fed():
    data=hotels.find()
    return render_template('feedback.html',hotels=data)
@app.route('/logout')
def logout():
    session['name']=''
    return render_template('guesthome.html')
@app.route('/userhome')
def userhome():
    return render_template('index.html')
@app.route('/hotelhome')
def hotelhome():
    return render_template('hotelindex.html')
@app.route('/guesthome')
def guestHome():
    return render_template('guesthome.html')
@app.route('/about')
def about():
    return render_template('about.html')
@app.route('/hlogout')
def hlog1():
    session['hotel']=''
    return render_template('mainpage.html')
if __name__=="__main__":
    app.run(debug=True)