import json
from datetime import date

# TODO: dodati type hinting na sve funkcije


OFFERS_FILE = "offers.json"
PRODUCTS_FILE = "products.json"
CUSTOMERS_FILE = "customers.json"


def load_data(filename):
    """Load data from a JSON file."""
    try:
        with open(filename, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print(f"Error decoding {filename}. Check file format.")
        return []


def save_data(filename, data):
    """Save data to a JSON file."""
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)


# TODO: Implementirajte funkciju za kreiranje nove ponude.
def create_new_offer(offers, products, customers):
    """
    Prompt user to create a new offer by selecting a customer, entering date,
    choosing products, and calculating totals.
    """
    # Omogućite unos kupca
    # Izračunajte sub_total, tax i total
    # Dodajte novu ponudu u listu offers

    ids_offer = [offer['offer_number'] for offer in offers]

    while True:
        offer_number = int(max(ids_offer)) + 1
        name = input(f"Unesite ime / naziv kupca: ")
        email = input(f"Unesi e-mail kupca: ").strip()
        vat_id = input(f"Unesi porezni ID kupca: ")
        while len(vat_id) != 10 or not vat_id.isdigit():
                print(f"Ili je broj znamenki netočan ili je upisan nedopušten znak. Probaj opet")
                vat_id = input(f"Unesi porezni ID kupca: ")
        date_now = (date.today()).strftime('%Y-%m-%d')
        new_customer = {
            'name' : name,
            'email' : email,
            'vat_id' : vat_id
        }

        customers.append(new_customer)

        new_offer = {
            'offer_number' : offer_number,
            'customer' : name,
            'date' : date_now,
            'items': []
        }

        print(f"-------------------------------\n"
              f"LISTA PROIZVODA: ||\n"
              f"-----------------ˇˇ------------")
        for product in products:
            print(f"ID proizvoda -> {product['id']}\n"
                  f"Naziv proizvoda -> {product['name']}\n"
                  f"Opis proizvoda -> {product['description']}\n"
                  f"Cijena proizvoda -> {product['price']}\n"
                  f"-----------------------------------------")
        
        product_id_input = input(f"Unesite ID proizvoda za kupiti (ako ih je više, odvoji ih zarezom): ")
        product_ids = [id.strip() for id in product_id_input.split(',')]  # Strip to remove any spaces
        sub_total = 0

        if len(product_ids) > 1:
            for id in product_ids:
                for product in products:
                    if int(id) == product['id']:
                        new_item = product.copy()
                        new_item['quantity'] = int(input(f"Koliku količinu proizvoda {id} trebaš? "))
                        new_item['item_total'] = new_item['quantity'] * product['price']
                        
                        new_offer['items'].append(new_item)
                        
                        sub_total += new_item['item_total']
                        break
                else:
                    print(f"Proizvod s ID -> {id} ne postoji")
        elif len(product_ids) == 1:
            for product in products:
                if int(product_ids[0]) == product['id']:
                    new_item = product.copy()
                    new_item['quantity'] = int(input(f"Koliku količinu navedenog proizvoda trebaš? "))
                    new_item['item_total'] = new_item['quantity'] * product['price']
                    
                    new_offer['items'].append(new_item)
                    
                    sub_total += new_item['item_total']
                    break
            else:
                print(f"Proizvod s ID -> {product_ids[0]} ne postoji")
        else:
            kraj = input(f"Nisi odabrao niti jednu ponudu. Želiš li nastaviti sa stvaranjem ponude? da/ne ")
            if kraj.lower() != 'da':
                break

        new_offer['sub_total'] = sub_total
        new_offer['tax'] = new_offer['sub_total'] * 0.1
        new_offer['total'] = new_offer['sub_total'] + new_offer['tax']

        offers.append(new_offer)

        kraj = input(f"Dodajemo još ponuda? da/ne ")
        if kraj.lower() != 'da':
            break
        




# TODO: Implementirajte funkciju za upravljanje proizvodima.
def manage_products(products):
    """
    Allows the user to add a new product or modify an existing product.
    """
    # Omogućite korisniku izbor između dodavanja ili izmjene proizvoda
    # Za dodavanje: unesite podatke o proizvodu i dodajte ga u listu products
    # Za izmjenu: selektirajte proizvod i ažurirajte podatke
    
    ids_product = [product['id'] for product in products]
   
    odabir = input(f"Želiš li postaviti novi proizvod (1) ili izmijeniti postojeći (2)? ")
    if odabir == "1":
        while True:
            id = max(ids_product) + 1
            name = input(f"Unesi naziv proizvoda: ").strip()
            description = input(f"Unesite opis proizvoda: ").strip()
            price = input(f"Unesite cijenu proizvoda: ")
            while not price.isdigit():
                    print(f"Nedopušten znak. Probaj opet")
                    price = input(f"Unesite cijenu proizvoda: ")
                
            ponuda = {
                'id' : id,
                'name' : name,
                'description' : description,
                'price' : price
            }
            
            products.append(ponuda)
            print(f"Dodan je novi proizvod:\n"
                f"ID -> {id}\n"
                f"Naziv proizvoda -> {name}\n"
                f"Opis proizvoda -> {description}\n"
                f"Cijena -> {price}")

           


    elif odabir == "2":
        while True:
            odabir_2 = int(input(f"Odaberi ID postojećeg proizvoda kojeg želiš promijeniti: "))
            
            while odabir_2 not in ids_product:
                print(f"Nepostojeći proizvod. Probaj opet.")
                odabir_2 = int(input(f"Odaberi ID postojećeg proizvoda kojeg želiš promijeniti: "))
                
            print(f"Odabrani proizvod -> {products[odabir_2]}")
            
            name = input(f"Unesi naziv proizvoda: ").strip()
            description = input(f"Unesite opis proizvoda: ").strip()
            price = input(f"Unesite cijenu proizvoda: ")
            
            while not price.isdigit():
                    print(f"Nedopušten znak. Probaj opet")
                    price = input(f"Unesite cijenu proizvoda: ")
                
            ponuda = {
                'name' : name,
                'description' : description,
                'price' : price
            }
            



