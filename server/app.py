from flask import Flask, request, jsonify, make_response
from flask_migrate import Migrate
from flask_restful import Resource, Api, reqparse
from models import db, User,Patient,Doctor,Department,Appointment
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, create_access_token,unset_jwt_cookies
from flask_cors import CORS, cross_origin
from flask_bcrypt import Bcrypt
from datetime import datetime
# from cloudinary.uploader import upload
# from cloudinary.utils import cloudinary_url



app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///nile_hospital.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.json.compact = False

app.secret_key = 'secret key'
app.config['JWT_SECRET_KEY'] = "b'\x03\xa3\x8c\xb3\n\xf4\x16aFh\xc5'"

db.init_app(app)

migrate = Migrate(app, db)
api = Api(app)
jwt = JWTManager(app)
bcrypt = Bcrypt(app)


class UserRegister(Resource):
    @cross_origin()
    def post (self):
        data = request.get_json()
        print(data)
        username = data.get("username")
        email = data.get("email")
        password = str(data.get("password"))
        role = data.get("role")
        
        
        print(f"This is {data}")
        
        #check if the user exists
        user_exists = User.query.filter(User.username==username) 
        
        # if user_exists:
        #     return jsonify({"Error":"User exists"})
        
        # if password and confirm_password doesn't match
        # if password != confirm_password:
        #     return jsonify({"Error":"Password and confirm_password don't match"})
        
        # creating encrypted passwords
        hashed_password = bcrypt.generate_password_hash(password)
       
        
        access_token = create_access_token(identity=username)
        # User.access_token = access_token
        
        new_user = User(
           username = username,
           email = email,
           password = hashed_password,
           role = role
            
        )
        db.session.add(new_user)
        db.session.commit()
        
        return jsonify({
            "id":"new_user.id",
            "username":"new_user.username",
            "access_token":access_token,
            "token":access_token
            
        })
        
api.add_resource(UserRegister,"/user/register")  

class UserLogin(Resource):
    def post(self):
        data = request.get_json()
        print(data)
        
        email = data.get("email")
        password = str(data.get("password"))

        user = User.query.filter_by(email=email).first()

        if user is None:
            return jsonify({'error': 'Unauthorized'}), 401

        if not bcrypt.check_password_hash(user.password, password):
            return jsonify({'error': 'Unauthorized, incorrect password'}), 401
        
        access_token = create_access_token(identity=email)
        user.access_token = access_token


        return jsonify({
            "id": user.id,
            "email": user.email,
            "access_token": user.access_token,
            "username": user.username,
            "role":user.role
        
        })
        
api.add_resource(UserLogin,"/user/login")         
    




class Logout(Resource):
    @jwt_required()
    def post(self):
        unset_jwt_cookies()
        return{"message":"Successfully logged out"} 
    
api.add_resource(Logout,"/user/logout") 

class Users(Resource):
    def get(self):
        users = [user.to_dict(only=('id', 'username', 'email',"role")) for user in User.query.all()]
        print("im a user", users)
        return make_response(jsonify(users),200)
    
api.add_resource(Users,"/users")     

class UserByID(Resource):

    def get(self,id):
        user = User.query.filter(User.id==id).first()

        if user:
            return make_response(jsonify(user.to_dict(only=("id","username","email","role"))),200) 

    def patch(self,id):

        data = request.get_json()

        user = User.query.filter(User.id==id).first()

        for attr in data:
            setattr(user,attr,data.get(attr)) 

        db.session.add(user)
        db.session.commit()

        return make_response(user.to_dict(only=("id","email","username","role")),200)

    def delete(self,id):

        user = User.query.filter(User.id==id).first()

        if user:
            db.session.delete(user)
            db.session.commit()
            return make_response("",204)
        else:
            return make_response(jsonify({"error":"User not found"}),404) 
        
api.add_resource(UserByID,"/users/<int:id>")    

class Patients(Resource):
    def get(self):
        patients = [patient.to_dict(only=("id", "first_name", "last_name", "phone","date_of_birth","gender","address")) for patient in Patient.query.all()]

        return make_response(patients, 200)
    
    def post(self):
        
        data = request.get_json()
        
        try:
            new_patient = Patient(
                first_name = data.get("first_name"),
                last_name = data.get("last_name"),
                phone = data.get("phone"),
                date_of_birth = datetime.strptime(data.get("date_of_birth"), '%Y/%d/%m').date(),
                gender = data.get("gender"),
                address = data.get("address")
                )
            db.session.add(new_patient)
            db.session.commit()
            
        except ValueError:
            return make_response(jsonify({"error":["validation errors"]})) 
        
        return make_response(new_patient.to_dict(only=("id", "first_name", "last_name", "phone","date_of_birth","gender","address")))
    
api.add_resource(Patients,"/patients")    

class PatientByID(Resource):
    def get(self,id):
        
        patient =   Patient.query.filter(Patient.id==id).first()
        
        if patient:
            return make_response(patient.to_dict(only=("id", "first_name", "last_name", "phone","date_of_birth","gender","address")) )
        else :
            return make_response(jsonify({"error":"Patient not found"}),404)
        
    def patch(self,id):
        

        data = request.get_json()

        patient = Patient.query.filter(Patient.id==id).first()

        for attr in data:
            setattr(patient,attr,data.get
                    (attr)) 

        db.session.add(patient)
        db.session.commit()

        return make_response(patient.to_dict(only=("id", "first_name", "last_name", "phone","date_of_birth","gender","address")),200)

    def delete(self,id):

        patient = Patient.query.filter(Patient.id==id).first()

        if patient:
            db.session.delete(patient)
            db.session.commit()
            return make_response("Patient Successfully deleted",204)
        else:
            return make_response(jsonify({"error":"Patient not found"}),404)
            
        
