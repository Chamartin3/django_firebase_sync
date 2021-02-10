from django.db import models

from django.contrib.auth.models import BaseUserManager 


class SyncAuthMixin:
    # firebase_app = 
    firebase_id = models.CharField(blank=True, null=True, max_length=90)
    def set_firebase_password(self, password):
        return self.firebase_app.update_user(self.firebase_id, password=password)

    def set_password(self, password):
        if self.firebase_id:
            self.set_firebase_password(password)
        elif self.email:
            self.get_firebase_user(password)
        return super(User,self).set_password(password)

    def get_firebase_user(self, password=None):
        fuser = self.firebase_app.get_or_create_user(email=self.email, password=password)
        if self.firebase_id is None:
            self.firebase_id = fuser.uid
            self.save()
        return fuser
    
    def sync_firebase_profile(self):

        fprofile = self.get_firebase_user()

        if fprofile.display_name:
            name, *lnames = fprofile.display_name.split(' ')
            lnames = ' '.join(lnames)

            if not self.first_name:
                self.first_name = name
            
            if not self.last_name:
                self.last_name = lnames
        
            self.save()

    @property
    def firebase_user(self):    
        return self.firebase_app.get_user(id=self.firebase_id)

    @property
    def firebase_user_token(self):
        return self.firebase_app.get_token(self.firebase_user)




class ExternalAppMixin:

    @property
    def firebase_user(self):
        if self.rol == '0':
            return  firebase_app.get_or_create_user(email=self.email)
        return None

    @property
    def login_firebase(self, game=None):
        if self.petroleo_user is None:
            return None
        app_login = firebase_app.login_url(self.petroleo_user)
        if game:
            return f'{app_login}&game={game}'
        return app_login
    
    def delete_fuirebase_user(self):
        try:
            user = firebase_app.get_user(email=self.email)
        except Exception as e:
            print(e)
            return False
        firebase_app.delete_user(uid=user.uid)
        return True


    @property
    def fullname(self):
        return f'{self.first_name} {self.last_name}'