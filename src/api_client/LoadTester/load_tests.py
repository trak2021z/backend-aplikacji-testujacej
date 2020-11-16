from api_client.LoadTester.abstract import LoadTesterBase
import os
from datetime import datetime
import requests
import decimal


class ExampleTest(LoadTesterBase):
    def set_up(self):
        pass

    def test_func(self):
        result = self.counted_requests.post("%s/rest-auth/login/" % os.getenv("BACKEND_URL"),
                                            json={"username": "szatku", "password": "qwert6"})
        print(self.counted_requests.get("%s/transaction/" % os.getenv("BACKEND_URL"),
                                        headers={"Authorization": "Bearer %s" % result.json()['token']}))
        print(self.counted_requests.get("%s/transaction/" % os.getenv("BACKEND_URL"),
                                        headers={"Authorization": "Bearer %s" % result.json()['token']}))
        print(self.counted_requests.get("%s/transaction/" % os.getenv("BACKEND_URL"),
                                        headers={"Authorization": "Bearer %s" % result.json()['token']}))

    def tear_down(self):
        pass


class BuyUntilFounds(LoadTesterBase):
    def set_up(self):
        username = "Stonks%s%d" % (datetime.now().strftime("%m%d%Y%H%M%S"), os.getpid())
        result = self.counted_requests.post("%s/rest-auth/registration/" % os.getenv("BACKEND_URL"),
                                            json={
                                                "username": username,
                                                "password1": "Stonk!2345",
                                                "password2": "Stonk!2345",
                                                "email": "%s@stonks.st" % username
                                            })
        self.user = result.json()['user']

    def test_func(self):
        result = self.counted_requests.post("%s/rest-auth/login/" % os.getenv("BACKEND_URL"),
                                            json={
                                                "username": self.user['username'],
                                                "password": "Stonk!2345"
                                            })
        token = result.json()['token']
        result = self.counted_requests.get("%s/stocks/" % os.getenv("BACKEND_URL"),
                                           headers={"Authorization": "Bearer %s" % token})
        while True:
            print(result)
            stocks = result.json()
            if not sum(map(lambda x: x['avail_amount'], stocks)):
                break

            for stock in stocks:
                result = self.counted_requests.post("%s/stocks/%d/buy/" % (os.getenv("BACKEND_URL"), stock['pk']),
                                                    headers={"Authorization": "Bearer %s" % token},
                                                    json={
                                                        'quantity': 1
                                                    })

            result = self.counted_requests.get("%s/stocks/" % os.getenv("BACKEND_URL"),
                                               headers={"Authorization": "Bearer %s" % token})

    def tear_down(self):
        if not hasattr(self, 'user'):
            return
        result = requests.post("%s/rest-auth/login/" % os.getenv("BACKEND_URL"),
                               json={"username": os.getenv("BACKEND_USER"), "password": os.getenv("BACKEND_PASSWORD")})
        requests.post("%s/user/delete/" % os.getenv("BACKEND_URL"), json={
            'users': [self.user['email']]
        },
                      headers={"OBCIAZNIK": "DUPA", "Authorization": "Bearer %s" % result.json()['token']})


class BuyOffersAll(LoadTesterBase):
    def set_up(self):
        username = "Stonks%s%d" % (datetime.now().strftime("%m%d%Y%H%M%S"), os.getpid())
        result = self.counted_requests.post("%s/rest-auth/registration/" % os.getenv("BACKEND_URL"),
                                            json={
                                                "username": username,
                                                "password1": "Stonk!2345",
                                                "password2": "Stonk!2345",
                                                "email": "%s@stonks.st" % username
                                            })
        self.user = result.json()['user']

    def test_func(self):
        result = self.counted_requests.post("%s/rest-auth/login/" % os.getenv("BACKEND_URL"),
                                            json={
                                                "username": self.user['username'],
                                                "password": "Stonk!2345"
                                            })
        token = result.json()['token']
        result = self.counted_requests.get("%s/stocks/" % os.getenv("BACKEND_URL"),
                                           headers={"Authorization": "Bearer %s" % token})
        print(result)
        stocks = result.json()

        for stock in stocks:
            result = self.counted_requests.post("%s/buyoffer/" % (os.getenv("BACKEND_URL")),
                                                headers={"Authorization": "Bearer %s" % token},
                                                json={
                                                    "stock": stock['pk'],
                                                    "unit_price": str(decimal.Decimal(stock['price']) + decimal.Decimal("0.01")),
                                                    "stock_amount": 1
                                                })

        result = self.counted_requests.get("%s/user/offers/" % os.getenv("BACKEND_URL"),
                                           headers={"Authorization": "Bearer %s" % token})

    def tear_down(self):
        if not hasattr(self, 'user'):
            return
        result = requests.post("%s/rest-auth/login/" % os.getenv("BACKEND_URL"),
                               json={"username": os.getenv("BACKEND_USER"), "password": os.getenv("BACKEND_PASSWORD")})
        requests.post("%s/user/delete/" % os.getenv("BACKEND_URL"), json={
            'users': [self.user['email']]
        },
                      headers={"OBCIAZNIK": "DUPA", "Authorization": "Bearer %s" % result.json()['token']})
