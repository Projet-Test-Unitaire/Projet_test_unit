#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  2 10:24:48 2021

@author: mockingbird
"""

# pytest -v --capture sys -rF --capture sys -rP --html=test_report.html tests/test_integration.py


import pytest
from tests.conftest import client, _server_start_index, _login_club, _load_clubs, _load_competitions, _book_place, _logout_club, _test_dashboard_page

# 13th test_integration [route : all]
"""
Tests d’intégration (fichier server.py) :
"""
def test_integration(client):
    _load_clubs()
    _load_competitions()
    _server_start_index(client) # index
    _test_dashboard_page(client)
    _login_club(client, 'kate@shelifts.co.uk')
    rv = client.get('/book/{}/{}'.format('Fall Classic', 'She Lifts'), follow_redirects = True)
    assert rv.status_code == 200
    assert rv.data.decode().find('<h2>Fall Classic</h2>')!= -1
    _book_place(client, 1, 12, 9, 'Fall Classic', 'She Lifts')
    _logout_club(client)