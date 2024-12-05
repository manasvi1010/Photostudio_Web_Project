from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///studio.db"  # Corrected URI key
db = SQLAlchemy(app)

class Studio(db.Model):
    sno = db.Column(db.Integer, primary_key=True)  # Corrected to primary_key
    Name = db.Column(db.String(50), nullable=False)
    Email = db.Column(db.String(50), nullable=False)
    Phone = db.Column(db.Integer, nullable=False)
    Message = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self,Name,Email,Phone,Message):
        self.Name=Name
        self.Email=Email
        self.Phone=Phone
        self.Message=Message
        
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/portfolio/<category>')
def portfolio(category):
    if category == 'portraits':
        return render_template('portraits.html')
    elif category == 'weddings':
        return render_template('weddings.html')
    elif category == 'fashions':
        return render_template('fashions.html')
    else:
        return "Portfolio not found", 404

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        Name = request.form['Name']
        Email = request.form['Email']
        Phone = request.form['Phone']
        Message = request.form['Message']
        #print(Name,Email,Phone,Message)
        data=Studio(Name,Email,Phone,Message)
        db.session.add(data)
        db.session.commit()
        return render_template('contact.html', message ='Thanks for your enquiry. We will connect with you shortly')

if __name__ == '__main__':

    with app.app_context():
        db.create_all()  
    app.run(debug=True)