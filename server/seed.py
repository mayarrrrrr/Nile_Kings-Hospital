from faker import Faker
from datetime import datetime
import random
from app import app
from models import db, Doctor, Patient, Appointment, Department, User

fake = Faker()

department_names = [
    "Cardiology",
    "Orthopedics",
    "Neurology",
    "Oncology",
    "Pediatrics",
    "Dermatology",
    "Gynecology",
    "Urology",
    "Ophthalmology",
    "ENT (Ear, Nose, Throat)",
    "Radiology",
    "Emergency Medicine",
    "Anesthesiology",
    "Psychiatry",
    "Physical Therapy",
    "Internal Medicine",
    "Surgery",
    "Pathology",
    "Gastroenterology",
    "Endocrinology"
]

doctor_specializations = [
    "Cardiology",
    "Orthopedic Surgery",
    "Neurology",
    "Oncology",
    "Pediatrics",
    "Dermatology",
    "Gynecology",
    "Urology",
    "Ophthalmology",
    "Ear, Nose, and Throat (ENT)",
    "Radiology",
    "Emergency Medicine",
    "Anesthesiology",
    "Psychiatry",
    "Physical Therapy",
    "Internal Medicine",
    "General Surgery",
    "Pathology",
    "Gastroenterology",
    "Endocrinology",
    "Hematology",
    "Pulmonology",
    "Rheumatology",
    "Infectious Disease",
    "Nephrology",
    "Geriatrics",
    "Cardiothoracic Surgery",
    "Plastic Surgery",
    "Neurosurgery",
    "Oncologic Surgery",
    "Hand Surgery",
    "Vascular Surgery",
    "Bariatric Surgery",
    "Oncologic Pathology",
    "Forensic Pathology",
    "Pediatric Surgery",
    "Hepatology",
    "Reproductive Endocrinology",
    "Allergy and Immunology",
    "Clinical Genetics",
    "Pain Medicine",
    "Sleep Medicine",
    "Sports Medicine",
    "Vascular Medicine",
    "Infectious Disease Medicine",
    "Neurophysiology",
    "Interventional Radiology",
    "Radiation Oncology",
    "Palliative Medicine",
    "Occupational Medicine"
]

appointment_reasons = [
    "Routine Checkup",
    "Follow-up Consultation",
    "Vaccination",
    "Prescription Refill",
    "Blood Test",
    "X-ray or Imaging",
    "Physical Therapy Session",
    "Dental Checkup",
    "Mental Health Counseling",
    "Surgical Consultation",
    "Chronic Disease Management",
    "Pregnancy Monitoring",
    "Allergy Testing",
    "Orthopedic Evaluation",
    "Hearing Test",
    "Eye Examination",
    "Dermatological Evaluation",
    "Cancer Screening",
    "Emergency Room Visit",
    "Second Opinion Consultation"
]

disease_list = [
    "Common Cold",
    "Influenza (Flu)",
    "Pneumonia",
    "Bronchitis",
    "Asthma",
    "Chronic Obstructive Pulmonary Disease (COPD)",
    "Hypertension (High Blood Pressure)",
    "Coronary Artery Disease",
    "Heart Failure",
    "Stroke",
    "Diabetes Mellitus",
    "Hypothyroidism",
    "Hyperthyroidism",
    "Obesity",
    "Arthritis",
    "Osteoporosis",
    "Rheumatoid Arthritis",
    "Gastroesophageal Reflux Disease (GERD)",
    "Peptic Ulcer Disease",
    "Irritable Bowel Syndrome (IBS)",
    "Inflammatory Bowel Disease (IBD)",
    "Gallstones",
    "Kidney Stones",
    "Urinary Tract Infection (UTI)",
    "Benign Prostatic Hyperplasia (BPH)",
    "Erectile Dysfunction (ED)",
    "Anxiety Disorders",
    "Depressive Disorders",
    "Bipolar Disorder",
    "Schizophrenia",
    "Attention Deficit Hyperactivity Disorder (ADHD)",
    "Alzheimer's Disease",
    "Parkinson's Disease",
    "Multiple Sclerosis (MS)",
    "Migraine",
    "Epilepsy",
    "Cancer (Various Types)",
    "Human Immunodeficiency Virus (HIV) Infection",
    "Acquired Immunodeficiency Syndrome (AIDS)",
    "Chlamydia",
    "Gonorrhea",
    "Syphilis",
    "Hepatitis (Various Types)",
    "Tuberculosis (TB)",
    "Malaria",
    "Dengue Fever",
    "Chikungunya Fever",
    "Zika Virus Infection",
    "Ebola Virus Disease",
    "COVID-19 (Coronavirus Disease)"
]

with app.app_context():

    # This will delete any existing rows
    # so you can run the seed file multiple times without having duplicate entries in your database
    print("Deleting data...")
    db.session.query(Appointment).delete()
    db.session.query(Patient).delete()
   
    db.session.query(Doctor).delete()
    db.session.query(Department).delete()
    db.session.query(User).delete()
    
    db.session.commit()

    # Creating departments
    print("Creating departments...")
    departments = []
    for _ in range(20):
        department = Department(
            name=random.choice(department_names),
            
           
            number_of_doctors=fake.random_int(min=1, max=10)
        )
        departments.append(department)

    db.session.add_all(departments)
    db.session.commit()

    # Creating doctors
    print("Creating doctors...")
    doctors = []
    for _ in range(15):
        doctor = Doctor(
            first_name=fake.name(),
            last_name = fake.name(),
            phone = fake.phone_number(),
            email = fake.email(),
            speciality=random.choice(doctor_specializations),
            gender =  random.choice(["female","male"]),
            image_url = random.choice(["https://www.scripps.org/sparkle-assets/preview_thumbnails/news_items/4213/default-7d52a31e13b4e0d9a0a96f291ddbdc98.jpg","https://www.aucmed.edu/sites/g/files/krcnkv361/files/styles/atge_3_2_crop_md/public/2021-11/large-Smile-Guy-web.jpg?h=6b55786a&itok=Wy7cQpYS"]),
            department_id=fake.random_int(min=1, max=30)
        )
        doctors.append(doctor)

    db.session.add_all(doctors)
    db.session.commit()

    

    # Creating patients
    print("Creating patients...")
    patients = []
    for _ in range(30):
        patient = Patient(
            first_name=fake.name(),
            last_name=fake.name(),
            phone = fake.phone_number(),
            date_of_birth=fake.date_time_this_year(before_now=True, after_now=False),
            gender=random.choice(["Male", "Female"]),
            address=fake.name(),
            
        )
        patients.append(patient)

    db.session.add_all(patients)
    db.session.commit()

    # Creating appointments
    print("Creating appointments...")
    appointments = []
    for _ in range(20):
        
        appointment = Appointment(
            appointment_date=fake.date_time_this_year(before_now=True, after_now=False),
            type_of_appointment=random.choice(appointment_reasons),
            patient_id=fake.random_element(elements=[patient.id for patient in patients]),
            doctor_id=fake.random_element(elements=[doc.id for doc in doctors])
            
            
        )
        appointments.append(appointment)

    db.session.add_all(appointments)
    db.session.commit()

    # Creating users
    # print("Creating users...")
    # users = []
    # for _ in range(10):  
    #     user = User(
    #         username=fake.name(),  
    #         _password_hash=fake.password(),
    #     )
    #     users.append(user)

    # db.session.add_all(users)
    # db.session.commit()

    print("Data seeding completed.")