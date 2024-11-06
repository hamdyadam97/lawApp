from django.db import models


# Create your models here.


class Office(models.Model):
    office_name = models.CharField(max_length=100)
    address = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # Related fields
    # Django's ORM automatically creates reverse relations, so we don’t need to define all of them
    # Here, we only define the ForeignKey fields for relation consistency.
    # Related_name helps refer to reverse access (for example, admin_set, request_set, etc., in related classes)

    def __str__(self):
        return self.office_name


class Case(models.Model):
    status = models.CharField(max_length=50, blank=True, null=True)
    plaintiff_name = models.CharField(max_length=100, blank=True, null=True)
    defendant_name = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    case_type = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    date = models.CharField(max_length=20, blank=True, null=True)
    time = models.CharField(max_length=10, blank=True, null=True)
    notes = models.JSONField(blank=True, null=True)
    user = models.ForeignKey('User.User', on_delete=models.CASCADE, related_name="cases")
    lawyer = models.ForeignKey('User.Lawyer', on_delete=models.SET_NULL, related_name="cases", null=True, blank=True)
    office = models.ForeignKey(Office, on_delete=models.SET_NULL, related_name="cases", null=True, blank=True)

    def __str__(self):
        return f"Case {self.id} - {self.status}"


class Document(models.Model):
    filename = models.CharField(max_length=255)
    file_path = models.CharField(max_length=255)
    document_type = models.CharField(max_length=50)
    uploader = models.ForeignKey('User.User', on_delete=models.CASCADE, related_name="documents")
    case = models.ForeignKey(Case, on_delete=models.SET_NULL, related_name="documents", null=True, blank=True)
    request = models.ForeignKey("Request", on_delete=models.SET_NULL, related_name="documents", null=True, blank=True)
    office = models.ForeignKey(Office, on_delete=models.SET_NULL, related_name="documents", null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.filename


class Request(models.Model):
    status = models.CharField(max_length=100, default="Pending")
    request_type = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    case_type = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    notes = models.JSONField(default=list, blank=True, null=True)
    plaintiff_name = models.CharField(max_length=100, blank=True, null=True)
    defendant_name = models.CharField(max_length=100, blank=True, null=True)
    national_address = models.CharField(max_length=200, blank=True, null=True)
    document_type = models.CharField(max_length=100, blank=True, null=True)
    judgment_document_path = models.CharField(max_length=200, blank=True, null=True)
    user = models.ForeignKey('User.User', on_delete=models.CASCADE, related_name="requests")
    case = models.ForeignKey(Case, on_delete=models.SET_NULL, related_name="requests", null=True, blank=True)
    office = models.ForeignKey(Office, on_delete=models.SET_NULL, related_name="requests", null=True, blank=True)
    lawyer = models.ForeignKey('User.Lawyer', on_delete=models.SET_NULL, related_name="requests", null=True, blank=True)

    def __str__(self):
        return f"Request {self.id} - {self.status}"