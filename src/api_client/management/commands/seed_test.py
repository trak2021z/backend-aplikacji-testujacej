from django.core.management.base import BaseCommand
from api_client.models import *
import random


class Command(BaseCommand):
    def handle(self, **options):
        Endpoint.objects.create(url="rest-auth/login/", name="Logowanie", request="")
        Endpoint.objects.create(url="rest-auth/logout/", name="Wylogowanie", request="")
        Endpoint.objects.create(url="rest-auth/user/", name="Szczegóły aktualnego użytkownika", request="")
        Endpoint.objects.create(url="rest-auth/registration/", name="Rejestracja użytkownika", request="")
        Endpoint.objects.create(url="rest-auth/password/change/", name="Zmiana hasła", request="")
        Endpoint.objects.create(url="company/", name="Lista wszystkich firm", request="")
        Endpoint.objects.create(url='company/<compsny_id>', name="Szczegóły dotyczące firmy", request="")
        Endpoint.objects.create(url='stocks/', name="Lista wszystkich dostępnych zasobów", request="")
        Endpoint.objects.create(url='stock/<stock_id>', name="Szczegóły pojedynczego zasobu", request="")
        Endpoint.objects.create(url='stock/<stock_id>/buy/', name="Szczegóły pojedynczego zasobu",
                                request='{"quantity": 0}')
        Endpoint.objects.create(url='stock/<stock_id>/sell/', name="Szczegóły pojedynczego zasobu",
                                request='{"quantity": 0}')
        Endpoint.objects.create(url='transaction/<stock_id>',
                                name="Lista wszystkich zleceń kupna i sprzedaży dla danego zasobu", request="")
        Endpoint.objects.create(url='transaction/>', name="Lista wszystkich zleceń kupna i sprzedaży", request="")
        Endpoint.objects.create(url='user/wallet/', name="Stan portfela obecnego użytkownika", request="")
        Endpoint.objects.create(url='user/stocks/', name="Lista zasobów posiadanych przez użytkownika", request="")
        Endpoint.objects.create(url='user/offers/', name="Lista obecnych ofert sprzedaży/kupna danego użytkownika",
                                request="")
        Endpoint.objects.create(url='user/history/', name="Lista zrealizowanych transakcji danego użytkownika",
                                request="")

        endpoints = Endpoint.objects.all()
        print(endpoints)
        for i in range(1, 25):
            test = Test.objects.create(name="Test %d" % i,
                                       description="Lorem ipsum maxad glodiam, habemus papam, Jebać PiS, Kaszanka.")
            print(test)
            for j, endpoint in enumerate(random.choices(endpoints, k=random.randint(1, len(endpoints)))):
                print(TestEndpoint.objects.create(test=test, endpoint=endpoint, order=j))

        print("DONE")