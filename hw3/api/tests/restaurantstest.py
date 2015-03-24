import requests
s = requests.Session()
host='http://localhost'   #  replace by your host here
s.headers.update({'Accept': 'application/json'})

r = s.get('http://localhost/restaurants',)
print r.status_code
if r.status_code == requests.codes.ok:
    print(r.json())

r = s.post('http://localhost/restaurants')
print '\n', r.status_code
if r.status_code == requests.codes.ok:
    print(r.text)


r = s.get('http://localhost/restaurants/11')
print '\n', r.status_code
if r.status_code == requests.codes.ok:
    print(r.text)

r = s.get('http://localhost/restaurants/11/categories')
print '\n', r.status_code
if r.status_code == requests.codes.ok:
    print(r.json())


r = s.get('http://localhost/restaurants/11/categories/82')
print '\n', r.status_code, r.text


r = s.get('http://localhost/restaurants/11/categories/82/items')
print '\n', r.status_code
if r.status_code == requests.codes.ok:
    print(r.json())

r = s.get('http://localhost/orders')
print '\n', r.status_code
if r.status_code == requests.codes.ok:
	print(r.json())

r = s.put('http://localhost/orders', json = {'userID': 1})
print '\n', r.status_code
if r.status_code == requests.codes.ok:
        print(r.json())

r = s.get('http://localhost/orders/4')
print '\n', r.status_code
if r.status_code == requests.codes.ok:
        print(r.json())

r = s.put('http://localhost/orders/4')
print '\n', r.status_code
if r.status_code == requests.codes.ok:
        print(r.text)

r = s.delete('http://localhost/orders/4')
print '\n', r.status_code
if r.status_code == requests.codes.ok:
        print(r.text)

r = s.get('http://localhost/orders/4/checkout')
print '\n', r.status_code
if r.status_code == requests.codes.ok:
        print(r.json())

r = s.put('http://localhost/orders/4/checkout')
print '\n', r.status_code
if r.status_code == requests.codes.ok:
        print(r.text)

r = s.put('http://localhost/orders/4/items/1205', json = {'quantity': 1})
print '\n', r.status_code
if r.status_code == requests.codes.ok:
        print(r.json())

r = s.get('http://localhost/orders/4/items/1205')
print '\n', r.status_code
if r.status_code == requests.codes.ok:
        print(r.json())

r = s.delete('http://localhost/orders/4/items/1205')
print '\n', r.status_code
if r.status_code == requests.codes.ok:
        print(r.json())
