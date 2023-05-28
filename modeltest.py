from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique = True)
    sponcer_id = db.Column(db.String(50), unique = True)
    name = db.Column(db.String(100),nullable=False)
    email = db.Column(db.String(120), unique=True,nullable=False)
    password = db.Column(db.String(100),nullable=False)
    contactNo = db.Column(db.String(80),nullable=False)
    country = db.Column(db.String(100))
    state = db.Column(db.String(100))
    district = db.Column(db.String(100))
    city = db.Column(db.String(100))
    pinCode = db.Column(db.Integer)
    nominee = db.Column(db.String(100))
    dateTime = db.Column(db.String(100))
    payments = db.relationship('Payment', backref='users')
    orders = db.relationship('Order', backref='users')

    def __init__(self, public_id,sponcer_id,name, email,password, contactNo,country,state, district,city,pinCode,nominee,dateTime):
        self.public_id = public_id
        self.sponcer_id = sponcer_id
        # self.ref_Id = ref_Id
        self.name = name
        self.email = email
        self.password = password
        self.contactNo = contactNo
        self.country = country
        self.state = state
        self.district = district
        self.city = city
        self.pinCode = pinCode
        self.nominee = nominee
        self.dateTime = dateTime

    def __repr__(self):
        return '%s /%s /%s /%s %s %s %s %s %s %s %s %s %s %s' % (self.id, self.public_id,self.sponcer_id, self.name, self.email,self.password, self.contactNo, self.country,self.state,self.district,self.city,self.pinCode,self.nominee,self.dateTime)
