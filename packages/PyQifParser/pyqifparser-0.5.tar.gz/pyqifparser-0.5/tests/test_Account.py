# -*- coding: utf-8 -*-
"""
@author: Uwe Ziegenhagen
"""

from Account import Account

def test_set_currency():
    a = Account()
    a.currency = 'EUR'
    assert a.currency == 'EUR'
    
def test_set_label():
    a = Account()
    a.label = 'Testlabel'
    assert a.label == 'Testlabel'

def test_set_description():
    a = Account()
    a.description = 'Test'
    assert a.description == 'Test'

def test_set_type():
    a = Account()
    a.type = 'CASH'
    assert a.type == 'CASH'

def test_clear():
    a = Account()
    a.type = 'CASH'
    a.description = 'Test'
    a.label = 'Testlabel'
    a.currency = 'EUR'
    a.clear()
    assert a.type == None    
    assert a.currency == None
    assert a.label == None
    assert a.description == None

