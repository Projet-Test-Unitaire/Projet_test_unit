#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  2 10:24:48 2021

@author: mockingbird
"""

import pytest

from server import app
        
# 1er test [root : index]
def test_server_start():
    client = app.test_client()
    rv = client.get('/', follow_redirects = False)
    assert rv.status_code == 200
    assert b'<form' in rv.data, b'<input' in rv.data
    
# 2nd test [root : showSummary][params : (email)]
def test_summary_print_on_email_valid():
    client = app.test_client()
    rv = client.post('/showSummary', data = dict(email = 'john@simplylift.co'), follow_redirects = True)
    assert rv.status_code == 200
    
def test_summary_print_on_email_invalid():
    client = app.test_client()
    rv = client.post('/showSummary', data = dict(email = 'test@simplylift.co'), follow_redirects = True)
    assert rv.status_code == 500

