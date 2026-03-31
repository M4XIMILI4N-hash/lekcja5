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