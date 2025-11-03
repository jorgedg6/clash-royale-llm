import requests
from bs4 import BeautifulSoup
import json

def read_all_cards():
    with open("data/game_cards.csv", "r") as f:
        lines = f.readlines()
        cards = [line.strip().split(",")[1] for line in lines[1:]]  # Salta el encabezado
        return cards

def fetch_top_decks(card_name):
    url = f"https://www.deckshop.pro/card/detail/{card_name.replace(' ', '-').replace('.', '').lower()}"
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    hrefs = [
        a["href"]
        for a in soup.find_all("a", href=True)
        if a["href"].startswith("/deck/detail/")
    ]
    hrefs = list(set(hrefs))
    top_decks = []
    for deck in hrefs:
        deck = deck.split("/deck/detail/")[1].replace("-", " ").title()
        top_decks.append(deck)
    return top_decks


if __name__ == "__main__":
    top_decks_per_card = {}
    all_cards = read_all_cards()
    for card in all_cards:
        print(f"Fetching top decks for card: {card}")
        card_name = card
        top_decks = fetch_top_decks(card_name)
        top_decks_per_card[card_name] = top_decks

    with open("top_decks_per_card.json", "w") as f:
        json.dump(top_decks_per_card, f, indent=2, ensure_ascii=False)
