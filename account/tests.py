from django.test import TestCase,Client
from django.urls import reverse
import json
from rest_framework import status
from .models import User
from .serializers import RegisterSerializer,LoginSerializer
from django.contrib.auth.hashers import make_password
from .views import send_verification_email,generate_verification_token
from django.core import mail
from django.conf import settings
from django.contrib.auth import get_user_model
from unittest.mock import patch
from rest_framework_simplejwt.tokens import RefreshToken
import jwt
# Create your tests here.
class AuthenticationTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.signup_url = reverse('register')
        self.login_url = reverse('login')
        #self.verify_email_url =  reverse('verify_email')
        self.verify_email_url = reverse('verify_email', kwargs={'token': 'dummy_token'})

        self.valid_user_data = {
            "firstname":"Stephen",
            "lastname":"Omondi",
            "email":"stephenondeyo0@gmail.com",
            "username":"Stephen8865",
            "password":"Kundan@123456",
            "course":"BSc Computer Science"
        }

        self.login_data = {
            "email":"stephenondeyo0@gmail.com",
            "password":"Kundan@123456"
        }
    
    def test_valid_signUp(self):
        response = self.client.post(
            self.signup_url,
            data = json.dumps(self.valid_user_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        #self.assertFalse(User.objects.get(email=self.valid_user_data['email']).is_active)
        print(response.status_code)
        print(response.json())



    def test_duplacate_email_signup(self):
        # First signup
        self.client.post(
            self.signup_url,
            data=json.dumps(self.valid_user_data),
            content_type='application/json'
        )
        # Duplicate Signup
        response = self.client.post(
            self.signup_url,
            data=json.dumps(self.valid_user_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
    
    def test_login_without_verification(self):
        # Create unverified user with properly hashed password
        User.objects.create(
            username = self.valid_user_data['username'],
            email = self.valid_user_data['email'],
            password = make_password(self.valid_user_data['password']),
            is_active = False
        )

        # Attempt login
        response = self.client.post(
            self.login_url,
            data=json.dumps(self.login_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)
    
    def test_login_after_verification(self):
        # Create user  with properly hashed password and set is_active to True
        User.objects.create(
            username = self.valid_user_data['username'],
            email = self.valid_user_data['email'],
            password = make_password(self.valid_user_data['password']),
            is_active = True
        )
        # Login attempt with verified user credentials
        login_data = {
            'email':'stephenondeyo0@gmail.com',
            'password':'Kundan@123456'    
        }
        response = self.client.post(
            self.login_url,
            data=json.dumps(login_data),
            content_type='application/json'
        )
        # Assert successful login
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data['data'])
        self.assertIn('refresh', response.data['data'])
        self.assertEqual(response.data['message'], 'Login successfull')
        

    def test_password_validation(self):
        invalid_data = self.valid_user_data.copy()
        invalid_data['password'] = 'weak'
        response = self.client.post(
            self.signup_url,
            data=json.dumps(invalid_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
    
    def test_required_fields(self):
        for field in ['firstname','lastname','email','password']:
            invalid_data = self.valid_user_data.copy()
            del invalid_data[field]
            response = self.client.post(
                self.signup_url,
                data=json.dumps(invalid_data),
                content_type='application/json'
            )
            self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)

class EmailVerificationTest(TestCase):
    def setUp(self):
        self.User = get_user_model()
        self.user_data = {
            'email':'test@example.com',
            'password':'Testpass@1234',
            'username':'testuser123'
        }
        self.user = self.User.objects.create_user(**self.user_data)

    def test_generate_verification_token(self):
        """"Test that a valid jwt token in generated for a user"""
        token = generate_verification_token(self.user)

        # verify that the token is a valid JWT
        try:
            decode_token = jwt.decode(
                token,settings.SECRET_KEY,
                algorithms=['HS256']
            )
            self.assertEqual(decode_token['user_id'],self.user.id)
        except jwt.InvalidTokenError:
            self.fail("Generated token is not a valid JWT")
    
    def test_send_verification_email(self):
        """Test that verification email is sent with correct content"""
        # clear the test outbox
        mail.outbox = []

            # Create a mock request object if needed
        from django.test.client import RequestFactory
        request = RequestFactory().get('/')

        # send verification email
        send_verification_email(request,self.user)


        # verify email content
        email = mail.outbox[0]
        self.assertEqual(email.subject,"Email Verification")
        self.assertEqual(email.from_email,settings.DEFAULT_FROM_EMAIL)
        self.assertEqual(email.to,[self.user.email])

