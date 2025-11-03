import sys
from typing import List
from bs4 import BeautifulSoup
import requests
from requests.adapters import HTTPAdapter, Retry



URL = ("https://www.deckshop.pro/check/?deck="
       "ElectroSpirit"
       "-Berserker"
       "-Firecracker"
       "-DartGob"
       "-RoyalHogs"
       "-Guards"
       "-Skarmy"
       "-Log")

# 1 -> 2 -> 3 -> 4 -> 5 -> 6
# RIP -> Bad -> Mediocre -> Good -> Great -> Godly!

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/127.0.0.0 Safari/537.36",
    "Accept-Language": "es-CL,es;q=0.9,en;q=0.8",
}

def get_session() -> requests.Session:
    """Crea una sesión con reintentos y timeouts razonables."""
    retries = Retry(
        total=5,
        backoff_factor=0.5,
        status_forcelist=(429, 500, 502, 503, 504),
        allowed_methods=("GET",)
    )
    s = requests.Session()
    s.headers.update(HEADERS)
    s.mount("https://", HTTPAdapter(max_retries=retries))
    s.mount("http://", HTTPAdapter(max_retries=retries))
    return s

def fetch_html(url: str, timeout: float = 15.0) -> str:
    sess = get_session()
    resp = sess.get(url, timeout=timeout)
    resp.raise_for_status()
    return resp.text

def extract_div_texts(html: str) -> List[str]:
    soup = BeautifulSoup(html, "lxml")  # usa lxml si está disponible
    # Selecciona exactamente los div con ambas clases
    divs = soup.select("div.w-full.mb-3")
    results = []
    for d in divs:
        # Obtiene texto limpio pero conservando saltos básicos
        text = " ".join(d.get_text(separator=" ", strip=True).split())
        if text:
            results.append(text)
    return results

def fetch_deck_rating(cards: List[str]) -> None:
    cards = [c.replace(" ", "") for c in cards]
    deck_str = "-".join(cards)
    url = f"https://www.deckshop.pro/check/?deck={deck_str}"
    html = fetch_html(url)
    texts = extract_div_texts(html)
    if not texts:
        return
    for i, t in enumerate(texts, 1):
        return t

if __name__ == "__main__":
    card_list = [
      "Bats",
      "Knight",
      "Hog Rider",
      "Skeletons",
      "Barbarian Barrel",
      "Firecracker",
      "Inferno Tower",
      "Poison"]
    fetch_deck_rating(card_list)
