# Projet 3 : Processeur de Texte (Résumé & Traduction)

**Binôme : 7**
**Projet réalisé par :**
* EL GHIOUAN ISRAE
* BENCHERAIK ABDESSAMAD

## Description du Projet
Application web Streamlit permettant aux utilisateurs de résumer des textes et les traduire vers différentes langues avec détection automatique de la langue source. Ce projet démontre un pipeline de Deep Learning complet, de la sélection des modèles à leur déploiement dans une interface interactive.

## Fonctionnalités
* **Résumé de Texte :** Modèle `facebook/bart-large-cnn` de Hugging Face
* **Traduction :** Modèles `Helsinki-NLP/opus-mt-...` de Hugging Face
* **Détection de Langue :** Identification automatique de la langue source
* **Interface Interactive :** Expérience utilisateur simple avec Streamlit

## Livrables
- **Démo fonctionnelle** : [Lien vers l'application Streamlit déployée](https://projet3-dl-texte-bout-en-bout.streamlit.app/)
- **Google Drive** contenant :
  1. Document Word ( pages)
  2. Vidéo de présentation ( minutes) : [Lien](https://drive.google.com/file/d/1abcXYZ123)
  3. Ce dépôt GitHub avec code source et documentation
  
  **Lien Google Drive** : [https://drive.google.com/drive/folders/1xYZ123ABC](https://drive.google.com/drive/folders/1xYZ123ABC)

## Captures d'Écran

**Exemple d'interface principale :**
[Interface Principale](images/c1.png)

**Exemple de résumé généré :**
<!-- ![Résumé Généré](images/screenshot_summary.png) -->
*Décommentez et remplacez par votre capture d'écran*

**Exemple de traduction :**
<!-- ![Traduction Effectuée](images/screenshot_translation.png) -->
*Décommentez et remplacez par votre capture d'écran*


## Installation et Exécution
1. **Cloner le dépôt :**
   ```bash
   git clone https://github.com/username/text-processor-app.git
   cd text-processor-app

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
