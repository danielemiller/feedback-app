from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from send_mail import send_mail

app = Flask(__name__)

ENV = 'prod'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:xihuan1!@localhost/scl_feedback'
else:    
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://ruqbofatierhql:e8e39e149b93b7dcf7d89e104928664422a33e17c47519829c975e651218ace7@ec2-3-222-11-129.compute-1.amazonaws.com:5432/d1u2a70s4vsnpf'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)
    customer = db.Column(db.String(200), unique=True)
    consultant = db.Column(db.String(200))
    rating = db.Column(db.Integer)
    comments = db.Column(db.Text())

    def __init__(self, customer, consultant, rating, comments): 
       self.customer = customer
       self.consultant = consultant
       self.rating = rating
       self.comments = comments 

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        customer = request.form['customer']
        consultant = request.form['consultant']
        rating = request.form['rating']
        comments = request.form['comments']
        #print(customer, consultant, rating, comments)
        if customer == '' or consultant == '':
            return render_template('index.html', message='Please enter required fields')
        if db.session.query(Feedback).filter(Feedback.customer == customer).count() == 0:
            data = Feedback(customer, consultant, rating, comments)
            db.session.add(data)
            db.session.commit()
            send_mail(customer, consultant, rating, comments)
            return render_template('success.html')
        return render_template('index.html', message='You have already submitted feedback')

if __name__ == '__main__':
    app.run()