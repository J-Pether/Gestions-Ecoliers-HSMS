from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.crypto import get_random_string
from .models import Etudiant, Cours, Inscription
from django.core.paginator import Paginator
from .forms import CoursForm
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from .forms import EtudiantForm  # il faut créer ce formulaire pour les étudiants





def admin_required(view_func):
    decorated_view_func = login_required(user_passes_test(lambda u: u.is_superuser)(view_func))
    return decorated_view_func


@admin_required
@login_required
def ajouter_cours(request):
    if request.method == "POST":
        form = CoursForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_cours')
    else:
        form = CoursForm()

    return render(request, 'cours/ajouter.html', {'form': form})

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')  # oubyen 'accueil' si ou vle
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")

    return render(request, 'auth/login.html')



def logout_view(request):
    logout(request)  # dekonekte itilizatè a
    messages.success(request, "Vous êtes déconnecté.")
    return redirect('login')  # voye itilizatè tounen sou login



def accueil(request):
    return render(request, 'accueil.html')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()

            # Create a student automatically
            Etudiant.objects.create(
                user=user,
                matricule=get_random_string(8),
                nom="Nom",
                prenom="Prenom",
                email=f"{user.username}@example.com",
                telephone="0000000000",
                date_naissance="2000-01-01",
                adresse="Non défini"
            )

            messages.success(request, "Compte créé avec succès ! Vous pouvez vous connecter.")
            return redirect('login')

    else:
        form = UserCreationForm()

    return render(request, 'auth/register.html', {'form': form})


@login_required
def dashboard(request):
    total_etudiants = Etudiant.objects.count()
    total_cours = Cours.objects.count()
    total_inscriptions = Inscription.objects.count()

    context = {
        'total_etudiants': total_etudiants,
        'total_cours': total_cours,
        'total_inscriptions': total_inscriptions,
    }

    return render(request, 'dashboard.html', context)


# ==========================
# ETUDIANTS
# ==========================

@login_required
def liste_etudiants(request):

    etudiants_list = Etudiant.objects.all()

    paginator = Paginator(etudiants_list, 5)

    page_number = request.GET.get('page')

    etudiants = paginator.get_page(page_number)

    return render(request, 'etudiants/liste.html', {
        'etudiants': etudiants
    })


@admin_required
@login_required
def ajouter_etudiant(request):
    if request.method == "POST":
        matricule = request.POST.get("matricule")
        nom = request.POST.get("nom")
        prenom = request.POST.get("prenom")
        email = request.POST.get("email")
        telephone = request.POST.get("telephone")
        date_naissance = request.POST.get("date_naissance")
        adresse = request.POST.get("adresse")

        Etudiant.objects.create(
            matricule=matricule,
            nom=nom,
            prenom=prenom,
            email=email,
            telephone=telephone,
            date_naissance=date_naissance,
            adresse=adresse
        )

        return redirect("liste_etudiants")

    return render(request, "etudiants/ajouter.html")


@login_required
def detail_etudiant(request, pk):
    etudiant = get_object_or_404(Etudiant, pk=pk)
    return render(request, 'etudiants/detail.html', {'etudiant': etudiant})


@admin_required
# Seulement l'admin peut modifier
@user_passes_test(lambda u: u.is_superuser)
@login_required
def modifier_etudiant(request, pk):
    etudiant = get_object_or_404(Etudiant, pk=pk)

    if request.method == "POST":
        form = EtudiantForm(request.POST, instance=etudiant)  # formulaire lié à l'étudiant
        if form.is_valid():
            form.save()  # sauvegarde les modifications
            messages.success(request, "Étudiant modifié avec succès !")
            return redirect('liste_etudiants')
    else:
        form = EtudiantForm(instance=etudiant)  # formulaire prérempli

    return render(request, 'etudiants/modifier.html', {'form': form, 'etudiant': etudiant})


@admin_required
# Seulement les admins peuvent supprimer
@user_passes_test(lambda u: u.is_superuser)
@login_required
def supprimer_etudiant(request, pk):
    etudiant = get_object_or_404(Etudiant, pk=pk)

    if request.method == "POST":
        etudiant.delete()  # Supprime l'étudiant de la base
        messages.success(request, "Étudiant supprimé avec succès !")
        return redirect('liste_etudiants')  # Retour à la liste

    return render(request, 'etudiants/supprimer.html', {'etudiant': etudiant})


# ==========================
# COURS
# ==========================



@login_required
def liste_cours(request):
    cours = Cours.objects.all()
    return render(request, 'cours/liste.html', {'cours': cours})


@admin_required
@login_required
def ajouter_cours(request):
    if request.method == "POST":
        form = CoursForm(request.POST)   # use your form here
        if form.is_valid():              # validate automatically
            form.save()                  # save to DB
            return redirect('liste_cours')
    else:
        form = CoursForm()               # empty form for GET request

    return render(request, 'cours/ajouter.html', {'form': form})  # pass form to template


@admin_required
# Seuls les admins peuvent modifier
@user_passes_test(lambda u: u.is_superuser)
@login_required
def modifier_cours(request, pk):
    cours = get_object_or_404(Cours, pk=pk)

    if request.method == "POST":
        form = CoursForm(request.POST, instance=cours)
        if form.is_valid():
            form.save()
            messages.success(request, "Cours modifié avec succès !")
            return redirect('liste_cours')
    else:
        form = CoursForm(instance=cours)

    return render(request, 'cours/modifier.html', {'form': form, 'cours': cours})


@admin_required
@user_passes_test(lambda u: u.is_superuser)
@login_required
def supprimer_cours(request, pk):
    cours = get_object_or_404(Cours, pk=pk)

    if request.method == "POST":
        cours.delete()
        messages.success(request, "Cours supprimé avec succès !")
        return redirect('liste_cours')

    return render(request, 'cours/supprimer.html', {'cours': cours})


# ==========================
# INSCRIPTIONS
# ==========================

@admin_required
@login_required
def liste_inscriptions(request):
    inscriptions = Inscription.objects.all()
    return render(request, 'inscriptions/liste.html', {'inscriptions': inscriptions})

@admin_required
@login_required
def ajouter_inscription(request):

    etudiants = Etudiant.objects.all()
    cours = Cours.objects.all()

    if request.method == "POST":

        etudiant_id = request.POST.get("etudiant")
        cours_id = request.POST.get("cours")

        etudiant = Etudiant.objects.get(id=etudiant_id)
        cours_obj = Cours.objects.get(id=cours_id)

        Inscription.objects.create(
            etudiant=etudiant,
            cours=cours_obj
        )

        return redirect('liste_inscriptions')

    return render(request,'inscriptions/ajouter.html',{
        'etudiants': etudiants,
        'cours': cours
    })