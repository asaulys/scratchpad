#!/usr/bin/env python

import json
import pprint
import requests
import typing


# TODO(aras) move this to a config
DEFAULT_URL = "https://jsonplaceholder.typicode.com/todos"


def get_text(url: str) -> typing.Union[str, None]:
  """performs get request and returns string
  """
  return requests.get(url).text

def process(url):
  text = get_text(url)
  json_data = json.loads(text)
  pprint.pprint(json_data)

def main():
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument("-u", "--url", dest="url", default=DEFAULT_URL, help="the url to query")
  args = parser.parse_args()
  
if __name__ == "__main__":
  main()
