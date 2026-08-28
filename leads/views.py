from datetime import timedelta
from urllib.parse import urlparse
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.decorators.http import require_POST
from .forms import LeadForm
from .models import Event, Lead, Visit

def clean(value, length=120): return (value or "").strip()[:length]
def attribution(request):
    ref = clean(request.META.get("HTTP_REFERER"), 255)
    try: ref = urlparse(ref).netloc[:255]
    except ValueError: ref = ""
    return {"utm_source":clean(request.GET.get("utm_source")),"utm_medium":clean(request.GET.get("utm_medium")),"utm_campaign":clean(request.GET.get("utm_campaign")),"referrer":ref}
def current_visit(request):
    if not request.session.session_key: request.session.create()
    return Visit.objects.filter(session_key=request.session.session_key).order_by("-created_at").first()
def landing(request):
    if not request.session.session_key: request.session.create()
    attrs = attribution(request)
    visit, _ = Visit.objects.get_or_create(session_key=request.session.session_key, defaults={**attrs,"path":"/","user_agent_category":"mobile" if "Mobile" in request.META.get("HTTP_USER_AGENT","") else "desktop"})
    form = LeadForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        lead = form.save(commit=False)
        for key, value in attrs.items(): setattr(lead, key, value or request.session.get(key, ""))
        lead.save()
        Event.objects.create(visit=visit, name="form_submit", path="/")
        return redirect("thanks")
    for key, value in attrs.items():
        if value: request.session[key] = value
    return render(request, "leads/landing.html", {"form":form})
def thanks(request): return render(request, "leads/thanks.html")
@require_POST
def event(request):
    name = clean(request.POST.get("name"), 20)
    if name not in dict(Event.ALLOWED): return JsonResponse({"ok":False}, status=400)
    Event.objects.create(visit=current_visit(request), name=name, path=clean(request.POST.get("path"),255) or "/")
    return JsonResponse({"ok":True})
@user_passes_test(lambda u: u.is_authenticated and u.is_staff)
def dashboard(request):
    since = timezone.now() - timedelta(days=7)
    visits, leads = Visit.objects.count(), Lead.objects.count()
    context = {"visits":visits,"leads":leads,"visits7":Visit.objects.filter(created_at__gte=since).count(),"leads7":Lead.objects.filter(created_at__gte=since).count(),"conversion":round(leads/visits*100,1) if visits else 0,"events":Event.objects.values("name").annotate(total=Count("id")).order_by("name"),"recent":Lead.objects.order_by("-created_at")[:10],"referrers":Visit.objects.exclude(referrer="").values("referrer").annotate(total=Count("id")).order_by("-total")[:5],"campaigns":Visit.objects.exclude(utm_campaign="").values("utm_campaign").annotate(total=Count("id")).order_by("-total")[:5]}
    return render(request, "leads/dashboard.html", context)
