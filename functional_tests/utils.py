from django.contrib.auth import get_user_model
User = get_user_model()


def create_user(email='foo@email.com', password='Abc123456789'):
    return User.objects.create_user(username=email,
                                    email=email,
                                    password=password)
