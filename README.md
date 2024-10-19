## My Pokémon TCG Collection

A toy project to keep track of my Pokémon TCG collection.

### How to use

#### Generate Collection
1. Clone the repository
2. Delete the `collection.json` file 
3. Create a free api key at [Pokémon TCG Developers](https://dev.pokemontcg.io/)
4. Create a file called `tcg_api.key` in the root of the project and paste your api key
5. Add the url of your profile picture in the `profile.txt`
6. Run the `fetch.py` script, and select your Pokémon card set and after that the number of the card you want to add to your collection. When finished, type `done` to save the collection. You can rerun the script and continue adding cards to your collection.

#### Generte static page for the GitHub Pages

1. Run the `generate.py` script to generate the `index.html` file
2. Push the changes to the repository
3. Go to the repository settings and enable the GitHub Pages
4. Access the page at `https://<your-username>.github.io/<repository-name>`


