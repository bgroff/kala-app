from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions

from organizations.models import Organization

from .parsers import XMLCompanyParser
from .renderers import XMLCompaniesRenderer
from .serializers import CompanySerializer

from ..people.parsers import XMLParser
from ..people.renderers import XMLPeopleRenderer


class CompaniesView(APIView):
    """
    View that will display XML for all companies.

    """
    parser_classes = [XMLCompanyParser]
    renderer_classes = [XMLCompaniesRenderer]
    authentication_classes = (
        authentication.TokenAuthentication,
        authentication.BasicAuthentication,
        authentication.SessionAuthentication

    )
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        """
        Return an xml version of all of the companies.
        """
        return Response({'companies': Organization.objects.all(), 'request_user': request.user})

    def post(self, request, format=None):
        if not request.user.is_admin:
            raise PermissionDenied()

        company_data = CompanySerializer(data=request.data)
        if company_data.is_valid():
            company = company_data.save()
            return Response({'companies': company, 'request_user': request.user}, status=HTTP_201_CREATED)
        return Response(company_data.errors, status=HTTP_400_BAD_REQUEST)


class CompanyView(APIView):
    """
    View a single company by pk.
    """
    parser_classes = [XMLCompanyParser]
    renderer_classes = [XMLCompaniesRenderer]
    authentication_classes = (
        authentication.TokenAuthentication,
        authentication.BasicAuthentication,
        authentication.SessionAuthentication
    )
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, pk, format=None):
        """
        Return a company by pk.
        """
        company = get_object_or_404(Organization, pk=pk)
        return Response({'companies': company, 'request_user': request.user})


class PeopleView(APIView):
    """
    View to show a all users associated with a company.
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
        Return a list of all users for a specific company.
        """
        company = get_object_or_404(Organization, pk=pk)
        return Response({'users': company.get_people(), 'request_user': request.user})
