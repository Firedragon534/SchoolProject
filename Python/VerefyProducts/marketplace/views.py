from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseBadRequest
from .models import Listing, ListingImage, Verification
from .forms import ListingForm
import json
from django.db import models as djmodels
def home(request):
    listings = Listing.objects.filter(status='active').order_by('-created_at')
    return render(request, 'marketplace/home.html', {'listings': listings})
@login_required
def create_listing(request):
    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.seller = request.user
            listing.status = 'pending_test'
            listing.save()
            # images
            files = request.FILES.getlist('images')
            for f in files:
                ListingImage.objects.create(listing=listing, image=f)
            return redirect('marketplace:listing_detail', pk=listing.pk)
    else:
        form = ListingForm()
    return render(request, 'marketplace/create_listing.html', {'form': form})
def listing_detail(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    return render(request, 'marketplace/listing_detail.html', {'listing': listing})
@login_required
def request_test(request, pk):
    listing = get_object_or_404(Listing, pk=pk, seller=request.user)
    listing.status = 'pending_test'
    listing.save()
    return redirect('marketplace:listing_detail', pk=pk)
@login_required
def verify_listing(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except:
            return HttpResponseBadRequest('Invalid JSON')
        verdict = data.get('verdict')
        checklist = data.get('checklist', {})
        notes = data.get('notes', '')
        v = Verification.objects.create(listing=listing, technician=request.user, verdict=verdict, notes=notes, checklist=checklist)
        return JsonResponse({'status':'ok','verdict': v.verdict})
    return render(request, 'marketplace/verify_listing.html', {'listing': listing})
from django.views.decorators.http import require_POST
@require_POST
def chatbot_api(request):
    try:
        data = json.loads(request.body)
    except:
        return HttpResponseBadRequest('Invalid JSON')
    message = data.get('message','').lower()
    if 'price' in message or 'how much' in message:
        # simple avg price suggestion based on title keywords
        words = [w for w in message.split() if len(w)>=3]
        qs = Listing.objects.filter(status='active')
        for w in words:
            qs = qs.filter(title__icontains=w)
        avg = qs.aggregate(djmodels.Avg('price'))['price__avg'] if qs.exists() else None
        if avg:
            return JsonResponse({'reply': f'Based on similar active listings a typical price is around {avg:.2f}.'})
        return JsonResponse({'reply': 'No similar active listings found. Try more specific model names.'})
    if 'recommend' in message or 'which' in message:
        return JsonResponse({'reply': 'Tell me the use case (gaming, office, repair) and your max budget and I will suggest parts.'})
    return JsonResponse({'reply': "I can help with price suggestions, part recommendations, and testing checklists."})
