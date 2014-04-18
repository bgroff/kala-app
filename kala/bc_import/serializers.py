from bc_import.models import BCCompany
from rest_framework import serializers


class BasecampCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = BCCompany

    def restore_object(self, attrs, instance=None):
        if instance:
            instance.bc_id = attrs.get('id', instance.bc_id)
            instance.name = attrs.get('name', instance.name)
            instance.address = attrs.get('address-one', instance.address)
            instance.address1 = attrs.get('address-two', instance.address1)
            instance.city = attrs.get('city', instance.city)
            instance.state = attrs.get('state', instance.state)
            instance.web = attrs.get('web-address', instance.web)
            instance.fax = attrs.get('phone-number-fax', instance.fax)
            instance.office = attrs.get('phone-number-office', instance.office)
            return instance
