from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login, logout_then_login
from documents.views import Home, CreateAccount, EditProfile

urlpatterns = patterns('',
    url(r'^$', login_required(Home.as_view()), name='home'),
    url(r'^login$', login, {'template_name': 'login.html'}, name='login'),
    url(r'^logout$', logout_then_login, {'login_url': '/login'}, name='logout'),
    url(r'^create_account$', CreateAccount.as_view(), name='create_account'),
    url(r'^edit_profile$', login_required(EditProfile.as_view()), name='edit_profile'),
    url(r'^', include('documents.urls')),
)
