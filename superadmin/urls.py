from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.homepage, name='dashboard'),
    path('login/', views.loginSuperAdmin, name='login'),
    path('tables/', views.tables, name='tables'),
    path('vendors/', views.vendor, name='vendors'),
    path('goal/', views.goalList, name='goal'),
    path('social/', views.socialList, name='social'),
    path('register/', views.register, name='register'),
    path('pendingUsers/', views.pendingUser, name='pending'),
    path('approveUsers/', views.approveUser, name='approve'),
    path('verify/<str:slug>/', views.verifyUser, name='verify-otp'),
    path('user-register/', views.registerUser, name='register-user'),
    path('goal-view/<int:id>/', views.goalView, name='goal_view'),
    path('user-view/<int:id>/', views.userView, name='user_view'),
    path('add-user/', views.addUser, name='add_user'),
    path('user-edit/<int:id>/', views.userUpdate, name='user_edit'),
    path('user-delete/<int:id>/', views.userDelete, name='user_delete'),
    path('vendor-view/<int:id>/', views.vendorView, name='vendor_view'),
    path('vendor-edit/<int:id>/', views.vendorUpdate, name='vendor_edit'),
    path('add-vendor/', views.addVendor, name='add_vendor'),
    path('vendor-delete/<int:id>/', views.vendorDelete, name='vendor_delete'),
    path('add-social/', views.addSocialLink, name='add_social'),
    path('logout/', views.logout, name='logout'),

]