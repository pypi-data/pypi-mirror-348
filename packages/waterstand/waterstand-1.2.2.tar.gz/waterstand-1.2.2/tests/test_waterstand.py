""" testen voor de package waterstand """
import json
import unittest
from unittest.mock import patch, MagicMock, ANY

from requests.exceptions import HTTPError, Timeout, RequestException

import waterstand


def create_mock_response(filenaam):
  """ maak een response van de testdata """
  with open(filenaam, 'r', encoding='utf-8') as fid:
    testdata = json.loads(fid.read().encode('utf-8'))

  print(testdata)

  mock_response = MagicMock()
  mock_response.getcode.return_value = 200
  mock_response.json.return_value = testdata
  mock_response.__enter__.return_value = mock_response
  return mock_response


class TestWaterstand(unittest.TestCase):
  """ Class voor het testen van de package waterstand """

  @patch('requests.get')
  def test_haalwaterstand(self, mock_requestsget):
    """ test van de normale flow """
    mock_requestsget.return_value = create_mock_response('tests/testdata.json')

    response = waterstand.haalwaterstand('Katerveer', 'KATV')
    verwacht = {'resultaat': 'OK', 'tijd': '23-11 16:50', 'nu': 84.0, 'morgen': 89.0}

    self.assertEqual(response, verwacht)

  @patch('requests.get')
  def test_haalwaterstand_timeformat(self, mock_requestsget):
    """ test 2 van de normale flow """
    mock_requestsget.return_value = create_mock_response('tests/testdata2.json')

    response = waterstand.haalwaterstand('Katerveer', 'KATV')
    verwacht = {'resultaat': 'OK', 'tijd': '23-11 16:50', 'nu': 84.0, 'morgen': 89.0}

    self.assertEqual(response, verwacht)

  @patch('requests.get', side_effect=HTTPError('', 0, '', None, None))
  def test_haalwaterstand_httperror(self, mock_requestsget):
    """ test van een HTTP-fout bij het ophalen """
    response = waterstand.haalwaterstand('Katerveer', 'KATV')

    expected = {'resultaat': 'NOK', 'error': ANY}
    self.assertEqual(response, expected)
    assert mock_requestsget.called

  @patch('requests.get', side_effect=TimeoutError)
  def test_haalwaterstand_timeouterror(self, mock_requestsget):
    """ test van een time-out bij het ophalen """
    response = waterstand.haalwaterstand('Katerveer', 'KATV')

    expected = {'resultaat': 'NOK', 'error': ANY}
    self.assertEqual(response, expected)
    assert mock_requestsget.called

  @patch('requests.get', side_effect=ConnectionError)
  def test_haalwaterstand_connectionerror(self, mock_requestsget):
    """ Test van een connection error bij het ophalen """
    response = waterstand.haalwaterstand('Katerveer', 'KATV')

    expected = {'resultaat': 'NOK', 'error': ANY}
    self.assertEqual(response, expected)
    assert mock_requestsget.called

  @patch('requests.get', side_effect=Timeout())
  def test_haalwaterstand_timeout(self, mock_requestsget):
    """ Test van een Time-out bij het ophalen """
    response = waterstand.haalwaterstand('Katerveer', 'KATV')

    expected = {'resultaat': 'NOK', 'error': ANY}
    self.assertEqual(response, expected)
    assert mock_requestsget.called

  @patch('requests.get', side_effect=RequestException())
  def test_haalwaterstand_requestexception(self, mock_requestsget):
    """ Test van een algemene exceptie bij het ophalen """
    response = waterstand.haalwaterstand('Katerveer', 'KATV')

    expected = {'resultaat': 'NOK', 'error': ANY}
    self.assertEqual(response, expected)
    assert mock_requestsget.called
