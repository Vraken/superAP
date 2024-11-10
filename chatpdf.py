import streamlit as st
import base64

import reederAiApi
from baseConnection import MySQLDatabase
from sourceInfo import sourceInfo

from tagWithColor import tagWithColor
from streamlit.logger import get_logger
import dynaStyle
import re

dynaStyle.setStyle();
## Initialisation des objets
# Rubriques

tagPeda = tagWithColor("Proposition pédagogique", "🟡")
tagReglementation = tagWithColor("Réglementation", "🔵")
tagFondamentaux = tagWithColor("Fondamentaux du scoutisme", "🟢")
tagSante = tagWithColor("Santé", "🟢")

# SourceInfo
guideReg = sourceInfo("Guide réglementaire du scoutisme", "d4d373cf-4da4-4420-9038-9956e2cac86d", [tagReglementation], "https://ressources.sgdf.fr/public/download/119/", "/resources/guide_reg.png")
Balise = sourceInfo("Balises", "10c283bf-524c-4553-9681-83934b8c9cbd", [tagPeda], "https://chefscadres.sgdf.fr/ressources/#/explore/tag/1101", "./resources/balise.png")
GPS = sourceInfo("GPS", "0d7d338b-4415-4772-99f2-31a98326f5bb", [tagPeda, tagFondamentaux], "https://ressources.sgdf.fr/public/download/1575/", "./resources/GPS.png")
pdfHygieneAcm = sourceInfo("Guide des pratiques d’hygiène de restauration en plein air", "61488718-29cc-4cd7-a9e7-89465dce0241", [tagReglementation],
                           "https://ressources.sgdf.fr/public/download/1896/")
ambitionEduc = sourceInfo("Ambitions éducatives", "b21e63dd-cc4b-423e-9073-f2363ebbff02", [tagPeda, tagFondamentaux], "https://chefscadres.sgdf.fr/ressources/#/explore/tag/386",
                          "/resources/ambitionEduc.png")
badenPowell = sourceInfo("Baden Powell", "1acca570-4822-4460-92b5-b4d1aa11e7a5", [tagFondamentaux], "http://www.thedump.scoutscan.com/yarns00-28.pdf", "./resources/bp.jpg")
sdjes = sourceInfo("SDJES", "5135358c-85f7-44e3-9933-9b0397343885", [tagReglementation], "https://acm-cvl.fr/memento/")
chenalMarin = sourceInfo("Chenal marin", "66cd2e0e-5009-43be-9ccd-67ef4cfa9546", [tagReglementation, tagPeda], "https://chefscadres.sgdf.fr/ressources/#/explore/tag/144",
                         "./resources/gouvernail-01.png")
ficheSante = sourceInfo("Fiches santé", "c8d66dbd-3a9c-4506-b955-566c19883bdf", [tagSante], "https://chefscadres.sgdf.fr/ressources/#/explore/tag/125", "./resources/malette_sante.png")

# Logger
logger = get_logger(__name__)

# BDD
db = MySQLDatabase(host="mysql-superap.alwaysdata.net", user=st.secrets["DB_USERNAME"], password=st.secrets["DB_PASSWORD"], database="superap_data")
db.connect()


def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()


## Début de l'appli

st.title("Ressources-Man")

listSourceInfo = [guideReg, GPS, Balise, pdfHygieneAcm, ambitionEduc, badenPowell, sdjes, chenalMarin, ficheSante]
listSourceInfoLabel = [sourceInfo.label for sourceInfo in listSourceInfo]
listRubrique = [tagReglementation, tagPeda, tagFondamentaux, tagSante]
listRubriqueLabel = [rubrique.label for rubrique in listRubrique]

def getSourceInfoFromTag(tag) -> list:
    return [sourceInfo for sourceInfo in listSourceInfo if tag in [tag.label for tag in sourceInfo.tags]]

if "labelState" not in st.session_state:
    st.session_state.labelState = []

if "rubriqueState" not in st.session_state:
    st.session_state["rubriqueState"] = []

if "questionState" not in st.session_state:
    st.session_state["questionState"] = ""


# if rubriquesSelect:
def rubriqueSelectChange():
    st.session_state.labelState = []
    for rubrique in st.session_state["rubriqueState"]:
        sourceInfoFromTag = getSourceInfoFromTag(rubrique)
        for sourceInfo in sourceInfoFromTag:
            if sourceInfo.label not in st.session_state.labelState:
                st.session_state.labelState.append(sourceInfo.label)


def getRubriqueFromlabel(rubriqueLabel) -> tagWithColor:
    return [rubrique for rubrique in listRubrique if rubriqueLabel == rubrique.label][0]


