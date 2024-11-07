from rest_framework import serializers

from Office.models import Request, Case, LegalDocument


class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = [
            'id', 'status', 'request_type', 'description', 'user_id', 'case_id', 'created_at',
            'case_type', 'location', 'notes', 'plaintiff_name', 'defendant_name', 'national_address',
            'document_type', 'judgment_document_path', 'office_id',
        ]
        read_only_fields = ['id', 'created_at']

# Serializer for Case model
class CaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Case
        fields = [
            'id', 'status', 'plaintiff_name', 'defendant', 'address', 'case_type', 'description',
            'date', 'time', 'notes', 'user', 'lawyer', 'office'
        ]
        read_only_fields = ['id', 'office', 'user']



class LegalDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = LegalDocument
        fields = ['id', 'title', 'description', 'file', 'created_at','admin']
        read_only_fields = ['id', 'created_at']