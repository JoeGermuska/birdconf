# Create your views here.
import os.path

import json

from django.conf import settings
from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.http import Http404
from datetime import date
import models 

PLAYLIST_PATH = os.path.join(settings.SITE_ROOT, "../data/playlists/complete.json")
all_playlists = json.load(open(PLAYLIST_PATH))

def track(request,slug=None):
    if slug is not None:
        raise Http404
    artist = request.REQUEST.get('artist')
    label = request.REQUEST.get('label')
    album = request.REQUEST.get('album')
    title = request.REQUEST.get('title')
    query = {}
    if artist: query['artist__icontains'] = artist
    if label: query['label__icontains'] = label
    if album: query['album__icontains'] = album
    if title: query['title__icontains'] = title
    tracks = models.Track.objects.filter(**query)
    return render_to_response("track.html",
    {   
        'artist': artist,
        'title': title,
        'album': album,
        'label': label,
        'tracks': tracks,
    })
def show(request, air_date):
    show = get_object_or_404(models.Show,air_date=air_date)
    try:
        previous = models.Show.objects.filter(air_date__lt=show.air_date).order_by('-air_date')[0]
    except IndexError:
        previous = None
    try:
        next = models.Show.objects.filter(air_date__gt=show.air_date)[0]
    except IndexError:
        next = None
    return render_to_response("show.html",
        {
            'show': show,
            'previous': previous,
            'next': next,
        }
    )

def all(request):
    playlists = models.Show.objects.all()
    return render_to_response("shows.html", 
        { 'shows': playlists,
          'title': "All of Joe's Playlists",
        })
        
def last_year(request):
    playlists = models.Show.objects.all()
    title = "compute title based on dates..."
    return render_to_response("shows.html", 
        { 'shows': playlists,
          'title': title,
        })
    
def mardigras(request):
    mgdates = [date(2014,3,4),date(2012,2,21),date(2009,2,17),date(2013,2,12)]
    title="Mardi Gras shows"
    shows = models.Show.objects.filter(air_date__in=mgdates)
    return render_to_response("shows.html", 
        { 'shows': shows,
          'title': title,
        })
