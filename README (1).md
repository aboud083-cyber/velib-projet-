# Vélib’ : disponibilité des vélos par station

Une visualisation locale des stations Vélib’ réalisée avec **Python**, à partir d’un export JSON de MongoDB. Elle permet de retrouver une station par son nom ou sa commune, de consulter le nombre de vélos classiques et électriques disponibles et de la situer sur une carte.

> **Périmètre :** il s’agit d’une photographie des données contenues dans l’export fourni. La page ne récupère pas les disponibilités en temps réel.

## Captures et aperçu

**1. Données de départ dans MongoDB Compass.** La collection `VelibDB.velib_collection` contient les champs du nom de station, de disponibilité et de localisation utilisés dans le projet.

![Capture de la collection Vélib’ dans MongoDB Compass](assets/capture_mongodb.png)

**2. Résultat du traitement Python.** Aperçu rendu de `index.html` : indicateurs globaux et premières stations classées par nombre de vélos disponibles. Cette image montre un extrait du tableau ; le fichier HTML contient les 1 517 stations.

![Aperçu de la visualisation HTML des vélos disponibles par station](assets/capture_visualisation.png)

## Résultat

| Indicateur dans l’export | Valeur |
| --- | ---: |
| Stations enregistrées | 1 517 |
| Stations ouvertes à la location | 1 496 |
| Vélos disponibles dans les stations ouvertes | 18 155 |

La page affiche une ligne par station, avec son nom, sa commune, le total de vélos disponibles, le nombre de vélos classiques et électriques, ainsi que son statut de location. Les stations ouvertes sont présentées en premier, puis classées selon le nombre de vélos disponibles. Le tableau reste visible même si JavaScript est désactivé ; la recherche intégrée est un confort supplémentaire.

## Voir la visualisation

Ouvrir **[`index.html`](index.html)** dans un navigateur après avoir téléchargé ou extrait les fichiers du projet. Aucun serveur et aucune dépendance Python ne sont nécessaires pour consulter la page déjà générée.

Le lien « Carte » de chaque station ouvre sa position sur OpenStreetMap ; cette fonction nécessite une connexion Internet.

## Reproduire le résultat avec Python

**Prérequis :** Python 3.9 ou une version plus récente. Le script n’utilise que la bibliothèque standard.

1. Conserver `visualiser_velib.py` et `VelibDB.velib_collection.json` dans le même dossier.
2. Depuis ce dossier, exécuter :

   ```bash
   python visualiser_velib.py
   ```

   Sous Windows, si la commande `python` n’est pas reconnue, essayer `py visualiser_velib.py`.

3. Ouvrir le fichier `index.html` créé par le script.

## Organisation

```text
.
├── README.md                        Présentation du projet
├── visualiser_velib.py             Traitement des données et création de la page
├── VelibDB.velib_collection.json   Export MongoDB utilisé
├── index.html                      Visualisation prête à consulter
└── assets/
    ├── capture_mongodb.png         Capture du jeu de données dans Compass
    └── capture_visualisation.png   Aperçu rendu de la visualisation
```

## Traitement des données

Le script charge les documents JSON exportés de MongoDB, puis lit les champs `name`, `nom_arrondissement_communes`, `numbikesavailable`, `mechanical`, `ebike`, `is_renting` et `coordonnees_geo`. Ce dernier champ est une chaîne JSON contenant la latitude et la longitude : elle est décodée avant de créer le lien vers la carte. Le script trie les stations et génère ensuite les lignes du tableau directement dans le HTML. La recherche par nom ou par commune fonctionne dans le navigateur quand JavaScript est activé.

## Limites importantes

- **Adresse :** le jeu de données ne fournit pas d’adresse postale complète. Le nom de la station et sa commune servent de repère, et les coordonnées permettent de vérifier son emplacement.
- **Actualisation :** les quantités affichées correspondent à cet export. Une consultation ultérieure ne donne pas automatiquement la disponibilité du moment.
- **Horodatage :** `duedate` vaut le 1er janvier 1970 sur les 1 517 documents. Cette valeur n’est pas utilisée comme date fiable de collecte.
- **Arrondissements :** la commune est indiquée comme « Paris » pour les stations parisiennes, sans numéro d’arrondissement dans ce champ.

## Présentation courte

> J’ai transformé un export MongoDB de stations Vélib’ en une page HTML générée par Python. Le projet rend les données faciles à consulter : recherche par station ou commune, détail des vélos disponibles et localisation cartographique. J’ai également signalé les limites du jeu de données, notamment l’absence d’adresse postale et d’horodatage fiable.