api.add_resource(PatientByID,"/patient/<int:id>")    

class Doctors(Resource):
    def get(self):
        doctors = [doctors.to_dict(only=('id','first_name', 'last_name', 'phone','email',"speciality",'gender','image_url')) for doctors in Doctor.query.all()]
        return make_response(doctors,200)
    
    def post(self):
        data = request.get_json()
        
        try:
            new_doctor = Doctor(
                first_name = data.get("first_name"),
                last_name = data.get("last_name"),
                phone = data.get("phone"),
                email = data.get("email"),
                speciality = data.get("speciality"),
                gender = data.get("gender"),
                image_url = data.get("image_url"),
                department_id = data.get("department_id")
               
                )
            db.session.add(new_doctor)
            db.session.commit()
            
        except ValueError:
            return make_response(jsonify({"error":["validation errors"]})) 
        
        return make_response(new_doctor.to_dict(only=("id", "first_name", "last_name", "phone","email","speciality","gender","image_url")))
    
    
api.add_resource(Doctors,"/doctors")  

class DoctorByID(Resource):
    def get(self,id):
        doctor = Doctor.query.filter(Doctor.id==id).first()
        
        if doctor:
            return make_response(doctor.to_dict(only=("id", "first_name", "last_name", "phone","email","speciality","gender","image_url")) )
        else :
            return make_response(jsonify({"error":"doctor not found"}),404)
        
    def patch(self,id):
        

        data = request.get_json()

        doctor = Doctor.query.filter(Doctor.id==id).first()

        for attr in data:
            setattr(doctor,attr,data.get(attr)) 

        db.session.add(doctor)
        db.session.commit()

        return make_response(doctor.to_dict(only=("id", "first_name", "last_name", "phone","email","speciality","gender","image_url")) )

    def delete(self, id):
        doctor = Doctor.query.filter(Doctor.id == id).first()

        if doctor:
            db.session.delete(doctor)
            db.session.commit()
            return make_response(jsonify({"message": "Doctor successfully deleted"}), 200)
        else:
            return make_response(jsonify({"error": "Doctor not found"}), 404)
    
        
api.add_resource(DoctorByID,"/doctor/<int:id>")  


class Appointments(Resource):
    def get(self):
        appointments = [appointments.to_dict(only=("id","appointment_date","type_of_appointment","patient_id","doctor_id")) for appointments in Appointment.query.all()]

        return make_response(appointments, 200)
    
    def post(self):
        data = request.get_json()
        
        try:
            new_appointment = Appointment(
                appointment_date = datetime.strptime(data.get("appointment_date"), '%Y/%d/%m').date(),
                type_of_appointment = data.get("type_of_appointment"),
                patient_id = data.get("patient_id"),
                doctor_id = data.get("doctor_id")
            )
            db.session.add(new_appointment)
            db.session.commit()
            
        except ValueError:
            return make_response(jsonify({"error":["validation errors"]})) 
        
        return make_response(new_appointment.to_dict(only=("id", "appointment_date", "type_of_appointment", "patient_id","doctor_id")))   
        
api.add_resource(Appointments,"/appointments")        
          

class Departments(Resource):
    def get(self):
        departments = [departments.to_dict(only=("id","name","number_of_doctors")) for departments in Department.query.all()]

        return make_response(departments, 200)
    
    def post(self):
        data = request.get_json()
        
        try:
            new_department = Department(
                name = data.get("name"),
                number_of_doctors = data.get("number_of_doctors")
            )
            db.session.add(new_department)
            db.session.commit()
            
        except ValueError:
            return make_response(jsonify({"error":["validation errors"]})) 
        
        return make_response(new_department.to_dict(only=("id", "name", "number_of_doctors", )))   
    
api.add_resource(Departments,"/departments") 

class DepartmentByID(Resource):
    def get(self,id):
        department = Department.query.filter(Department.id==id).first()
        
        if department:
            return make_response(department.to_dict(only=("id", "name", "number_of_doctors")) )
        else :
            return make_response(jsonify({"error":"department not found"}),404)
        
    def patch(self,id):
        

        data = request.get_json()

        department = Department.query.filter(Department.id==id).first()

        for attr in data:
            setattr(department,attr,data.get(attr)) 

        db.session.add(department)
        db.session.commit()

        return make_response(department.to_dict(only=("id", "name", "number_of_doctors")) )

    def delete(self, id):
        department = Department.query.filter(Department.id == id).first()

        if department:
            db.session.delete(department)
            db.session.commit()
            return make_response(jsonify({"message": "department successfully deleted"}), 200)
        else:
            return make_response(jsonify({"error": "department not found"}), 404)    
        
api.add_resource(DepartmentByID,"/departments/<int:id>")     

   
        
           
        

  
                  
        

if __name__ == "__main__":
    app.run(port=5555,debug=True) 