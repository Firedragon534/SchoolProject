from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()
class Listing(models.Model):
    STATUS_CHOICES = [
        ('draft','Draft'),
        ('pending_test','Pending Test'),
        ('verified','Verified'),
        ('active','Active'),
        ('rejected','Rejected'),
        ('sold','Sold'),
    ]
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listings')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    condition = models.CharField(max_length=100, blank=True)
    serial_number = models.CharField(max_length=200, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"
class ListingImage(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='listing_images/')
class Verification(models.Model):
    VERDICT = [('pass','Pass'), ('fail','Fail')]
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='verifications')
    technician = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='verifications_done')
    verdict = models.CharField(max_length=10, choices=VERDICT)
    notes = models.TextField(blank=True)
    tested_at = models.DateTimeField(auto_now_add=True)
    checklist = models.JSONField(default=dict, blank=True)
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.verdict == 'pass':
            self.listing.status = 'verified'
        else:
            self.listing.status = 'rejected'
        self.listing.save()
    def __str__(self):
        return f"Verification: {self.listing.title} -> {self.verdict}"
