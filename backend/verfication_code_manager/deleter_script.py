import datetime
import sys
sys.path.append("..")
from users.models import VerficationCode

# script 

def delete_invalid_verification_codes():
    VerficationCode.objects.filter(expire_date__lte=datetime.datetime.now()).delete()