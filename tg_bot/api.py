import http.client


def getMockData(id=1):
  conn = http.client.HTTPSConnection('jsonplaceholder.typicode.com')
  conn.request('GET', '/todos/' + str(id))

  res = conn.getresponse()

  if res.status == 200:
    return res.read().decode()

  conn.close()
  raise Exception("Request error")
