from io import StringIO

from django.db.models import QuerySet
from django.utils.six import iteritems
from django.utils.xmlutils import SimplerXMLGenerator
from django.utils.encoding import smart_text
from rest_framework.renderers import BaseRenderer


class XMLPeopleRenderer(BaseRenderer):
    """
    Renderer which serializes to XML.
    """
    media_type = 'application/xml'
    format = 'xml'
    charset = 'utf-8'
    item_tag_name = 'person'
    root_tag_name = 'people'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        """
        Renders `data` into serialized XML.
        """
        if data is None:
            return ''

        stream = StringIO()

        xml = SimplerXMLGenerator(stream, self.charset)
        xml.startDocument()
        # If we do not have users or request_user then we have errors
        if not data.get('users', False) and not data.get('request_user', False):
            self._to_errors(data, xml)
            xml.endDocument()
            return stream.getvalue()

        # If users are a list, deal with that
        if type(data['users']) is QuerySet or type(data['users']) is list:
            xml.startElement('people', {'type': 'array'})

            self._to_xml(data['users'], data['request_user'], xml)

            xml.endElement('people')
        # Otherwise just render a person
        else:
            self.render_person(data['users'], data['request_user'], xml)
        xml.endDocument()
        return stream.getvalue()

    def _to_xml(self, users, request_user, xml):
        for user in users:
            self.render_person(user, request_user, xml)

    def render_person(self, user, request_user, xml):
            xml.startElement('person', {})
            xml.startElement('id', {'type': 'integer'})
            xml.characters(smart_text(user.id))
            xml.endElement('id')
            xml.startElement('uuid', {'type': 'uuid'})
            xml.characters(smart_text(user.uuid))
            xml.endElement('uuid')
            xml.startElement('created-at', {'type': 'datetime'})
            xml.characters(smart_text(user.date_joined.isoformat()))
            xml.endElement('created-at')
            xml.startElement('first-name', {})
            xml.characters(smart_text(user.first_name))
            xml.endElement('first-name')
            xml.startElement('last-name', {})
            xml.characters(smart_text(user.last_name))
            xml.endElement('last-name')
            xml.startElement('title', {})
            try:
                xml.characters(smart_text(user.title if user.title else ''))
            except AttributeError:
                xml.characters(smart_text(''))
            xml.endElement('title')
            xml.startElement('email-address', {})
            xml.characters(smart_text(user.email))
            xml.endElement('email-address')
            xml.startElement('im-handle', {})
            try:
                xml.characters(smart_text(user.im_handle if user.im_handle else ''))
            except AttributeError:
                xml.characters(smart_text(''))
            xml.endElement('im-handle')
            xml.startElement('im-service', {})
            try:
                xml.characters(smart_text(user.im_service if user.im_service else ''))
            except AttributeError:
                xml.characters(smart_text(''))
            xml.endElement('im-service')
            xml.startElement('phone-number-office', {})
            try:
                xml.characters(smart_text(user.phone if user.phone else ''))
            except AttributeError:
                xml.characters(smart_text(''))
            xml.endElement('phone-number-office')
            xml.startElement('phone-number-office-ext', {})
            try:
                xml.characters(smart_text(user.ext if user.ext else ''))
            except AttributeError:
                xml.characters(smart_text(''))
            xml.endElement('phone-number-office-ext')
            xml.startElement('phone-number-mobile', {})
            try:
                xml.characters(smart_text(user.phone_mobile if user.phone_mobile else ''))
            except AttributeError:
                xml.characters(smart_text(''))
            xml.endElement('phone-number-mobile')
            xml.startElement('phone-number-home', {})
            try:
                xml.characters(smart_text(user.phone_home if user.phone_home else ''))
            except AttributeError:
                xml.characters(smart_text(''))
            xml.endElement('phone-number-home')
            xml.startElement('phone-number-fax', {})
            try:
                xml.characters(smart_text(user.phone_fax if user.phone_fax else ''))
            except AttributeError:
                xml.characters(smart_text(''))
            xml.endElement('phone-number-fax')
            xml.startElement('company-id', {'type': 'integer'})
            try:
                xml.characters(smart_text(user.organizations.first().id if user.organizations.first() else ''))
            except AttributeError:
                xml.characters(smart_text(''))
            xml.endElement('company-id')
            xml.startElement('client-id', {'type': 'integer'})
            try:
                xml.characters(smart_text(user.client.id if user.client.id else ''))
            except AttributeError:
                xml.characters(smart_text(''))
            xml.endElement('client-id')
            xml.startElement('avatar-url', {})
            try:
                xml.characters(smart_text(user.avatar_url if user.avatar_url else ''))
            except AttributeError:
                xml.characters(smart_text(''))
            xml.endElement('avatar-url')
            if request_user.is_superuser:
                xml.startElement('user-name', {})
                xml.characters(smart_text(user.username))
                xml.endElement('user-name')

                xml.startElement('administrator', {'type': 'boolean'})
                xml.characters(smart_text(str(user.is_superuser).lower()))
                xml.endElement('administrator')

                xml.startElement('deleted', {'type': 'boolean'})
                xml.characters(smart_text(str(not user.is_active)).lower())
                xml.endElement('deleted')

                xml.startElement('has-access-to-new-projects', {'type': 'boolean'})
                try:
                    xml.characters(
                        smart_text(
                            str(user.access_new_projects).lower() if user.access_new_projects else str(False).lower()
                        )
                    )
                except AttributeError:
                    xml.characters(smart_text(''))
                xml.endElement('has-access-to-new-projects')
            xml.endElement('person')

    def _to_errors(self, data, xml):
        xml.startElement('errors', {})
        if data.get('id', False):
            xml.startElement('id', {'type': 'integer'})
            for error in data['id']:
                xml.startElement('error', {})
                xml.characters(smart_text(error))
                xml.endElement('error')
            xml.endElement('id')

        if data.get('uuid', False):
            xml.startElement('uuid', {'type': 'uuid'})
            for error in data['uuid']:
                xml.startElement('error', {})
                xml.characters(smart_text(error))
                xml.endElement('error')
            xml.endElement('uuid')

        if data.get('username', False):
            xml.startElement('user-name', {})
            for error in data['username']:
                xml.startElement('error', {})
                xml.characters(smart_text(error))
                xml.endElement('error')
            xml.endElement('user-name')

        if data.get('first_name', False):
            xml.startElement('first-name', {})
            for error in data['first_name']:
                xml.startElement('error', {})
                xml.characters(smart_text(error))
                xml.endElement('error')
            xml.endElement('first-name')

        if data.get('last_name', False):
            xml.startElement('last-name', {})
            for error in data['last_name']:
                xml.startElement('error', {})
                xml.characters(smart_text(error))
                xml.endElement('error')
            xml.endElement('last-name')

        if data.get('title', False):
            xml.startElement('title', {})
            for error in data['title']:
                xml.startElement('error', {})
                xml.characters(smart_text(error))
                xml.endElement('error')
            xml.endElement('title')

        if data.get('email', False):
            xml.startElement('email-address', {})
            for error in data['email']:
                xml.startElement('error', {})
                xml.characters(smart_text(error))
                xml.endElement('error')
            xml.endElement('email-address')

        if data.get('im_handler', False):
            xml.startElement('im-handler', {})
            for error in data['im_handler']:
                xml.startElement('error', {})
                xml.characters(smart_text(error))
                xml.endElement('error')
            xml.endElement('im-handler')

        if data.get('im_service', False):
            xml.startElement('im-service', {})
            for error in data['im_service']:
                xml.startElement('error', {})
                xml.characters(smart_text(error))
                xml.endElement('error')
            xml.endElement('im-service')

        if data.get('phone', False):
            xml.startElement('phone-number-office', {})
            for error in data['phone']:
                xml.startElement('error', {})
                xml.characters(smart_text(error))
                xml.endElement('error')
            xml.endElement('phone-number-office')

        if data.get('phone_ext', False):
            xml.startElement('phone-number-office-ext', {})
            for error in data['ext']:
                xml.startElement('error', {})
                xml.characters(smart_text(error))
                xml.endElement('error')
            xml.endElement('phone-number-office-ext')

        if data.get('mobile', False):
            xml.startElement('phone-number-mobile', {})
            for error in data['mobile']:
                xml.startElement('error', {})
                xml.characters(smart_text(error))
                xml.endElement('error')
            xml.endElement('phone-number-mobile')

        if data.get('home', False):
            xml.startElement('phone-number-home', {})
            for error in data['home']:
                xml.startElement('error', {})
                xml.characters(smart_text(error))
                xml.endElement('error')
            xml.endElement('phone-number-home')

        if data.get('fax', False):
            xml.startElement('phone-number-fax', {})
            for error in data['fax']:
                xml.startElement('error', {})
                xml.characters(smart_text(error))
                xml.endElement('error')
            xml.endElement('phone-number-fax')

        if data.get('company', False):
            xml.startElement('company-id', {})
            for error in data['companies']:
                xml.startElement('error', {})
                xml.characters(smart_text(error))
                xml.endElement('error')
            xml.endElement('company-id')

        if data.get('client', False):
            xml.startElement('client-id', {})
            for error in data['client']:
                xml.startElement('error', {})
                xml.characters(smart_text(error))
                xml.endElement('error')
            xml.endElement('client-id')

        if data.get('avatar_url', False):
            xml.startElement('avatar-url', {})
            for error in data['avatar_url']:
                xml.startElement('error', {})
                xml.characters(smart_text(error))
                xml.endElement('error')
            xml.endElement('avatar-url')

        if data.get('is_superuser', False):
            xml.startElement('administrator', {})
            for error in data['is_superuser']:
                xml.startElement('error', {})
                xml.characters(smart_text(error))
                xml.endElement('error')
            xml.endElement('administrator')

        if data.get('access_new_projects', False):
            xml.startElement('has-access-to-new-projects', {})
            for error in data['access_new_projects']:
                xml.startElement('error', {})
                xml.characters(smart_text(error))
                xml.endElement('error')
            xml.endElement('has-access-to-new-projects')

        xml.endElement('errors')
