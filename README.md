# Projet Flask

Ce projet est une application web construite avec Flask. Elle utilise Bulma pour le CSS et inclut des fichiers JavaScript pour des fonctionnalités supplémentaires.

## Structure du projet

- `app.py` : Le fichier principal de l'application Flask.
- `instance/` : Contient les fichiers de configuration spécifiques à l'instance.
- `static/` : Contient les fichiers statiques comme les CSS et les JavaScript.
  - `css/` : Contient les fichiers CSS.
    - `bulma.min.css` : Framework CSS Bulma.
  - `js/` : Contient les fichiers JavaScript.
    - `daygrid.min.js` : Bibliothèque JavaScript pour les calendriers.
    - `main.min.js` : Fichier JavaScript principal.
- `templates/` : Contient les fichiers HTML pour les templates.
  - `archived.html` : Template pour les archives.
  - `calendar.html` : Template pour le calendrier.
  - `index.html` : Template pour la page d'accueil.

## Installation

1. Clonez le dépôt :
    ```sh
    git clone https://github.com/Mounik/TodoList.git
    ```
2. Accédez au répertoire du projet :
    ```sh
    cd TodoList
    ```
3. Créez un environnement virtuel :
    ```sh
    python -m venv env
    ```
4. Activez l'environnement virtuel :
    - Sur macOS/Linux :
        ```sh
        source env/bin/activate
        ```
    - Sur Windows :
        ```sh
        .\env\Scripts\activate
        ```
5. Installez les dépendances :
    ```sh
    pip install -r requirements.txt
    ```

## Utilisation

Pour démarrer l'application, exécutez :
```sh
python app.py
```

L'application sera accessible à l'adresse http://127.0.0.1:5000/.