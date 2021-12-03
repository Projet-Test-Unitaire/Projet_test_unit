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


def _login_club(client):
    rv = client.post('/showSummary', data = dict(email = 'admin@irontemple.com'), follow_redirects = True)
    assert rv.status_code == 200
    assert rv.data.decode().find("Welcome, admin@irontemple.com") != -1

def _book_place(client, placesToPurchase, newAvailiblePLaces=None, newAvailiblePoints=None):
    rv = client.post('/purchasePlaces', data =dict(club = 'Iron Temple', competition='Spring Festival', places = placesToPurchase), follow_redirects = True)
    data = rv.data.decode()
    assert 'Great-booking complete!' in data
    assert 'Points available: {}'.format(newAvailiblePoints) in data
    assert 'Number of Places: {}'.format(newAvailiblePLaces) in data

def _book_place_failed(client, placesToPurchase):
    rv = client.post('/purchasePlaces', data =dict(club = 'Iron Temple', competition='Spring Festival', places = placesToPurchase), follow_redirects = True)
    data = rv.data.decode()
    assert 'Not enought points !' in data or 'Not enought places availible !' in data or 'Too many places requiered' in data, 'Invalid amount of requiered places' in data

def _logout_club(client):
    rv = client.get("/logout")
    assert rv.status_code == 302

def _server_start_index(client):
    rv = client.get('/')
    assert rv.status_code == 200
    assert b'<form' in rv.data, b'<input' in rv.data

def _load_clubs():
    clubs = loadClubs()
    assert clubs != []
    assert list(clubs[0].keys()) == ['name', 'email', 'points']

def _load_competitions():
    clubs = loadCompetitions()
    assert clubs != []
    assert list(clubs[0].keys()) == ['name', 'date', 'numberOfPlaces']