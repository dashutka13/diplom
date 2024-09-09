from django.urls import path

from users.apps import UsersConfig
from users.views import LoginView, LogoutView, RegisterView, UserUpdateView, UserListView, UserDetailView, \
    UserDeleteView

app_name = UsersConfig.name

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('user/', UserListView.as_view(), name='user_list'),
    path('user/<int:pk>/update/', UserUpdateView.as_view(), name='user_update'),
    path('user/<int:pk>/detail/', UserDetailView.as_view(), name='user_detail'),
    path('user/<int:pk>/delete/', UserDeleteView.as_view(), name='user_delete'),
]
