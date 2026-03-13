from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.accueil, name='accueil'),

    path('dashboard/', views.dashboard, name='dashboard'),
    path('cours/add/', views.ajouter_cours, name='ajouter_cours'),
    path('cours/', views.liste_cours, name='liste_cours'),
    # AUTHENTICATION
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='auth/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    # ETUDIANTS
    path('etudiants/', views.liste_etudiants, name='liste_etudiants'),
    path('etudiants/ajouter/', views.ajouter_etudiant, name='ajouter_etudiant'),
    path('etudiants/<int:pk>/', views.detail_etudiant, name='detail_etudiant'),
    path('etudiants/<int:pk>/modifier/', views.modifier_etudiant, name='modifier_etudiant'),
    path('etudiants/<int:pk>/supprimer/', views.supprimer_etudiant, name='supprimer_etudiant'),

    # COURS
    path('cours/', views.liste_cours, name='liste_cours'),
    path('cours/ajouter/', views.ajouter_cours, name='ajouter_cours'),
    path('cours/<int:pk>/modifier/', views.modifier_cours, name='modifier_cours'),
    path('cours/<int:pk>/supprimer/', views.supprimer_cours, name='supprimer_cours'),

    # INSCRIPTIONS
    path('inscriptions/', views.liste_inscriptions, name='liste_inscriptions'),
    path('inscriptions/ajouter/', views.ajouter_inscription, name='ajouter_inscription'),
]