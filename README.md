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
<kbd> ![Interface Principale](/images/c1.png) </kbd>

**Exemple de résumé généré :**
<kbd> ![Résumé Généré](/images/c2.png) </kbd>

**Exemple de traduction :**
<kbd> ![Traduction Effectuée](/images/c3.png) </kbd>

## Bibliothèques Principales Utilisées

*   **Streamlit :** Pour la création de l'interface web.
*   **Hugging Face Transformers :** Pour l'accès aux modèles pré-entraînés de résumé et de traduction.
*   **PyTorch :** Backend pour les modèles Transformers.
*   **SentencePiece :** Utilisé par les tokenizers de certains modèles Transformers.
*   **Langdetect :** Pour la détection de la langue source du texte.
