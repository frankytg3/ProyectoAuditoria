
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class EmailOrUsernameModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            # Intenta obtener el usuario por email
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            try:
                # Si no se encuentra, intenta obtener el usuario por nombre de usuario
                user = UserModel.objects.get(username=username)
            except UserModel.DoesNotExist:
                return None

        # Verifica la contraseña y si el usuario está activo
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
