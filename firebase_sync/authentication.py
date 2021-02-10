# Python
import os

# Django
from django.conf import settings
from django.utils import timezone


# Django Rest Framework
from rest_framework import authentication
from rest_framework import exceptions

# Exceptions
from .exceptions import FirebaseError
from .exceptions import InvalidAuthToken
from .exceptions import NoAuthToken

# Firebase Auth
from firebase_admin import auth




def link_firebase_user(UserModel,uid, email, password):
    msg = None
    try:
        user = UserModel.objects.get(email=email)
        print('Email encontrado')
        athenticated = authenticate(email=email, password=password)
        if athenticated:
            print('Autneticado! agregando credenciales de firebase')
            # if password is correct
            athenticated.firebase_id = uid
            athenticated.save()
            athenticated.set_firebase_password(password)
            athenticated.sync_firebase_profile()
        else:
            print('Autenticacion requerida')
            msg='Contraseña requerida'
            # password required
            user = None

    except UserModel.DoesNotExist:
        print('Email no encontrado, creando usuario')
        user = User.objects.create_user(email, password=password, firebase_id=uid)
        user.sync_firebase_profile()
        msg='Usuario Creado'
        # User is created
    return user, msg


def crossed_autentication(UserModel, request, email, password):
    token = request.META.get('HTTP_FIREBASE')
    user = None
    decoded_token = None
    message = None

    if token:
        try:
            decoded_token = lms_app.verify_token(token)
            print('Token Decoded')
        except Exception as e:
            user = authenticate(
                email=email, 
                password=password
            )
            if user:
                user.get_firebase_user()

    if decoded_token:
        firebase_id = decoded_token.get('uid')
        firebase_email = decoded_token.get('email')
        try:
            # The user is liked to a local user by firebase ID
            user = User.objects.get(firebase_id=firebase_id)
            print('ID de firebase encontrado')
            providers = [p.provider_id for p in user.firebase_user.provider_data]
            if 'password' not in providers:
                print('password not found in providers')
                user, message = link_firebase_user(firebase_id, user.email, password)

        except UserModel.DoesNotExist:
            user, message = link_firebase_user(firebase_id, firebase_email, password)


    else:
        user = authenticate(email=email, password=password)
        if user:
            user.get_firebase_user()
            user.sync_firebase_profile()

    return user, message

