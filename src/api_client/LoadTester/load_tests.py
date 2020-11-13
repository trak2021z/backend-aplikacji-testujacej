from api_client.LoadTester.abstract import LoadTesterBase
import os


class ExampleTest(LoadTesterBase):
    def set_up(self):
        pass

    def test_func(self):
        result = self.counted_requests.post("%s/rest-auth/login/" % os.getenv("BACKEND_URL"), json={"username": "szatku", "password": "qwert6"})
        print(self.counted_requests.get("%s/transaction/" % os.getenv("BACKEND_URL"), headers={"Authorization": "Bearer %s" % result.json()['token']}))
        print(self.counted_requests.get("%s/transaction/" % os.getenv("BACKEND_URL"), headers={"Authorization": "Bearer %s" % result.json()['token']}))
        print(self.counted_requests.get("%s/transaction/" % os.getenv("BACKEND_URL"), headers={"Authorization": "Bearer %s" % result.json()['token']}))

    def tear_down(self):
        pass