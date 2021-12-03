#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  2 13:05:16 2021

@author: mockingbird
"""
import pytest
from server import app, loadClubs, loadCompetitions, index, showSummary, book, purchasePlaces, logout

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
    assert 'Not enought points !' in data or 'Not enought places availible !' in data or 'Too many places requiered' in data

def _logout_user(client):
    rv = client.get("/logout")
    assert rv.status_code == 302

def _load_All(client):
    # index()
    # loadClubs()
    # loadCompetitions()
    # showSummary()
    book('Iron Temple', 'Spring Festival')
    purchasePlaces()
    logout()