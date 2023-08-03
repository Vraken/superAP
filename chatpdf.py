import streamlit as st
import requests

st.title("Super AP")

# sourceInfo = st.selectbox("Source d'info", ("Tous", "Guide_reg", "GPS"))
listSourceInfo = ["Guide_reg", "GPS"]
sourceInfo = st.selectbox("Source d'info", (listSourceInfo+["Tous"]))

pdfGuideReg = "d4d373cf-4da4-4420-9038-9956e2cac86d"
pdfBalises = "10c283bf-524c-4553-9681-83934b8c9cbd"


question = st.text_input("Posez une question :")
session = requests.Session()
session.headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
}


def askQuestion(question, sourceInfo):
    uuidPdf = pdfGuideReg
    if sourceInfo == "Guide_reg":
        uuidPdf = pdfGuideReg
    elif sourceInfo == "GPS":
        uuidPdf = pdfBalises

    history.append(question)
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
    # Afficher la réponse
    if response.status_code == 200:
        answer = response.json()
        st.sidebar.write(question)
        st.markdown("---")
        st.subheader("Source : "+sourceInfo)
        st.write(answer['data']['answer'])
        # with st.expander("Sources"):
        for i in range(min(len(answer['data']['sources']), 3)):
            source = answer['data']['sources'][i]
            with st.expander("Page " + str(source['page_number'])):
                st.write(source['raw_chunk'])

    else:
        st.error("Une erreur s'est produite lors de l'appel à l'API Reeder.")


if question:
    if sourceInfo == "Tous":
        askQuestion(question, "Guide_reg")
        askQuestion(question, "GPS")
    else:
        askQuestion(question, sourceInfo)

