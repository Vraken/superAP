import socket

import streamlit as st
import requests
from sourceInfo import sourceInfo
import random


st.title("Super AP")

guideReg = sourceInfo("Guide réglementaire du scoutisme", "d4d373cf-4da4-4420-9038-9956e2cac86d","https://ressources.sgdf.fr/public/download/119/","/resources/guide_reg.png")
Balise = sourceInfo("Balises", "10c283bf-524c-4553-9681-83934b8c9cbd","https://chefscadres.sgdf.fr/ressources/#/explore/tag/1101","./resources/balise.png")
GPS = sourceInfo("GPS", "0d7d338b-4415-4772-99f2-31a98326f5bb","https://ressources.sgdf.fr/public/download/1575/","./resources/GPS.png")
pdfHygieneAcm = sourceInfo("Guide des bonnes pratiques de l'hygiène de la restauration en ACM", "61488718-29cc-4cd7-a9e7-89465dce0241","https://ressources.sgdf.fr/public/download/1896/")

listSourceInfo = [guideReg, Balise, GPS, pdfHygieneAcm]
labels = [sourceInfo.label for sourceInfo in listSourceInfo]

sourceInfoLabel = st.multiselect("Interlocuteurs", labels, labels)

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

def getSourceInfoFromLabel(label) -> sourceInfo:
    return [sourceInfo for sourceInfo in listSourceInfo if sourceInfo.label == label][0]


def askQuestion(question, sourceInfoLabel):
    sourceInfo = getSourceInfoFromLabel(sourceInfoLabel)
    avatar = sourceInfo.avatar
    print("avatar :"+ avatar)
    print("socket.gethostname(); "+socket.gethostname())

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
        # st.markdown("---")
        # st.subheader("Source : "+sourceInfo)
        completeAnswer = answer['data']['answer']

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
        print(response)

if question:
    with st.chat_message("user",avatar="https://img.icons8.com/?size=512&id=AZBAeQBAUxm0&format=png"):
        st.write(question)

    for source in sourceInfoLabel:
        askQuestion(question, source)
