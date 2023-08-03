import streamlit as st
import requests

st.title("Super AP")

# Labels
labelGuideReg = "Guide réglementaire du scoutisme"
labelBalise = "Balises"
labelGPS = "GPS"

#Refs des pdf
pdfGuideReg = "d4d373cf-4da4-4420-9038-9956e2cac86d"
pdfBalises = "10c283bf-524c-4553-9681-83934b8c9cbd"
pdfGps = "0d7d338b-4415-4772-99f2-31a98326f5bb"

listSourceInfo = [labelGuideReg, labelGPS, labelBalise]
sourceInfo = st.multiselect("Interlocuteurs", listSourceInfo, listSourceInfo)


question = st.chat_input("Poser une question")
session = requests.Session()
session.headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
}

st.sidebar.title("Sources")


def askQuestion(question, sourceInfo):
    uuidPdf = pdfGuideReg
    if sourceInfo == labelGuideReg:
        uuidPdf = pdfGuideReg
    elif sourceInfo == labelGPS:
        uuidPdf = pdfGps
    elif sourceInfo == labelBalise:
        uuidPdf = pdfBalises

    with st.spinner(text=sourceInfo + " est en train d'écrire ..."):
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
                                    "sec-ch-ua": "\"Not/A)Brand\";v=\"99\", \"Brave\";v=\"115\", \"Chromium\";v=\"115\"",
                                    "sec-ch-ua-mobile": "?0",
                                    "sec-ch-ua-platform": "\"Windows\"",
                                    "sec-fetch-dest": "empty",
                                    "sec-fetch-mode": "cors",
                                    "sec-fetch-site": "cross-site",
                                    "sec-gpc": "1"
                                },
                                json={
                                    "collectionuuid": uuidPdf,
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
        # st.write(completeAnswer)
        with st.chat_message(sourceInfo, avatar="📖"):
            st.markdown(f"**{sourceInfo}**")
            st.write(completeAnswer)

        st.sidebar.subheader(sourceInfo)
        for i in range(min(len(answer['data']['sources']), 3)):
            source = answer['data']['sources'][i]
            with st.sidebar.expander("Page " + str(source['page_number'])):
                st.write(source['raw_chunk'])
            # st.sidebar.write(f"{source['raw_chunk']}")
            # st.sidebar.markdown(f"_Page {str(source['page_number'])}_")

    else:
        st.error("Une erreur s'est produite lors de l'appel à l'API Reeder.")


if question:
    with st.chat_message("user"):
        st.write(question)

    for source in sourceInfo:
        askQuestion(question, source)
