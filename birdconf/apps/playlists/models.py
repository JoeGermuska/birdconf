from django.db import models

from datetime import date
from urlparse import urljoin

class Track(models.Model):
    """An individual recording, which might be played on more than one occasion. Not currently
    worrying about the same recording appearing on multiple albums."""
    artist = models.TextField(null=True)
    title = models.TextField(null=True)
    album = models.TextField(null=True)
    label = models.TextField(null=True)
    
    class Meta:
        ordering = []
        verbose_name, verbose_name_plural = "Track", "Tracks"

    def __unicode__(self):
        return u"'%s' by %s" % (self.title,self.artist)

    @models.permalink
    def get_absolute_url(self):
        return ('Track', [self.id])

class Show(models.Model):
    """(Show description)"""
    air_date = models.DateField(blank=False, null=True, auto_now_add=False)
    tracks = models.ManyToManyField(Track, through='ShowTrack')

    class Meta:
        ordering = []
        verbose_name, verbose_name_plural = "Show", "Shows"

    def __unicode__(self):
        try:
            return self.air_date.strftime('%Y-%m-%d')
        except AttributeError:
            return self.air_date

    @models.permalink
    def get_absolute_url(self):
        return ('show', [self.air_date.strftime('%Y-%m-%d')])

class ShowTrack(models.Model):
    """An occasion on which a track was played on a specific show."""
    show = models.ForeignKey(Show)
    track = models.ForeignKey(Track)
    played_at = models.DateTimeField(blank=True, null=True, auto_now_add=False)
    display_order = models.IntegerField()

    class Meta:
        ordering = ['display_order']
        verbose_name, verbose_name_plural = "ShowTrack", "ShowTracks"

    def __unicode__(self):
        return u"ShowTrack"

    @models.permalink
    def get_absolute_url(self):
        return ('ShowTrack', [self.id])

class AudioFile(models.Model):
    """(AudioFile description)"""
    url = models.URLField(blank=False, verify_exists=True,unique=True)
    show = models.ForeignKey(Show,blank=True)

    class Meta:
        ordering = ['url']
        verbose_name, verbose_name_plural = "AudioFile", "AudioFiles"

    def __unicode__(self):
        return self.url

    @models.permalink
    def get_absolute_url(self):
        return ('AudioFile', [self.id])


def show_from_json(air_date,tracks):
    s = Show(air_date=air_date)
    s.save()
    for i,d in enumerate(tracks):
        match_dict = {
        }
        t,created = Track.objects.get_or_create(artist=d.get('artist'),title=d.get('track'),album=d.get('album'),label=d.get('label'))
        try:
            st = ShowTrack(show=s,track=t,played_at="%(date_str)s %(time_str)s" % d,display_order=i)
        except KeyError:
            st = ShowTrack(show=s,track=t,display_order=i)
        st.save()
    return s
    
def track_from_json(d):
    """
    {u'album': u'Closer',
     u'artist': u'Paul Bley Trio',
     u'date_str': u'2008-09-09',
     u'label': u'ESP Disk',
     u'time_str': u'05:00:00',
     u'track': u'Cartoon',
     u'unix_time': 1220954400.0}
    """
    t = Track(show)
    t.artist=d['artist']
    t.title=d['track']
    t.album=d['album']
    t.label=d['label']
    t.played_at="%(date_str)s %(time_str)s" % d
    return t

def add_audio_files():
    BASE = "http://blog.germuska.com/wnur/"
    with open("data/playlists/audio_urls.txt") as f:
        for line in f:
            line = line.strip()
            dot,date,filename = line.split('/')
            air_date = '-'.join([date[:4],date[4:6],date[6:]])
            try:
                show = models.Show.objects.get(air_date=air_date)
                af = models.AudioFile(url=urljoin(BASE,line), show=show)
                af.save()
            except Exception, e:
                print e

