import streamlit as st
from transformers import pipeline
import time # Pour simuler un délai si nécessaire pour le spinner
import traceback # Pour un logging d'erreur détaillé
from langdetect import detect, DetectorFactory, LangDetectException # Pour la détection de langue

# Assurer la reproductibilité pour langdetect (optionnel mais bonne pratique)
DetectorFactory.seed = 0

# --- Application Principale ---
st.set_page_config(page_title="Processeur de Texte", layout="wide", page_icon="✍️")

# --- CSS Personnalisé pour des couleurs plus vives en mode sombre ---
custom_css = """
<style>
    /* Rendre le texte général un peu plus clair */
    body .stApp {
        color: #E0E0E0; /* Gris clair au lieu du blanc pur pour éviter d'être trop criard */
    }

    /* Titres principaux */
    h1, h2 {
        color: #C5CAE9; /* Bleu lavande clair */
    }
    h3 {
       color: #B3E5FC; /* Cyan clair */
    }


    /* Améliorer la lisibilité des messages st.info, st.success, st.warning, st.error */
    .stAlert > div[role="alert"] {
        color: #FFFFFF !important; /* Texte blanc dans les alertes */
        background-color: rgba(255, 255, 255, 0.1) !important; /* Fond légèrement transparent */
    }
    .stAlert[data-baseweb="notification"][data-kind="info"] {
        background-color: #2E4053 !important; /* Bleu foncé pour info */
        border-left: 5px solid #5DADE2 !important;
    }
    .stAlert[data-baseweb="notification"][data-kind="success"] {
        background-color: #1E4D2B !important; /* Vert foncé pour success */
        border-left: 5px solid #58D68D !important;
    }
    .stAlert[data-baseweb="notification"][data-kind="warning"] {
        background-color: #5D4037 !important; /* Marron foncé pour warning */
        border-left: 5px solid #F5B041 !important;
    }
    .stAlert[data-baseweb="notification"][data-kind="error"] {
        background-color: #5E3530 !important; /* Rouge foncé pour error */
        border-left: 5px solid #EC7063 !important;
    }

    /* Améliorer le texte dans les zones de texte désactivées (résultats) */
    .stTextArea textarea[disabled] {
        background-color: rgba(70, 70, 90, 0.5) !important; /* Fond légèrement plus clair pour le résultat */
        color: #F0F0F0 !important; /* Texte du résultat plus clair */
        border: 1px solid #4A4A6A !important;
    }
    
    /* Améliorer le placeholder des text_area */
    .stTextArea textarea::placeholder {
        color: #A0A0B0 !important;
    }

    
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)


# --- Chargement des Modèles (mis en cache pour la performance) ---
@st.cache_resource
def charger_resumeur():
    """Charge le pipeline de résumé."""
    try:
        resumeur = pipeline("summarization", model="facebook/bart-large-cnn")
        return resumeur
    except Exception as e:
        st.error(f"Erreur critique lors du chargement du modèle de résumé : {e}")
        st.text(traceback.format_exc())
        return None

@st.cache_resource
def charger_traducteur(nom_modele="Helsinki-NLP/opus-mt-en-fr"):
    """Charge un pipeline de traduction pour un modèle donné."""
    try:
        traducteur = pipeline("translation", model=nom_modele)
        return traducteur
    except Exception as e:
        print(f"AVERTISSEMENT: Impossible de charger le modèle de traduction {nom_modele}: {e}")
        return None


st.title("✍️ Processeur de Texte : Résumé & Traduction")
st.markdown("""
Bienvenue sur Processeur de Texte !
1. Entrez votre texte dans la zone ci-dessous.
2. Obtenez un résumé concis.
3. Traduisez le texte original vers différentes langues.
""")

# --- Charger les modèles ---
resumeur = charger_resumeur()

# --- Entrée Utilisateur ---
st.header("Saisissez votre texte ici :")
texte_original = st.text_area("Entrez le texte à traiter :", height=200,
                              placeholder="Collez votre long article, e-mail ou tout contenu textuel ici...",
                              key="texte_original_input")

col1, col2 = st.columns(2)

# --- Section Résumé ---
with col1:
    st.subheader("📜 Résumé du Texte")
    if resumeur:
        st.info("ℹ️ Le modèle de résumé actuel (`facebook/bart-large-cnn`).")
        if st.button("Générer le résumé", key="bouton_resumer", use_container_width=True):
            texte_a_resumer = texte_original.strip()
            if texte_a_resumer:
                with st.spinner("Génération du résumé... veuillez patienter."):
                    try:
                        nb_mots = len(texte_a_resumer.split())
                        
                        if nb_mots == 0:
                            final_min_len = 1; final_max_len = 5
                            st.text_area("Résumé :", value="Texte d'entrée vide.", height=150, disabled=True, key="resume_output_vide")
                        else:
                            if nb_mots < 20:
                                final_min_len = max(1, int(nb_mots * 0.4)) 
                                final_max_len = nb_mots + 10
                            elif nb_mots < 70:
                                final_min_len = max(10, int(nb_mots * 0.25))
                                final_max_len = max(final_min_len + 15, int(nb_mots * 0.6))
                            else:
                                final_min_len = max(30, int(nb_mots * 0.1))
                                final_max_len = min(150, max(final_min_len + 20, int(nb_mots * 0.4)))

                            final_min_len = max(1, final_min_len)
                            final_max_len = max(final_min_len + 3, final_max_len, 5)
                            if final_min_len >= final_max_len:
                                final_min_len = max(1, int(final_max_len / 2))
                                final_max_len = max(final_min_len + 3, final_max_len, 5)

                            resultat_resume = resumeur(texte_a_resumer, 
                                                       max_length=final_max_len, 
                                                       min_length=final_min_len, 
                                                       do_sample=False)

                            if resultat_resume and isinstance(resultat_resume, list) and len(resultat_resume) > 0 and "summary_text" in resultat_resume[0]:
                                st.success("Résumé généré !")
                                st.text_area("Résumé :", value=resultat_resume[0]['summary_text'], height=150, disabled=True, key="resume_output")
                            else:
                                st.error("Impossible de générer le résumé.")
                                st.json(resultat_resume)
                    except Exception as e:
                        st.error(f"Une erreur est survenue lors du résumé : {e}")
                        st.text(traceback.format_exc())
            else:
                st.warning("Veuillez d'abord saisir du texte à résumer.")
    else:
        st.error("Le modèle de résumé n'a pas pu être chargé.")

# --- Section Traduction ---
with col2:
    st.subheader("🌐 Traduction du Texte Original")

    # Définition des langues supportées pour la traduction (codes ISO 639-1)
    # Ces codes doivent correspondre à ceux utilisés par les modèles Helsinki-NLP
    langues_helsinki_supportees = {
        "Anglais": "en", "Français": "fr", "Espagnol": "es", "Allemand": "de", 
        "Italien": "it", "Russe": "ru", "Chinois (Simplifié)": "zh", 
        "Japonais": "jap", "Arabe": "ar", "Hindi": "hi", "Portugais": "pt"
    }

    # Selectbox pour la langue cible uniquement
    langue_cible_selectionnee_affichage = st.selectbox(
        "Traduire vers :", options=list(langues_helsinki_supportees.keys()), index=0, key="langue_cible_select"
    )
    code_langue_cible = langues_helsinki_supportees[langue_cible_selectionnee_affichage]

    # Espace pour afficher la langue détectée
    langue_detectee_placeholder = st.empty()

    if st.button("Traduire le texte", key="bouton_traduire", use_container_width=True):
        texte_a_traduire = texte_original.strip()
        if texte_a_traduire:
            code_langue_source = None
            nom_langue_source_affichee = "Inconnue"
            try:
                lang_code_detecte = detect(texte_a_traduire)
                # Essayer de mapper le code détecté à nos noms de langue pour l'affichage
                # et vérifier si c'est une langue source supportée par nos modèles Helsinki-NLP
                for nom, code_iso in langues_helsinki_supportees.items():
                    # Certains modèles Helsinki utilisent des codes légèrement différents (ex: 'jap' vs 'ja')
                    # langdetect retourne les codes ISO 639-1 standards ('ja', 'zh-cn', etc.)
                    # Pour simplifier, nous allons juste vérifier si le début du code détecté correspond
                    if lang_code_detecte.startswith(code_iso) or \
                       (code_iso == 'jap' and lang_code_detecte == 'ja') or \
                       (code_iso == 'zh' and lang_code_detecte.startswith('zh')): # 'zh' pour 'zh-cn', 'zh-tw'
                        code_langue_source = code_iso # Utiliser le code Helsinki
                        nom_langue_source_affichee = nom
                        break
                
                if code_langue_source:
                    langue_detectee_placeholder.info(f"Langue source détectée : **{nom_langue_source_affichee}** ({code_langue_source})")
                else:
                    langue_detectee_placeholder.warning(f"Langue détectée : '{lang_code_detecte}'. Traduction depuis cette langue non directement supportée par les modèles pré-sélectionnés. Tentative avec 'en' comme source si possible.")
                    # Fallback sur l'anglais si la détection échoue ou n'est pas dans notre liste directe
                    # Ce fallback est discutable, on pourrait aussi afficher une erreur.
                    # Pour l'instant, on ne force pas de fallback, l'utilisateur doit savoir.
                    st.error(f"Impossible de trouver un modèle de traduction direct pour la langue source '{lang_code_detecte}'.")


            except LangDetectException:
                langue_detectee_placeholder.error("Impossible de détecter la langue source. Le texte est peut-être trop court ou ambigu.")
                code_langue_source = None # Indique un échec de détection

            if code_langue_source: # Procéder uniquement si la langue source est identifiée et supportée
                if code_langue_source == code_langue_cible:
                    st.warning("La langue source détectée et la langue cible sont identiques !")
                else:
                    nom_modele_traduction = f"Helsinki-NLP/opus-mt-{code_langue_source}-{code_langue_cible}"
                    traducteur_specifique = charger_traducteur(nom_modele_traduction)

                    if traducteur_specifique:
                        with st.spinner(f"Traduction de '{nom_langue_source_affichee}' vers '{langue_cible_selectionnee_affichage}'... veuillez patienter."):
                            try:
                                nb_mots_trad = len(texte_a_traduire.split())
                                trad_max_len = min(512, max(30, nb_mots_trad * 4))
                                resultat_traduction = traducteur_specifique(texte_a_traduire, max_length=trad_max_len)
                                
                                if resultat_traduction and isinstance(resultat_traduction, list) and len(resultat_traduction) > 0 and "translation_text" in resultat_traduction[0]:
                                    st.success(f"Traduction vers '{langue_cible_selectionnee_affichage}' réussie !")
                                    st.text_area(f"Texte traduit en {langue_cible_selectionnee_affichage} :", 
                                                 value=resultat_traduction[0]['translation_text'], height=150, 
                                                 disabled=True, key="traduction_output")
                                else:
                                    st.error(f"Impossible de traduire le texte avec le modèle {nom_modele_traduction}. Format inattendu ou modèle non supporté (le couple de langues {code_langue_source}-{code_langue_cible} n'existe peut-être pas).")
                                    st.json(resultat_traduction)
                            except Exception as e:
                                st.error(f"Une erreur est survenue lors de la traduction ({nom_modele_traduction}) : {e}")
                                st.text(traceback.format_exc())
                    else:
                        st.error(f"Le modèle de traduction pour {nom_langue_source_affichee} ({code_langue_source}) vers {langue_cible_selectionnee_affichage} ({code_langue_cible}) n'a pas pu être chargé. Ce couple de langues n'est peut-être pas disponible.")
            # else:
                # Message d'erreur déjà géré par la logique de détection de langue

        else:
            st.warning("Veuillez d'abord saisir du texte à traduire.")

# --- Pied de Page (Footer) ---
st.markdown("---")
st.markdown(f"""
<div class="footer-text" style="text-align: center; padding: 10px; font-size: 1em;">
    <p>Projet 3 - End-to-End Deep Learning - Binôme 7</p>
    <p>Réalisé par : <strong>Israe EL GHIOUAN</strong> & <strong>Abdessamad BENCHERAIK</strong></p>
    <p><a href="#" target="_blank">Voir le code source sur GitHub</a></p>
</div>
""", unsafe_allow_html=True)