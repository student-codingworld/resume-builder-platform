from django.test import TestCase, Client
from .models import Resume
import json

class ResumeTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.resume_data = {
            "full_name": "John Doe",
            "email": "john@example.com",
            "phone": "1234567890",
            "skills": [{"category": "Languages", "items": "Python, Django"}],
            "experience": [{"title": "Dev", "company": "A", "date": "2022", "location": "NY", "description": ["Did stuff"]}],
            "education": [{"institution": "Uni", "degree": "BS", "date": "2020", "location": "NY", "grade": "4.0"}],
            "projects": [{"title": "Proj 1", "tech": "React", "link": "http://a.com", "description": ["Built it"]}],
            "certifications": ["Cert A"],
            "github_url": "http://github.com/john",
            "linkedin_url": "http://linkedin.com/in/john"
        }
        self.resume = Resume.objects.create(**self.resume_data)

    def test_create_resume(self):
        response = self.client.post('/api/create/', self.resume_data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('id' in response.json())

    def test_list_resumes(self):
        response = self.client.get('/api/list/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.json()) >= 1)

    def test_view_resume(self):
        response = self.client.get(f'/api/view/{self.resume.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['full_name'], "John Doe")

    def test_download_resume(self):
        response = self.client.get(f'/api/download/{self.resume.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')

    def test_view_resume_not_found(self):
        response = self.client.get('/api/view/9999/')
        self.assertEqual(response.status_code, 404)

    def test_download_resume_not_found(self):
        response = self.client.get('/api/download/9999/')
        self.assertEqual(response.status_code, 404)
