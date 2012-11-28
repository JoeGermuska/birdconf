#!/usr/bin/env python
# -*- coding: utf-8 -*-
from lxml.html import parse as html_parse
from dateutil.parser import parse as date_parse
from lxml import etree
from lxml.cssselect import CSSSelector
from urllib2 import urlopen
from urlparse import urljoin
from time import mktime
import codecs
from csvkit import UnicodeCSVWriter
from django.conf import settings
import os, os.path
import json
from django.conf import settings
import re
from playlists import models

PATTERN = re.compile(r'^(.+?)_(\d+?)$')

JSON_PATH = os.path.join(settings.SITE_ROOT,"../data/playlists/complete.json")

DJ_SEARCH_URL = "http://www.wnur.org/playlist/search/?pickdj=Joe+G"

KEEPER_KEYS = [u'album',
 u'artist',
 u'track',
 u'unix_time',
 u'label',
 u'date_str',
 u'time_str']

def load_json_playlists():
    return json.load(open(JSON_PATH))
    
def dump_json_playlists(playlists):
    with open(JSON_PATH,"w") as f:
        json.dump(playlists,f,indent=2)
    print "json dumped"    


def update_json_from_forms():
    shows = load_json_playlists()
    air_dates = set(s[0] for s in shows)
    for dir,subdirs,files in os.walk(os.path.join(settings.SITE_ROOT,'../data/forms2scrape')):
        for fn in files:
            datestr,ext = fn.split('.')
            if date_parse(datestr).strftime('%Y-%m-%d') in air_dates:
                print "found show, skipping %s" % (fn)
            else:
                date_str,tracks = parse_playlist_form(open(os.path.join(dir,fn)))
                shows.append((date_str,tracks))
                print "added %s" % date_str

    return shows

def print_show(show):
    if len(show) == 2:
        show = show[-1]
    # else assume it's jus the tracks    
    tmpl = u'%(artist)s: “%(track)s” – %(album)s (%(label)s)'
    for track in show:
        rendered = tmpl % track
        print rendered.encode('utf-8')

def add_playlist_from_form(path):
    if not os.path.isabs(path):
        path = os.path.join(settings.SITE_ROOT,path)
    show = parse_playlist_form(open(path))
    shows = load_json_playlists()
    shows.append(show)
    dump_json_playlists(shows)
    print_show(show)
    
def parse_playlist_form(fp):
    show_date = None
    doc = html_parse(fp)
    inputs = {}
    for input in doc.getroot().body.xpath('//input[@type="text"]'):
        if input.attrib['name'] == 'date':
            show_date = date_parse(input.attrib['value'])
        elif PATTERN.match(input.attrib['name']):
            field,num = PATTERN.match(input.attrib['name']).groups()
            if field == 'timestamp':
                try:
                    time = date_parse(input.attrib['value'])
                    real_date = date_parse(show_date.strftime('%Y-%m-%d') + ' ' + time.strftime('%H:%M:%S'))
                    d = inputs.setdefault(int(num),{})
                    d['unix_time'] = mktime(real_date.timetuple())
                    d['date_str'] = real_date.strftime('%Y-%m-%d')
                    d['time_str'] = real_date.strftime('%H:%M:%S')
                except: pass # 'auto' probably
            else:
                try:
                    value = input.attrib['value']
                    inputs.setdefault(int(num),{})[field] = value
                except KeyError: pass
                
    show = []
    for k in sorted(inputs):
        d = dict((key,inputs[k].get(key,None)) for key in KEEPER_KEYS)
        if filter(None,d.values()):
            show.append(d)
    return (show[0]['date_str'],show)

def show_links():
    a = CSSSelector('a').path
    doc = html_parse(urlopen(DJ_SEARCH_URL))
    for link in doc.getroot().xpath(a):
        href = link.attrib.get('href')
        if href and href.startswith('../archive/?date='):
            yield urljoin(DJ_SEARCH_URL,href)

def parse_text_files():
    BASE = 'data/playlists/txt'
    shows = []
    for fn in os.listdir(BASE):
        datepart = fn.split('.')[0]
        date = u'-'.join([datepart[:4],datepart[4:6],datepart[6:]])
        tracks = parse_txt_file(os.path.join(BASE,fn))
        shows.append((unicode(date),tracks))
    return shows

TRACK_PATTERN = re.compile(r'^(?P<artist>.+): “(?P<track>.+)” – (?P<album>.+)?\s*(?:\((?P<label>.+)\))$')
TRACK_PATTERN2 = re.compile(r'^(?P<artist>.+):\s+“(?P<track>.+)”\s*$')
TRACK_PATTERN3 = re.compile(r'^(?P<artist>.+): “(?P<track>.+)”?\s*(?:\((?P<label>.+)\))$')
TRACK_PATTERN4 = re.compile(r'^(?P<artist>.+): “(?P<track>.+)” – (?P<album>.+)?$')
def parse_txt_file(path):
    tracks = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            try:
                if TRACK_PATTERN.match(line):
                    match = TRACK_PATTERN.match(line)
                elif TRACK_PATTERN2.match(line):
                    match = TRACK_PATTERN2.match(line)
                elif TRACK_PATTERN3.match(line): 
                    match = TRACK_PATTERN3.match(line)
                else: match = TRACK_PATTERN4.match(line)
                tracks.append(match.groupdict())
            except AttributeError: # only five lines in Pieter's show so handled manually after the fact for now...
                print "Weird line in %s!\n%s" % (path,line)
                tracks.append(line)
    return tracks