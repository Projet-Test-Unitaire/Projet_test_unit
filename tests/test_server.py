#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  2 10:24:48 2021

@author: mockingbird
"""

import pytest
from tests.conftest import client, _login_club, _book_place, _book_place_failed, _logout_user, _load_All
        
# 2nd test [route : index]
"""
Ecrire un test unitaire pour s’assurer que le serveur se lance correctement et que la page index s’affiche
proprement ?
"""            
def test_home_page_returns_correct_html(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'<input' in response.data        
	
def test_server_start(client):
    rv = client.get('/', follow_redirects = False)
    assert rv.status_code == 200
    assert b'<form' in rv.data, b'<input' in rv.data
    
# 3rd test [route : showSummary][params : (email)]
"""
Un test unitaire pour s’assurer qu’un Summary est affiché lorsqu'un secretary email (d’un club) est saisi dans
le formulaire de la page index ?
"""
def test_summary_print_on_email_valid(client):
    _login_club(client)

# 4th test [route : showSummary][params : (email)]
"""
Un test unitaire pour s'assurer qu’un message d’erreur est affiché lorsque le secrétaire du club saisi un
email incorrect (par exemple : “Désolé, cet email n'a pas été trouvé”) ?
"""
def test_summary_print_on_email_invalid(client):
    rv = client.post('/showSummary', data = dict(email = 'test@simplylift.co'), follow_redirects = True)
    assert rv.status_code == 403
    print(rv.data)
    assert rv.data.decode().find("Sorry, this doesn&#39;t exist !") != -1

# 5th test [route : book]
"""
Un test pour s'assurer qu'il affiche une page booking.html pour un club ou une compétition valide ?
"""
def test_booking_valid_params(client):
    rv = client.get('/book/{}/{}'.format('Spring Festival', 'Iron Temple'), follow_redirects = True)
    assert rv.status_code == 200
    assert rv.data.decode().find('<h2>Spring Festival</h2>')!= -1

# 6th test [route : book]
"""
Un test pour s'assurer que l'interface utilisateur empêche la réservation d'un club ou d'une compétition
non valide ?
"""
def test_booking_invalid_params(client):
    _login_club(client)
    rv = client.get('/book/{}/{}'.format('test_competition', 'test_club'), follow_redirects = True)
    assert rv.status_code == 400
    assert rv.data.decode().find('Something went wrong-please try again')!= -1

# 7th test [route : book/purchasePlaces][params : (email, compétition, club, points)]
"""
Un test pour s'assurer que lorsque l’User achète avec succès, les places sont correctement déduites du
concours et les points déduits d'un club ?
"""
def test_but_success_decrement_point_to_point(client):
    _login_club(client)
    _book_place(client, 1, 24, 1)

# 8th test [route : book/purchasePlaces][params : ()]
"""
Un test pour s'assurer qu'il affiche le message d'erreur souhaité lorsqu'il y a plus de 12 places ?
"""
def test_error_msg_places(client):
    _login_club(client)
    _book_place_failed(client, 13)

# 9th test [route : book/purchasePlaces]
"""
Un test pour s'assurer qu'il affiche le message d'erreur souhaité lorsque l'utilisateur s'engage à acheter
plus de places que les points disponibles ?
"""
def test_not_enough_points(client):
    _login_club(client)
    _book_place_failed(client, 12)

# 10th page web [route : dashboard]
""" 
Livrable : Une page séparée qui comprends un tableau montrant la liste des clubs et les soldes de points
respectifs actualisés. Aussi, les utilisateurs peuvent voir le tableau sans se connecter.
"""
 # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
 # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

# 11th page web [route : dashboard]
""" 
Modifier la valeur des points (selon le mail de Zayn) : L'échange actuel de 1 point = 1 place de compétition
a été mis à jour de sorte que 3 points = 1 place de compétition.
"""
def test_but_success_decrement_point_to_3point(client):
    _login_club(client)
    _book_place(client, 0, 24, 1)

# 12th test [route : logout]
"""
Test unitaire pour logout ?
"""
def test_logout(client):
    _logout_user(client)

# 13th test_integration [route : all]
"""
Tests d’intégration (fichier server.py) :
"""
def test_integration(client):
    _load_All(client)

# 14th rapport [FINAL]
"""
Vérifier la couverture des tests. Livrable : rapport de couverture achevés.
"""