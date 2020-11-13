from django.core.management.base import BaseCommand
from api_client.models import *
import random


class Command(BaseCommand):
    def handle(self, **options):
        log_in = Endpoint.objects.create(url="rest-auth/login/", name="Logowanie", request="")
        log_out = Endpoint.objects.create(url="rest-auth/logout/", name="Wylogowanie", request="")
        user = Endpoint.objects.create(url="rest-auth/user/", name="Szczegóły aktualnego użytkownika", request="")
        registration = Endpoint.objects.create(url="rest-auth/registration/", name="Rejestracja użytkownika", request="")
        password_change = Endpoint.objects.create(url="rest-auth/password/change/", name="Zmiana hasła", request="")
        company = Endpoint.objects.create(url="company/", name="Lista wszystkich firm", request="")
        company_detail = Endpoint.objects.create(url='company/<company_id>', name="Szczegóły dotyczące firmy", request="")
        stocks = Endpoint.objects.create(url='stocks/', name="Lista wszystkich dostępnych zasobów", request="")
        stock_detail = Endpoint.objects.create(url='stock/<stock_id>', name="Szczegóły pojedynczego zasobu", request="")
        stock_buy = Endpoint.objects.create(url='stock/<stock_id>/buy/', name="Szczegóły pojedynczego zasobu",
                                request='{"quantity": 0}')
        stock_create = Endpoint.objects.create(url='stock/<stock_id>/sell/', name="Szczegóły pojedynczego zasobu",
                                request='{"quantity": 0}')
        transactions_stock = Endpoint.objects.create(url='transaction/<stock_id>',
                                name="Lista wszystkich zleceń kupna i sprzedaży dla danego zasobu", request="")
        transactions = Endpoint.objects.create(url='transaction/>', name="Lista wszystkich zleceń kupna i sprzedaży", request="")
        wallet = Endpoint.objects.create(url='user/wallet/', name="Stan portfela obecnego użytkownika", request="")
        user_stocks = Endpoint.objects.create(url='user/stocks/', name="Lista zasobów posiadanych przez użytkownika", request="")
        offers = Endpoint.objects.create(url='user/offers/', name="Lista obecnych ofert sprzedaży/kupna danego użytkownika",
                                request="")
        history = Endpoint.objects.create(url='user/history/', name="Lista zrealizowanych transakcji danego użytkownika",
                                request="")

        endpoints = Endpoint.objects.all()
        print(endpoints)

        example_test = Test.objects.create(name= "Example Test", description="Example Test", class_name="ExampleTest")
        TestEndpoint.objects.create(test=example_test, endpoint=log_in, order=0)
        TestEndpoint.objects.create(test=example_test, endpoint=transactions, order=1)
        TestEndpoint.objects.create(test=example_test, endpoint=transactions, order=2)
        TestEndpoint.objects.create(test=example_test, endpoint=transactions, order=3)

        print("DONE")