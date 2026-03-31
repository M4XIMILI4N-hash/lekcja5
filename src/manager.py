from src.models import Apartment, Bill, Parameters, Tenant, Transfer, ApartmentSettlement, TenantSettlement


class Manager:
    def __init__(self, parameters: Parameters):
        self.parameters = parameters 

        self.apartments = {}
        self.tenants = {}
        self.transfers = []
        self.bills = []
       
        self.load_data()

    def load_data(self):
        self.apartments = Apartment.from_json_file(self.parameters.apartments_json_path)
        self.tenants = Tenant.from_json_file(self.parameters.tenants_json_path)
        self.transfers = Transfer.from_json_file(self.parameters.transfers_json_path)
        self.bills = Bill.from_json_file(self.parameters.bills_json_path)

    def check_tenants_apartment_keys(self) -> bool:
        for tenant in self.tenants.values():
            if tenant.apartment not in self.apartments:
                return False
        return True
    

    def get_apartment_costs(self, apartment_key: str, year: int = None, month: int = None) -> float | None:
        
        if apartment_key not in self.apartments:
            return None
        
        
        if month is not None and (month < 1 or month > 12):
            raise ValueError("Miesiąc musi być z zakresu od 1 do 12")
        
        total_costs = 0.0
        
        for bill in self.bills:
          
            if bill.apartment != apartment_key:
                continue
                
           
            if year is not None and bill.settlement_year != year:
                continue
                
            
            if month is not None and bill.settlement_month != month:
                continue
                
            
            total_costs += bill.amount_pln
                
        return total_costs
    

    def create_apartment_settlement(self, apartment_key: str, year: int, month: int):
      
        bills_sum = self.get_apartment_costs(apartment_key, year, month)
        
     
        if bills_sum is None:
            return None
            
        return ApartmentSettlement(
            apartment=apartment_key,
            month=month,
            year=year,
            total_rent_pln=0.0,
            total_bills_pln=bills_sum,
            total_due_pln=bills_sum
        )
    


    def create_tenant_settlements(self, apartment_settlement):
       
        apartment_tenants = [
            tenant for tenant in self.tenants.values() 
            if tenant.apartment == apartment_settlement.apartment
        ]
        
       
        if not apartment_tenants:
            return []
            
      
        split_bills = apartment_settlement.total_bills_pln / len(apartment_tenants)
        
        tenant_settlements = []
        for tenant in apartment_tenants:
            settlement = TenantSettlement(
                tenant=tenant.name,
                apartment_settlement=apartment_settlement.apartment,
                month=apartment_settlement.month,
                year=apartment_settlement.year,
                rent_pln=0.0, 
                bills_pln=split_bills,
                total_due_pln=split_bills, 
                balance_pln=0.0
            )
            tenant_settlements.append(settlement)
            
        return tenant_settlements