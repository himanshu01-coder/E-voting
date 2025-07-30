from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import UserRegister, Candidate, Vote, AllowedVoterID

def fpass(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = UserRegister.objects.get(email__iexact=email)
            send_mail(
                'Password Reset Request',
                f'Hello {user.fullname}, your password is: {user.password}',
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
            messages.success(request, "Check your email for reset instructions.")
        except UserRegister.DoesNotExist:
            messages.error(request, "No account found with that email.")

    return render(request, "fpass.html")


def vote(request):
    if 'user_id' not in request.session:
        return redirect('login')

    user = UserRegister.objects.get(id=request.session['user_id'])

    if Vote.objects.filter(user=user).exists():
        messages.info(request, "You have already voted.")
        return redirect('confirm')

    candidates = Candidate.objects.all()

    if request.method == 'POST':
        candidate_id = request.POST.get('candidate_id')
        candidate = Candidate.objects.get(id=candidate_id)
        Vote.objects.create(user=user, candidate=candidate)
        candidate.votes += 1
        candidate.save()
        return redirect('confirm')

    return render(request, 'vote.html', {'candidates': candidates})


def index(request):
    if 'user_id' not in request.session:
        return redirect('login')
    return render(request, "index.html")


def result(request):
    candidates = Candidate.objects.all()
    total_votes = sum(c.votes for c in candidates)
    return render(request, 'result.html', {'candidates': candidates, 'total_votes': total_votes})


def profile(request):
    if 'user_id' not in request.session:
        return redirect('login')

    user = UserRegister.objects.get(id=request.session['user_id'])

    if request.method == 'POST':
        new_name = request.POST.get('fullname')
        new_email = request.POST.get('email')
        user.fullname = new_name
        user.email = new_email
        user.save()
        messages.success(request, "Profile updated successfully.")

    return render(request, "profile.html", {"user": user})


def confirm(request):
    return render(request, "confirm.html")

def vote1(request):
    return render(request, "vote1.html")

def vote2(request):
    return render(request, "vote2.html")

def vote3(request):
    return render(request, "vote3.html")


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        voter_id = request.POST['voter_id']

        if not AllowedVoterID.objects.filter(voter_id=voter_id).exists():
            messages.error(request, "Invalid Voter ID.")
            return render(request, "login.html")

        try:
            user = UserRegister.objects.get(email=email, password=password, voter_id=voter_id)
            request.session['user_id'] = user.id
            return redirect('index')
        except UserRegister.DoesNotExist:
            messages.error(request, "Wrong email, password, or voter ID.")

    return render(request, "login.html")


def register(request):
    if request.method == 'POST':
        fullname = request.POST['fullname']
        email = request.POST['email']
        voter_id = request.POST['voter_id']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if not AllowedVoterID.objects.filter(voter_id=voter_id).exists():
            messages.error(request, "Voter ID not found in allowed list.")
            return render(request, "register.html")

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, "register.html")

        if UserRegister.objects.filter(email=email).exists() or UserRegister.objects.filter(voter_id=voter_id).exists():
            messages.error(request, "User already exists with this email or voter ID.")
            return render(request, "register.html")

        user = UserRegister(fullname=fullname, email=email, voter_id=voter_id, password=password)
        user.save()
        messages.success(request, "Registered successfully.")
        return redirect("login")

    return render(request, "register.html")


def logout(request):
    request.session.flush()
    return redirect('login')