# TODO: Implementirajte funkciju za upravljanje kupcima.
def manage_customers(customers):
    """
    Allows the user to add a new customer or view all customers.
    """
    # Za dodavanje: omogući unos imena kupca, emaila i unos VAT ID-a
    # Za pregled: prikaži listu svih kupaca
    odabir = input("Želiš li dodati novog kupca (1) ili vidjeti postojeće (2)? ")
    if odabir == '1':
        while True:
            name = input(f"Unesi ime / naziv kupca: ").strip()
            email = input(f"Unesi e-mail kupca: ").strip()
            vat_id = input(f"Unesi porezni ID kupca: ")
            while len(vat_id) != 10 or not vat_id.isdigit():
                print(f"Ili je broj znamenki netočan ili je upisan nedopušten znak. Probaj opet")
                vat_id = input(f"Unesi porezni ID kupca: ")
            novi_kupac = {
                'name' : name,
                'email' : email,
                'vat_id' : vat_id
            }
            customers.append(novi_kupac)
            print(f"Ime / naziv kupca -> {novi_kupac['name']}\n"
                  f"E-mail -> {novi_kupac['email']}\n"
                  f"Porezni ID -> {novi_kupac['vat_id']}")

        
    elif odabir == '2':
        try:
            for customer in customers:
                print(f"Ime / naziv kupca -> {customer['name']}\n"
                      f"E-mail -> {customer['email']}\n"
                      f"Porezni ID -> {customer['vat_id']}\n"
                      f"-----------------------------------")
        except Exception as e:
            print(f"Greška -> {e}")
    else:
        print(f"Nepostojeća opcija. Probaj opet")


# TODO: Implementirajte funkciju za prikaz ponuda.
def display_offers(offers):
    """
    Display all offers, offers for a selected month, or a single offer by ID.
    """
    # Omogućite izbor pregleda: sve ponude, po mjesecu ili pojedinačna ponuda
    # Prikaz relevantnih ponuda na temelju izbora
    
    odabir = input(f"Želiš li vidjeti ponude po mjesecu (1), pojedinačnu ponudu (2) ili sve ponude (3)? ")
    if odabir == '1':
        pass
    if odabir == '2':
        pass
            
    if odabir == '3':
        for offer in offers:
            print(f"----------------------------------------------------------------------------------------------")
            print(f"Ponuda br: {offer['offer_number']}, Kupac: {offer['customer']}, Datum ponude: {offer['date']}")
            print("Stavke:")
            for item in offer["items"]:
                print(f"  - {item['product_name']} (ID: {item['product_id']}): {item['description']}")
                print(f"    Kolicina: {item['quantity']}, Cijena: ${item['price']}, Ukupno: ${item['item_total']}")
            print(f"Ukupno: ${offer['sub_total']}, Porez: ${offer['tax']}, Ukupno za platiti: ${offer['total']}")
            print(f"----------------------------------------------------------------------------------------------")
            
    


# Pomoćna funkcija za prikaz jedne ponude
def print_offer(offer):
    """Display details of a single offer."""
    print(f"Ponuda br: {offer['offer_number']}, Kupac: {offer['customer']['name']}, Datum ponude: {offer['date']}")
    print("Stavke:")
    for item in offer["items"]:
        print(f"  - {item['product_name']} (ID: {item['product_id']}): {item['description']}")
        print(f"    Kolicina: {item['quantity']}, Cijena: ${item['price']}, Ukupno: ${item['item_total']}")
    print(f"Ukupno: ${offer['sub_total']}, Porez: ${offer['tax']}, Ukupno za platiti: ${offer['total']}")


    

def main():
    # Učitavanje podataka iz JSON datoteka
    offers = load_data(OFFERS_FILE)
    products = load_data(PRODUCTS_FILE)
    customers = load_data(CUSTOMERS_FILE)

    while True:
        print("\nOffers Calculator izbornik:")
        print("1. Kreiraj novu ponudu")
        print("2. Upravljanje proizvodima")
        print("3. Upravljanje korisnicima")
        print("4. Prikaz ponuda")
        print("5. Izlaz")
        choice = input("Odabrana opcija: ")

        if choice == "1":
            create_new_offer(offers, products, customers)
        elif choice == "2":
            manage_products(products)
        elif choice == "3":
            manage_customers(customers)
        elif choice == "4":
            display_offers(offers)
        elif choice == "5":
            # Pohrana podataka prilikom izlaza
            save_data(OFFERS_FILE, offers)
            save_data(PRODUCTS_FILE, products)
            save_data(CUSTOMERS_FILE, customers)
            break
        else:
            print("Krivi izbor. Pokusajte ponovno.")


if __name__ == "__main__":
    main()