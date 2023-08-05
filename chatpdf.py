import streamlit as st
import requests
from sourceInfo import sourceInfo
import random
from tagWithColor import tagWithColor
from streamlit.logger import get_logger

## Initialisation des objets
# Rubriques

tagPeda = tagWithColor("Proposition pédagogique", "🟡")
tagReglementation = tagWithColor("Réglementation", "🔵")
tagFondamentaux = tagWithColor("Fondamentaux du scoutisme", "🟢")

# SourceInfo
guideReg = sourceInfo("Guide réglementaire du scoutisme", "d4d373cf-4da4-4420-9038-9956e2cac86d", [tagReglementation], "https://ressources.sgdf.fr/public/download/119/", "/resources/guide_reg.png")
Balise = sourceInfo("Balises", "10c283bf-524c-4553-9681-83934b8c9cbd", [tagPeda], "https://chefscadres.sgdf.fr/ressources/#/explore/tag/1101", "./resources/balise.png")
GPS = sourceInfo("GPS", "0d7d338b-4415-4772-99f2-31a98326f5bb", [tagPeda, tagFondamentaux], "https://ressources.sgdf.fr/public/download/1575/", "./resources/GPS.png")
pdfHygieneAcm = sourceInfo("Guide des bonnes pratiques de l'hygiène de la restauration en ACM", "61488718-29cc-4cd7-a9e7-89465dce0241", [tagReglementation],
                           "https://ressources.sgdf.fr/public/download/1896/")
ambitionEduc = sourceInfo("Ambitions éducatives", "b21e63dd-cc4b-423e-9073-f2363ebbff02", [tagPeda, tagFondamentaux], "https://chefscadres.sgdf.fr/ressources/#/explore/tag/386",
                          "/resources/ambitionEduc.png")
badenPowell = sourceInfo("Baden Powell", "1acca570-4822-4460-92b5-b4d1aa11e7a5", [tagFondamentaux], "http://www.thedump.scoutscan.com/yarns00-28.pdf", "./resources/bp.jpg")

logger = get_logger(__name__)
## Début de l'appli

st.title("Resources-Man")
listSourceInfo = [guideReg, Balise, GPS, pdfHygieneAcm, ambitionEduc, badenPowell]
listSourceInfoLabel = [sourceInfo.label for sourceInfo in listSourceInfo]
listRubrique = [tagFondamentaux, tagPeda, tagReglementation]
listRubriqueLabel = [rubrique.label for rubrique in listRubrique]

def getSourceInfoFromTag(tag) -> list:
    return [sourceInfo for sourceInfo in listSourceInfo if tag in [tag.label for tag in sourceInfo.tags]]


if "labelState" not in st.session_state:
    st.session_state.labelState = []

if "rubriqueState" not in st.session_state:
    st.session_state["rubriqueState"] = []


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
    return [sourceInfo for sourceInfo in listSourceInfo if sourceInfo.label == label][0]


def formatSourceInfo(sourceInfoLabel):
    sourceInfo = getSourceInfoFromLabel(sourceInfoLabel)
    sourceInfoLabelFormatted = ""
    for rubrique in sourceInfo.tags:
        sourceInfoLabelFormatted += f'{rubrique.color}'
    sourceInfoLabelFormatted += f" {sourceInfo.label}"
    return sourceInfoLabelFormatted


rubriquesSelect = st.multiselect("Rubriques", listRubriqueLabel, on_change=rubriqueSelectChange, key="rubriqueState", format_func=formatRubrique, placeholder="Choisir une rubrique")

sourceInfoLabelSelect = st.multiselect("Interlocuteurs", st.session_state.labelState, st.session_state.labelState, placeholder="Choisir un interlocuteur")

question = st.chat_input("Poser une question")
session = requests.Session()

user_agent_list = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
]

session.headers = {
    "User-Agent": random.choice(user_agent_list)
}

st.sidebar.title("Sources")


def askQuestion(question, sourceInfoLabel):
    sourceInfo = getSourceInfoFromLabel(sourceInfoLabel)

    logger.info(f"Asking '{sourceInfoLabel}' question : '{question}'")
    with st.spinner(text=sourceInfo.label + " est en train d'écrire ..."):
        response = session.post("https://reederproduction.uk.r.appspot.com/querycollection",
                                headers={
                                    "authority": "reederproduction.uk.r.appspot.com",
                                    "method": "POST",
                                    "path": "/querycollection",
                                    "scheme": "https",
                                    "accept": "application/json, text/plain, */*",
                                    "accept-encoding": "gzip, deflate, br",
                                    "accept-language": "fr-FR,fr;q=0.7",
                                    "origin": "https://reeder.ai",
                                    "referer": "https://reeder.ai/",
                                    "sec-fetch-dest": "empty",
                                    "sec-fetch-mode": "cors",
                                    "sec-fetch-site": "cross-site",
                                    "sec-gpc": "1"
                                },
                                json={
                                    "collectionuuid": str(sourceInfo.refId),
                                    "question": question
                                }
                                )
        # st.success('Prêt!')
    # Afficher la réponse
    if response.status_code == 200:
        answer = response.json()
        completeAnswer = answer['data']['answer']
        logger.info(completeAnswer)

        with st.chat_message(sourceInfo.label, avatar=sourceInfo.avatar):
            st.markdown(f"**{sourceInfo.label}**")
            st.write(completeAnswer)

        st.sidebar.subheader(sourceInfo.label)
        st.sidebar.write(f"[Télécharger]({sourceInfo.link})")
        for i in range(min(len(answer['data']['sources']), 3)):
            source = answer['data']['sources'][i]
            with st.sidebar.expander("Page " + str(source['page_number'])):
                st.write(source['raw_chunk'])

    else:
        st.error("Une erreur s'est produite lors de l'appel à l'API Reeder.")
        logger.error(response)


if question:
    with st.chat_message("user", avatar="https://img.icons8.com/?size=512&id=iLOt-63q7jv2&format=png"):
        st.write(question)

    for source in sourceInfoLabelSelect:
        askQuestion(question, source)
