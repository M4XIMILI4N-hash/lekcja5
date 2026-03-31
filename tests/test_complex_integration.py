from src.manager import Manager
from src.models import Parameters, Bill

def test_get_apartment_costs():

    parameters = Parameters()
    manager = Manager(parameters)
    
  
    manager.apartments = {'A1': 'DummyApartment'}
    

    manager.bills = [
      
        Bill(amount_pln=150.0, date_due="2024-03-10", apartment='A1', settlement_year=2024, settlement_month=3, type="prąd"),
        Bill(amount_pln=100.0, date_due="2024-03-15", apartment='A1', settlement_year=2024, settlement_month=3, type="woda"),
        Bill(amount_pln=200.0, date_due="2024-03-20", apartment='A1', settlement_year=2024, settlement_month=3, type="gaz"),
        
        
        Bill(amount_pln=999.0, date_due="2024-04-10", apartment='A1', settlement_year=2024, settlement_month=4, type="prąd"), # Zły miesiąc
        Bill(amount_pln=999.0, date_due="2023-03-10", apartment='A1', settlement_year=2023, settlement_month=3, type="prąd"), # Zły rok
        Bill(amount_pln=999.0, date_due="2024-03-10", apartment='B2', settlement_year=2024, settlement_month=3, type="prąd"), # Złe mieszkanie
    ]


    
    
    assert manager.get_apartment_costs('Nieistniejace_Mieszkanie', 2024, 3) is None
    
  
    assert manager.get_apartment_costs('A1', 2024, 5) == 0.0
    
    
    assert manager.get_apartment_costs('A1', 2024, 3) == 450.0


def test_apartment_costs_with_optional_parameters():
    manager = Manager(Parameters())
    manager.bills.append(Bill(
        apartment='apart-polanka',
        date_due='2025-03-15',
        settlement_year=2025,
        settlement_month=2,
        amount_pln=1250.0,
        type='rent'
    ))

    manager.bills.append(Bill(
        apartment='apart-polanka',
        date_due='2024-03-15',
        settlement_year=2024,
        settlement_month=2,
        amount_pln=1150.0,
        type='rent'
    ))

    manager.bills.append(Bill(
        apartment='apart-polanka',
        date_due='2024-02-02',
        settlement_year=2024,
        settlement_month=1,
        amount_pln=222.0,
        type='electricity'
    ))

    costs = manager.get_apartment_costs('apartment-1', 2024, 1)
    assert costs is None

    costs = manager.get_apartment_costs('apart-polanka', 2024, 3)
    assert costs == 0.0

    costs = manager.get_apartment_costs('apart-polanka', 2024, 1)
    assert costs == 222.0

    costs = manager.get_apartment_costs('apart-polanka', 2025, 1)
    assert costs == 910.0
    
    costs = manager.get_apartment_costs('apart-polanka', 2024)
    assert costs == 1372.0

    costs = manager.get_apartment_costs('apart-polanka')
    assert costs == 3532.0

def test_apartment_costs_invalid_month():
    parameters = Parameters()
    manager = Manager(parameters)
    manager.apartments = {'A1': 'DummyApartment'}
    
   
    import pytest
    with pytest.raises(ValueError, match="Miesiąc musi być z zakresu od 1 do 12"):
        manager.get_apartment_costs('A1', 2024, 13)