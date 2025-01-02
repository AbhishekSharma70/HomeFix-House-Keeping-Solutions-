from flask import Flask, request, jsonify, render_template,url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS 
import os
from datetime import datetime, timedelta
from flask import send_from_directory
from tasks import send_whatsapp_message_to_professional,send_whatsapp_message
from celery import Celery
from flask_mail import Mail, Message
from sqlalchemy import and_
from io import StringIO
import csv
from flask_jwt_extended import JWTManager,create_access_token,jwt_required,get_jwt_identity 
from functools import wraps
import redis
import json
from celery.schedules import crontab


app = Flask(__name__, static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config.from_object('config.Config')
celery_app=Celery(app.name,broker=app.config['CELERY_BROKER_URL'])
celery_app.conf.update(app.config)
db = SQLAlchemy(app)
CORS(app)
UPLOAD_FOLDER=os.path.join(os.getcwd(),'static','documents')
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER

app.config['MAX_CONTENT_LENGTH']=16*1024*1024
API_KEY='test_e45ce78303de0c5bed58fd60de7b6b2b'
AUTH_TOKEN='test_b7ae1977f197cbe8f35f7205e91f5fb3'

mail=Mail(app)

app.config['JWT_SECRET_KEY']='124$5'
app.config['JWT_ACCESS_TOKEN_EXPIRES']=timedelta(days=10)

jwt=JWTManager(app)

redis_client=redis.StrictRedis(host='localhost',port=6379,db=0,decode_responses=True)
CACHE_TIMEOUT=300


def cache_result(cache_key):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            
            cached_data = redis_client.get(cache_key)
            if cached_data:
                return jsonify(json.loads(cached_data))
            
            
            result = func(*args, **kwargs)
            redis_client.setex(cache_key, CACHE_TIMEOUT, json.dumps(result.get_json()))
            return result
        return wrapper
    return decorator
    



from models import Admin, ServiceProfessional, Customer,ServiceRequest,Service,BookedServiceRequest,AdminServicePackage,BookedAdminServicePackage


@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/admin_login1')
def admin_login1():
    return render_template('admin_login.html')

@app.route('/service_professional_login1')
def service_professional_login1():
    return render_template('service_professional_login.html')

@app.route('/customer_login1')
def customer_login1():
    return render_template('customer_login.html')

@app.route('/admin_signup1')
def admin_signup1():
    return render_template('admin_signup.html')

@app.route('/service_professional_signup1')
def service_professional_signup1():
    return render_template('service_professional_signup.html')

@app.route('/customer_signup1')
def customer_signup1():
    return render_template('customer_signup.html')


@app.route('/api/admin_signup', methods=['POST'])
def admin_signup():
    data = request.get_json()
    username = data['username']
    password = data['password']

    existing_admin = Admin.query.filter_by(username=username).first()
    if existing_admin:
        return jsonify({"message": "Username already exists!"}), 400
    
    new_admin = Admin(username=username, password=password)
    db.session.add(new_admin)
    db.session.commit()

    return jsonify({"message": "Signup successful!"}), 201


@app.route('/api/admin_login', methods=['POST'])
def admin_login():
    data = request.get_json()
    username = data['username']
    password = data['password']

    admin = Admin.query.filter_by(username=username).first()

    if admin and admin.password == password:
        access_token=create_access_token(identity={"id":admin.id,"role":"admin"})
        return jsonify({"message": "Login successful!","access_token":access_token}), 200
    else:
        return jsonify({"message": "Invalid credentials!"}), 401


@app.route('/api/service_professional_signup', methods=['POST'])
def service_professional_signup():
    data = request.form
    username = data['username']
    password = data['password']
    fullname = data['fullname']
    service_type = data['service_type']
    experience = data['experience']
    phone_number=data['phone_number']
    address = data['address']
    pincode = data['pincode']

    document = request.files['document']  

    existing_user = ServiceProfessional.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({"message": "Username already exists!"}), 400

    document_filename = None
    if document:
        document_filename =document.filename
        document.save(os.path.join(app.config['UPLOAD_FOLDER'],document_filename))

    new_professional = ServiceProfessional(
        username=username,
        password=password,
        fullname=fullname,
        service_type=service_type,
        experience=experience,
        phone_number=phone_number,
        document=document_filename,
        address=address,
        pincode=pincode
    )

    db.session.add(new_professional)
    db.session.commit()

    return jsonify({"message": "Signup successful!"}), 201


@app.route('/api/service_professional_login', methods=['POST'])
def service_professional_login():
    data = request.get_json()
    username = data['username']
    password = data['password']

    professional = ServiceProfessional.query.filter_by(username=username).first()

    if professional is None:
        return jsonify({"message":"Invalid credentials!"}),401

    if professional.flagged:
        return jsonify({"message":"You are blocked. Please contact admin"}),403

    if professional.verification_status=='pending':
        return jsonify({'message':'Your account is pending approval by admin.'}),403
    elif professional.verification_status=='rejected':
        return jsonify({'message':'Your account has been rejected by admin'}),403

    if professional and professional.password == password:
        access_token=create_access_token(identity={"id":professional.id,"role":"service_professional"})
        return jsonify({"message": "Login successful!",
        'professional_id':professional.id,
        'access_token':access_token}), 200
    else:
        return jsonify({"message": "Invalid credentials!"}), 401


@app.route('/api/customer_signup', methods=['POST'])
def customer_signup():
    data = request.get_json()
    username = data['username']
    password = data['password']
    full_name = data['full_name']
    phone_number=data['phone_number']
    address = data['address']
    pincode = data['pincode']
    latitude=data['latitude']
    longitude=data['longitude']

    existing_customer = Customer.query.filter_by(username=username).first()
    if existing_customer:
        return jsonify({"message": "Username already exists!"}), 400

    new_customer = Customer(
        username=username,
        password=password,
        full_name=full_name,
        phone_number=phone_number,
        address=address,
        pincode=pincode,
        latitude=latitude,
        longitude=longitude
    )

    db.session.add(new_customer)
    db.session.commit()
    return jsonify({"message": "Signup successful!"}), 201


@app.route('/api/customer_login', methods=['POST'])
def customer_login():
    data = request.get_json()
    username = data['username']
    password = data['password']

    customer = Customer.query.filter_by(username=username).first()

    if customer is None:
        return jsonify({"message":"Invalid credentials!"}),401

    if customer.flagged:
        return jsonify({"message":"You are blocked. Please contact admin"})

    if customer and customer.password == password:
        access_token=create_access_token(identity={"id":customer.id,"role":"customer"})
        return jsonify({"message": "Login successful!",
        "customer_id":customer.id,
        "access_token":access_token}), 200
    else:
        return jsonify({"message": "Invalid credentials!"}), 401

@app.route('/api/professionals', methods=['GET'])
@jwt_required()
def get_professionals():
    
    service_type = request.args.get('service_type')

    current_user=get_jwt_identity()
    customer_id = current_user.get('id')  
    
    if not service_type:
        return jsonify({'error': 'Service type and Customer ID are required'}), 400

    if current_user.get('role')!='customer':
        return ({'error':'Access forbidden: Only customers can access these endpoint'}),403

    
    customer = Customer.query.filter_by(id=customer_id).first()
    if not customer:
        return jsonify({'error': 'Customer not found'}), 404
    
    
    customer_pincode = customer.pincode
    min_pincode = int(customer_pincode) - 3
    max_pincode = int(customer_pincode) + 3

   
    professionals = ServiceProfessional.query.filter(
        ServiceProfessional.service_type == service_type,
        ServiceProfessional.verification_status=='approved',
        ServiceProfessional.pincode >= min_pincode,
        ServiceProfessional.pincode <= max_pincode
    ).all()

    
    if not professionals:
        return jsonify({'message': 'No professionals found for this service type', 'professionals': []}), 200

    return jsonify({
        'professionals': [{
            'id': prof.id,
            'fullname': prof.fullname,
            'service_type': prof.service_type,
            'experience': prof.experience,
            'address': prof.address,
            'pincode': prof.pincode
        } for prof in professionals]
    }), 200

@app.route('/api/professionals/<int:professionalId>',methods=['GET'])
@jwt_required()
def get_professionals_profile(professionalId):
    current_user=get_jwt_identity()
    role=current_user['role']
    if role!='customer':
        return jsonify({'message':'Unauthorized Access'}),403
    professional=ServiceProfessional.query.get(professionalId)
    if professional:
        return jsonify({
            'id':professional.id,
            'fullname':professional.fullname,
            'experience':professional.experience,
            'address':professional.address,
            'pincode':professional.pincode
        }),200
    else:
        return jsonify({'message':'Professional not found'}),404

@app.route('/api/service_requests',methods=['POST'])
def create_service_request():
    data=request.get_json()
    customer_id=data.get('customer_id')
    professional_id=data.get('professional_id')
    date_of_request=datetime.strptime(data.get('date_of_request'),'%Y-%m-%d').date()
    service_status=data.get('service_status')
    description=data.get('description')
    price=data.get('price')
    
    customer=Customer.query.get(customer_id)

    if not customer_id or not professional_id or not date_of_request or not service_status:
        return jsonify({'message':'Missing required fields'}),400

    service_request=ServiceRequest(
        customer_id=customer_id,
        professional_id=professional_id,
        date_of_request=date_of_request,
        description=description,       
        service_status=service_status,
        price=price
    )

    try:
        db.session.add(service_request)
        db.session.commit()
        professional=ServiceProfessional.query.get(professional_id)
        if professional and professional.phone_number:
            send_whatsapp_message_to_professional.delay(professional.phone_number,service_request.description,customer.full_name,customer.address,customer.pincode)
        return jsonify({'message':'Service request created successfully!'}),201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message':'Failed to create service request','error':str(e)}),500

@app.route('/api/customer_requests/<int:customer_id>',methods=['GET'])
@jwt_required()
def get_customer_requests(customer_id):
    current_user=get_jwt_identity()
    role=current_user['role']
    if role!='customer':
        return jsonify({'message':'Unauthorized access'}),403

    service_requests=ServiceRequest.query.filter_by(customer_id=customer_id,service_status='assigned').all()

    response=[{
        'id':req.id,
        'professional_id':req.professional_id,
        'professional_name':req.professional.fullname,
        'service_type':req.professional.service_type,
        'phone_number':req.professional.phone_number,
        'remarks':req.remarks,
        'description':req.description,
        'status':req.service_status,
        'date_of_request':req.date_of_request.strftime('%Y-%m-%d')
    } for req in service_requests]

    return jsonify({'service_requests':response}),200

@app.route('/api/service_professional_requests/<int:professional_id>',methods=['GET'])
@jwt_required()
def get_service_professional_requests(professional_id):
    current_user=get_jwt_identity()
    role=current_user['role']
    if role!='service_professional':
        return jsonify({'message':'Unauthorized access'}),403
    service_requests=ServiceRequest.query.filter_by(professional_id=professional_id,service_status='requested').all()
    if not service_requests:
        return jsonify({"message":"No incoming service request found"}),404
    return jsonify({
        'service_requests':[{
            'id':req.id,
            'customer_id':req.customer_id,
            'customer_name':req.customer.full_name,
            'service_type':req.professional.service_type,
            'professional_name':req.professional.fullname,
            'professional_id':req.professional_id,
            'phone_number':req.customer.phone_number,
            'description':req.description,
            'remarks':req.remarks,
            'status':req.service_status,
            'date_of_request':req.date_of_request.strftime('%Y-%m-%d')
        }for req in service_requests]
    }),200

@app.route('/api/service_requests/<int:request_id>/accept', methods=['PATCH'])
@jwt_required()
def accept_service_request(request_id):
    current_user=get_jwt_identity()
    role=current_user['role']
    if role!='service_professional':
        return jsonfiy({'message':'Unauthorized access'}),403
    service_request = ServiceRequest.query.get_or_404(request_id)
    if service_request.service_status != 'requested':
        return jsonify({'message': 'Service request is not in a valid state to be accepted'}), 400
    
    service_request.service_status = 'assigned'
    try:
        db.session.commit()
        return jsonify({'message': 'Service request accepted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Failed to accept service request', 'error': str(e)}), 500

@app.route('/api/service_requests/<int:request_id>/reject', methods=['PATCH'])
@jwt_required()
def reject_service_request(request_id):
    current_user=get_jwt_identity()
    role=current_user['role']
    if role!='service_professional':
        return jsonify({'message':'Unauthorized access'}),403
    service_request = ServiceRequest.query.get_or_404(request_id)
    if service_request.service_status != 'requested':
        return jsonify({'message': 'Service request is not in a valid state to be rejected'}), 400
    
    service_request.service_status = 'rejected'
    try:
        db.session.commit()
        return jsonify({'message': 'Service request rejected successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Failed to reject service request', 'error': str(e)}), 500

@app.route('/api/service_requests/<int:request_id>/close', methods=['PATCH'])
def close_service_request(request_id):
    service_request = ServiceRequest.query.get_or_404(request_id)
    
    if service_request.service_status != 'assigned':
        return jsonify({'message': 'Service request is not in a valid state to be closed'}), 400

    service_request.service_status = 'closed'

    data = request.get_json()
    date_of_completion=datetime.strptime(data.get('dateOfCompletion'),'%Y-%m-%d').date()
    remarks = data.get('remarks')
    rating = data.get('rating')
    
    if remarks:
        service_request.remarks = remarks
    if rating:
        service_request.rating = rating
    if date_of_completion:
        service_request.date_of_completion=date_of_completion

    try:
        db.session.commit()
        return jsonify({'message': 'Service request closed successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Failed to close service request', 'error': str(e)}), 500

@app.route('/api/services',methods=['POST'])
@jwt_required()
def create_service_package():
    current_user=get_jwt_identity()
    role=current_user['role']
    if role!='service_professional':
        return jsonify({'message':'Unauthorized access'}),403
    
    data=request.get_json()
    professional_id=data.get('professional_id')
    price=data.get('price')
    name=data.get('name')
    service_type=data.get('service_type')
    time_required=data.get('time_required')
    description=data.get('description')

    professional=ServiceProfessional.query.get(professional_id)
    if not professional:
        return jsonify({'error':'Service professional not found'}),404
    
    new_package=Service(
        professinal_id=professional_id,
        name=name,
        price=price,
        service_type=service_type,
        time_required=time_required,
        description=description
    )

    db.session.add(new_package)
    db.session.commit()
    return jsonify({'message':'Service package created successfully'}),201

@app.route('/api/service_packages', methods=['GET'])
@jwt_required()
def get_service_packages():

    current_user=get_jwt_identity()
    role=current_user['role']
    if role!='customer':
        return jsonify({'message':'Unauthorized access'}),403

    service_type = request.args.get('service_type')
    customer_id = request.args.get('customer_id')

    if not service_type or not customer_id:
        return jsonify({'error': 'Service type and customer ID are required'}), 400

    
    customer = Customer.query.filter_by(id=customer_id).first()

    if not customer:
        return jsonify({'error': 'Customer not found'}), 404

    customer_pincode = customer.pincode

    
    min_pincode = int(customer_pincode) - 3
    max_pincode = int(customer_pincode) + 3

    
    service_packages = Service.query.join(ServiceProfessional).filter(
        Service.service_type == service_type,
        ServiceProfessional.pincode >= min_pincode,
        ServiceProfessional.pincode <= max_pincode
    ).all()

    if not service_packages:
        return jsonify({'message': 'No service packages found for this service type and location range'}), 404

    return jsonify({
        'service_packages': [{
            'id': pkg.id,
            'name': pkg.name,
            'price': pkg.price,
            'description': pkg.description,
            'time_required': pkg.time_required,
            'professional_id': pkg.professinal_id,
            'professional_name': pkg.professional.fullname,
            'professional_pincode': pkg.professional.pincode
        } for pkg in service_packages]
    }), 200

@app.route('/api/book_service/<int:package_id>',methods=['POST'])
@jwt_required()
def book_service_package(package_id):
    current_user=get_jwt_identity()
    role=current_user['role']
    if role!='customer':
        return jsonify({'message':'Unauthorized access'}),403
    data=request.get_json()
    customer_id=data.get('customer_id')
    service_package=Service.query.get([package_id])
    customer=Customer.query.get(customer_id)
    if not service_package or not customer:
        return jsonify({'error':'Service package or customer not found'}),404
    
    booked_package=BookedServiceRequest(
        package_id=service_package.id,
        customer_id=customer.id,
        customer_name=customer.full_name,
        package_name=service_package.name,
        professional_id=service_package.professional.id,
        date_of_request=datetime.utcnow()
    )
    db.session.add(booked_package)
    db.session.commit()
    return jsonify({'message':'Package booked successfully'}),201

@app.route('/api/professional_booked_packages/<int:professional_id>',methods=['GET'])
@jwt_required()
def get_booked_service_packages(professional_id):
    current_user=get_jwt_identity()
    role=current_user['role']
    if role!='service_professional':
        return jsonify({'message':'Unauthorized access'}),403
    booked_packages=BookedServiceRequest.query.filter_by(professional_id=professional_id,status='pending').all()
    booked_package_list=[{
        'id':package.id,
        'package_id':package.package_id,
        'package_name':package.package_name,
        'customer_id':package.customer_id,
        'address':package.customer.address,
        'phone_number':package.customer.phone_number,
        'customer_name':package.customer_name,
        'status':package.status,
    }for package in booked_packages]

    return jsonify({'booked_packages':booked_package_list}),200

@app.route('/api/booked_service_packages/customer/<int:customer_id>',methods=['GET'])
@jwt_required()
def get_accepted_booked_service_packages(customer_id):
    current_user=get_jwt_identity()
    role=current_user['role']
    if role!='customer':
        return jsonify({'message':'Unauthorized access'}),403
    booked_packages=BookedServiceRequest.query.filter_by(customer_id=customer_id,status='accepted').all()
    if not booked_packages:
        return jsonify({'error':'No accepted service package found for this customer'}),404
    booked_packages_list=[{
        'id':package.id,
        'package_name':package.service.name,
        'package_id':package.service.id,
        'professional_name':package.professional.fullname,
        'customer_id':package.customer_id,
        'customer_name':package.customer_name,
        'phone_number':package.professional.phone_number,
        'description':package.service.description,
        'status':package.status
    }for package in booked_packages]
    return jsonify({'accepted_packages':booked_packages_list}),200

    

@app.route('/api/booked_service_packages/<int:booked_service_request_id>/accept', methods=['PATCH'])
@jwt_required()
def accept_booked_package(booked_service_request_id):
    current_user=get_jwt_identity()
    role=current_user['role']
    if role!='service_professional':
        return jsonify({'message':'Unauthorized access'}),403
    data = request.get_json()  
    service_status = data.get('service_status')  

    if service_status is None:
        return jsonify({"message": "Invalid data."}), 400  

    
    booked_package = BookedServiceRequest.query.get(booked_service_request_id)
    if booked_package:
        booked_package.status = service_status  
        db.session.commit()  
        return jsonify({"message": "Package accepted."}), 200
    else:
        return jsonify({"message": "Package not found."}), 404

@app.route('/api/booked_service_packages/<int:booked_service_request_id>/reject', methods=['PATCH'])
@jwt_required()
def reject_booked_package(booked_service_request_id):
    current_user=get_jwt_identity()
    role=current_user['role']
    if role!='service_professional':
        return jsonfiy({'message':'Unauthorized access'}),403
    data = request.get_json()  
    service_status = data.get('service_status')  

    if service_status is None:
        return jsonify({"message": "Invalid data."}), 400  

    
    booked_package = BookedServiceRequest.query.get(booked_service_request_id)
    if booked_package:
        booked_package.status = service_status 
        db.session.commit()  
        return jsonify({"message": "Package rejected."}), 200
    else:
        return jsonify({"message": "Package not found."}), 404

@app.route('/api/booked_service_packages/<int:booked_service_request_id>/close',methods=['PATCH'])
def close_service_package(booked_service_request_id):
    data=request.get_json()
    booked_package=BookedServiceRequest.query.get(booked_service_request_id)
    if booked_package:
        booked_package.status='closed'
        booked_package.remarks=data.get('remarks')
        booked_package.rating=data.get('rating')
        booked_package.date_of_completion=datetime.strptime(data.get('dateOfCompletion'),'%Y-%m-%d').date()
        db.session.commit()
        return jsonify({'message':'Service package closed successfully'}),200
    else:
        return jsonify({'error':'Package not found'}),404

@app.route('/api/customer/<int:customer_id>/service_requests',methods=['GET'])
def get_customer_requested_service_requests(customer_id):
    service_requests=ServiceRequest.query.filter_by(customer_id=customer_id,service_status='requested').all()

    if not service_requests:
        return jsonify({'message':'No requested services found for this customer'}),404

    request_list=[{
        'id':request.id,
        'date_of_request':request.date_of_request,
        'description':request.description,
        'price':request.price,
        'service_type':request.professional.service_type,
        'full_name':request.professional.fullname,
        'status':request.service_status
    }for request in service_requests]

    return jsonify({'requests':request_list}),200

@app.route('/api/service_requests/<int:service_request_id>',methods=['PUT'])
def edit_service_request(service_request_id):
    data=request.get_json()
    service_request=ServiceRequest.query.get(service_request_id)

    if not service_request:
        return jsonify({'error':'Service Request not found'}),404

    if 'date_of_request' in data:
        service_request.date_of_request=datetime.strptime(data['date_of_request'],'%Y-%m-%d').date()

    if 'description' in data:
        service_request.description=data['description']

    if 'price' in data:
        service_request.price=data['price']

    db.session.commit()
    return jsonify({'message':'Service Request updated successfully'}),200

@app.route('/api/service_requests/completed/<int:customer_id>',methods=['GET'])
@jwt_required()
def get_completed_service_requests(customer_id):
    current_user=get_jwt_identity()
    role=current_user['role']
    if role!='customer':
        return jsonify({'message':'Unauthorized access'}),403
    
    completed_requests=ServiceRequest.query.filter_by(customer_id=customer_id,service_status='closed').all()
    return jsonify([{
        'id':req.id,
        'customer_id':req.customer_id,
        'customer_name':req.customer.full_name,
        'date_of_request':req.date_of_request,
        'description':req.description,
        'price':req.price,
        'status':req.service_status,
        'remarks':req.remarks,
        'rating':req.rating
    }for req in completed_requests])

@app.route('/api/booked_service_packages/completed/<int:customer_id>',methods=['GET'])
@jwt_required()
def get_completed_booked_packages(customer_id):
    current_user=get_jwt_identity()
    role=current_user['role']
    if role!='customer':
        return jsonify({'message':'Unauthorized access'}),403
    completed_packages=BookedServiceRequest.query.filter_by(customer_id=customer_id,status='closed').all()
    return jsonify([{
        'id':pkg.id,
        'name':pkg.service.name,
        'customer_id':pkg.customer_id,
        'professional_id':pkg.professional_id,
        'professional_name':pkg.professional.fullname,
        'status':pkg.status,
        'remarks':pkg.remarks,
        'rating':pkg.rating
    }for pkg in completed_packages]),200


@app.route('/api/professional/service_requests/completed/<int:professional_id>',methods=['GET'])
@jwt_required()
def get_professional_completed_service_requests(professional_id):
    current_user=get_jwt_identity()
    role=current_user['role']
    if role!='service_professional':
        return jsonfiy({'message':'Unauthorized Access'}),403
    completed_requests=ServiceRequest.query.filter_by(professional_id=professional_id,service_status='closed').all()
    return jsonify([{
        'id':req.id,
        'customer_id':req.customer_id,
        'customer_name':req.customer.full_name,
        'date_of_request':req.date_of_request,
        'description':req.description,
        'price':req.price,
        'status':req.service_status,
        'remarks':req.remarks,
        'rating':req.rating,
        'is_complaint':req.is_complaint
    }for req in completed_requests])

@app.route('/api/professional/booked_service_packages/completed/<int:professional_id>',methods=['GET'])
@jwt_required()
def get_professional_completed_booked_packages(professional_id):
    current_user=get_jwt_identity()
    role=current_user['role']
    if role!='service_professional':
        return jsonfiy({'message':'Unauthorized Access'}),403
    completed_packages=BookedServiceRequest.query.filter_by(professional_id=professional_id,status='closed').all()
    return jsonify([{
        'id':pkg.id,
        'name':pkg.service.name,
        'customer_id':pkg.customer_id,
        'professional_id':pkg.professional_id,
        'professional_name':pkg.professional.fullname,
        'status':pkg.status,
        'remarks':pkg.remarks,
        'rating':pkg.rating,
        'is_complaint':pkg.is_complaint
    }for pkg in completed_packages]),200

@app.route('/api/users',methods=['GET'])
@jwt_required()
def get_all_users():
    current_user=get_jwt_identity()
    role=current_user['role']
    if role!='admin':
        return jsonify({'message':'Unauthorized access'}),403
    
    customers=Customer.query.all()
    professionals=ServiceProfessional.query.all()
    customer_data=[{
        'id':customer.id,
        'name':customer.full_name,
        'address':customer.address,
        'pincode':customer.pincode,
        'flagged':customer.flagged
    }for customer in customers]

    professional_data=[{
        'id':professional.id,
        'name':professional.fullname,
        'service_type':professional.service_type,
        'address':professional.address,
        'pincode':professional.pincode,
        'flagged':professional.flagged
    }for professional in professionals]

    return jsonify({
        'customers':customer_data,
        'professionals':professional_data
    }),200

@app.route('/api/users/block/<int:user_id>',methods=['PATCH'])
@jwt_required()
def block_user(user_id):

    current_user=get_jwt_identity()
    role=current_user['role']
    if role!='admin':
        return jsonify({'message':'Unauthorized access'}),403
    
    data=request.get_json()
    user_type=data.get('user_type')
    if user_type == 'customer':
        customer=Customer.query.get(user_id)
        if customer:
            customer.flagged=not customer.flagged
            db.session.commit()
            return jsonify({'message':'Customer block status updated'}),200
        else:
            return jsonify({'error':'Customer not found'}),404
    elif user_type == 'professional':
        professional=ServiceProfessional.query.get(user_id)
        if professional:
            professional.flagged=not professional.flagged
            db.session.commit()
            return jsonify({'message':'Service Professional block status updated'}),200
        else:
            return jsonify({'error':'Service Professional not found'}),404
    else:
        return jsonify({'error':'Invalid user type'}),400

@app.route('/api/pending_professionals',methods=['GET'])
@jwt_required()
def get_pending_professionals():
    current_user=get_jwt_identity()
    role=current_user['role']
    if role!='admin':
        return jsonify({'message':'Unauthorized access'}),403
    pending_professionals=ServiceProfessional.query.filter_by(verification_status='pending').all()
    professionals_data=[{
        'id':professional.id,
        'full_name':professional.fullname,
        'service_type':professional.service_type,
        'address':professional.address,
        'pincode':professional.pincode,
        'document':professional.document
    }for professional in pending_professionals]

    return jsonify({'professionals':professionals_data})

@app.route('/api/approve_professional/<int:id>',methods=['POST'])
@jwt_required()
def approve_professionals(id):
    current_user=get_jwt_identity()
    role=current_user['role']
    if role!='admin':
        return jsonify({'message':'Unauthorized access'}),403
    professional=ServiceProfessional.query.get(id)
    if not professional:
        return jsonify({'message':'Professional not found'}),404
    
    professional.verification_status='approved'
    db.session.commit()
    return jsonify({'message':f'Professional {professional.fullname} has been approved'})

@app.route('/api/reject_professional/<int:id>',methods=['POST'])
@jwt_required()
def reject_professionals(id):
    current_user=get_jwt_identity()
    role=current_user['role']
    if role!='admin':
        return jsonify({'message':'Unauthorized access'}),403
    professional=ServiceProfessional.query.get(id)
    if not professional:
        return jsonify({'message':'Profesional not found'}),404
    
    professional.verification_status='rejected'
    db.session.commit()
    return jsonify({'message':f'Professional {professional.fullname} has been rejected'})

@app.route('/static/documents/<filename>')
def serve_documents(filename):
    return send_from_directory('static/documents',filename)

@app.route('/api/customer_service_professional_count',methods=['GET'])
def customer_service_professional_count():
    customer_count=Customer.query.count()
    professional_count=ServiceProfessional.query.count()
    return jsonify({
        'customers':customer_count,
        'professionals':professional_count
    }),200

@app.route('/api/blocked_unblocked_users',methods=['GET'])
def blocked_unblocked_users():
    blocked_customers=Customer.query.filter_by(flagged=True).count()
    unblocked_customers=Customer.query.filter_by(flagged=False).count()
    blocked_professionals=ServiceProfessional.query.filter_by(flagged=True).count()
    unblocked_professionals=ServiceProfessional.query.filter_by(flagged=False).count()

    return jsonify({
        'blocked_customers':blocked_customers,
        'unblocked_customers':unblocked_customers,
        'blocked_professionals':blocked_professionals,
        'unblocked_professionals':unblocked_professionals
    }),200

@app.route('/api/service_professionals_by_type',methods=['GET'])
@cache_result('service_professionals_by_type')
def get_service_professionals_by_type():
    data={
    'Carpenter':ServiceProfessional.query.filter_by(service_type='Carpenter').count(),
    'Plumber':ServiceProfessional.query.filter_by(service_type='Plumber').count(),
    'AC Repair':ServiceProfessional.query.filter_by(service_type='AC Repair').count(),
    'Saloon':ServiceProfessional.query.filter_by(service_type='Saloon').count(),
    'Cleaner':ServiceProfessional.query.filter_by(service_type='Cleaner').count(),
    'Painter':ServiceProfessional.query.filter_by(service_type='Painter').count()
    }
    return jsonify(data)

@app.route('/api/service_requests_by_type',methods=['GET'])
@cache_result('service_requests_by_type')
def get_service_requests_by_type():
    data={
        'Carpenter':ServiceRequest.query.join(ServiceProfessional).filter(ServiceProfessional.service_type=='Carpenter').count(),
        'Plumber':ServiceRequest.query.join(ServiceProfessional).filter(ServiceProfessional.service_type=='Plumber').count(),
        'AC Repair':ServiceRequest.query.join(ServiceProfessional).filter(ServiceProfessional.service_type=='AC Repair').count(),
        'Saloon':ServiceRequest.query.join(ServiceProfessional).filter(ServiceProfessional.service_type=='Saloon').count(),
        'Cleaner':ServiceRequest.query.join(ServiceProfessional).filter(ServiceProfessional.service_type=='Cleaner').count(),
        'Painter':ServiceRequest.query.join(ServiceProfessional).filter(ServiceProfessional.service_type=='Painter').count()
    }
    return jsonify(data)

@app.route('/api/service_packages_by_type',methods=['GET'])
@cache_result('service_packages_by_type')
def get_service_packages_by_type():
    data={
    'Carpenter':Service.query.filter_by(service_type='Carpenter').count(),
    'Plumber':Service.query.filter_by(service_type='Plumber').count(),
    'AC Repair':Service.query.filter_by(service_type='AC Repair').count(),
    'Saloon':Service.query.filter_by(service_type='Saloon').count(),
    'Cleaner':Service.query.filter_by(service_type='Cleaner').count(),
    'Painter':Service.query.filter_by(service_type='Painter').count()
    }
    return jsonify(data)

@app.route('/api/homefix_packages_by_type',methods=['GET'])
@cache_result('homefix_packages_by_type')
def get_homefix_packages_by_type():
    data={
    'Carpenter':AdminServicePackage.query.filter_by(service_type='Carpenter').count(),
    'Plumber':AdminServicePackage.query.filter_by(service_type='Plumber').count(),
    'AC Repair':AdminServicePackage.query.filter_by(service_type='AC Repair').count(),
    'Saloon':AdminServicePackage.query.filter_by(service_type='Saloon').count(),
    'Cleaner':AdminServicePackage.query.filter_by(service_type='Cleaner').count(),
    'Painter':AdminServicePackage.query.filter_by(service_type='Painter').count()
    }
    return jsonify(data)


@app.route('/api/request_activity_report', methods=['POST'])
@jwt_required()
def request_activity_report():
    data = request.get_json()

    current_user=get_jwt_identity()
    role=current_user['role']

    if role!='customer':
        return jsonify({'message':'Unauthorized access'}), 403

    date = data.get('date')
    customer_id = data.get('customer_id')
    email = data.get('email')

    if not date or not customer_id:
        return jsonify({'message': 'Date or customer ID not provided'}), 400

    try:
       
        end_date = datetime.strptime(date, '%Y-%m-%d').date()
        start_date = end_date - timedelta(days=30)

        
        customer = Customer.query.get(customer_id)
        if not customer:
            return jsonify({'message': 'Customer not found'}), 404

       
        closed_requests = ServiceRequest.query.filter(
            and_(
                ServiceRequest.customer_id == customer_id,
                ServiceRequest.service_status == 'closed',
                ServiceRequest.date_of_request.between(start_date, end_date)
            )
        ).all()

        
        closed_packages = BookedServiceRequest.query.filter(
            and_(
                BookedServiceRequest.customer_id == customer_id,
                BookedServiceRequest.status == 'closed',
                BookedServiceRequest.date_of_request.between(start_date, end_date)
            )
        ).all()

        closed_admin_packages = BookedAdminServicePackage.query.filter(
            and_(
                BookedAdminServicePackage.customer_id == customer_id,
                BookedAdminServicePackage.status == 'closed',
                BookedAdminServicePackage.date_of_completion.between(start_date, end_date)
            )
        ).all()

        
        html_content = f"""
    
        <h2>Activity Report (from {start_date} to {end_date})</h2>

        <h3>Closed Service Requests</h3>
        <ul>
        {" ".join([f"<li>Request ID: {r.id}, Type: {r.professional.service_type}, Date: {r.date_of_request}, Description: {r.description}, Professional: {r.professional.fullname}, Remarks: {r.remarks}, Rating: {r.rating}</li>" for r in closed_requests])}
        </ul>
        
        <h3>Closed Service Packages</h3>
        <ul>
        {" ".join([f"<li>Package Name: {p.package_name}, Professional: {p.professional.fullname}, Remarks: {p.remarks}, Rating: {p.rating}, Status: {p.status}</li>" for p in closed_packages])}
        </ul>

        <h3>Closed HomeFix Packages</h3>
        <ul>
        {" ".join([f"<li>Package Name: {a.package.name}, Professional: {a.professional.fullname}, Remarks: {a.remarks}, Rating: {a.rating}, Status: {a.status}</li>" for a in closed_admin_packages])}
        </ul>
        """



       
        
        msg = Message('Your Monthly Activity Report', recipients=[email])
        msg.html = html_content

        mail.send(msg)

        return jsonify({'message': 'Activity report sent successfully!'}), 200

    except Exception as e:
        return jsonify({'message': 'Failed to send activity report', 'error': str(e)}), 500

@app.route('/api/send_report_email', methods=['POST'])
@jwt_required()
def send_report_email():
    try:
        

        current_user=get_jwt_identity()
        role=current_user['role']

        if role!='admin':
            return jsonify({'message':'Unauthorized access'}),403


        if not request.is_json:
            return jsonify({'message': 'Request must be JSON'}), 400

        
        data = request.get_json()

        
        end_date_str = data.get('end_date')
        email = data.get('email')

        
        if not end_date_str or not email:
            return jsonify({'message': "Both 'end_date' and 'email' are required."}), 400

        
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d')

        
        start_date = end_date - timedelta(days=30)

       
        closed_service_requests = ServiceRequest.query.filter(
            ServiceRequest.service_status == 'closed',
            ServiceRequest.date_of_completion.between(start_date, end_date)
        ).all()

        
        closed_booked_packages = BookedServiceRequest.query.filter(
            BookedServiceRequest.status == 'closed',
            BookedServiceRequest.date_of_completion.between(start_date, end_date)
        ).all()

        closed_booked_admin_packages=BookedAdminServicePackage.query.filter(
            BookedAdminServicePackage.status =='closed',
            BookedAdminServicePackage.date_of_completion.between(start_date,end_date)
        ).all()

        print(closed_booked_admin_packages)


       
        csv_output = StringIO()
        csv_writer = csv.writer(csv_output)

  
        csv_writer.writerow(['Closed Service Requests'])
        csv_writer.writerow(['Service ID', 'Customer ID', 'Professional ID', 'Date of Request', 'Date of Completion', 'Remarks'])

        for request1 in closed_service_requests:
            csv_writer.writerow([request1.id, request1.customer_id, request1.professional_id, request1.date_of_request,
                                 request1.date_of_completion, request1.remarks])

        csv_writer.writerow([])  

       
        csv_writer.writerow(['Closed Booked Service Packages'])
        csv_writer.writerow(['Package ID', 'Customer ID', 'Professional ID', 'Package Name', 'Date of Request', 'Date of Completion'])

        for package in closed_booked_packages:
            csv_writer.writerow([package.id, package.customer_id, package.professional_id, package.package_name,
                                 package.date_of_request, package.date_of_completion])

        csv_writer.writerow([])

        csv_writer.writerow(['Closed HomeFix Packages'])
        csv_writer.writerow(['Package ID', 'Customer ID', 'Professional ID', 'Admin Package Name', 'Date of Request', 'Date of Completion'])

        

        for admin_package in closed_booked_admin_packages:
            csv_writer.writerow([admin_package.id, admin_package.customer_id, admin_package.service_professional_id, admin_package.package.name,
                                 admin_package.date_of_request, admin_package.date_of_completion])

        csv_output.seek(0) 

        
        msg = Message(subject="Your Requested Report",
                      sender="abhisheksharma010802@gmail.com",
                      recipients=[email])
        msg.body = "Here is your report with closed service requests and closed booked packages."

       
        msg.attach("service_requests_report.csv", "text/csv", csv_output.getvalue())

       
        mail.send(msg)

     
        return jsonify({'message': 'Report successfully submitted.'}), 200

    except Exception as e:
        
        print(f"Error: {e}")
        return jsonify({'message': 'An unexpected error occurred.'}), 500

@app.route('/api/service_requests/<int:request_id>', methods=['GET'])
def get_service_request(request_id):
    service_request = ServiceRequest.query.get_or_404(request_id)
    return jsonify({
        'id': service_request.id,
        'amount': service_request.price,
        'professional_id': service_request.professional_id,
        'name':service_request.professional.fullname

    })

@app.route('/api/service-professionals/<string:service_type>', methods=['GET'])
@jwt_required()
def get_service_professionals(service_type):
    try:
       
        current_user=get_jwt_identity()
        role=current_user['role']
        if role!='admin':
            return jsonify({'message':'Unauthorized access'}),403

        professionals = ServiceProfessional.query.filter_by(service_type=service_type).all()
        professional_data = [
            {
                'id': professional.id,
                'full_name': professional.fullname,
                'service_type': professional.service_type,
                'experience': professional.experience,
                'address': professional.address
            }
            for professional in professionals
        ]
        return jsonify(professional_data), 200
    except Exception as e:
        return jsonify({'error': f"Error fetching professionals: {str(e)}"}), 500

@app.route('/api/professional/<int:id>', methods=['GET'])
@jwt_required()
def get_professional_profile(id):
    try:
        current_user=get_jwt_identity()
        role=current_user['role']
        if role!='admin':
            return jsonify({'message':'Unauthorized access'}),403

        professional = ServiceProfessional.query.get(id)
        if not professional:
            return jsonify({'error': 'Professional not found'}), 404
        
        professional_data = {
            'id': professional.id,
            'full_name': professional.fullname,
            'service_type': professional.service_type,
            'experience': professional.experience,
            'address': professional.address,
            'pincode':professional.pincode
        }
        return jsonify(professional_data), 200
    except Exception as e:
        return jsonify({'error': f"Error fetching professional: {str(e)}"}), 500

@app.route('/api/admin/services', methods=['POST'])
@jwt_required()
def create_service_package_admin():
    try:
        current_user=get_jwt_identity()
        role=current_user['role']
        if role!='admin':
            return jsonify({'message':'Unauthorized access'}),403
        data = request.get_json()

        
        service_name = data.get('name')
        base_price = data.get('base_price')
        time_required = data.get('time_required')
        description = data.get('description')
        service_type = data.get('service_type')
        service_professional_id = data.get('service_professional_id')

        
        service = AdminServicePackage(
            name=service_name,
            base_price=base_price,
            time_required=time_required,
            description=description,
            service_type=service_type,
            service_professional_id=service_professional_id
        )
        db.session.add(service)
        db.session.commit()

        return jsonify({'message': 'Service created successfully'}), 201
    except Exception as e:
        return jsonify({'error': f"Error creating service: {str(e)}"}), 500

@app.route('/api/packages/<string:service_type>', methods=['GET'])
@jwt_required()
def get_admin_packages_by_type(service_type):
    current_user=get_jwt_identity()
    role=current_user['role']
    if role!='customer':
        return jsonify({'message':'Unauthorized access'}),304
    packages = AdminServicePackage.query.filter_by(service_type=service_type).all()
    result = [
        {
            'id': package.id,
            'name': package.name,
            'base_price': package.base_price,
            'description': package.description,
            'service_type': package.service_type,
            'service_professional_id':package.service_professional_id
        }
        for package in packages
    ]
    return jsonify(result)

@app.route('/api/book_package', methods=['POST'])
@jwt_required()
def book_package():
    try:
        data = request.get_json()

        current_user=get_jwt_identity()
        role=current_user['role']
        if role!='customer':
            return jsonify({'message':'Unauthorized access'}),403

        customer_id = data.get('customer_id')
        package_id = data.get('package_id')
        service_professional_id = data.get('service_professional_id')
        date_of_request = datetime.strptime(data.get('date_of_request'),'%Y-%m-%d')  
        
        if not all([customer_id, package_id, service_professional_id]):
            return jsonify({"error": "Missing required fields"}), 400

       
        booked_package = BookedAdminServicePackage(
            customer_id=customer_id,
            package_id=package_id,
            service_professional_id=service_professional_id,  
            date_of_request=date_of_request,
            status='requested'  
        )

        
        db.session.add(booked_package)
        db.session.commit()

        return jsonify({"message": "Package booked successfully!"}), 200

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Failed to book package"}), 500

@app.route('/api/professional_packages/<int:professional_id>', methods=['GET'])
@jwt_required()
def get_professional_admin_packages(professional_id):
    current_user=get_jwt_identity()
    role=current_user['role']
    if role!='service_professional':
        return jsonify({'message':'Unauthorized access'}),403
    packages = BookedAdminServicePackage.query.filter(
        BookedAdminServicePackage.service_professional_id==professional_id,
        BookedAdminServicePackage.status == 'requested',
        BookedAdminServicePackage.package_id.isnot(None)
    ).all()
    print(packages)
    package_list = []
    for pkg in packages:
        package_list.append({
            'id': pkg.id,
            'package_id': pkg.package_id,
            'package_name': pkg.package.name,  
            'customer_id': pkg.customer_id,
            'customer_phone_number':pkg.customer.phone_number,
            'customer_name':pkg.customer.full_name,
            'status': pkg.status,
            'date_of_request': pkg.date_of_request,
            'remarks': pkg.remarks,
            'rating': pkg.rating,
        })
    return jsonify(package_list)

@app.route('/api/update_package_status', methods=['POST'])
@jwt_required()
def update_admin_package_status():
    current_user=get_jwt_identity()
    role=current_user['role']
    if role!='service_professional':
        return jsonfiy({'message':'Unauthorized access'}),403
    data = request.json
    package_id = data.get('package_id')
    status = data.get('status')

    
    package = BookedAdminServicePackage.query.get(package_id)
    
    if package:
        package.status = status
        db.session.commit()
        return jsonify({"message": f"Package status updated to {status}"})
    else:
        return jsonify({"error": "Package not found"}), 404

@app.route('/api/customer_booked_packages/<int:customer_id>', methods=['GET'])
@jwt_required()
def get_customer_booked_packages(customer_id):
   
    current_user=get_jwt_identity()
    role=current_user['role']
    if role!='customer':
        return jsonify({'message':'Unauthorized access'}),403

    booked_packages = BookedAdminServicePackage.query.filter(
        BookedAdminServicePackage.customer_id == customer_id,
        BookedAdminServicePackage.status == 'assigned',
        BookedAdminServicePackage.package_id.isnot(None)
    ).all()

    response_data = []
    for package in booked_packages:
        response_data.append({
            'id':package.id,
            'package_id': package.package_id,
            'package_name': package.package.name,
            'status': package.status,
            'date_of_request': package.date_of_request,
            'remarks': package.remarks,
            'rating': package.rating
        })

    return jsonify(response_data), 200

@app.route('/api/close_package/<int:pkg_id>', methods=['POST'])
def close_package(pkg_id):
    data = request.get_json()
    completion_date = datetime.strptime(data.get('completion_date'),'%Y-%m-%d') 
    
    remarks = data.get('remarks')
    rating = data.get('rating')

    
    package = BookedAdminServicePackage.query.get(pkg_id)
    
    if not package:
        return jsonify({"error": "Package not found"}), 404

   
    package.date_of_completion = completion_date
    package.remarks = remarks
    package.rating = rating
    package.status = 'closed'

    
    db.session.commit()

    return jsonify({"message": "Package closed successfully"}), 200

@app.route('/api/booked_admin_service_packages/completed/<customer_id>', methods=['GET'])
@jwt_required()
def get_completed_admin_service_packages(customer_id):
    current_user=get_jwt_identity()
    role=current_user['role']
    if role!='customer':
        return jsonify({'message':'Unauthorized access'}),403
    completed_admin_packages = BookedAdminServicePackage.query.filter_by(customer_id=customer_id, status='closed').all()
    
    
    result = []
    for package in completed_admin_packages:
        result.append({
            'id': package.id,
            'name': package.package.name,
            'customer_id': package.customer_id,
            'professional_id': package.package.service_professional_id,
            'status': package.status,
            'remarks': package.remarks,
            'rating': package.rating,
            'professional_name': package.professional.fullname
        })
    
    return jsonify(result)


@app.route('/api/professional/booked_admin_service_packages/completed/<int:professional_id>',methods=['GET'])
@jwt_required()
def get_professional_completed_admin_service_packages(professional_id):
    current_user=get_jwt_identity()
    role=current_user['role']
    if role!='service_professional':
        return jsonify({'message':'Unauthorized access'}),403
    completed_admin_packages = BookedAdminServicePackage.query.filter_by( service_professional_id=professional_id, status='closed').all()
    
    
    result = []
    for package in completed_admin_packages:
        result.append({
            'id': package.id,
            'name': package.package.name,
            'customer_id': package.customer_id,
            'professional_id': package.professional.id,
            'status': package.status,
            'remarks': package.remarks,
            'rating': package.rating,
            'professional_name': package.professional.fullname,
            'is_complaint':package.is_complaint
        })
    
    return jsonify(result)


@app.route('/api/admin_service_packages/<service_type>', methods=['GET'])
@jwt_required()
def get_admin_service_packages(service_type):
    
    current_user=get_jwt_identity()
    role=current_user['role']
    if role!='admin':
        return jsonify({'message':'Unauthorized access'}),403
    admin_packages = AdminServicePackage.query.filter_by(service_type=service_type).all()

    
    packages_list = [{
        'id': package.id,
        'package_name': package.name,
        'description': package.description,
        'time_required': package.time_required,
        'professional_name': package.service_professional.fullname
    } for package in admin_packages]

    return jsonify({'packages': packages_list})

@app.route('/api/update_service_package/<int:pkg_id>', methods=['PUT'])
@jwt_required()
def update_service_package(pkg_id):
    current_user=get_jwt_identity()
    role=current_user['role']
    if role!='admin':
        return jsonfiy({'message':'Unauthorized access'})
    package = AdminServicePackage.query.get(pkg_id)
    if not package:
        return jsonify({'error': 'Package not found'}), 404

    data = request.get_json()
    package.name = data.get('package_name')
    package.base_price=data.get('base_price')
    package.description = data.get('description')
    package.time_required = data.get('time_required')
    package.service_type=data.get('service_type')
    package.service_professional_id = data.get('service_professional_id')
    
    db.session.commit()
    return jsonify({'message': 'Package updated successfully'}), 200

@app.route('/api/service_package/<int:pkg_id>', methods=['GET'])
@jwt_required()
def get_service_package(pkg_id):
    
    current_user=get_jwt_identity()
    role=current_user['role']
    if role!='admin':
        return jsonify({'message':'Unauthorized access'}),403

    package = AdminServicePackage.query.get(pkg_id)
    
    
    if not package:
        return jsonify({'error': 'Package not found'}), 404
    
    
    package_data = {
        'id': package.id,
        'base_price':package.base_price,
        'package_name': package.name,
        'description': package.description,
        'time_required': package.time_required,
        'professional_name': package.service_professional.fullname,
        'service_type':package.service_type
    }
    
    
    return jsonify({'package': package_data}), 200

@app.route('/api/delete_service_package/<int:pkg_id>', methods=['DELETE'])
@jwt_required()
def delete_admin_service_package(pkg_id):
    try:
        current_user=get_jwt_identity()
        role=current_user['role']
        if role!='admin':
            return jsonify({'message':'Unauthorized access'}),403
        package = AdminServicePackage.query.get(pkg_id)

        if not package:
            return jsonify({"message": "Package not found"}), 404


        booked_packages=BookedAdminServicePackage.query.filter_by(package_id=pkg_id).all()
        for pkg in booked_packages:
            if pkg.status=='assigned':
                return jsonify({'message':'This package cannot be deleted because it is booked by a customer'})
        
        for pkg in booked_packages:
            db.session.delete(pkg)

        if package:
            db.session.delete(package)
            db.session.commit()

        return jsonify({"message": "Admin service package and related booked packages deleted successfully!"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500


@app.route('/api/professional_service_packages/<int:professional_id>',methods=['GET'])
@jwt_required()
def get_professional_packages(professional_id):
    current_user=get_jwt_identity()
    role=current_user['role']
    if role!='service_professional':
        return jsonify({'message':'Unauthorized access'}),403
    service_packages=Service.query.filter_by(professinal_id=professional_id).all()
    if not service_packages:
        return jsonify({"message":"No Service Packages not found"}),404
    
    packages_list = [{
        'id': package.id,
        'package_name': package.name,
        'description': package.description,
        'time_required': package.time_required,
        'price':package.price
    } for package in service_packages]

    return jsonify({'packages': packages_list})


@app.route('/api/professional/service_packages/<int:pkgId>',methods=['GET'])
@jwt_required()
def professional_service_packages_view(pkgId):
    current_user=get_jwt_identity()
    role=current_user['role']
    if role!='service_professional':
        return jsonify({'message':'Unauthorized access'}),403
    service_package=Service.query.filter_by(id=pkgId).first()

    package_data={
        'name':service_package.name,
        'description':service_package.description,
        'time_required':service_package.time_required,
        'price':service_package.price,
    }

    return jsonify({'package':package_data})


@app.route('/api/professional/update_service_package/<int:pkgId>',methods=['PUT'])
@jwt_required()
def professional_update_service_packages(pkgId):
    current_user=get_jwt_identity()
    role=current_user['role']
    if role!='service_professional':
        return jsonify({'message':'Unauthorized access'}),403
    package = Service.query.get(pkgId)
    print(package)
    if not package:
        return jsonify({'error': 'Package not found'}), 404

    data = request.get_json()
    package.name = data.get('name')
    package.price=data.get('price')
    package.description = data.get('description')
    package.time_required = data.get('time_required')

    db.session.commit()
    return jsonify({'message': 'Package updated successfully'}), 200

@app.route('/api/customers_profile/<int:customer_id>',methods=['GET'])
@jwt_required()
def get_customer_profile(customer_id):
    current_user=get_jwt_identity()
    role=current_user['role']

    if role!='customer':
        return jsonify({'message':'Unauthorized access'}),403
    
    customer=Customer.query.get(customer_id)
    if not customer:
        return jsonify({'message':'Customer not found'}), 404
    
    customer_data={
        'username':customer.username,
        'password':customer.password,
        'full_name':customer.full_name,
        'phone_number':customer.phone_number,
        'address':customer.address,
        'pincode':customer.pincode,
    }

    return jsonify({'customer_data':customer_data}), 200

@app.route('/api/customer_update_profile/<int:customer_id>',methods=['PUT'])
@jwt_required()
def update_customer(customer_id):
    data=request.get_json()

    current_user=get_jwt_identity()
    role=current_user['role']

    if role!='customer':
        return jsonify({'message':'Unauthorized access'}),403
    
    customer=Customer.query.get(customer_id)
    if not customer:
        return jsonify({'error':'Customer not found'}),404
    
    customer.username=data.get('username')
    customer.password=data.get('password')
    customer.full_name=data.get('full_name')
    customer.phone_number=data.get('phone_number')
    customer.address=data.get('address')
    customer.pincode=data.get('pincode')

    db.session.commit()
    return jsonify({'message':'Customer Profile updated successfully'}), 200


@app.route('/api/service-professionals_profile/<int:professional_id>',methods=['GET'])
@jwt_required()
def get_professional_update_profile(professional_id):
    current_user=get_jwt_identity()
    role=current_user['role']
    if role!='service_professional':
        return jsonify({'message':'Unauthorized access'}),403
    professional=ServiceProfessional.query.get(professional_id)
    if not professional:
        return jsonify({'message':'Professional not found'}), 404
    
    professional_data={
        'username':professional.username,
        'password':professional.password,
        'fullname':professional.fullname,
        'phone_number':professional.phone_number,
        'experience':professional.experience,
        'address':professional.address,
        'pincode':professional.pincode,
    }

    return jsonify({'professional_data':professional_data}), 200

@app.route('/api/professional_update_profile/<int:professional_id>',methods=['PUT'])
@jwt_required()
def update_professional(professional_id):
    current_user=get_jwt_identity()
    role=current_user['role']
    if role!='service_professional':
        return jsonify({'message':'Unauthorized access'}),403
    data=request.get_json()
    professional=ServiceProfessional.query.get(professional_id)
    if not professional:
        return jsonify({'error':'Customer not found'}),404
    
    professional.username=data.get('username')
    professional.password=data.get('password')
    professional.fullname=data.get('fullname')
    professional.phone_number=data.get('phone_number')
    professional.experience=data.get('experience')
    professional.address=data.get('address')
    professional.pincode=data.get('pincode')

    db.session.commit()
    return jsonify({'message':'Professional Profile updated successfully'}), 200

@app.route('/api/professional/delete_service_package/<int:pkg_id>',methods=['DELETE'])
@jwt_required()
def delete_service_package(pkg_id):

    try:
        current_user=get_jwt_identity()
        role=current_user['role']
        if role!='service_professional':
            return jsonify({'message':'Unauthorized access'}),403
        booked_requests=BookedServiceRequest.query.filter_by(package_id=pkg_id).all()

        for request in booked_requests:
            if request.status=='accepted':
                return jsonify({'message':'This package cannot be deleted because it is booked by a customer'})

        for request in booked_requests:
            db.session.delete(request)
        
        service_package=Service.query.get(pkg_id)
        if service_package:
            db.session.delete(service_package)
            db.session.commit()
            return jsonify({'message':'Package and assosciated requests deleted successfully'}),200
        else:
            return jsonfiy({"message":"Service Package not found"}),404
    except Exception as e:
        db.session.rollback()
        return jsonify({'message':'An error occurred: '+str(e)}),500

@app.route('/api/about', methods=['GET'])
def get_about_page():
    data = {}

    
    cached_professionals = redis_client.get('service_professionals_by_type') 
    cached_requests = redis_client.get('service_requests_by_type')
    cached_packages = redis_client.get('service_packages_by_type')
    cached_homefix = redis_client.get('homefix_packages_by_type')

    
    data['service_professionals'] = json.loads(cached_professionals) if cached_professionals else get_service_professionals_by_type().get_json()
    data['service_requests'] = json.loads(cached_requests) if cached_requests else get_service_requests_by_type().get_json()
    data['service_packages'] = json.loads(cached_packages) if cached_packages else get_service_packages_by_type().get_json()
    data['homefix_packages'] = json.loads(cached_homefix) if cached_homefix else get_homefix_packages_by_type().get_json()

    
    about_info = {
        'description': "Welcome to our wonderful Household Services App! Here, we pride ourselves on connecting you with highly skilled, dedicated professionals ready to assist with everything from plumbing to painting.",
        'data_summary': data,
        'note': "All data here represents a fresh snapshot of active professionals, ongoing requests, and service packages available."
    }

    return jsonify(about_info)

@app.route('/api/service_requests/requested', methods=['GET'])
@jwt_required()
def get_requested_service_requests():

    try:
        current_user=get_jwt_identity()
        role=current_user['role']
        if role!='customer':
            return jsonify({'message':'Unauthorized access'}),403
        
        service_requests = ServiceRequest.query.filter_by(service_status='requested').all()
        requests_list = [
            {
                "id": req.id,
                "customer_id": req.customer_id,
                "professional_id": req.professional_id,
                "date_of_request": req.date_of_request,
                "description": req.description,
                "price": req.price
            }
            for req in service_requests
        ]
        return jsonify({"service_requests": requests_list}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/service_requests/<int:request_id>/update', methods=['PUT'])
@jwt_required()
def update_service_request(request_id):
    data = request.get_json()
    try:
       
        current_user=get_jwt_identity()
        role=current_user['role']
        if role!='customer':
            return jsonify({'message':'Unauthorized access'}),403
        service_request = ServiceRequest.query.get(request_id)
        if not service_request:
            return jsonify({"error": "Service request not found"}), 404
        
        
        if 'description' in data:
            service_request.description = data['description']
        if 'price' in data:
            service_request.price = data['price']
        if 'date_of_request' in data:
            service_request.date_of_request = datetime.strptime(data['date_of_request'], '%Y-%m-%d')
        
        
        db.session.commit()
        return jsonify({"message": "Service request updated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route('/api/professional/<int:professional_id>/reviews', methods=['GET'])

def get_professional_reviews(professional_id):

    service_requests = ServiceRequest.query.filter_by(professional_id=professional_id,service_status='closed').all()
    booked_service_requests = BookedServiceRequest.query.filter_by(professional_id=professional_id,status='closed').all()
    admin_service_packages = BookedAdminServicePackage.query.filter_by(service_professional_id=professional_id,status='closed').all()

    reviews = []
    for req in service_requests:
        reviews.append({
            'type': 'Service Request',
            'rating': req.rating,
            'review': req.remarks,
            'customer_id': req.customer_id
        })

    for req in booked_service_requests:
        reviews.append({
            'type': 'Booked Service Request',
            'rating': req.rating,
            'review': req.remarks,
            'customer_id': req.customer_id
        })

    for package in admin_service_packages:
        reviews.append({
            'type': 'Booked Admin Service Package',
            'rating': package.rating,
            'review': package.remarks,
            'customer_id': package.customer_id
        })

    return jsonify({'reviews': reviews})

@app.route('/api/customer/<int:customer_id>/reviews',methods=['GET'])
def get_customer_reviews(customer_id):

    service_requests = ServiceRequest.query.filter_by(customer_id=customer_id,service_status='closed').all()
    booked_service_requests = BookedServiceRequest.query.filter_by(customer_id=customer_id,status='closed').all()
    admin_service_packages = BookedAdminServicePackage.query.filter_by(customer_id=customer_id,status='closed').all()

    reviews = []
    for req in service_requests:
        reviews.append({
            'type': 'Service Request',
            'View': req.complaint,
            'professional_id': req.professional_id
        })

    for req in booked_service_requests:
        reviews.append({
            'type': 'Booked Service Request',
            'View': req.complaint,
            'professional_id': req.professional_id
        })

    for package in admin_service_packages:
        reviews.append({
            'type': 'Booked Admin Service Package',
            'View': package.complaint,
            'professional_id': package.service_professional_id
        })

    return jsonify({'reviews': reviews})

@app.route('/api/service_requests_report_customer/<int:request_id>/update',methods=['PUT'])
@jwt_required()
def update_service_requests_report_customer(request_id):
    data = request.get_json()
    try:
        
        current_user=get_jwt_identity()
        role=current_user['role']
        if role!='service_professional':
            return jsonify({'message':'Unauthorized access'}),403
        service_request = ServiceRequest.query.get(request_id)
        if not service_request:
            return jsonify({"error": "Service request not found"}), 404
        
       
        if service_request.is_complaint:
            return jsonify({'message':'Already rated the customer'})

        if 'complaint' in data:
            service_request.complaint = data['complaint']
            service_request.is_complaint=True
        
       
        db.session.commit()
        return jsonify({"message": "Service request updated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route('/api/service_package_report_customer/<int:request_id>/update',methods=['PUT'])
@jwt_required()
def update_service_package_report_customer(request_id):
    data = request.get_json()
    try:
        
        current_user=get_jwt_identity()
        role=current_user['role']
        if role!='service_professional':
            return jsonify({'message':'Unauthorized access'}),403
        booked_service_request = BookedServiceRequest.query.get(request_id)
        if not booked_service_request:
            return jsonify({"error": "Booked Service Request not found"}), 404

        if booked_service_request.is_complaint:
            return jsonify({'message':'Already rated the customer'})
        
        
        if 'complaint' in data:
            booked_service_request.complaint = data['complaint']
            booked_service_request.is_complaint=True
        
        
        db.session.commit()
        return jsonify({"message": "Booked Service Request updated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route('/api/homefix_package_report_customer/<int:request_id>/update',methods=['PUT'])
@jwt_required()
def update_homefix_package_report_customer(request_id):
    data = request.get_json()
    try:
        
        current_user=get_jwt_identity()
        role=current_user['role']
        if role!='service_professional':
            return jsonify({'message':'Unauthorized access'}),403
        homefix_service_request = BookedAdminServicePackage.query.get(request_id)
        if not homefix_service_request:
            return jsonify({"error": "Homefix Package not found"}), 404

        if homefix_service_request.is_complaint:
            return jsonify({'message':'Already rated the customer'})
        

        
        if 'complaint' in data:
            homefix_service_request.complaint = data['complaint']
            homefix_service_request.is_complaint=True
        
        
        db.session.commit()
        return jsonify({"message": "Homefix Package updated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500



@app.route('/api/service_requests/<int:request_id>/location',methods=['GET'])
@jwt_required()
def get_service_request_location(request_id):
    current_user=get_jwt_identity()
    role=current_user['role']
    if role!='service_professional':
        return jsonfiy({'message':'Unauthorized access'}),403

    service_request=ServiceRequest.query.get(request_id)
    if not service_request:
        return jsonify({'error':'Service Request not found'}),404

    location={
        'latitude':service_request.customer.latitude,
        'longitude':service_request.customer.longitude
    }

    return jsonify({'location':location}),200

@app.route('/api/booked_packages/<int:booked_service_request_id>/location',methods=['GET'])
@jwt_required()
def get_booked_service_request_location(booked_service_request_id):
    current_user=get_jwt_identity()
    role=current_user['role']
    if role!='service_professional':
        return jsonfiy({'message':'Unauthorized access'}),403

    booked_service_request=BookedServiceRequest.query.get(booked_service_request_id)
    if not booked_service_request:
        return jsonify({'error':'Booked Service Request not found'}),404

    location={
        'latitude':booked_service_request.customer.latitude,
        'longitude':booked_service_request.customer.longitude
    }

    return jsonify({'location':location}),200

@app.route('/api/admin_requests/<int:package_id>/location',methods=['GET'])
@jwt_required()
def get_admin_service_request_location(package_id):
    current_user=get_jwt_identity()
    role=current_user['role']
    if role!='service_professional':
        return jsonfiy({'message':'Unauthorized access'}),403

    booked_admin_service_request=BookedAdminServicePackage.query.get(package_id)
    if not booked_admin_service_request:
        return jsonify({'error':'HomeFix Package not found'}),404

    location={
        'latitude':booked_admin_service_request.customer.latitude,
        'longitude':booked_admin_service_request.customer.longitude
    }

    return jsonify({'location':location}),200

@celery_app.task()
def send_whatsapp_notifications():
    try:
        service_requests=ServiceRequest.objects.filter(service_status='Requested').all()
        for request in service_requests:
            professional=request.professional
            send_whatsapp_message.delay(professional,"Service Request",{
                "description":request.description,
                "customer_name":request.customer.full_name,
                "customer_address":request.customer.address,
                "customer_pincode":request.customer.pincode
            })

        booked_service_requests=BookedServiceRequest.objects.filter(status='pending').all()
        for request in booked_service_requests:
            professional=request.professional
            send_whatsapp_message.delay(professional,"Service Packages",{
                "description":request.description,
                "customer_name":request.customer.full_name,
                "customer_address":request.customer.address,
                "customer_pincode":request.customer.pincode
            })

        booked_admin_service_requests=BookedAdminServicePackage.objects.filter(status='requested').all()
        for request in booked_admin_service_requests:
            professional=request.professional
            send_whatsapp_message.delay(professional,"HomeFix Packages",{
                "description":request.description,
                "customer_name":request.customer.full_name,
                "customer_address":request.customer.address,
                "customer_pincode":request.customer.pincode
            })
        
    except Exception as e:
            print(f"Error occurred while sending whatsapp messages: {str(e)} ")



with app.app_context():
    db.create_all()

if __name__ == '__main__':
    db.init_app()
    app.run(port=8000,debug=True)

