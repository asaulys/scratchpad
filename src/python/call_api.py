import requests

#
# more:
#   https://realpython.com/api-integration-in-python/
#
url = "http://icanhazip.com"
timeout = 5.0

try:
  response = requests.get(url, timeout=timeout)
  response.raise_for_status()
except requests.exceptions.HTTPError as errh:
  print(errh)
  raise
except requests.exceptions.ConnectionError as errc:
  print(errc)
  raise
except requests.exceptions.Timeout as errt:
  print(errt)
  raise
except requests.exceptions.RequestException as err:
  print(err)
  raise
