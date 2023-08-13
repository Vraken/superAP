import requests
import random

user_agent_list = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
]


def askDocument(docId, question):
    session = requests.Session()
    session.headers = {
        "User-Agent": random.choice(user_agent_list)
    }
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
                                "collectionuuid": str(docId),
                                "question": question
                            }
                            )
    return response
