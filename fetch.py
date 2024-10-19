import requests
import json
import os

POKEMON_TCG_API = "https://api.pokemontcg.io/v2"

def load_api_key(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith("my_api_key"):
                return line.split('=')[1].strip()

POKEMON_TCG_API_KEY = load_api_key("tcg_api.key")

def fetch_sets():
    """Fetch all available TCG sets."""
    url = f"{POKEMON_TCG_API}/sets"
    headers = {'X-Api-Key': POKEMON_TCG_API_KEY}
    response = requests.get(url, headers=headers)
    data = response.json()
    sets = data['data']
    return sets

def display_sets(sets):
    """Display a list of sets for the user to choose from."""
    for idx, set_data in enumerate(sets, start=1):
        print(f"{idx}. {set_data['name']} ({set_data['id']})")
    selected_set = int(input("Select a set by number: ")) - 1
    return sets[selected_set]

def main():
    sets = fetch_sets()
    selected_set = display_sets(sets)
    print(f"You selected: {selected_set['name']} ({selected_set['id']})")
    return selected_set

def fetch_card_by_code(set_id, card_code):
    """Fetch card information from the API using the set ID and card number."""
    url = f"{POKEMON_TCG_API}/cards/{set_id}-{card_code}"
    headers = {'X-Api-Key': POKEMON_TCG_API_KEY}
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"Error fetching card data: {response.status_code}")
        return None
    
    card_data = response.json().get('data', {})
    
    if not card_data:
        print(f"No card found for code: {set_id}-{card_code}")
        return None

    # Automatically assign the first available rarity or 'unknown' if not available
    card_data['rarity'] = card_data.get('rarity', 'unknown').lower()
    
    return card_data

def add_cards_to_collection(set_id):
    """Repeatedly ask the user to insert card codes and automatically add them to the collection."""
    # Try to load the existing collection if the file exists
    if os.path.exists("collection.json"):
        with open("collection.json", "r") as f:
            try:
                card_collection = json.load(f)
            except json.JSONDecodeError:
                card_collection = []
    else:
        card_collection = []
    
    while True:
        card_code = input("Enter card code (or 'done' to finish): ").strip()
        if card_code.lower() == 'done':
            break
        
        card_data = fetch_card_by_code(set_id, card_code)
        
        if card_data:
            # Automatically add the card with its default or fetched rarity
            card_collection.append(card_data)
            print(f"Added {card_data['name']} with rarity {card_data['rarity'].capitalize()} to collection.")
    
    return card_collection

if __name__ == "__main__":
    selected_set = main()
    collection = add_cards_to_collection(selected_set['id'])
    # Save the updated collection back to the file without overwriting
    with open("collection.json", "w") as f:
        json.dump(collection, f, indent=4)
