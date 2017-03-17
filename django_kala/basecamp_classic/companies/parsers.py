"""
Provides XML parsing support.
"""
from django.conf import settings
from rest_framework.exceptions import ParseError
from rest_framework.parsers import BaseParser

import defusedxml.ElementTree as etree


class XMLCompanyParser(BaseParser):
    """
    XML company parser.
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
                data['id'] = str(field.text)
            if field.tag == 'uuid':
                data['uuid'] = str(field.text)
            if field.tag == 'name':
                data['name'] = str(field.text)

            if field.tag == 'web-address':
                data['website'] = str(field.text)

            if field.tag == 'phone-number-office':
                data['phone'] = str(field.text)
            if field.tag == 'phone-number-fax':
                data['fax'] = str(field.text)

            if field.tag == 'address-one':
                data['address'] = str(field.text)
            if field.tag == 'address-two':
                data['address1'] = str(field.text)
            if field.tag == 'city':
                data['city'] = str(field.text)
            if field.tag == 'state':
                data['state'] = str(field.text)
            if field.tag == 'country':
                data['country'] = str(field.text)
            if field.tag == 'time-zone-id':
                data['timezone'] = str(field.text)
            if field.tag == 'locale':
                data['locale'] = str(field.text)

        return data
