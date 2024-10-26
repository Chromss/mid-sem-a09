import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from .models import Journal
from .jurnalform import JournalForm


@login_required
def journal_home(request):
    journals = Journal.objects.all().order_by('-created_at')  # Urutkan berdasarkan tanggal terbaru
    return render(request, 'main/journal_home.html', {'journals': journals})

@login_required(login_url='/login')
def create_journal(request):
       if request.method == 'POST':
           form = JournalForm(request.POST, request.FILES)
           if form.is_valid():
               journal = form.save(commit=False)
               journal.author = request.user
               journal.save()
               return redirect('main:journal_home')
       else:
           form = JournalForm()
       return render(request, 'main/create_journal.html', {'form': form})

@login_required(login_url='/login')
def like_journal(request, journal_id):
    journal = get_object_or_404(Journal, id=journal_id)
    if request.user in journal.likes.all():
        journal.likes.remove(request.user)
    else:
        journal.likes.add(request.user)
    return redirect('main:journal_home')

@login_required(login_url='/login')
def journal_history(request):
    journals = Journal.objects.filter(author=request.user)
    return render(request, 'main/journal_history.html', {'journals': journals})

def specific_journal(request, journal_id):
    journal = get_object_or_404(Journal, id=journal_id)
    return render(request, 'main/specific_journal.html', {'journal': journal})

@login_required(login_url='/login')
def edit_journal(request, journal_id):
    journal = get_object_or_404(Journal, id=journal_id, author=request.user)
    if request.method == 'POST':
        form = JournalForm(request.POST, request.FILES, instance=journal)
        if form.is_valid():
            form.save()
            return redirect('main:specific_journal', journal_id=journal.id)
    else:
        form = JournalForm(instance=journal)
    return render(request, 'main/edit_journal.html', {'form': form, 'journal': journal})

@login_required(login_url='/login')
def delete_journal(request, journal_id):
    journal = get_object_or_404(Journal, id=journal_id, author=request.user)
    journal.delete()
    return redirect('main:journal_home')

@login_required
def save_journal(request, journal_id):
    journal = get_object_or_404(Journal, id=journal_id)
    SavedJournal.objects.get_or_create(journal=journal, user=request.user)
    return redirect('journal_home')

def journal_detail(request, journal_id):
    journal = get_object_or_404(Journal, id=journal_id)
    return render(request, 'main/spesific_journal.html', {'journal': journal})


def register(request):
    form = UserCreationForm()
    last_login = request.COOKIES.get('last_login', 'Never')

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('main:login')
    context = {'form': form, 'last_login': last_login}
    return render(request, 'register.html', context)

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('main:journal_home')  # Ganti 'home' dengan nama URL halaman utama Anda
        else:
            # Tambahkan pesan error jika login gagal
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    return render(request, 'login.html')

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')
    return response