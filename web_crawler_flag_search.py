import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from collections import deque
import time


def get_liens(url, domaine, timeout=5):
    """Récupère tous les liens absolus d'une page, filtrés sur le domaine cible."""
    liens = []
    try:
        page = requests.get(url, timeout=timeout, headers={"User-Agent": "Mozilla/5.0"})
        page.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Erreur sur {url} : {e}")
        return liens, None

    contenu = BeautifulSoup(page.text, "html.parser")

    for a in contenu.find_all("a"):
        href = a.get("href")
        if not href or href.startswith(("mailto:", "tel:", "javascript:", "#")):
            continue
        url_absolue = urljoin(url, href)
        if urlparse(url_absolue).netloc == domaine:
            liens.append(url_absolue)

    return liens, contenu.get_text()


def recherche_flag(flag, racine, max_pages=500, delai=0.5):
    """Parcourt le site en largeur (BFS) à la recherche du flag."""
    domaine = urlparse(racine).netloc
    a_visiter = deque([racine])
    visites = set()
    compteur = 0

    while a_visiter and compteur < max_pages:
        url = a_visiter.popleft()

        if url in visites:
            continue
        visites.add(url)

        print(f"Analyse de {url}")
        liens, texte = get_liens(url, domaine)
        compteur += 1

        if texte is None:
            continue  # page inaccessible, on passe

        if flag in texte:
            print("\nFlag trouvé !")
            print(f"Lien : {url}")
            print(f"Nombre de pages analysées : {compteur}")
            return True, url, compteur

        for lien in liens:
            if lien not in visites:
                a_visiter.append(lien)

        time.sleep(delai)  # pour ne pas se faire bloquer

    print("Flag non trouvé.")
    print(f"Nombre de pages analysées : {compteur}")
    return False, None, compteur


if __name__ == "__main__":
    flag = " "
    racine = " "
    trouve, lien_flag, nb_pages = recherche_flag(flag, racine)