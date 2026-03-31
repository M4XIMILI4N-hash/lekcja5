from src.manager import Manager
from src.models import Parameters, Bill
from src.models import ApartmentSettlement
from src.models import TenantSettlement, Tenant
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


def test_tdd_create_apartment_settlement():
  
    parameters = Parameters()
    manager = Manager(parameters)
    manager.apartments = {'A1': 'DummyApartment', 'A2': 'DummyApartment'}
    
    
    manager.bills = [
        Bill(amount_pln=200.0, date_due="2024-05-10", apartment='A1', settlement_year=2024, settlement_month=5, type="prąd"),
        Bill(amount_pln=300.0, date_due="2024-05-15", apartment='A1', settlement_year=2024, settlement_month=5, type="woda"),
        Bill(amount_pln=999.0, date_due="2024-06-10", apartment='A1', settlement_year=2024, settlement_month=6, type="gaz"), # Inny miesiąc
    ]

    
    settlement_a1 = manager.create_apartment_settlement('A1', 2024, 5)
    
    assert settlement_a1 is not None 
    assert isinstance(settlement_a1, ApartmentSettlement) 
    assert settlement_a1.apartment == 'A1' 
    assert settlement_a1.year == 2024
    assert settlement_a1.month == 5 
    assert settlement_a1.total_bills_pln == 500.0 
    assert settlement_a1.total_rent_pln == 0.0 
    
   
    settlement_empty = manager.create_apartment_settlement('A2', 2024, 5)
    
    assert settlement_empty is not None 
    assert settlement_empty.apartment == 'A2' 
    assert settlement_empty.total_bills_pln == 0.0 
    assert settlement_empty.total_due_pln == 0.0 


def test_tdd_create_tenant_settlements():
    parameters = Parameters()
    manager = Manager(parameters)
    
   
    apt_settlement = ApartmentSettlement(
        apartment='A1', month=5, year=2024, 
        total_rent_pln=0.0, total_bills_pln=600.0, total_due_pln=600.0
    )

    
    manager.tenants = {
        't1': Tenant(name="Jan", apartment="A1", room="R1", rent_pln=1000, deposit_pln=1000, date_agreement_from="2024-01-01", date_agreement_to="2024-12-31"),
        't2': Tenant(name="Anna", apartment="A1", room="R2", rent_pln=1000, deposit_pln=1000, date_agreement_from="2024-01-01", date_agreement_to="2024-12-31"),
        't3': Tenant(name="Ktoś Inny", apartment="B2", room="R1", rent_pln=1000, deposit_pln=1000, date_agreement_from="2024-01-01", date_agreement_to="2024-12-31") # Inne mieszkanie
    }
    
    results_2_tenants = manager.create_tenant_settlements(apt_settlement)
    assert isinstance(results_2_tenants, list) 
    assert len(results_2_tenants) == 2 
    assert results_2_tenants[0].bills_pln == 300.0 
    assert results_2_tenants[1].bills_pln == 300.0 
    assert results_2_tenants[0].apartment_settlement == 'A1'

    
    manager.tenants = {
        't1': Tenant(name="Jan", apartment="A1", room="R1", rent_pln=1000, deposit_pln=1000, date_agreement_from="2024-01-01", date_agreement_to="2024-12-31")
    }
    results_1_tenant = manager.create_tenant_settlements(apt_settlement)
    assert len(results_1_tenant) == 1 # 6
    assert isinstance(results_1_tenant[0], TenantSettlement) # 7
    assert results_1_tenant[0].bills_pln == 600.0 # 8
    
    
    manager.tenants = {}
    results_0_tenants = manager.create_tenant_settlements(apt_settlement)
    assert isinstance(results_0_tenants, list) # 9
    assert len(results_0_tenants) == 0 # 10