from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login, logout_then_login
from kala.views import Home, LicenseView, UserDocumentationView
from people.views import EditProfile

urlpatterns = patterns('',
                       url(
                           regex=r'^$',
                           view=Home.as_view(),
                           name='home'
                       ),

                       url(
                           regex=r'^login$',
                           view=login,
                           kwargs={'template_name': 'login.html'},
                           name='login'
                       ),
                       url(
                           regex=r'^logout$',
                           view=logout_then_login,
                           kwargs={'login_url': '/login'},
                           name='logout'
                       ),
                       #    url(r'^create_account$', CreateAccount.as_view(), name='create_account'),
                       url(
                           regex=r'^edit_profile/(?P<pk>\d+)$',
                           view=EditProfile.as_view(),
                           name='edit_profile'
                       ),

                       url(
                           r'^companies/',
                           include('companies.urls'),
                       ),

                       url(
                           r'^documents/',
                           include('documents.urls'),
                       ),

                       url(
                           r'^people/',
                           include('people.urls'),
                       ),

                       url(
                           r'^projects/',
                           include('projects.urls'),
                       ),

                       url(
                           r'^import/',
                           include('bc_import.urls'),
                       ),

                        url(
                            regex=r'^license$',
                            view=LicenseView.as_view(),
                            name='license',
                        ),
                        url(
                            regex=r'^user_documentation$',
                            view=UserDocumentationView.as_view(),
                            name='user_documentation',
                        ),
)
