#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  2 13:05:16 2021

@author: mockingbird
"""
import pytest
from server import app, loadClubs, loadCompetitions

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def _server_start_index(client):
    rv = client.get('/')
    assert rv.status_code == 200
    template = app.jinja_env.get_template('index.html')
    assert template.render() == rv.get_data(as_text=True) 

def _pages_return_correct_html_get(client, route, page):
    rv = client.get(route, follow_redirects = True)
    assert rv.status_code == 200
    template = app.jinja_env.get_template(page)
    assert template.render() == rv.get_data(as_text=True) 

def _login_club(client):
    email = 'admin@irontemple.com'
    rv = client.post('/showSummary', data = dict(email = email), follow_redirects = True)
    assert rv.status_code == 200
    assert rv.data.decode().find("Welcome, {}".format(email)) != -1

def _book_place(client, placesToPurchase, newAvailiblePLaces=None, newAvailiblePoints=None):
    rv = client.post('/purchasePlaces', data =dict(club = 'Iron Temple', competition='Grand Canyon', places = placesToPurchase), follow_redirects = True)
    data = rv.data.decode()
    assert 'Great-booking complete!' in data
    assert '<span class="text-muted h4">Points available: {}</span>'.format(newAvailiblePoints) in data
    assert '<td>{}</td>'.format(newAvailiblePLaces) in data

def _book_place_failed(client, placesToPurchase, club, competition, error):
    rv = client.post('/purchasePlaces', data =dict(club = club, competition = competition , places = placesToPurchase), follow_redirects = True)
    data = rv.data.decode()
    if error == 1:
        assert data.find('Not enought points !') or data.find('Not enought places availible !') or data.find('Invalid amount of requiered places')
    elif error == 2:
        assert data.find('Too many places requiered')
    elif error == 3:
        assert data.find('Old date, booking impossible !')

def _logout_club(client):
    rv = client.get("/logout", follow_redirects=True)
    assert rv.status_code == 200
    data = rv.data.decode()
    assert '<li>You&#39;re now disconnected</li>' in data


def _load_clubs():
    clubs = loadClubs()
    assert clubs != []
    assert list(clubs[0].keys()) == ['name', 'email', 'points', 'id']

def _load_competitions():
    clubs = loadCompetitions()
    assert clubs != []
    assert list(clubs[0].keys()) == ['name', 'date', 'numberOfPlaces', 'id']