def formatRubrique(rubriqueLabel):
    rubrique = getRubriqueFromlabel(rubriqueLabel)
    # return f'{rubrique.color} #{rubriqueLabel}'
    return f'#{rubriqueLabel}'


def getSourceInfoFromLabel(label) -> sourceInfo:
    print("getSourceInfoFromLabel " + str(label))
    return [sourceInfo for sourceInfo in listSourceInfo if sourceInfo.label == label][0]


def formatSourceInfo(sourceInfoLabel):
    sourceInfo = getSourceInfoFromLabel(sourceInfoLabel)
    sourceInfoLabelFormatted = ""
    for rubrique in sourceInfo.tags:
        sourceInfoLabelFormatted += f'{rubrique.color}'
    sourceInfoLabelFormatted += f" {sourceInfo.label}"
    return sourceInfoLabelFormatted


rubriquesSelect = st.multiselect("Rubriques", listRubriqueLabel, on_change=rubriqueSelectChange, key="rubriqueState", format_func=formatRubrique, placeholder="Choisir une rubrique")

sourceInfoLabelSelect = st.multiselect("Interlocuteurs", st.session_state.labelState, placeholder="Choisir un interlocuteur")

question = st.chat_input("Poser une question")


# top5Container = st.sidebar.container()
sourceContainer = st.sidebar.container()
sourceContainer.header("Sources")


def askQuestion(question, sourceInfoLabel):
    sourceInfo = getSourceInfoFromLabel(sourceInfoLabel)
    db.increment_or_insert(question, sourceInfo.label)
    logger.info(f"Asking '{sourceInfoLabel}' question : '{question}'")
    with st.spinner(text=sourceInfo.label + " est en train d'écrire ..."):
        response = reederAiApi.askDocument(docId=sourceInfo.refId, question=question)
        # st.success('Prêt!')
    # Afficher la réponse
    if response.status_code == 200:
        print(response.text)
        fragments = response.text.split("<next>")
        cleaned_fragments = [fragment.replace("data:", "") for fragment in fragments]
        full_text = "".join(cleaned_fragments).split("sourcetext")

        answer = full_text
        if sourceInfoLabel == badenPowell.label and "Qui est Marc Torrent".lower() in question.lower():
            completeAnswer = "Né un 25 février, quelques jours après BP, Marc Torrent est un pilier du scoutisme en France. Il a notamment créer un groupe dans l'Oise dans sa jeunesse. Fort de son expérience, il est le seul scout à avoir été reconnu par Jean-Jacques Goldman alors qu'il était dans la queue du self de Jambville. Compteur de dukou depuis peu, il tient le titre de champion du monde de compteur de dukou avec un total de 45 fois dans une phrase. Poké-Stat de son territoire, Essonne Levant, et fort de ses anecdotes, il est indéniablement une personne que l'on veut dans son équipe ❤️"
        else:
            completeAnswer = full_text[0]
        logger.info(completeAnswer)

        with st.chat_message(sourceInfo.label, avatar=sourceInfo.avatar):
            st.markdown(f"**{sourceInfo.label}**")
            st.write(completeAnswer)

        sourceContainer.subheader(sourceInfo.label)
        sourceContainer.write(f"[Télécharger]({sourceInfo.link})")

        for i in range(min(len(full_text[0]), 3)):
            regex_pattern = r'sourcepage:(\d+)'
            match = re.search(regex_pattern, full_text[i])
            if match:
                page_number = match.group(1)
                with sourceContainer.expander("Page " + page_number):
                    st.write(full_text[i].split("sourcepage")[0])


    else:
        st.error("Une erreur s'est produite lors de l'appel à l'API Reeder.")
        logger.error(response)


def askQuestions(question):
    if not sourceInfoLabelSelect:
        st.warning("Selectionnez au moins un interlocuteur")
    else:
        # Formate la question
        question = question.capitalize()
        if "?" not in question:
            question += " ?"
        with st.chat_message("user", avatar="https://img.icons8.com/?size=512&id=iLOt-63q7jv2&format=png"):
            st.write(question)
        for source in sourceInfoLabelSelect:
            askQuestion(question, source)


if question:
    # Warning : veuillez selectionner un interlocuteur
    askQuestions(question)

# top5Container.header("Top 5 des questions")
# top_questions = db.get_top_questions()
# for questionTop, total_calls in top_questions:
#     if top5Container.button(f"{questionTop} ({total_calls})", type="primary") and sourceInfoLabelSelect:
#         askQuestions(questionTop)


st.sidebar.write(dynaStyle.getFooter(), unsafe_allow_html=True)
#

db.disconnect()
