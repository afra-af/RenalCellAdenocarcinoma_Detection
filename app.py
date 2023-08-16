     #This line imports the necessary modules from the Flask framework. Flask is used to create the Flask application, render_template is used to render HTML templates, 
     # redirect and url_for are used for URL redirection, and request is used to handle HTTP requests.
from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy #an interface to interact with databases.
from datetime import datetime 




import numpy as np
import pickle # to convert objects in binary form



app = Flask(__name__) #This line creates a Flask application instance.
#This code loads a pre-trained machine learning model from a file named 'Kidney.pkl'.
# open('Kidney.pkl', 'rb') opens the file in binary mode ('rb') for reading.
model = pickle.load(open('Kidney.pkl', 'rb')) 
# config mysql with flask application
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/contact'
db=SQLAlchemy(app)  #  This allows the Flask application to interact with the MySQL database using SQLAlchemy,

class Contacts(db.Model): #contact database model 
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80),  nullable=False)
    email = db.Column(db.String(20), nullable=False)
    number = db.Column(db.String(12),  nullable=False)
    message = db.Column(db.String(120),  nullable=False)
    date = db.Column(db.String(12), nullable=True)

class Appointment(db.Model):  # appointment database model
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80),  nullable=False)
    phone_num = db.Column(db.String(12),  nullable=False)
    symptoms = db.Column(db.String(120),  nullable=False)
    date = db.Column(db.String(12), nullable=False)
    time= db.Column(db.String(12), nullable=False)



#route function with url and https methos 
@app.route('/',methods=['GET']) # it maps the root URL of the application to the function home().
def home(): # executed when the root URL is accessed with the GET method.
    return render_template('index.html')

#The use of both "GET" and "POST" methods in the route definition allows the route to handle both HTTP GET requests (retrieving data or rendering forms) and HTTP POST requests (submitting form data or performing actions). The specific behavior and implementation details will depend on the code inside the associated function.
@app.route('/index',methods=['GET','POST'])

# will get executed when we access index page
def index():
    if(request.method=='POST'):
        name=request.form.get('name') # fields retrived from the submitted form
        phone=request.form.get('phone')
        symptom=request.form.get('symptom')
        date = request.form.get('date')
        time = request.form.get('time')
        entry = Appointment(name=name, phone_num=phone,symptoms=symptom,date=date,time=time)
        db.session.add(entry)
        db.session.commit()
    
    return render_template('index.html')
    

@app.route('/contact',methods=['GET', 'POST'])
def contact():
    
    if(request.method=='POST'):
        name=request.form.get('name')
        email=request.form.get('email')
        phone=request.form.get('phone')
        message=request.form.get('message')
        entry = Contacts(name=name, number=phone,message=message,date=datetime.now(),email=email)
        db.session.add(entry)
        db.session.commit()
        
    return render_template('contact.html')

@app.route('/contactres',methods=['GET', 'POST'])
def contactresult():
    
    if(request.method=='POST'):
        name=request.form.get('name')
        email=request.form.get('email')
        phone=request.form.get('phone')
        message=request.form.get('message')
        entry = Contacts(name=name, number=phone,message=message,date=datetime.now(),email=email)
        db.session.add(entry)
        db.session.commit()
        
    return render_template('contactresult.html')


@app.route('/about',methods=['GET'])
def about():
    return render_template('about.html')


@app.route('/form_login',methods=['GET','POST'])
def form():
    title= "Thank You!"
    if(request.method=='POST'):
        name=request.form.get('name')
        phone=request.form.get('phone')
        symptom=request.form.get('symptom')
        date = request.form.get('date')
        time = request.form.get('time')
        entry = Appointment(name=name, phone_num=phone,symptoms=symptom,date=date,time=time)
        db.session.add(entry)
        db.session.commit()
    
    return render_template('form.html', title=title)


#defines a Flask route for handling form submissions on the "/predict" URL. 
# When a form is submitted with a POST request, the form field values are extracted, a prediction is made using the pre-trained model, and the result is rendered in the "result.html" template.
@app.route("/predict", methods=['POST'])
def predict():
    if request.method == 'POST':
        sg = float(request.form['sg'])
        htn = float(request.form['htn'])
        hemo = float(request.form['hemo'])
        dm = float(request.form['dm'])
        al = float(request.form['al'])
        appet = float(request.form['appet'])
        rc = float(request.form['rc'])
        pc = float(request.form['pc'])

        values = np.array([[sg, htn, hemo, dm, al, appet, rc, pc]])
        prediction = model.predict(values)

        return render_template('result.html', prediction=prediction)


if __name__ == "__main__":
    app.run(debug=True) # argument enables debugging features and provides more detailed error messages if any issues occur.

