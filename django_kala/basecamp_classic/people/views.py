from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions

from django.contrib.auth import get_user_model

from .parsers import XMLParser
from .renderers import XMLPeopleRenderer
from .serializers import UserSerializer

User = get_user_model()


class MeView(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    parser_classes = [XMLParser]
    renderer_classes = [XMLPeopleRenderer]
    authentication_classes = (
        authentication.TokenAuthentication,
        authentication.BasicAuthentication,
        authentication.SessionAuthentication

    )
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        return Response({'users': request.user, 'request_user': request.user})


class PeopleView(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    parser_classes = [XMLParser]
    renderer_classes = [XMLPeopleRenderer]
    authentication_classes = (
        authentication.TokenAuthentication,
        authentication.BasicAuthentication,
        authentication.SessionAuthentication
    )
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        include_deleted = request.GET.get('include_deleted', False)
        if request.user.is_admin and include_deleted == 'true':
            # TODO: Use an is_active mixin to filter between deleted and non-deleted
            users = User.objects.all()
        else:
            users = User.objects.all()
        return Response({'users': users, 'request_user': request.user})

    def post(self, request, format=None):
        if not request.user.is_admin:
            raise PermissionDenied()

        user_data = UserSerializer(data=request.data)
        if user_data.is_valid():
            user = user_data.save()
            return Response({'users': user, 'request_user': User.objects.first()}, status=HTTP_201_CREATED)
#        raise Exception(str(user_data.errors['username']))
        return Response(user_data.errors, status=HTTP_400_BAD_REQUEST)


class PersonView(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    parser_classes = [XMLParser]
    renderer_classes = [XMLPeopleRenderer]
    authentication_classes = (
        authentication.TokenAuthentication,
        authentication.BasicAuthentication,
        authentication.SessionAuthentication
    )
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, pk, format=None):
        """
        Return a list of all users.
        """
        user = get_object_or_404(User, pk=pk)
        return Response({'users': user, 'request_user': request.user})
