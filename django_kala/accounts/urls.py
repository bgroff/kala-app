from django.conf.urls import url
from django.contrib.auth.views import login, logout_then_login
from .views import EditProfile, PeopleView


urlpatterns = [
   url(regex=r'^$',
       view=PeopleView.as_view(),
       name='accounts',
   ),

   url(
       regex=r'^login/$',
       view=login,
       kwargs={'template_name': 'login.html'},
       name='login'
   ),
   url(
       regex=r'^logout/$',
       view=logout_then_login,
       kwargs={'login_url': '/login'},
       name='logout'
   ),
   #    url(r'^create_account$', CreateAccount.as_view(), name='create_account'),
   url(
       regex=r'^edit_profile/(?P<pk>\d+)/$',
       view=EditProfile.as_view(),
       name='edit_profile'
   ),
]
