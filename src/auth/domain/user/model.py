## auth/domain/models.py
import uuid

from tortoise import fields, models

class User(models.Model):
    id = fields.UUIDField(pk=True,default=uuid.uuid4)
    email = fields.CharField(max_length=255, unique=True)
    #password = fields.CharField(max_length=255)
    name = fields.CharField(max_length=255)
    provider = fields.CharField(max_length=50)  # 예: 'google', 'kakao', 'local'
    provider_user_id = fields.CharField(max_length=128)  # ex: 구글 sub
    access_token = fields.TextField()
    refresh_token = fields.TextField(null=True)
    expires_at = fields.FloatField()
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "users"
        unique_together = (("provider", "provider_user_id"),)