from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
         UserModel = get_user_model()
         print(f"Auth attempt - username: {username}")
         try:
             user = UserModel.objects.get(email=username)
             print(f"User found: {user}")
             if user.check_password(password):
                 print("Password check passed")
                 return user
             print("Password check failed")
         except UserModel.DoesNotExist:
              print("User not found")
         return None