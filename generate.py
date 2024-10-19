from jinja2 import Template
import json

def generate_html(cards, profile_image_url):
    """Generate a single HTML page for the entire card collection grouped by set."""
    
    # First, we need to group the cards by set
    sets = {}
    total_value = 0
    for card in cards:
        set_name = card['set']['name']
        
        total_value += float(card['cardmarket']['prices']['averageSellPrice'])
        
        if set_name not in sets:
            sets[set_name] = {
                'logo': card['set']['images']['logo'],
                'cards': []
            }
        sets[set_name]['cards'].append(card)

    # Next, we need to sort the cards within each set by their card number
    for set_name, set_data in sets.items():
        set_data['cards'] = sorted(set_data['cards'], key=lambda x: int(x['number']))

      # Updated template to group cards by set and show the set logo
    total_value = str(round(total_value, 2))
    total_owned_cards = len(cards)
    total_set_cards = int(set_data['cards'][0]['set']['printedTotal'])
    total_real_cards = int(set_data['cards'][0]['set']['total'])
    template_str = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My Pokémon TCG Collection</title>
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {
            font-family: 'Arial', sans-serif;
            background-color: #fff5f5;
            color: #333;
            margin: 0;
            padding: 0;
        }
        h1 {
            background-color: #ff1a1a;
            color: white;
            padding: 30px;
            text-align: center;
            margin-bottom: 40px;
            border-radius: 0 0 20px 20px;
            position: relative;
        }
        .profile-image {
            position: absolute;
            top: 10px;
            left: 20px;
            width: 90px;
            height: 90px;
            border-radius: 50%;
            object-fit: cover;
            border: 3px solid white;
        }
        h2 {
            text-align: center;
            margin-bottom: 20px;
            font-size: 1.8rem;
            color: #555;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        .card {
            background-color: white;
            border: 1px solid #ddd;
            border-radius: 12px;
            transition: transform 0.3s ease-in-out, box-shadow 0.3s;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
            overflow: hidden;
            position: relative;
            cursor: pointer;
        }
        .card:hover {
            transform: scale(1.05);
            box-shadow: 0 6px 15px rgba(0, 0, 0, 0.15);
        }
        .card-body {
            text-align: center;
            padding: 15px;
            position: relative;
        }
        .card-title {
            font-size: 1.2rem;
            font-weight: bold;
            margin-bottom: 5px;
        }
        .card-rarity {
            font-size: 0.9rem;
            margin-bottom: 10px;
            text-transform: capitalize;
            color: #333;
        }
        .gold-rarity {
            color: gold;
            font-weight: bold;
        }
        .card-img-top {
            max-height: 240px;
            object-fit: contain;
            width: 100%;
            border-radius: 8px;
            margin-bottom: 15px;
        }
        .card-number {
            font-weight: bold;
            font-size: 0.9rem;
            padding: 2px 6px;
            margin-bottom: 10px; /* Space between number and image */
            background-color: rgba(255, 255, 255, 0.8);
            border-radius: 4px;
        }
        .set-logo {
            text-align: center;
            margin: 40px 0;
        }
        .set-logo img {
            max-width: 300px;
        }
        .pagination {
            margin: 30px 0;
        }
        .pagination a {
            color: white;
            background-color: #ff1a1a;
            margin: 0 5px;
            padding: 10px 20px;
            text-decoration: none;
            border-radius: 5px;
        }
        .pagination a:hover {
            background-color: #cc0000;
        }

        /* Fullscreen image overlay */
        .fullscreen-overlay {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0, 0, 0, 0.9);
            justify-content: center;
            align-items: center;
            z-index: 9999;
        }
        .fullscreen-overlay img {
            max-width: 90%;
            max-height: 90%;
        }
        .fullscreen-overlay.active {
            display: flex;
        }
    </style>
</head>
<body>
    <h1>
        <img src="{{ profile_image_url }}" alt="Profile Image" class="profile-image">
        My Pokémon TCG Collection
    </h1>

    <div class="container">
        
        <!-- Loop through each set -->
        {% for set_name, set_data in sets.items() %}
        <div class="set-section">
            <div class="set-logo">
                <img src="{{ set_data['logo'] }}" alt="{{ set_name }} Logo">
               
            </div>
            <div class="row">
                <!-- Loop through each card in the set -->
                {% for card in set_data['cards'] %}
                <div class="col-lg-4 col-md-6 col-sm-12 mb-4">
                    <div class="card h-100" data-card-image="{{ card['images']['large'] }}">
                        <div class="card-body">
                            <!-- Card number before the image -->
                            <p class="card-number">#{{ card['number'].zfill(3) }}</p>
                            <img src="{{ card['images']['large'] }}" class="card-img-top" alt="{{ card['name'] }}">
                            <h5 class="card-title">{{ card['name'] }}</h5>
                            <!-- Card rarity below the name with conditional formatting for 'rare' -->
                            {% if 'rare' in card['rarity'] | lower %}
                                <p class="card-rarity gold-rarity">{{ card['rarity'] | lower }}</p>
                            {% else %}
                                <p class="card-rarity">{{ card['rarity'] | lower }}</p>
                            {% endif %}
                        </div>
                    </div>
                </div>
                {% endfor %}
            </div>
        </div>
        {% endfor %}
        <!-- <p> Total evaluation: {{total_value}}</p> -->
         <h2>Progress {{total_owned_cards}} / {{total_set_cards}} ({{total_real_cards}})</h2>
    </div>

    <!-- Fullscreen Overlay -->
    <div class="fullscreen-overlay" id="fullscreen-overlay">
        <img id="fullscreen-image" src="" alt="Fullscreen Image">
    </div>

    <!-- Bootstrap JS and dependencies -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            const overlay = document.getElementById('fullscreen-overlay');
            const fullscreenImage = document.getElementById('fullscreen-image');
            const cards = document.querySelectorAll('.card');

            cards.forEach(card => {
                card.addEventListener('click', function() {
                    const imageUrl = card.getAttribute('data-card-image');
                    fullscreenImage.src = imageUrl;
                    overlay.classList.add('active');
                });
            });

            overlay.addEventListener('click', function() {
                overlay.classList.remove('active');
            });
        });
    </script>
</body>
</html>
    """

    template = Template(template_str)
    html_content = template.render(sets=sets,
                                    profile_image_url=profile_image_url,
                                    total_value=total_value,
                                    total_owned_cards=total_owned_cards,
                                    total_set_cards=total_set_cards,
                                    total_real_cards=total_real_cards)
    
    with open("index.html", "w") as f:
        f.write(html_content)
    
    print("HTML page generated as 'index.html'.")

if __name__ == "__main__":
    with open("profile.txt", "r") as f:
        profile_image_url = f.read().strip()
    
    with open("collection.json", "r") as f:
        card_collection = json.load(f)
    
    generate_html(card_collection, profile_image_url)
