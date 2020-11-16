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
                                    description="Kupno kolejnych akcji z listy do końca funduszy lub akcji", class_name="BuyUntilFounds")
        testEnd1_1 = TestEndpoint.objects.create(test=test_1, endpoint=registration, order=0)
        testEnd1_2 = TestEndpoint.objects.create(test=test_1, endpoint=log_in, order=testEnd1_1.endpoint.pk)
        testEnd1_3 = TestEndpoint.objects.create(test=test_1, endpoint=stocks, order=testEnd1_2.endpoint.pk)
        testEnd1_4 = TestEndpoint.objects.create(test=test_1, endpoint=wallet, order=testEnd1_3.endpoint.pk)
        TestEndpoint.objects.create(test=test_1, endpoint=stock_buy, order=testEnd1_4.endpoint.pk)

        test_2 = Test.objects.create(name= "Oferty kupna do oporu", 
                                    description="Wystawiaj oferty kupna do końca akcji", class_name="Test2")
        testEnd2_1 = TestEndpoint.objects.create(test=test_2, endpoint=registration, order=0)
        testEnd2_2 = TestEndpoint.objects.create(test=test_2, endpoint=log_in, order=testEnd2_1.endpoint.pk)
        testEnd2_3 = TestEndpoint.objects.create(test=test_2, endpoint=stocks, order=testEnd2_2.endpoint.pk)
        testEnd2_4 = TestEndpoint.objects.create(test=test_2, endpoint=buy_offer, order=testEnd2_3.endpoint.pk)
        TestEndpoint.objects.create(test=test_2, endpoint=offers, order=testEnd2_4.endpoint.pk)

        test_3 = Test.objects.create(name= "Kupuj do oporu i wystawiaj oferty sprzedaży", 
                                    description="Kupno do oporu, wystawiaj oferty sprzedaży do końca akcji", class_name="Test3")
        testEnd3_1 = TestEndpoint.objects.create(test=test_3, endpoint=registration, order=0)
        testEnd3_2 = TestEndpoint.objects.create(test=test_3, endpoint=log_in, order=testEnd3_1.endpoint.pk)
        testEnd3_3 = TestEndpoint.objects.create(test=test_3, endpoint=stocks, order=testEnd3_2.endpoint.pk)
        testEnd3_4 = TestEndpoint.objects.create(test=test_3, endpoint=wallet, order=testEnd3_3.endpoint.pk)
        testEnd3_5 = TestEndpoint.objects.create(test=test_3, endpoint=stock_buy, order=testEnd3_4.endpoint.pk)
        testEnd3_6 = TestEndpoint.objects.create(test=test_3, endpoint=user_stocks, order=testEnd3_5.endpoint.pk)
        testEnd3_7 = TestEndpoint.objects.create(test=test_3, endpoint=sell_offer, order=testEnd3_6.endpoint.pk)
        testEnd3_8 = TestEndpoint.objects.create(test=test_3, endpoint=offers, order=testEnd3_7.endpoint.pk)
        TestEndpoint.objects.create(test=test_3, endpoint=history, order=testEnd3_8.endpoint.pk)

        test_4 = Test.objects.create(name= "Kupuj i sprzedawaj", 
                                    description="Kupno do oporu, wystawiaj oferty do połowy posiadanych akcji", class_name="Test4")
        testEnd4_1 = TestEndpoint.objects.create(test=test_4, endpoint=registration, order=0)
        testEnd4_2 = TestEndpoint.objects.create(test=test_4, endpoint=log_in,  order=testEnd4_1.endpoint.pk)
        testEnd4_3 = TestEndpoint.objects.create(test=test_4, endpoint=stocks, order=testEnd4_2.endpoint.pk)
        testEnd4_4 = TestEndpoint.objects.create(test=test_4, endpoint=wallet, order=testEnd4_3.endpoint.pk)
        testEnd4_5 = TestEndpoint.objects.create(test=test_4, endpoint=stock_buy, order=testEnd4_4.endpoint.pk)
        testEnd4_6 = TestEndpoint.objects.create(test=test_4, endpoint=user_stocks, order=testEnd4_5.endpoint.pk)
        testEnd4_7 = TestEndpoint.objects.create(test=test_4, endpoint=sell_offer, order=testEnd4_6.endpoint.pk)
        testEnd4_8 = TestEndpoint.objects.create(test=test_4, endpoint=offers, order=testEnd4_7.endpoint.pk)
        testEnd4_9 = TestEndpoint.objects.create(test=test_4, endpoint=sell_offer, order=testEnd4_8.endpoint.pk)
        TestEndpoint.objects.create(test=test_4, endpoint=stock_sell, order=testEnd4_9.endpoint.pk)

        test_5 = Test.objects.create(name= "Kupuj do oporu", 
                                    description="Kupno danej akcji do końca akcji lub funduszy", class_name="Test5")
        testEnd5_1 = TestEndpoint.objects.create(test=test_5, endpoint=registration, order=0)
        testEnd5_2 = TestEndpoint.objects.create(test=test_5, endpoint=log_in, order=testEnd5_1.endpoint.pk)
        testEnd5_3 = TestEndpoint.objects.create(test=test_5, endpoint=stocks, order=testEnd5_2.endpoint.pk)
        testEnd5_4 = TestEndpoint.objects.create(test=test_5, endpoint=wallet, order=testEnd5_3.endpoint.pk)
        TestEndpoint.objects.create(test=test_5, endpoint=stock_buy, order=testEnd5_4.endpoint.pk)

        test_6 = Test.objects.create(name= "Wyświetl wszystko", 
                                    description="Wyświetlanie kolejno wszystkich list i historii", class_name="Test6")
        testEnd6_1 = TestEndpoint.objects.create(test=test_6, endpoint=registration, order=0)
        testEnd6_2 = TestEndpoint.objects.create(test=test_6, endpoint=log_in, order=testEnd6_1.endpoint.pk)
        testEnd6_3 = TestEndpoint.objects.create(test=test_6, endpoint=stocks, order=testEnd6_2.endpoint.pk)
        testEnd6_4 = TestEndpoint.objects.create(test=test_6, endpoint=user_stocks, order=testEnd6_3.endpoint.pk)
        testEnd6_5 = TestEndpoint.objects.create(test=test_6, endpoint=company, order=testEnd6_4.endpoint.pk)
        testEnd6_6 = TestEndpoint.objects.create(test=test_6, endpoint=company_detail, order=testEnd6_5.endpoint.pk)
        testEnd6_7 = TestEndpoint.objects.create(test=test_6, endpoint=offers, order=testEnd6_6.endpoint.pk)
        TestEndpoint.objects.create(test=test_6, endpoint=price_history, order=testEnd6_7.endpoint.pk)

        print("DONE")