from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('dashboard/', views.dashboard_view, name="dashboard"),
    path('user/', views.user_view, name="user"),
    path('add_user/', views.add_user_view, name="add_user"),
    path('edit_user/<int:pk>', views.edit_user_view, name="edit_user"),
    path('delete_user/<int:pk>', views.delete_user_view, name="delete_user"),

    path('buku_kas/', views.buku_view, name="buku"),
    path('add_buku_kas/', views.add_buku_view, name="add_buku"),
    path('edit_buku_kas/<int:pk>', views.edit_buku_view, name="edit_buku"),
    path('delete_buku_kas/<int:pk>', views.delete_buku_view, name="delete_buku"),

    path('laporan_harian/', views.laporan_harian_view, name="laporan_harian"),
    path('laporan_bulanan/', views.laporan_bulanan_view, name="laporan_bulanan"),
]
