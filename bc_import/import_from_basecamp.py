from datetime import datetime
import urllib
from bc_import.models import BCPerson, BCCompany, BCProject, BCDocumentVersion
from django.conf import settings
from django.utils import timezone
from django.utils.timezone import make_aware
from documents.models import Documents

import requests
import xml.etree.ElementTree as ET


def import_groups(service, username, password):
    r = requests.get('%s/companies.xml' % service, auth=(username, password))
    if r.status_code != 200:
        return r.status_code
    xml = ET.fromstring(r.text)
    count = 0
    for company in xml.findall('company'):
        name = company.find('name').text
        address = company.find('address-one').text
        address1 = company.find('address-two').text
        country = company.find('country').text

        country = 'US' # Not Correct
        city = company.find('city').text
        state = company.find('state').text
        bc_id = company.find('id').text
        locale = company.find('locale').text
        fax = company.find('phone-number-fax').text
        phone = company.find('phone-number-office').text
        web = company.find('web-address').text
        timezone = company.find('time-zone-id').text
        if timezone == 'Hawaii':
            timezone = 'Pacific/Honolulu'
        else:
            timezone = 'Pacific/Honolulu'
        BCCompany.objects.create(name=name, address=address, address1=address1, country=country, city=city, state='HI',
                               bc_id=bc_id, locale=locale, fax=fax, phone=phone, website=web, timezone=timezone)
        count += 1
    return count


def import_users(service, username, password):
    r = requests.get('%s/people.xml' % service, auth=(username, password))
    if r.status_code != 200:
        return r.status_code
    xml = ET.fromstring(r.text)
    count = 0
    for person in xml.findall('person'):
        p = BCPerson()
        p.date_joined = datetime.strptime(person.find('created-at').text, '%Y-%m-%dT%H:%M:%SZ')
        p.is_active = person.find('deleted').text
        p.access_new_projects = True if person.find('has-access-to-new-projects').text == 'true' else False
        p.bc_id = person.find('id').text
        p.im_handle = person.find('im-handle').text
        p.im_service = person.find('im-service').text
        p.fax = person.find('phone-number-fax').text
        p.home = person.find('phone-number-home').text
        p.mobile = person.find('phone-number-mobile').text
        p.office = person.find('phone-number-office').text
        p.ext = person.find('phone-number-office-ext').text
        p.title = person.find('title').text
        p.last_updated = datetime.strptime(person.find('updated-at').text, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=timezone.utc)
        p.first_name = person.find('first-name').text
        p.last_name = person.find('last-name').text
        p.company = BCCompany.objects.get(bc_id=person.find('company-id').text)
        p.timezone = person.find('time-zone-name').text
        p.username = person.find('user-name').text
        p.is_superuser = True if person.find('administrator').text == 'true' else False
        p.email = person.find('email-address').text
        p.avatar_url = person.find('avatar-url').text
        if p.username is None:
            p.username = p.email
        p.save()
        count += 1
    return count


def import_projects(service, username, password):
    r = requests.get('%s/projects.xml' % service, auth=(username, password))
    if r.status_code != 200:
        return r.status_code
    xml = ET.fromstring(r.text)
    count = 0
    for project in xml.findall('project'):
        p = BCProject()
        p.name = project.find('name').text
        p.bc_id = project.find('id').text
        if project.find('last-changed-on').text is not None:
            p.changed = datetime.strptime(project.find('last-changed-on').text, '%Y-%m-%dT%H:%M:%SZ')
        p.created = datetime.strptime(project.find('created-on').text, '%Y-%m-%d')
        p.is_active = project.find('status').text
        p.company = BCCompany.objects.get(bc_id=project.find('company').find('id').text)
        p.save()
        count += 1
    return count


def import_documents(service, username, password, project_id):
    n = 0
    count = 0
    while True:
        r = requests.get('%s/projects/%s/attachments.xml?n=%i' % (service, project_id, n), auth=(username, password))
        if r.status_code != 200:
            return r.status_code
        xml = ET.fromstring(r.text)

        documents = xml.findall('attachment')
        for document in documents:
            d = BCDocumentVersion()
            d.bc_id = document.find('id').text
            d.created = datetime.strptime(document.find('created-on').text, '%Y-%m-%dT%H:%M:%SZ')
            d.bc_size = document.find('byte-size').text
            d.bc_category = document.find('category-id').text
            d.bc_collection = document.find('collection').text
            d.bc_latest = True if document.find('current').text == 'true' else False
            d.description = document.find('description').text
            d.name = document.find('name').text
            try:
                d.person = BCPerson.objects.get(bc_id=document.find('person-id').text)
            except BCPerson.DoesNotExist:
                d.person = None
            d.bc_project = BCProject.objects.get(bc_id=document.find('project-id').text)
            d.bc_url = document.find('download-url').text
            d.save(save_document=False)
            count += 1
        if len(documents) >= 100:
            n += 100
        else:
            break
    return count


def import_file(service, username, password, url, uuid):
    r = requests.get(url, auth=(username, password))
    if r.status_code != 200:
        return r.status_code
    file_name = urllib.unquote(r.url.split('/')[-1:][0])
    file_path = settings.DOCUMENT_ROOT + uuid
    f = open(file_path + file_name, 'w')
    f.write(r.content)
    return file_path, file_name


def create_document_from_document_version(document_version):
    assert type(document_version) is BCDocumentVersion, 'The parameter must be of type DocumentVersion'
    document = Documents.objects.create(name=document_version.name, project=document_version.bc_project, date=document_version.created)
    for document_version in BCDocumentVersion.objects.filter(bc_collection=document_version.bc_collection):
        document_version.document = document
        document_version.save()

#for project in BCProject.objects.all(): import_from_basecamp.import_documents(project.bc_id) #Get all the document versions

#BCDocumentVersion.objects.all().order_by('bc_collection').distinct('bc_collection') # get all the document

# for bd_doc in BCDocumentVersion.objects.all().order_by('bc_collection').distinct('bc_collection'): import_from_basecamp.create_document_from_document_version(bd_doc) # create all the documents

#v.file, v.name = import_from_basecamp.import_file(v.bc_url, v.uuid) # Get the file