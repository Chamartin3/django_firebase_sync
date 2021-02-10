
import firebase_admin
from firebase_admin import credentials, auth, firestore
from .exceptions import InvalidAuthToken


class FirebaseApp:
    """
    Uses an app to interact with it
    """

    def __init__(self, credentials_path, *args, app_name="default", **kwargs):
        cred = credentials.Certificate(credentials_path)
        self.app = firebase_admin.initialize_app(cred, name=app_name)
        self.baseURL = kwargs['url']


    def verify_token(self, token):
        try:
            decoded_token = auth.verify_id_token(token, app=self.app)
        except Exception:
            raise InvalidAuthToken("Invalid auth token")
            return None
        return decoded_token


    def get_users(self):
        """
        the auth users
        """
        return [{'email': u.email,'id': u.localId } for u in auth.list_users(app=self.app).iterate_all()]

    def get_user(self, **kwargs):
        uid = kwargs.get('id', None)
        if uid:
            return auth.get_user(app=self.app, uid=uid)
        email = kwargs.get('email', None)
        if email:
            return auth.get_user_by_email(app=self.app, email=email)
        raise Exception('User id or Email is required')        
    
    def get_or_create_user(self, **kwargs):
        try:
            return self.get_user(**kwargs)
        except auth.UserNotFoundError:
            email = kwargs.get('email', None)
            if email is None:
                raise Exception('User Email is required')
            return self.create_user(**kwargs)
    
    def create_user(self,**kwargs):
        return auth.create_user(app=self.app, **kwargs)

    def update_user(self, uid, **kwargs):
        return auth.update_user(uid, app=self.app, **kwargs)

    def delete_user(self,**kwargs):
        return auth.delete_user(app=self.app, **kwargs)

    def get_token(self, user):
        return auth.create_custom_token(user)
    
    def login_url(self,user):
        return f'{self.baseURL}?token={self.get_token(user)}'

    def firestore(self):
        return firestore.client(app=self.app)




        
