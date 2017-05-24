from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions


from .parsers import XMLParser
from .renderers import XMLPeopleRenderer
from .serializers import UserSerializer

User = get_user_model()


class MeView(APIView):
    """
    View that will display XML for the current user.

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
        Return an xml version of the current user.
        """
        return Response({'users': request.user, 'request_user': request.user})


class PeopleView(APIView):
    """
    View to list all users in the system. You can also POST to this view with an xml person if you are an
    administrator.

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
            return Response({'users': user, 'request_user': user}, status=HTTP_201_CREATED)
        return Response(user_data.errors, status=HTTP_400_BAD_REQUEST)


class PersonView(APIView):
    """
    View to show a single user in the system.

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
