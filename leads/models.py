from django.db import models

class Attribution(models.Model):
    utm_source = models.CharField(max_length=120, blank=True)
    utm_medium = models.CharField(max_length=120, blank=True)
    utm_campaign = models.CharField(max_length=120, blank=True)
    referrer = models.CharField(max_length=255, blank=True)
    class Meta:
        abstract = True

class Visit(Attribution):
    session_key = models.CharField(max_length=40, db_index=True)
    path = models.CharField(max_length=255, default="/")
    user_agent_category = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Lead(Attribution):
    name = models.CharField(max_length=120)
    email = models.EmailField(unique=True)
    company = models.CharField(max_length=160, blank=True)
    message = models.TextField(max_length=1000, blank=True)
    consent = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return f"{self.name} <{self.email}>"

class Event(models.Model):
    ALLOWED = (("cta_click","CTA click"),("form_start","Form start"),("form_submit","Form submit"))
    visit = models.ForeignKey(Visit, null=True, blank=True, on_delete=models.SET_NULL, related_name="events")
    name = models.CharField(max_length=20, choices=ALLOWED)
    path = models.CharField(max_length=255, default="/")
    created_at = models.DateTimeField(auto_now_add=True)
