import streamlit as st
from transformers import pipeline
import time # Pour simuler un délai si nécessaire pour le spinner
import traceback # Pour un logging d'erreur détaillé
from langdetect import detect, DetectorFactory, LangDetectException # Pour la détection de langue

# Assurer la reproductibilité pour langdetect (optionnel mais bonne pratique)
DetectorFactory.seed = 0

# --- Configuration de la Page (DOIT ÊTRE LA PREMIÈRE COMMANDE STREAMLIT) ---
st.set_page_config(page_title="Processeur de Texte", layout="wide", page_icon="✍️")


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

# --- Application Principale ---
st.title("✍️ Processeur de Texte : Résumé & Traduction")
st.markdown("""
Bienvenue sur Processeur de Texte !
1. Entrez votre texte dans la zone ci-dessous.
2. Obtenez un résumé concis (optimisé pour l'anglais).
3. Traduisez le texte original vers différentes langues (la langue source sera auto-détectée).
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
        st.info("ℹ️ Le modèle de résumé (`facebook/bart-large-cnn`) est optimisé pour l'anglais.")
        if st.button("Générer le résumé", key="bouton_resumer", use_container_width=True):
            texte_a_resumer = texte_original.strip()
            if texte_a_resumer:
                with st.spinner("Génération du résumé... veuillez patienter."):
                    try:
                        nb_mots = len(texte_a_resumer.split())
                        
                        if nb_mots == 0:
                            # final_min_len = 1; final_max_len = 5 # Non utilisé si on n'appelle pas resumeur
                            st.text_area("Résumé :", value="Texte d'entrée vide.", height=150, disabled=True, key="resume_output_vide")
                        else:
                            # Nouvelle logique pour min_length et max_length (basée sur la discussion précédente)
                            if nb_mots < 50: # Pour les textes plus courts
                                final_min_len = max(10, int(nb_mots * 0.3))
                                final_max_len = max(final_min_len + 10, int(nb_mots * 0.7))
                            else: # Pour les textes plus longs
                                final_min_len = max(50, int(nb_mots * 0.15)) # Au moins 50 mots ou 15%
                                final_max_len = min(200, max(final_min_len + 30, int(nb_mots * 0.5))) # Max 200 mots, ou 50%

                            # --- Ajustements de sécurité critiques ---
                            final_min_len = max(1, final_min_len)
                            # max_length doit être > min_length et assez grand pour les tokens spéciaux
                            final_max_len = max(final_min_len + 3, final_max_len, 5) 
                            if final_min_len >= final_max_len: # Ultime vérification
                                final_min_len = max(1, int(final_max_len / 2))
                                # S'assurer que max_len est toujours plus grand
                                final_max_len = max(final_min_len + 3, final_max_len, 5)
                            # --- Fin des ajustements de sécurité ---

                            # Décommenter pour le débogage des longueurs
                            # st.caption(f"DEBUG - Résumé: nb_mots={nb_mots}, min_len={final_min_len}, max_len={final_max_len}")
                            
                            resultat_resume = resumeur(texte_a_resumer, 
                                                       max_length=final_max_len, 
                                                       min_length=final_min_len, 
                                                       do_sample=False)

                            if resultat_resume and isinstance(resultat_resume, list) and len(resultat_resume) > 0 and "summary_text" in resultat_resume[0]:
                                st.success("Résumé généré !")
                                st.text_area("Résumé :", value=resultat_resume[0]['summary_text'], height=150, disabled=True, key="resume_output")
                            else:
                                st.error("Impossible de générer le résumé. Le format de sortie est peut-être inattendu.")
                                st.json(resultat_resume) # Pour débogage
                    except Exception as e:
                        st.error(f"Une erreur est survenue lors du résumé : {e}")
                        st.text(traceback.format_exc()) # Pour débogage
            else:
                st.warning("Veuillez d'abord saisir du texte à résumer.")
    else:
        st.error("Le modèle de résumé n'a pas pu être chargé.")

# --- Section Traduction ---
with col2:
    st.subheader("🌐 Traduction du Texte Original")

    langues_helsinki_supportees = {
        "Anglais": "en", "Français": "fr", "Espagnol": "es", "Allemand": "de", 
        "Italien": "it", "Russe": "ru", "Chinois (Simplifié)": "zh", 
        "Japonais": "jap", "Arabe": "ar", "Hindi": "hi", "Portugais": "pt"
    }

    langue_cible_selectionnee_affichage = st.selectbox(
        "Traduire vers :", options=list(langues_helsinki_supportees.keys()), index=0, key="langue_cible_select"
    )
    code_langue_cible = langues_helsinki_supportees[langue_cible_selectionnee_affichage]

    langue_detectee_placeholder = st.empty()

    if st.button("Traduire le texte", key="bouton_traduire", use_container_width=True):
        texte_a_traduire = texte_original.strip()
        if texte_a_traduire:
            code_langue_source = None
            nom_langue_source_affichee = "Inconnue"
            try:
                lang_code_detecte = detect(texte_a_traduire)
                for nom, code_iso in langues_helsinki_supportees.items():
                    if lang_code_detecte.startswith(code_iso) or \
                       (code_iso == 'jap' and lang_code_detecte == 'ja') or \
                       (code_iso == 'zh' and lang_code_detecte.startswith('zh')):
                        code_langue_source = code_iso
                        nom_langue_source_affichee = nom
                        break
                
                if code_langue_source:
                    langue_detectee_placeholder.info(f"Langue source détectée : **{nom_langue_source_affichee}** ({code_langue_source})")
                else:
                    langue_detectee_placeholder.warning(f"Langue détectée : '{lang_code_detecte}'. Ce couple de traduction n'est peut-être pas directement supporté.")

            except LangDetectException:
                langue_detectee_placeholder.error("Impossible de détecter la langue source. Le texte est peut-être trop court ou ambigu.")
                code_langue_source = None 

            if code_langue_source: 
                if code_langue_source == code_langue_cible:
                    st.warning("La langue source détectée et la langue cible sont identiques !")
                else:
                    nom_modele_traduction = f"Helsinki-NLP/opus-mt-{code_langue_source}-{code_langue_cible}"
                    traducteur_specifique = charger_traducteur(nom_modele_traduction)

                    if traducteur_specifique:
                        with st.spinner(f"Traduction de '{nom_langue_source_affichee}' vers '{langue_cible_selectionnee_affichage}'... veuillez patienter."):
                            try:
                                nb_mots_trad = len(texte_a_traduire.split())
                                trad_max_len = min(512, max(30, nb_mots_trad * 4)) # Limite typique des modèles Helsinki
                                resultat_traduction = traducteur_specifique(texte_a_traduire, max_length=trad_max_len)
                                
                                if resultat_traduction and isinstance(resultat_traduction, list) and len(resultat_traduction) > 0 and "translation_text" in resultat_traduction[0]:
                                    st.success(f"Traduction vers '{langue_cible_selectionnee_affichage}' réussie !")
                                    st.text_area(f"Texte traduit en {langue_cible_selectionnee_affichage} :", 
                                                 value=resultat_traduction[0]['translation_text'], height=150, 
                                                 disabled=True, key="traduction_output")
                                else:
                                    st.error(f"Impossible de traduire le texte avec le modèle {nom_modele_traduction}. Le couple de langues {code_langue_source}-{code_langue_cible} n'existe peut-être pas ou le format de sortie est inattendu.")
                                    st.json(resultat_traduction)
                            except Exception as e:
                                st.error(f"Une erreur est survenue lors de la traduction ({nom_modele_traduction}) : {e}")
                                st.text(traceback.format_exc())
                    else:
                        st.error(f"Le modèle de traduction pour {nom_langue_source_affichee} ({code_langue_source}) vers {langue_cible_selectionnee_affichage} ({code_langue_cible}) n'a pas pu être chargé. Ce couple de langues n'est peut-être pas disponible.")
            elif texte_a_traduire: # Si du texte est présent mais code_langue_source est None
                # Le message d'erreur ou d'avertissement de langue_detectee_placeholder est déjà affiché
                # Donc, pas besoin d'un autre message ici, sauf si on veut être plus explicite.
                # st.error("La traduction ne peut pas continuer car la langue source n'a pas été correctement identifiée ou supportée.")
                pass

        else:
            st.warning("Veuillez d'abord saisir du texte à traduire.")

# --- Pied de Page (Footer) ---
st.markdown("---") 
st.markdown(f"""
<div style="text-align: center; padding: 10px; font-size: 0.9em;">
    <p style="margin-bottom: 2px;">Projet 3 - End-to-End Deep Learning - Binôme 7</p>
    <p style="margin-bottom: 2px;">Réalisé par : <strong>Israe EL GHIOUAN</strong> & <strong>Abdessamad BENCHERAIK</strong></p>
    <p><a href="[VOTRE_LIEN_GITHUB_ICI]" target="_blank">Voir le code source sur GitHub</a></p>
</div>
""", unsafe_allow_html=True)
