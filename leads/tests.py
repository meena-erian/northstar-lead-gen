from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from .models import Event, Lead, Visit
class FlowTests(TestCase):
    def test_visit_deduplicates_per_session(self):
        self.client.get("/"); self.client.get("/"); self.assertEqual(Visit.objects.count(),1)
    def test_lead_persists_with_attribution(self):
        response=self.client.post("/?utm_source=linkedin&utm_campaign=launch",{"name":"Ava","email":"AVA@example.com","company":"Acme","message":"More pipeline","consent":"on"})
        self.assertRedirects(response,"/thanks/"); lead=Lead.objects.get(); self.assertEqual(lead.email,"ava@example.com"); self.assertEqual(lead.utm_source,"linkedin"); self.assertEqual(Event.objects.filter(name="form_submit").count(),1)
    def test_invalid_form(self):
        response=self.client.post("/",{"name":"Ava","email":"bad"}); self.assertEqual(response.status_code,200); self.assertEqual(Lead.objects.count(),0)
    def test_event_allowlist(self):
        self.client.get("/"); self.assertEqual(self.client.post(reverse("event"),{"name":"cta_click","path":"/"}).status_code,200); self.assertEqual(self.client.post(reverse("event"),{"name":"evil"}).status_code,400); self.assertEqual(Event.objects.count(),1)
    def test_dashboard_requires_staff(self):
        user=get_user_model().objects.create_user("user",password="test-pass-123")
        self.client.force_login(user); self.assertEqual(self.client.get(reverse("dashboard")).status_code,302)
        user.is_staff=True; user.save(); self.assertEqual(self.client.get(reverse("dashboard")).status_code,200)
