import streamlit as st
import requests
import base64

from baseConnection import MySQLDatabase
from sourceInfo import sourceInfo
import random
from tagWithColor import tagWithColor
from streamlit.logger import get_logger

st.set_page_config(page_title="Ressources-Man", page_icon="📖")

hide_default_format = """
       <style>
        #MainMenu {visibility: hidden; }
       footer {visibility: visible;
        position:fixed;
       bottom:0;}
        }
       </style>
       """
st.markdown(hide_default_format, unsafe_allow_html=True)

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
pdfHygieneAcm = sourceInfo("Guide des bonnes pratiques de l'hygiène de la restauration en ACM", "61488718-29cc-4cd7-a9e7-89465dce0241", [tagReglementation],
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
db = MySQLDatabase(host="mysql-superap.alwaysdata.net", user=st.secrets["DB_USERNAME"], password=st.secrets["DB_PASSWORD"], database="superap_bdd")
db.connect()


def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()


## Début de l'appli

st.title("Resources-Man")

page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
background-image: url("https://raw.githubusercontent.com/Vraken/superAP/master/resources/background.svg");
background-size: 25%;
background-position: bottom right;
background-repeat: no-repeat;
background-attachment: local;
background-color:rgba(0, 0, 0, 0);
}}



[data-testid="stHeader"] {{
background: rgba(0,0,0,0);
}}

</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)
st.markdown(
    """
    <style>
    button[kind="primary"] {
        background: none!important;
        border: none;
        padding: 0!important;
        color: black !important;
        text-decoration: none;
        cursor: pointer;
        border: none !important;
        text-align: left;
    }
    button[kind="primary"]:hover {
        text-decoration: none;
        color: black !important;
    }
    button[kind="primary"]:focus {
        outline: none !important;
        box-shadow: none !important;
        color: black !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

listSourceInfo = [guideReg, Balise, GPS, pdfHygieneAcm, ambitionEduc, badenPowell, sdjes, chenalMarin, ficheSante]
listSourceInfoLabel = [sourceInfo.label for sourceInfo in listSourceInfo]
listRubrique = [tagFondamentaux, tagPeda, tagReglementation, tagSante]
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

# top5Container = st.sidebar.container()
sourceContainer = st.sidebar.container()
sourceContainer.header("Sources")


def askQuestion(question, sourceInfoLabel):
    sourceInfo = getSourceInfoFromLabel(sourceInfoLabel)
    db.increment_or_insert(question, sourceInfo.label)
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
        if sourceInfoLabel == badenPowell.label and "Qui est Marc Torrent".lower() in question.lower():
            completeAnswer = "Né un 25 février, quelques jours après BP, Marc Torrent est un pilier du scoutisme en France. Il a notamment créer un groupe dans l'Oise dans sa jeunesse. Fort de son expérience, il est le seul scout à avoir été reconnu par Jean-Jacques Goldman alors qu'il était dans la queue du self de Jambville. Compteur de dukou depuis peu, il tient le titre de champion du monde de compteur de dukou avec un total de 45 fois dans une phrase. Poké-Stat de son territoire, Essonne Levant, et fort de ses anecdotes, il est indéniablement une personne que l'on veut dans son équipe ❤️"
        else:
            completeAnswer = answer['data']['answer']
        logger.info(completeAnswer)

        with st.chat_message(sourceInfo.label, avatar=sourceInfo.avatar):
            st.markdown(f"**{sourceInfo.label}**")
            st.write(completeAnswer)

        sourceContainer.subheader(sourceInfo.label)
        sourceContainer.write(f"[Télécharger]({sourceInfo.link})")
        for i in range(min(len(answer['data']['sources']), 3)):
            source = answer['data']['sources'][i]
            with sourceContainer.expander("Page " + str(source['page_number'])):
                st.write(source['raw_chunk'])

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

ft = """
<style>
a:link , a:visited{
color: #808080;  /* theme's text color hex code at 75 percent brightness*/
background-color: transparent;
text-decoration: none;
}

a:hover,  a:active {
color: #808080; /* theme's primary color*/
background-color: transparent;
text-decoration: underline;
}

#page-container {
  position: relative;
  min-height: 10vh;
}

footer{
    visibility:hidden;
}

.footer {
position: fixed !important;
left: 0;
top:230px;
bottom: 0;
width: 100%;
background-color: transparent;
color: #808080; /* theme's text color hex code at 50 percent brightness*/
text-align: left; /* you can replace 'left' with 'center' or 'right' if you want*/
}
</style>

<div id="page-container">

<footer>
<p style='font-size: 0.875em;'>Des questions, remarques, suggestions ?
<br/>
<a href="mailto:superap@alwaysdata.net">superap@alwaysdata.net</a>
</p>
</footer>

</div>
"""
st.sidebar.write(ft, unsafe_allow_html=True)
#

db.disconnect()
