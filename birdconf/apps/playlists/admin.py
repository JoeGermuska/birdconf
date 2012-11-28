from django.contrib import admin
from playlists.models import Show, Track

class TrackAdmin(admin.ModelAdmin):
    list_filter = ('artist','label')

class ShowAdmin(admin.ModelAdmin):
    list_filter = ('air_date',)

admin.site.register(Track, TrackAdmin)
admin.site.register(Show, ShowAdmin)
