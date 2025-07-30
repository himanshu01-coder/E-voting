from django.db import models

class UserRegister(models.Model):
    fullname = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    voter_id = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.fullname

class Candidate(models.Model):
    name = models.CharField(max_length=100)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class Vote(models.Model):
    user = models.OneToOneField(UserRegister, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.fullname} voted for {self.candidate.name}"

class AllowedVoterID(models.Model):
    voter_id = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.voter_id
