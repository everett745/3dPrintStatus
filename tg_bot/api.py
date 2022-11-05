import http.client
import json
from io import BytesIO

from PIL import Image

API_DOMAIN = '26.57.44.204'
API_PORT = 8080

STATUS_VALUE = {
  0: 'Замечена ошибка. Рекомендуется остановить печать',
  1: 'Все хорошо',
}


def getResponse(url):
  conn = http.client.HTTPConnection(API_DOMAIN, API_PORT)
  conn.request('GET', url)
  return conn.getresponse()


def makeRequest(url):
  res = getResponse(url)

  if res.status == 200:
    return json.loads(res.read().decode())

  raise Exception("Request error")


def getPrintStatusPicture():
  res = getResponse('/api/printstatus/getpicture').read()
  img = Image.open(BytesIO(res))
  return img


def getPrintStatus():
  data = makeRequest('/api/printstatus')
  image = getPrintStatusPicture()

  return {
    'status': STATUS_VALUE[data['status']],
    'image': image
  }
