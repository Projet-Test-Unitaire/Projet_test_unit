#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  2 10:24:48 2021

@author: mockingbird
"""

# pytest -v --capture sys -rF --capture sys -rP --html=test_report.html tests/test_integration.py


import pytest
from tests.conftest import client, _server_start_index, _login_club, _load_clubs, _load_competitions, _book_place, _logout_club

# 13th test_integration [route : all]
"""
Tests d’intégration (fichier server.py) :
"""
def test_integration(client):
    _load_clubs()
    _load_competitions()
    _server_start_index(client) # index
    _login_club(client)
    rv = client.get('/book/{}/{}'.format('Spring Festival', 'Iron Temple'), follow_redirects = True)
    assert rv.status_code == 200
    assert rv.data.decode().find('<h2>Spring Festival</h2>')!= -1
    _book_place(client, 1, 12, 10)
    _logout_club(client)