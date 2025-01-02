from flask_sqlalchemy import SQLAlchemy 
from app import db
from datetime import datetime

class Admin(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(80),unique=True,nullable=False)
    password=db.Column(db.String(80),nullable=False)

class ServiceProfessional(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(80),unique=True,nullable=False)
    password=db.Column(db.String(80),nullable=False)
    fullname=db.Column(db.String(80),nullable=False)
    service_type=db.Column(db.String(120),nullable=False)
    experience=db.Column(db.String(120),nullable=False)
    phone_number=db.Column(db.String(120),nullable=False)
    address=db.Column(db.String(120),nullable=False)
    pincode=db.Column(db.String(6),nullable=False)
    flagged=db.Column(db.Boolean,default=False)
    requests=db.relationship('ServiceRequest',backref='professional',lazy=True)
    document=db.Column(db.String(120),nullable=False)
    verification_status=db.Column(db.String(120),default='pending')
    
class Customer(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(80),unique=True,nullable=False)
    password=db.Column(db.String(80),nullable=False)
    full_name=db.Column(db.String(120),nullable=False)
    phone_number=db.Column(db.String(120),nullable=False)
    address=db.Column(db.String(120),nullable=False)
    pincode=db.Column(db.String(6),nullable=False)
    flagged=db.Column(db.Boolean,default=False)
    latitude=db.Column(db.Float,nullable=False)
    longitude=db.Column(db.Float,nullable=False)

class Service(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    professinal_id=db.Column(db.Integer,db.ForeignKey('service_professional.id'),nullable=False)
    name=db.Column(db.String(120),nullable=False)
    price=db.Column(db.Float,nullable=False)
    service_type=db.Column(db.String(50),nullable=False)
    time_required=db.Column(db.String(120),nullable=False)
    description=db.Column(db.Text,nullable=True)
    professional=db.relationship('ServiceProfessional',backref='services')

class BookedServiceRequest(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    package_id=db.Column(db.Integer,db.ForeignKey('service.id'),nullable=False)
    customer_id=db.Column(db.Integer,db.ForeignKey('customer.id'),nullable=False)
    customer_name=db.Column(db.String(100),nullable=False)
    professional_id=db.Column(db.Integer,db.ForeignKey('service_professional.id'),nullable=True)
    package_name=db.Column(db.String(100),nullable=False)
    status=db.Column(db.String(50),default='pending',nullable=True)
    remarks=db.Column(db.Text,nullable=True)
    rating=db.Column(db.Integer,nullable=True)
    date_of_request=db.Column(db.Date,nullable=False)
    date_of_completion=db.Column(db.Date,nullable=True)
    service=db.relationship('Service',backref='booked_requests',lazy=True)
    customer=db.relationship('Customer',backref='booked_requests',lazy=True)
    professional=db.relationship('ServiceProfessional',backref='booked_requests',lazy=True)
    complaint=db.Column(db.Text,nullable=True)
    is_complaint=db.Column(db.Boolean,nullable=True)

class ServiceRequest(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    customer_id=db.Column(db.Integer,db.ForeignKey('customer.id'),nullable=False)
    professional_id=db.Column(db.Integer,db.ForeignKey('service_professional.id'),nullable=False)
    date_of_request=db.Column(db.Date,nullable=False)
    date_of_completion=db.Column(db.Date,nullable=True)
    service_status=db.Column(db.String(10),nullable=False,default='requested')
    remarks=db.Column(db.Text,nullable=True)
    description=db.Column(db.Text,nullable=True)
    price=db.Column(db.Float,nullable=True)
    rating=db.Column(db.Integer,nullable=True)
    customer=db.relationship('Customer',backref='service_requests',lazy=True)
    complaint=db.Column(db.Text,nullable=True)
    is_complaint=db.Column(db.Boolean,nullable=True)

class AdminServicePackage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    base_price = db.Column(db.Float, nullable=False)
    time_required = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=True)
    service_type = db.Column(db.String(50), nullable=False)
    service_professional_id = db.Column(db.Integer, db.ForeignKey('service_professional.id'), nullable=False)
    service_professional = db.relationship('ServiceProfessional', backref='admin_service_packages')

    booked_packages=db.relationship('BookedAdminServicePackage',backref='package',cascade="all, delete-orphan",passive_deletes=True)

class BookedAdminServicePackage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    package_id = db.Column(db.Integer, db.ForeignKey('admin_service_package.id',ondelete='CASCADE'),nullable=True)
    date_of_request = db.Column(db.Date,nullable=True)
    date_of_completion = db.Column(db.Date, nullable=True)
    status=db.Column(db.String(50),default='pending',nullable=True)
    remarks=db.Column(db.Text,nullable=True)
    rating=db.Column(db.Integer,nullable=True)
    
    service_professional_id = db.Column(db.Integer, db.ForeignKey('service_professional.id'), nullable=False)
    customer = db.relationship('Customer', backref='booked_admin_service_packages', lazy=True)
    
    professional = db.relationship(
        'ServiceProfessional',
        primaryjoin="ServiceProfessional.id == BookedAdminServicePackage.service_professional_id",
        backref='booked_admin_service_packages'
    )

    complaint=db.Column(db.Text,nullable=True)
    is_complaint=db.Column(db.Boolean,nullable=True)






    



