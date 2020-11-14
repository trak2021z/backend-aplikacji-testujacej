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
        stock_buy = Endpoint.objects.create(url='stock/<stock_id>/buy/', name="Kupno pojedynczego zasobu",
                                request='{"quantity": 0}')
        stock_sell = Endpoint.objects.create(url='stock/<stock_id>/sell/', name="Sprzedaż pojedynczego zasobu",
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
        buy_offer = Endpoint.objects.create(url='buyoffer/', name="Oferty kupna",
                                request="")
        sell_offer = Endpoint.objects.create(url='selloffer/', name="Oferty sprzedaży",
                                request="")
        price_history = Endpoint.objects.create(url='price_history/', name="Historia cen akcji",
                                request="")                        

        endpoints = Endpoint.objects.all()
        print(endpoints)

        test_1 = Test.objects.create(name= "Kupuj kolejne, dopóki są fundusze", 
                                    description="Kupno kolejnych akcji z listy do końca funduszy lub akcji", class_name="Test1")
        TestEndpoint.objects.create(test=test_1, endpoint=registration, order=0)
        TestEndpoint.objects.create(test=test_1, endpoint=log_in, order=1)
        TestEndpoint.objects.create(test=test_1, endpoint=stocks, order=2)
        TestEndpoint.objects.create(test=test_1, endpoint=wallet, order=3)
        TestEndpoint.objects.create(test=test_1, endpoint=stock_buy, order=4)

        test_2 = Test.objects.create(name= "Oferty kupna do oporu", 
                                    description="Wystawiaj oferty kupna do końca akcji", class_name="Test2")
        TestEndpoint.objects.create(test=test_2, endpoint=registration, order=0)
        TestEndpoint.objects.create(test=test_2, endpoint=log_in, order=1)
        TestEndpoint.objects.create(test=test_2, endpoint=stocks, order=2)
        TestEndpoint.objects.create(test=test_2, endpoint=buy_offer, order=3)
        TestEndpoint.objects.create(test=test_2, endpoint=offers, order=4)

        test_3 = Test.objects.create(name= "Kupuj do oporu i wystawiaj oferty sprzedaży", 
                                    description="Kupno do oporu, wystawiaj oferty sprzedaży do końca akcji", class_name="Test3")
        TestEndpoint.objects.create(test=test_3, endpoint=registration, order=0)
        TestEndpoint.objects.create(test=test_3, endpoint=log_in, order=1)
        TestEndpoint.objects.create(test=test_3, endpoint=stocks, order=2)
        TestEndpoint.objects.create(test=test_3, endpoint=wallet, order=3)
        TestEndpoint.objects.create(test=test_3, endpoint=stock_buy, order=4)
        TestEndpoint.objects.create(test=test_3, endpoint=user_stocks, order=5)
        TestEndpoint.objects.create(test=test_3, endpoint=sell_offer, order=6)
        TestEndpoint.objects.create(test=test_3, endpoint=offers, order=7)
        TestEndpoint.objects.create(test=test_3, endpoint=history, order=8)

        test_4 = Test.objects.create(name= "Kupuj i sprzedawaj", 
                                    description="Kupno do oporu, wystawiaj oferty do połowy posiadanych akcji", class_name="Test4")
        TestEndpoint.objects.create(test=test_4, endpoint=registration, order=0)
        TestEndpoint.objects.create(test=test_4, endpoint=log_in, order=1)
        TestEndpoint.objects.create(test=test_4, endpoint=stocks, order=2)
        TestEndpoint.objects.create(test=test_4, endpoint=wallet, order=3)
        TestEndpoint.objects.create(test=test_4, endpoint=stock_buy, order=4)
        TestEndpoint.objects.create(test=test_4, endpoint=user_stocks, order=5)
        TestEndpoint.objects.create(test=test_4, endpoint=sell_offer, order=6)
        TestEndpoint.objects.create(test=test_4, endpoint=offers, order=7)
        TestEndpoint.objects.create(test=test_4, endpoint=sell_offer, order=8)
        TestEndpoint.objects.create(test=test_4, endpoint=stock_sell, order=9)

        test_5 = Test.objects.create(name= "Kupuj do oporu", 
                                    description="Kupno danej akcji do końca akcji lub funduszy", class_name="Test5")
        TestEndpoint.objects.create(test=test_5, endpoint=registration, order=0)
        TestEndpoint.objects.create(test=test_5, endpoint=log_in, order=1)
        TestEndpoint.objects.create(test=test_5, endpoint=stocks, order=2)
        TestEndpoint.objects.create(test=test_5, endpoint=wallet, order=3)
        TestEndpoint.objects.create(test=test_5, endpoint=stock_buy, order=4)

        test_6 = Test.objects.create(name= "Wyświetl wszystko", 
                                    description="Wyświetlanie kolejno wszystkich list i historii", class_name="Test6")
        TestEndpoint.objects.create(test=test_6, endpoint=registration, order=0)
        TestEndpoint.objects.create(test=test_6, endpoint=log_in, order=1)
        TestEndpoint.objects.create(test=test_6, endpoint=stocks, order=2)
        TestEndpoint.objects.create(test=test_6, endpoint=user_stocks, order=3)
        TestEndpoint.objects.create(test=test_6, endpoint=company, order=4)
        TestEndpoint.objects.create(test=test_6, endpoint=company_detail, order=5)
        TestEndpoint.objects.create(test=test_6, endpoint=offers, order=6)
        TestEndpoint.objects.create(test=test_6, endpoint=price_history, order=7)

        print("DONE")