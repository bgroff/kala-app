from io import StringIO

from django.db.models import QuerySet
from django.utils.xmlutils import SimplerXMLGenerator
from django.utils.encoding import smart_str
from rest_framework.renderers import BaseRenderer


class XMLCompaniesRenderer(BaseRenderer):
    """
    Renderer which serializes to XML.
    """
    media_type = 'application/xml'
    format = 'xml'
    charset = 'utf-8'
    item_tag_name = 'company'
    root_tag_name = 'companies'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        """
        Renders `data` into serialized XML.
        """
        if data is None:
            return ''

        stream = StringIO()

        xml = SimplerXMLGenerator(stream, self.charset)
        xml.startDocument()
        # If we do not have companies or request_user then we have errors
        if not data.get('companies', False) and not data.get('request_user', False):
            self._to_errors(data, xml)
            xml.endDocument()
            return stream.getvalue()

        # If users are a list, deal with that
        if type(data['companies']) is QuerySet:
            xml.startElement('companies', {'type': 'array'})

            self._to_xml(data['companies'], data['request_user'], xml)

            xml.endElement('companies')
        # Otherwise just render a company
        else:
            self.render_company(data['companies'], data['request_user'], xml)
        xml.endDocument()
        return stream.getvalue()

    def _to_xml(self, companies, request_user, xml):
        for company in companies:
            self.render_company(company, request_user, xml)

    def render_company(self, company, request_user, xml):
            xml.startElement('company', {})
            xml.startElement('id', {'type': 'integer'})
            xml.characters(smart_str(company.id))
            xml.endElement('id')
            xml.startElement('uuid', {'type': 'uuid'})
            xml.characters(smart_str(company.uuid))
            xml.endElement('uuid')
            xml.startElement('name', {})
            xml.characters(smart_str(company.name))
            xml.endElement('name')

            xml.startElement('web-site', {})
            try:
                xml.characters(smart_str(company.website if company.website else ''))
            except AttributeError:
                xml.characters(smart_str(''))
            xml.endElement('web-site')

            xml.startElement('address-one', {})
            try:
                xml.characters(smart_str(company.address if company.address else ''))
            except AttributeError:
                xml.characters(smart_str(''))
            xml.endElement('address-one')
            xml.startElement('address-two', {})
            try:
                xml.characters(smart_str(company.address1 if company.address1 else ''))
            except AttributeError:
                xml.characters(smart_str(''))
            xml.endElement('address-two')
            xml.startElement('city', {})
            try:
                xml.characters(smart_str(company.city if company.city else ''))
            except AttributeError:
                xml.characters(smart_str(''))
            xml.endElement('city')
            xml.startElement('state', {})
            try:
                xml.characters(smart_str(company.state if company.state else ''))
            except AttributeError:
                xml.characters(smart_str(''))
            xml.endElement('state')
            xml.startElement('zip', {})
            try:
                xml.characters(smart_str(company.zip if company.zip else ''))
            except AttributeError:
                xml.characters(smart_str(''))
            xml.endElement('zip')
            xml.startElement('country', {})
            try:
                xml.characters(smart_str(company.country if company.country else ''))
            except AttributeError:
                xml.characters(smart_str(''))
            xml.endElement('country')
            xml.startElement('time-zone', {})
            try:
                xml.characters(smart_str(company.timezone if company.timezone else ''))
            except AttributeError:
                xml.characters(smart_str(''))
            xml.endElement('time-zone')

            xml.startElement('phone-number-office', {})
            try:
                xml.characters(smart_str(company.phone if company.phone else ''))
            except AttributeError:
                xml.characters(smart_str(''))
            xml.endElement('phone-number-office')
            xml.startElement('phone-number-fax', {})
            try:
                xml.characters(smart_str(company.fax if company.fax else ''))
            except AttributeError:
                xml.characters(smart_str(''))
            xml.endElement('phone-number-fax')

            xml.endElement('company')

    def _to_errors(self, data, xml):
        xml.startElement('errors', {})
        if data.get('id', False):
            xml.startElement('id', {'type': 'integer'})
            for error in data['id']:
                xml.startElement('error', {})
                xml.characters(smart_str(error))
                xml.endElement('error')
            xml.endElement('id')

        if data.get('uuid', False):
            xml.startElement('uuid', {'type': 'uuid'})
            for error in data['uuid']:
                xml.startElement('error', {})
                xml.characters(smart_str(error))
                xml.endElement('error')
            xml.endElement('uuid')

        if data.get('name', False):
            xml.startElement('name', {})
            for error in data['name']:
                xml.startElement('error', {})
                xml.characters(smart_str(error))
                xml.endElement('error')
            xml.endElement('name')

        if data.get('website', False):
            xml.startElement('web-site', {})
            for error in data['website']:
                xml.startElement('error', {})
                xml.characters(smart_str(error))
                xml.endElement('error')
            xml.endElement('web-site')

        if data.get('address', False):
            xml.startElement('address-one', {})
            for error in data['address']:
                xml.startElement('error', {})
                xml.characters(smart_str(error))
                xml.endElement('error')
            xml.endElement('address-one')

        if data.get('address1', False):
            xml.startElement('address-two', {})
            for error in data['address1']:
                xml.startElement('error', {})
                xml.characters(smart_str(error))
                xml.endElement('error')
            xml.endElement('address1')

        if data.get('city', False):
            xml.startElement('city', {})
            for error in data['city']:
                xml.startElement('error', {})
                xml.characters(smart_str(error))
                xml.endElement('error')
            xml.endElement('city')

        if data.get('state', False):
            xml.startElement('state', {})
            for error in data['state']:
                xml.startElement('error', {})
                xml.characters(smart_str(error))
                xml.endElement('error')
            xml.endElement('state')

        if data.get('zip', False):
            xml.startElement('zip', {})
            for error in data['zip']:
                xml.startElement('error', {})
                xml.characters(smart_str(error))
                xml.endElement('error')
            xml.endElement('zip')

        if data.get('country', False):
            xml.startElement('country', {})
            for error in data['country']:
                xml.startElement('error', {})
                xml.characters(smart_str(error))
                xml.endElement('error')
            xml.endElement('country')

        if data.get('timezone', False):
            xml.startElement('time-zone', {})
            for error in data['timezone']:
                xml.startElement('error', {})
                xml.characters(smart_str(error))
                xml.endElement('error')
            xml.endElement('time-zone')

        if data.get('locale', False):
            xml.startElement('locale', {})
            for error in data['locale']:
                xml.startElement('error', {})
                xml.characters(smart_str(error))
                xml.endElement('error')
            xml.endElement('locale')

        if data.get('phone', False):
            xml.startElement('phone-number-office', {})
            for error in data['phone']:
                xml.startElement('error', {})
                xml.characters(smart_str(error))
                xml.endElement('error')
            xml.endElement('phone-number-office')

        if data.get('fax', False):
            xml.startElement('phone-number-fax', {})
            for error in data['fax']:
                xml.startElement('error', {})
                xml.characters(smart_str(error))
                xml.endElement('error')
            xml.endElement('phone-number-fax')

        xml.endElement('errors')
