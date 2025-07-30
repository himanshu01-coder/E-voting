from django.contrib import admin
from .models import UserRegister, Candidate, Vote, AllowedVoterID

admin.site.register(Candidate)
admin.site.register(Vote)
admin.site.register(UserRegister)
admin.site.register(AllowedVoterID)
