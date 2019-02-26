from models import AppealReceiptsData
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AppealReceiptsData
        fields = ('state_name', 'year', 'total_appeal_receipts')
