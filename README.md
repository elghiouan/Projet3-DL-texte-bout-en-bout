# Processeur de Texte : Résumé & Traduction (Projet 3)

Ce projet est une application web développée avec Streamlit qui permet aux utilisateurs de :
1.  Générer un résumé concis d'un texte fourni.
2.  Traduire le texte original vers plusieurs langues, avec détection automatique de la langue source.

Il s'agit d'une démonstration d'un pipeline de Deep Learning de bout en bout, de la sélection des modèles pré-entraînés à leur déploiement dans une application interactive.

**Réalisé par (Binôme 7):**
*   Israe EL GHIOUAN
*   Abdessamad BENCHERAIK

## Fonctionnalités

*   **Résumé de Texte :** Utilise le modèle `facebook/bart-large-cnn` de Hugging Face Transformers.
*   **Traduction de Texte :** Utilise divers modèles `Helsinki-NLP/opus-mt-...` de Hugging Face Transformers.
*   **Détection Automatique de la Langue Source :** Utilise la bibliothèque `langdetect` pour identifier la langue du texte d'entrée avant la traduction.
*   **Interface Utilisateur Interactive :** Construite avec Streamlit pour une expérience utilisateur simple et directe.
*   **Personnalisation CSS :** Amélioration de la lisibilité en mode sombre.


## Démo en Ligne

[Lien vers la Démo Streamlit Déployée - À AJOUTER ICI]

## Vidéo de simulatuon
Video : google drive link

## Captures d'Écran

*(Insérez ici vos captures d'écran. Vous pouvez les ajouter dans un sous-dossier `images/` et les lier ici.)*

**Exemple d'interface principale :**
<!-- ![Interface Principale](images/screenshot_main.png) -->
*Décommentez et remplacez par votre capture d'écran*

**Exemple de résumé généré :**
<!-- ![Résumé Généré](images/screenshot_summary.png) -->
*Décommentez et remplacez par votre capture d'écran*

**Exemple de traduction :**
<!-- ![Traduction Effectuée](images/screenshot_translation.png) -->
*Décommentez et remplacez par votre capture d'écran*


## Installation et Exécution Locale

Suivez ces étapes pour exécuter l'application sur votre machine locale :

1.  **Cloner le dépôt (si ce n'est pas déjà fait) :**
    ```bash
    git clone [URL_DE_VOTRE_DEPOT_GITHUB_ICI]
    cd nom-du-dossier-du-projet
    ```

2.  **Créer et activer un environnement virtuel (recommandé avec Python 3.12) :**
    ```bash
    # Assurez-vous que py -3.12 (ou python3.12) pointe vers votre installation Python 3.12
    py -3.12 -m venv venv312 
    ```

    Changer les regles d'éxecution :
    *   `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process`

    Activer l'environnement :
    *   Windows (PowerShell) : `.\venv312\Scripts\activate`
    *   macOS/Linux : `source ./venv312/bin/activate`

3.  **Installer les dépendances :**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Exécuter l'application Streamlit :**
    ```bash
    streamlit run app.py
    ```
    L'application devrait s'ouvrir dans votre navigateur web à l'adresse `http://localhost:8501`.

## Bibliothèques Principales Utilisées

*   **Streamlit :** Pour la création de l'interface web.
*   **Hugging Face Transformers :** Pour l'accès aux modèles pré-entraînés de résumé et de traduction.
*   **PyTorch :** Backend pour les modèles Transformers.
*   **SentencePiece :** Utilisé par les tokenizers de certains modèles Transformers.
*   **Langdetect :** Pour la détection de la langue source du texte.

## Déploiement

Cette application peut être facilement déployée sur [Streamlit Community Cloud](https://streamlit.io/cloud) en liant ce dépôt GitHub.

---