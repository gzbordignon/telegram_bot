from django.test import TestCase

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


class MyTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        data_users = [
            {
                'name': 'Fulano de Tal',
                'email': 'fulano@gmail.com',
                'department': 'Back-end',
                'salary': '5000',
                'birth_date': '06-10-1990',
            },
            {
                'name': 'Ciclano de Tal',
                'email': 'ciclano@gmail.com',
                'department': 'DevOps',
                'salary': '10000',
                'birth_date': '03-05-1982',
            },
            {
                'name': 'João da Silva',
                'email': 'joao@gmail.com',
                'department': 'Front-end',
                'salary': '5000',
                'birth_date': '15-08-1992',
            },
        ]

        self.new_employee_data = {
            'name': 'Pedro Silveira',
            'email': 'pedro@gmail.com',
            'department': 'Fullstack',
            'salary': '8000',
            'birth_date': '22-07-1985',
        }

        for employee in data_employees:
            serializer = EmployeeSerializer(data=employee)
            if serializer.is_valid():
                serializer.save()

        self.employees = Employee.objects.all()

        self.first_employee = Employee.objects.first()
