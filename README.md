# Django Firebase AuthSync

A set of tools that helps to synchronize a Django base authentication, with a firebase autentication. It also provides functions and mixins to extend the main User model an sync it with firebase.

## Initialization

Initia

llize a Django App using the Firebase Class. 

```python
from firebase_sync import FirebaseApp 
fireapp = FirebaseApp('path/to/credentials.json',
                      app_name='default'
                     url='https://app.url.com')
```

This firebase app can now interact in many ways with the firebase app, as an example adding a property to your User Model:

```python

class User(AbstractUser):
    """User model."""
    firebase_app = fireapp
    firebase_id = models.CharField(blank=True, null=True, max_length=90, unique=True)
    def get_firebase_user(self, password=None):
        user = self.firebase_app.get_or_create_user(email=self.email, password=password)
        if self.firebase_id is None:
            self.firebase_id = user.uid
            self.save()
        return user
```

You could also make use of the mixins.

```python
from firebase_sync.mixins import SyncAuthMixin,  ExternalAppMixin

class User(SyncAuthMixin, AbstractUser):
    """Sincronizes the internal user model with firebase user"""
   

class User(ExternalAppMixin, AbstractUser):
    """Gets the autentication indormation ."""
```

Automatic Login syncronization

```python
from firebase_sync.autentication import crossed_autentication
class AuthView(APIView):

    def post(self, request, *args, **kwargs):
        """ Login a traves de una petición Ajax"""
        email = request.data.get('email'),
        password = request.data.get('password')
        user, message = crossed_autentication(request,email,password)
        if user is not None:
            if user.is_active:
                login(request, user)
                display_message = message if message is not None else "Éxito"
                return Response({'message':display_message}, status=202)
            else:
                return Response({'message':"Este Usuario se encuentra inactivo o bloqueado, contacte a un adminitrador para mas información"}, status=401)
        else:
            display_message = message if message is not None else "Combinación de usuario y contraseña incorrecto"
            return Response({'message':display_message}, status=401)
```



## API

**FirebaseApp**

- login_url : creates a link to login through token autentcation
- verify_token: verifyes the user token
- get_users: returns an users dictionary list created
- get_or_create_user: recieves an email or en uid to retrieve or create an user
- delete_user: deletes firebase user
- update_user: updates an user.