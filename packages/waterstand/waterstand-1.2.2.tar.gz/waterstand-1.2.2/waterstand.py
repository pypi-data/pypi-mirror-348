"""
Ophalen van de waterstand. Gegevens komen van https://waterinfo.rws.nl/ en de gegevens voor vandaag
en morgen worden er uit gehaald.
"""
from datetime import datetime, timedelta

import requests


def leesjson(url: str) -> dict:
  """
  Haal JSON van de URL op
  :param url: URL waar de JSON opgehaald moet worden
  :type url: str
  :return: JSON
  :rtype: dict
  """
  try:
    headers = {'Accept': 'application/json'}
    req = requests.get(url, headers=headers, verify=False, timeout=10, allow_redirects=False)
    contentjson = req.json()
    contentjson['resultaat'] = 'OK'
    return contentjson
  except (ConnectionError,
          TimeoutError,
          requests.exceptions.HTTPError,
          requests.exceptions.RequestException) as error:
    return {'resultaat': 'NOK',
            'error': f'Error: Data ophalen mislukt vanwege {error}\nURL: {url}'}


def leeswaterstandjson(naam: str, afkorting: str) -> dict:
  """
  Lees de informatie van bepaalde locatie van de API van RWS.
  :param naam: Naam van de locatie
  :type naam: str
  :param afkorting: Afkorting van de locatie
  :type afkorting: str
  :return: JSON met de waardes van de waterstanden
  :rtype: dict
  """
  url = 'https://waterinfo.rws.nl/api/chart/get' + \
        f'?mapType=waterhoogte&locationCodes={naam}({afkorting})&values=-48,48'
  return leesjson(url)


def bepaalstanden(waterstandjson: dict) -> dict:
  """
  Haal de noodzakelijke gegevens van de waterstand uit de gegevens van RWS.
  :param waterstandjson: Dict met de gegevens van de waterstanden
  :type waterstandjson: dict
  :return: JSON met de waardes van de waterstanden
  :rtype: dict
  """
  if waterstandjson['resultaat'] == 'NOK':
    return waterstandjson
  laatstetijdgemeten = waterstandjson['t0']
  gemetenstanden = waterstandjson['series'][0]['data']
  voorspeldestanden = waterstandjson['series'][1]['data']

  hoogtenu = -999
  for stand in gemetenstanden:
    if stand['dateTime'] == laatstetijdgemeten:
      hoogtenu = stand['value']

  if laatstetijdgemeten.endswith('Z'):
    tijdpatroon = '%Y-%m-%dT%H:%M:%SZ'
    deltatijd = 1
  else:
    tijdpatroon = '%Y-%m-%dT%H:%M:%S+02:00'
    deltatijd = 1

  laatstetijdobj = datetime.strptime(laatstetijdgemeten, tijdpatroon) \
                   + timedelta(hours=deltatijd)
  weergavetijd = laatstetijdobj.strftime('%d-%m %H:%M')
  morgenobj = laatstetijdobj + timedelta(days=1)
  morgentekst = morgenobj.strftime(tijdpatroon)

  hoogtemorgen = hoogtenu
  for stand in voorspeldestanden:
    if stand['dateTime'] == morgentekst:
      hoogtemorgen = stand['value']
  returnjson = {'resultaat': 'OK',
                'tijd': weergavetijd,
                'nu': hoogtenu,
                'morgen': hoogtemorgen}
  return returnjson


def haalwaterstand(naam: str, afkorting: str) -> dict:
  """
  Haal de waterstand van een locatie bij RWS en haal de noodzakelijke waarden daar uit.
  :param naam: Naam van de locatie
  :type naam: str
  :param afkorting: Afkorting van de locatie
  :type afkorting: str
  :return: JSON met de waardes van de waterstanden
  :rtype: dict
  """
  contentjson = leeswaterstandjson(naam, afkorting)
  return bepaalstanden(contentjson)
