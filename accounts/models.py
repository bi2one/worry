from django.db import models
from django.contrib.auth.models import User

import base64, hashlib, random

def getHashCode():
    return base64.b64encode(hashlib.sha256(str(random.getrandbits(256))).digest(),
                            random.choice(['rA','aZ','gQ','hH','hG','aR','DD'])).rstrip('==')

class FindPasswordHash(models.Model) :
    user = models.ForeignKey(User)
    hashcode = models.CharField(max_length=255, default=getHashCode())

    created = models.DateTimeField(auto_now_add=True)
