import csv
import os
from dataclasses import dataclass
from typing import List

@dataclass
class Card:
    id: str
    name: str
    rarity: str
    elixirCost: int
    maxLevel: int
    maxEvolutionLevel: int
    icon: str
    evolution_icon: str

@dataclass
class PlayerCards:
    tag: str
    available_cards: List[Card]
    deck_cards: List[Card]
    deleted_cards: List[Card] | None = None

@dataclass
class PlayerStats:
    tag: str
    name: str
    expLevel: int
    trophies: int
    bestTrophies: int
    wins: int
    losses: int
    battleCount: int
    threeCrownWins: int
    arena: str
    clan: str
    favCard: str
    starPoints: int
    expPoints: int
    totalExpPoints: int

def extract_and_map_player_cards(player_row, all_cards):
    card_map = {card.id: card for card in all_cards}
    
    available_cards = []
    deck_cards = []

    tag = player_row['tag']

    for card_id, value_str in list(player_row.items())[1:]:
        if card_id in card_map and value_str.isdigit():
            value = int(value_str)
            card = card_map[card_id]
            
            if value >= 1:
                available_cards.append(card)
            if value == 2:
                deck_cards.append(card)
    
    return PlayerCards(tag=tag, available_cards=available_cards, deck_cards=deck_cards)

def read_player_card_data(file_path, all_cards):
    player_cards_list = []
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            player_cards = extract_and_map_player_cards(row, all_cards)
            player_cards_list.append(player_cards)
    return player_cards_list

def read_game_card_data(file_path):
    cards_list = []
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            cards_list.append(Card(**row))
    return cards_list

def read_player_stats_data(file_path):
    stats_dict = {}
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            stats_dict[row['tag']] = PlayerStats(**row)
    return stats_dict

def read_player_tags_data(file_path):
    tags = []
    with open(file_path, mode='r', encoding='utf-8') as file:
        lines = file.readlines()
        for line in lines:
            tags.append(line.strip())
    return tags

def read_all_game_data(dir_path='data'):
    card_path = os.path.join(dir_path, 'game_cards.csv')
    player_path = os.path.join(dir_path, 'player_cards.csv')
    player_stats_path = os.path.join(dir_path, 'player_stats.csv')
    player_tags_path = os.path.join(dir_path, 'player_tags.csv')
    
    game_cards = read_game_card_data(card_path)
    player_cards_list = read_player_card_data(player_path, game_cards)
    player_stats = read_player_stats_data(player_stats_path)
    player_tags = read_player_tags_data(player_tags_path)

    return game_cards, player_cards_list, player_stats, player_tags

if __name__ == "__main__":
    game_cards, player_cards_list, player_stats, player_tags = read_all_game_data()
    
    print("Game Cards:")
    for card in game_cards:
        print(f" - {card.name} (ID: {card.id})")
    
    print("\nPlayer Cards:")
    for player in player_cards_list:
        print(f"\nPlayer: {player.tag}")
        print(f"  Deck cards ({len(player.deck_cards)}): {[card.name for card in player.deck_cards]}")