"""
Django management command to populate the database with sample data.
"""
from django.core.management.base import BaseCommand
from core.models import User, Doctor, Patient, Appointment, Prescription, Invoice, Payment, MedicalRecord, Operation, Leave
from django.utils import timezone
from datetime import timedelta
import random


class Command(BaseCommand):
    help = 'Populate the database with sample data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating sample data...')
        
        # Create admin if not exists
        if not User.objects.filter(username='admin').exists():
            admin = User.objects.create_superuser(
                username='admin',
                email='admin@hospital.com',
                password='admin123',
                user_type='admin',
                first_name='Admin',
                last_name='User'
            )
            self.stdout.write(self.style.SUCCESS('Admin user created: admin / admin123'))
        
        # Create doctors
        specialties = ['Cardiology', 'Neurology', 'Orthopedics', 'Pediatrics', 'Dermatology', 
                      'General Medicine', 'Ophthalmology', 'ENT', 'Psychiatry', 'Gynecology']
        
        doctor_count = 0
        for i in range(1, 31):
            username = f'doctor{i}'
            if not User.objects.filter(username=username).exists():
                first_names = ['John', 'Sarah', 'Michael', 'Emma', 'David', 'Lisa', 'Robert', 
                             'Jennifer', 'William', 'Maria', 'James', 'Patricia', 'Richard', 
                             'Linda', 'Thomas', 'Barbara', 'Charles', 'Susan', 'Daniel', 'Jessica',
                             'Matthew', 'Karen', 'Anthony', 'Nancy', 'Mark', 'Betty', 'Donald', 
                             'Helen', 'Steven', 'Dorothy']
                last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller',
                            'Davis', 'Rodriguez', 'Martinez', 'Hernandez', 'Lopez', 'Gonzalez',
                            'Wilson', 'Anderson', 'Thomas', 'Taylor', 'Moore', 'Jackson', 'Martin',
                            'Lee', 'Perez', 'Thompson', 'White', 'Harris', 'Sanchez', 'Clark', 
                            'Ramirez', 'Lewis', 'Robinson']
                
                first_name = random.choice(first_names)
                last_name = random.choice(last_names)
                specialty = random.choice(specialties)
                
                user = User.objects.create_user(
                    username=username,
                    email=f'{username}@hospital.com',
                    password='doctor123',
                    user_type='doctor',
                    first_name=first_name,
                    last_name=last_name
                )
                
                Doctor.objects.create(
                    user=user,
                    specialty=specialty,
                    experience=random.randint(1, 20),
                    qualification='MD, ' + specialty,
                    consultation_fee=random.randint(500, 2000),
                    available=True
                )
                doctor_count += 1
        
        self.stdout.write(self.style.SUCCESS(f'Created {doctor_count} doctors'))
        
        # Create patients
        patient_count = 0
        for i in range(1, 64):
            username = f'patient{i}'
            if not User.objects.filter(username=username).exists():
                first_names = ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve', 'Frank', 'Grace', 
                             'Henry', 'Ivy', 'Jack', 'Kate', 'Liam', 'Mia', 'Noah', 'Olivia',
                             'Paul', 'Quinn', 'Rachel', 'Sam', 'Tina', 'Uma', 'Victor', 'Wendy',
                             'Xavier', 'Yara', 'Zack', 'Amy', 'Ben', 'Chloe', 'David', 'Eva',
                             'Felix', 'Gina', 'Harry', 'Iris', 'Jake', 'Kelly', 'Leo', 'Maya',
                             'Nathan', 'Oscar', 'Pam', 'Quentin', 'Rosa', 'Steve', 'Tara', 'Umar',
                             'Vera', 'Wade', 'Xena', 'Yusuf', 'Zara', 'Andy', 'Bella', 'Chris',
                             'Dora', 'Eric', 'Fiona', 'George', 'Hannah', 'Ian', 'Julia', 'Kevin']
                last_names = ['Anderson', 'Baker', 'Clark', 'Davis', 'Evans', 'Foster', 'Green',
                            'Hill', 'Irving', 'Jackson', 'King', 'Lewis', 'Martin', 'Nelson',
                            'Oliver', 'Parker', 'Quinn', 'Roberts', 'Scott', 'Taylor', 'Underwood',
                            'Vaughn', 'Ward', 'Xavier', 'Young', 'Zimmerman']
                
                first_name = random.choice(first_names)
                last_name = random.choice(last_names)
                
                user = User.objects.create_user(
                    username=username,
                    email=f'{username}@email.com',
                    password='patient123',
                    user_type='patient',
                    first_name=first_name,
                    last_name=last_name
                )
                
                Patient.objects.create(
                    user=user,
                    date_of_birth=timezone.now().date() - timedelta(days=random.randint(7300, 29200)),
                    gender=random.choice(['M', 'F']),
                    blood_group=random.choice(['A+', 'A-', 'B+', 'B-', 'O+', 'O-', 'AB+', 'AB-']),
                    phone=''.join([str(random.randint(0, 9)) for _ in range(10)]),
                    address=f'{random.randint(1, 999)} Main Street, City'
                )
                patient_count += 1
        
        self.stdout.write(self.style.SUCCESS(f'Created {patient_count} patients'))
        
        # Create appointments
        doctors = Doctor.objects.all()
        patients = Patient.objects.all()
        
        if doctors and patients:
            for i in range(50):
                Appointment.objects.create(
                    patient=random.choice(patients),
                    doctor=random.choice(doctors),
                    appointment_date=timezone.now() + timedelta(days=random.randint(-30, 30)),
                    appointment_time=f'{random.randint(9, 17)}:00',
                    status=random.choice(['pending', 'confirmed', 'completed', 'cancelled']),
                    symptoms=f'Symptoms for appointment {i+1}',
                    notes=f'Notes for appointment {i+1}'
                )
            self.stdout.write(self.style.SUCCESS('Created 50 appointments'))
        
        self.stdout.write(self.style.SUCCESS('Sample data population completed!'))
