import streamlit as st


def setStyle():
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

    page_bg_img = f"""
    <style>
    [data-testid="stAppViewContainer"] > .main {{
    background-image: url("https://raw.githubusercontent.com/Vraken/superAP/master/resources/background_opaque.png");
    background-size: 50%;
    background-position: top right;
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


def getFooter():
    return """
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
    .viewerBadge_link__qRIco{
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
     <a href="mailto:superap@alwaysdata.net">superap@alwaysdata.net <img src="https://img.icons8.com/?size=512&id=jfsBIWKX4Re4&format=png" height="15" margin="1px"></a>
    </p>
    </footer>

    </div>
    """
