from django.contrib import admin
from .models import Listing, ListingImage, Verification
class ListingImageInline(admin.TabularInline):
    model = ListingImage
@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ('title','seller','price','status','created_at')
    list_filter = ('status','condition')
    inlines = [ListingImageInline]
@admin.register(Verification)
class VerificationAdmin(admin.ModelAdmin):
    list_display = ('listing','verdict','technician','tested_at')
    readonly_fields = ('tested_at',)
