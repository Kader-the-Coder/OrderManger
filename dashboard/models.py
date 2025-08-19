from django.db import models
from accounts.models import CustomUser, Company


class CompanyInvitation(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='invitations')
    invited_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='invitations')
    invited_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='sent_invitations')
    created_at = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)
