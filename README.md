# Web Crawler - Recherche de flag

Petit crawler en Python qui parcourt un site web en largeur (BFS) à la
recherche d'un mot ou d'une chaîne de caractères (`flag`) dans le contenu
des pages, en restant sur le même domaine que la page racine.

## Fonctionnement

1. Part d'une URL racine.
2. Récupère tous les liens `<a href="...">` de la page.
3. Convertit les liens relatifs en liens absolus et ne garde que ceux
   appartenant au même domaine que la racine.
4. Visite chaque lien un par un (file d'attente), en évitant de revisiter
   une page déjà vue.
5. Vérifie si le `flag` apparaît dans le texte de la page.
6. S'arrête dès que le flag est trouvé, ou après `max_pages` pages
   analysées, ou quand il n'y a plus de lien à visiter.

## Prérequis

```bash
pip install requests beautifulsoup4
```

## Utilisation

Éditer les valeurs de `flag` et `racine` en bas du script :

```python
flag = "FLAG{...}"
racine = "https://exemple.com"
```

Puis lancer :

```bash
python web_crawler_flag_search.py
```

## Paramètres utiles

| Paramètre   | Rôle                                                       | Défaut |
|-------------|-------------------------------------------------------------|--------|
| `max_pages` | Nombre maximum de pages analysées avant abandon             | 500    |
| `delai`     | Pause (en secondes) entre deux requêtes                     | 0.5    |
| `timeout`   | Délai d'attente max pour chaque requête HTTP                | 5      |

## Sortie

Le script affiche au fur et à mesure les pages analysées, puis à la fin :

- si le flag est trouvé : l'URL de la page concernée et le nombre de
  pages analysées ;
- sinon : un message d'échec avec le nombre total de pages analysées.

## Limites connues

- Ne suit que les liens `<a href="...">` (pas les liens générés en
  JavaScript, ni les formulaires).
- Reste volontairement sur le même domaine que la racine (pas de crawl
  externe).
- Pas d'authentification gérée si le site en nécessite une.

## Usage responsable

Ce crawler envoie des requêtes HTTP automatisées. À n'utiliser que sur
des sites dont vous avez l'autorisation de tester (CTF, environnement
de test, site vous appartenant), en respectant le `robots.txt` et les
conditions d'utilisation du site ciblé.
