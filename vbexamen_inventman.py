examen vorig jaar:
class Batch:
    def __init__(self, quantity, cost_per_unit):
        self.quantity = quantity
        self.cost_per_unit = cost_per_unit
    def __str__(self):
        return f"Batch(quantity={self.quantity}, cost_per_unit={self.cost_per_unit})"

class Product:
    def __init__(self, product_name, batches, holding_cost, stockout_penalty):
        self.product_name = product_name
        self.batches = batches
        self.holding_cost = holding_cost
        self.stockout_penalty = stockout_penalty
    #NIEUWE batch toevoegen aan de stack
    def add_batch(self, quantity, cost_per_unit):
        new_batch = Batch(quantity, cost_per_unit)
        self.batches.append(new_batch)
    #kan de vraag beantwoord worden
    def fulfill_demand(self, demand):
        while demand > 0 and len(self.batches) > 0:
            top = self.batches[-1]
            if top.quantity > demand:
                top.quantity -= demand
                return 0
            else:
                demand -= top.quantity
                self.batches.pop()
        if demand > 0:
            return demand * self.stockout_penalty
        return 0
    #totale aanhoud kosten
    def calculate_holding_cost(self):
        lijst = []
        for batch in self.batches:
            lijst.append(batch.quantity)
        total = sum(lijst) * self.holding_cost
        return total
    #tostring methode
    def __str__(self):
        resultaat = f"Product {self.product_name}:\n"
        for batch in self.batches:
            resultaat += f"Batch(quantity={batch.quantity}, cost_per_unit={batch.cost_per_unit})\n"
        return resultaat
class Inventory_Manager:    #product_name als sleutel
    def __init__(self):
        self.products = {}
    def add_product(self, product_name, holding_cost, stockout_penalty):
        new_product = Product(product_name, [], holding_cost, stockout_penalty)
        if new_product.product_name not in self.products:
            self.products[new_product.product_name] = new_product
        else:
            print(f"Product {new_product.product_name} already exists.")
    #product aanvullen door nieuwe batch aan de stack toe te voegen
    def restock_product(self, product_name, quantity, cost_per_unit):
        if product_name not in self.products:
            print(f"Product {product_name} not found")
        else:
            self.products[product_name].add_batch(quantity, cost_per_unit)
    #willekeurige vraag voor elk product genereren
    def simulate_demand(self, min_demand = 0, max_demand = 20):
        from random import randint
        demand_dict = {}
        for product_name in self.products:
            demand = randint(min_demand, max_demand)
            demand_dict[product_name] = demand
        return demand_dict
    #simuleer dag van operaties, retourneer aanhoudings- en stockout kosten
    def simulate_day(self, demand):
        def simulate_day(self, demand):
            total_stockout = 0
            total_holding = 0
            for product_name, product in self.products.items():
                vraag = demand[product_name]

                stockout_cost = product.fulfill_demand(vraag)
                holding_cost = product.calculate_holding_cost()

                total_stockout += stockout_cost
                total_holding += holding_cost
            return total_holding, total_stockout
    #opslaan naar csv
    def save_to_csv(self, filename):
        file = open(filename, "w")
        for product_name in self.products:
            product = self.products[product_name]
            for batch in product.batches:
                file.write(f"{product_name},{batch.quantity},{batch.cost_per_unit}\n")
        file.close()
    #laden van CSV
    def load_from_csv(self, filename):
        file = open(filename, "r")
        for line in file:
            line = line.strip()
            if not line:
                continue
            delen = line.split(",")
            product_name = delen[0]
            quantity = int(delen[1])
            cost_per_unit = float(delen[2])
            if product_name not in self.products:
                self.add_product(product_name, 0, 0)
            self.add_product(product_name, quantity, cost_per_unit)
        file.close()
    #inventory printen
    def print_inventory(self):
        print("Current inventory:")
        for product_name in self.products:
            print(f"Product {product_name}:")
            for batch in self.products[product_name].batches:
                print(f"Batch(quantity={batch.quantity}, cost_per_unit={batch.cost_per_unit})")
#main methode
def main():
    manager = Inventory_Manager()
    #2 producten toevoegen
    manager.add_product("Voetbal", 3, 15)
    manager.add_product("Fiets", 39, 315)
    #voor elk product 2 batches toevoegen
    manager.restock_product("Voetbal", 50, 2.5)
    manager.restock_product("Fiets", 30, 3.0)
    # 3. Simuleer de vraag
    demand = manager.simulate_demand(10, 20)
    print("Gegenereerde vraag per product:", demand)
    # 4. Simuleer de dag met die vraag
    holding_cost, stockout_cost = manager.simulate_day(demand)
    print("Totale holding cost:", holding_cost)
    print("Totale stockout cost:", stockout_cost)
    # 5. Toon de voorraad
    manager.print_inventory()
    # 6. Opslaan in CSV
    manager.save_to_csv("inventory.csv")
    print("Voorraad opgeslagen in inventory.csv")

________________________________________
Van: Klaas D'haen <Klaas.Dhaen@UGent.be>
Verzonden: woensdag 19 november 2025 11:34
Aan: Victor De Greef <Victor.DeGreef@UGent.be>
Onderwerp: code parkings simuleren 
 
import heapq
 
class PriorityQueue:
    def __init__(self):
        self.content = []
 
    def add(self, item):
        heapq.heappush(self.content, item)
 
    def peek(self):
        return self.content[0]
 
    def poll(self):
        return heapq.heappop(self.content) if len(self.content) > 0 else None
 
    def is_empty(self):
        return len(self.content) == 0
 
    def __str__(self):
        return str(heapq.nsmallest(len(self.content), self.content))
 
 
def simuleer_parking(plaatsen, bloktijd, klanten):
    # Wachtrij met aankomsten: prioriteit = (tijd, winkeltijd)
    # Bij gelijke aankomsttijd gaat kortste winkeltijd eerst
    aankomst_queue = PriorityQueue()
    for (t, w) in klanten:
        aankomst_queue.add((t, w))
 
    # Parking bezette plaatsen: prioriteit op vertrektijd
    # item = (vertrektijd, w)
    parking = PriorityQueue()
 
    vrije_plaatsen = plaatsen
    laatste_vertrektijd = 0
 
    while not aankomst_queue.is_empty() or not parking.is_empty():
        # Bepaal volgende gebeurtenis:
        # - de volgende aankomsttijd
        # - de volgende vertrektijd
        volgende_aankomst = aankomst_queue.peek()[0] if not aankomst_queue.is_empty() else float('inf')
        volgende_vertrek = parking.peek()[0] if not parking.is_empty() else float('inf')
 
        # Óf eerst iemand vertrekt
        if volgende_vertrek <= volgende_aankomst:
            # Verwijder van parking
            vertrektijd, _ = parking.poll()
            vrije_plaatsen += 1
            laatste_vertrektijd = vertrektijd
 
        else:
            # Eerst komt iemand aan
            aankomsttijd, winkeltijd = aankomst_queue.poll()
 
            if vrije_plaatsen > 0:
                # Parkeren kan
                vrije_plaatsen -= 1
                vertrek = aankomsttijd + winkeltijd
                parking.add((vertrek, winkeltijd))
                laatste_vertrektijd = max(laatste_vertrektijd, vertrek)
 
            else:
                # Parking vol → opnieuw proberen na bloktijd
                nieuwe_tijd = aankomsttijd + bloktijd
                aankomst_queue.add((nieuwe_tijd, winkeltijd))
 
    return laatste_vertrektijd
