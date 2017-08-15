"""
Provides XML parsing support.
"""
import distutils

from django.conf import settings
from rest_framework.exceptions import ParseError
from rest_framework.parsers import BaseParser

import defusedxml.ElementTree as etree
import dateparser


class XMLParser(BaseParser):
    """
    XML parser.
    """

    media_type = 'application/xml'

    def parse(self, stream, media_type=None, parser_context=None):
        """
        Parses the incoming bytestream as XML and returns the resulting data.
        """

        parser_context = parser_context or {}
        encoding = parser_context.get('encoding', settings.DEFAULT_CHARSET)
        parser = etree.DefusedXMLParser(encoding=encoding)
        try:
            tree = etree.parse(stream, parser=parser, forbid_dtd=True)
        except (etree.ParseError, ValueError) as exc:
            raise ParseError(detail=str(exc))
        data = self._xml_convert(tree.getroot())

        return data

    def _xml_convert(self, element):
        """
        convert the xml `element` into the corresponding python object
        """
        data = {}

        fields = list(element)
        for field in fields:
            if field.tag == 'id':
                data['id'] = int(field.text)
            if field.tag == 'user-name':
                data['username'] = str(field.text)
            if field.tag == 'created-at':
                data['date_joined'] = dateparser.parse(field.text)
            if field.tag == 'first-name':
                data['first_name'] = str(field.text)
            if field.tag == 'last-name':
                data['last_name'] = str(field.text)
            if field.tag == 'title':
                data['title'] = str(field.text)
            if field.tag == 'email-address':
                data['email'] = str(field.text)

            if field.tag == 'im-handle':
                data['im_handle'] = str(field.text)
            if field.tag == 'im-service':
                data['im_service'] = str(field.text)

            if field.tag == 'phone-number-office':
                data['phone'] = str(field.text)
            if field.tag == 'phone-number-office-ext':
                data['ext'] = str(field.text)
            if field.tag == 'phone-number-mobile':
                data['mobile'] = str(field.text)
            if field.tag == 'phone-number-home':
                data['home'] = str(field.text)
            if field.tag == 'phone-number-fax':
                data['fax'] = str(field.text)

            if field.tag == 'company-id':
                data['organizations'] = [int(field.text)] if field.text else None
            if field.tag == 'client-id':
                data['client_id'] = int(field.text) if field.text else None

            if field.tag == 'avatar-url':
                data['avatar_url'] = str(field.text)

            if field.tag == 'administrator':
                data['is_admin'] = bool(distutils.util.strtobool(field.text))
            if field.tag == 'deleted':
                data['is_active'] = not(bool(distutils.util.strtobool(field.text)))
            if field.tag == 'has-access-to-new-projects':
                data['access_new_projects'] = bool(distutils.util.strtobool(field.text))
        return data
