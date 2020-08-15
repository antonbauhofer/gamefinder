# Import libraries
import streamlit as st
import pandas as pd
from plotly import graph_objs as go
import random


def main():
    """ Gamefinder App """

    # ----- STYLING
    hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        </style>
    """
    st.markdown(hide_menu_style, unsafe_allow_html=True)

    # ----- FUNCTIONS

    # Import data
    @st.cache
    def load_data(url):
        data = pd.read_excel(url)
        return data

    # Sort data by distance to input
    def nearest(bew_d, koo_d, gru_d, bue_d, nam_d):
        games_sort = games.assign(g=(games['Bewegung'] - bew_d) ** 2 + (games['Koordination'] - koo_d) ** 2 +
                                    (games['Gruppendynamik'] - gru_d) ** 2 + (games['Buehnenpraesenz'] - bue_d) ** 2 +
                                    (games['Namen'] - nam_d) ** 2).sort_values('g').drop('g', axis=1)
        return games_sort.index

        # Create polar plot

    def polar(entry_id):
        polar_fig = go.Figure(
            data=[dict(type='scatterpolar',
                       r=list(games.iloc[entry_id, 4:9]),
                       theta=['Bewegung', 'Koordination', 'Gruppendynamik', 'Bühnenpräsenz', 'Namen'],
                       fill='toself')],
            layout=dict()
        )
        st.plotly_chart(polar_fig)

    # Create bar chart
    def bar(entry_id):
        bar_fig = go.Figure(go.Bar(
            x=games.iloc[entry_id, 8:3:-1],
            y=['Namen lernen', 'Bühnenpräsenz', 'Gruppendynamik', 'Koordination', 'Bewegung'],
            orientation='h',
            marker=dict(
                color=['rgba(38, 24, 74, 0.8)', 'rgba(71, 58, 131, 0.8)',
                       'rgba(122, 120, 168, 0.8)', 'rgba(164, 163, 204, 0.85)',
                       'rgba(190, 192, 213, 1)']
            )))

        bar_fig.update_layout(
            xaxis=dict(
                showgrid=False,
                showline=False,
                showticklabels=False,
                zeroline=True,
            ),
            yaxis=dict(
                showgrid=False,
                showline=True,
                showticklabels=True,
                zeroline=True,
            ),
            paper_bgcolor='white',
            plot_bgcolor='white',
            margin=dict(l=0, r=0, t=0, b=0),
            showlegend=False,
            height=80,
        )

        bar_fig.update_xaxes(range=[0, 10])

        #        st.plotly_chart(bar_fig, height=80, width=300, config=dict(displayModeBar=False, staticPlot=True))
        st.plotly_chart(bar_fig, config=dict(displayModeBar=False,
                                                        staticPlot=True,
                                                        scrollZoom=False,
                                                        editable=False))

    # ----- LOAD DATA

    games = load_data('https://raw.githubusercontent.com/bauhofer/data/master/games.xlsx')

    # ----- INTRO

    st.title("Der interaktive Spielegenerator")

    st.markdown(
        """<div style="color:grey;">Bewege die Slider im Seitenmenü links und entdecke neue Aufwärmspiele.</div>""",
        True)
    st.markdown(" ----- ")

    # ----- USER INPUTS

    st.sidebar.markdown(
        "Starte den Zufallsgenerator oder bewege die Slider um die Auswahl der angezeigten Spiele anzupassen.")

    # Initialize sliders
    slider_default = 5

    # Zufallsgenerator
    if st.sidebar.button('Zufallsgenerator'):
        random_var = True
    else:
        random_var = False

        # Attribut Auswahl
    if random_var:
        bew_sl = st.sidebar.slider('Bewegung', 0, 10, random.randrange(0, 11, 1), 1)
        koo_sl = st.sidebar.slider('Koordination', 0, 10, random.randrange(0, 11, 1), 1)
        gru_sl = st.sidebar.slider('Gruppendynamik', 0, 10, random.randrange(0, 11, 1), 1)
        bue_sl = st.sidebar.slider('Bühnenpräsenz', 0, 10, random.randrange(0, 11, 1), 1)
        nam_sl = st.sidebar.slider('Namen Lernen', 0, 10, random.randrange(0, 11, 1), 1)
    else:
        bew_sl = st.sidebar.slider('Bewegung', 0, 10, slider_default, 1)
        koo_sl = st.sidebar.slider('Koordination', 0, 10, slider_default, 1)
        gru_sl = st.sidebar.slider('Gruppendynamik', 0, 10, slider_default, 1)
        bue_sl = st.sidebar.slider('Bühnenpräsenz', 0, 10, slider_default, 1)
        nam_sl = st.sidebar.slider('Namen Lernen', 0, 10, slider_default, 1)

    # OPTION: Drop-down Menü für Anzahl der angezeigten Ergebnisse
    #    game_num_sl = st.sidebar.selectbox("Anzahl der dargestellten Ergebnisse", ("1", "2", "3", "4", "5"), 2)
    #    if game_num_sl == '1':
    #        game_num =1
    #    if game_num_sl == '2':
    #        game_num =2
    #    if game_num_sl == '3':
    #        game_num =3
    #    if game_num_sl == '4':
    #        game_num =4
    #    if game_num_sl == '5':
    #        game_num =5

    game_num_in = st.sidebar.number_input('Anzahl der angezeigten Spiele:',
                                          min_value=0, max_value=games.shape[0], value=3)
    game_num = game_num_in

    # Impressum
    impressum = False
    if st.sidebar.checkbox("Impressum anzeigen", False):
        impressum = True

    #    # OPTION: Spielerklärungen verstecken
    #    if st.sidebar.checkbox("Spielerklärungen verstecken", False):
    #        descriptions = False
    #    else:
    #        descriptions = True

    # ----- OUTPUTS

    # Find closes entries
    order = nearest(bew_sl, koo_sl, gru_sl, bue_sl, nam_sl)

    # Print games
    for i in range(0, game_num):
        st.subheader(games.iloc[order[i], 0])
        bar(order[i])
        st.markdown('Kategorie: ' + games.iloc[order[i], 2] + ', Hilfsmittel: ' + games.iloc[order[i], 3])
        #        st.markdown('<div style="font-weight:450; font-size:small">Kategorie: </div>' + '<div style="font-size:small">' + str(games.iloc[order[i], 2]) + '</div>' + 'Test', True)
        st.markdown(games.iloc[order[i], 1])
        if not games.isna().iloc[order[i], 9]:
            if st.checkbox("Varianten anzeigen", False, key=i):
                st.markdown('Variante 1: ' + games.iloc[order[i], 9])
                if not games.isna().iloc[order[i], 10]:
                    st.markdown('Variante 2: ' + games.iloc[order[i], 10])
                if not games.isna().iloc[order[i], 11]:
                    st.markdown('Variante 3: ' + games.iloc[order[i], 11])
        #                if not games.isna().iloc[order[i], 12]:
        #                    st.markdown('Variante 4: ' + games.iloc[order[i], 12])

        st.markdown(" ----- ")
    if bew_sl == slider_default and koo_sl == slider_default and gru_sl == slider_default and bue_sl == slider_default and nam_sl == slider_default:
        st.markdown(
            """<div style="color:grey;">Bewege die Slider im Seitenmenü links und entdecke neue Aufwärmspiele.</div>""",
            True)

    #        # OPTION: Checkbox for Radar Plot
    #        if st.checkbox("Attribute anzeigen", False, i):
    #            polar(order[i])

    # ----- FOOTER

    if impressum:
        st.markdown(" ----- ")
        st.markdown("""<div style="color:grey;">Impressum.</div>""", True)
        #        st.markdown("""<div style="color:grey;">Der Author der Seite übernimmt keine Haftung für die gezeigten Inhalte.</div>""", True)
        st.markdown(
            """<div style="color:grey;">Verantwortlicher: Anton Bauhofer, Trakehner Platz 2, 81929 München, Germany. T: +49 (0) 178 1033054. E: antonbauhofer@gmail.com</div>""",
            True)
        st.markdown(
            """<div style="color:grey;">1. Inhalt des Onlineangebots: Der Autor übernimmt keinerlei Gewähr für die Aktualität, Korrektheit, Vollständigkeit oder Qualität der bereitgestellten Informationen. Haftungsan-sprüche gegen den Autor, welche sich auf Schäden materieller oder ideeller Art beziehen, die durch die Nutzung oder Nichtnutzung der dargebotenen Informationen bzw. durch die Nutzung fehlerhafter und unvollständiger Informationen verursacht wurden, sind grundsätzlich ausgeschlossen, sofern seitens des Autors kein nachweislich vorsätzliches oder grob fahrlässiges Verschulden vorliegt. Alle Angebote sind freibleibend und unverbindlich. Der Autor behält es sich ausdrücklich vor, Teile der Seiten oder das gesamte Angebot ohne gesonderte Ankündigung zu verändern, zu ergänzen, zu löschen oder die Veröffentlichung zeitweise oder endgültig einzustellen.</div>""",
            True)
        st.markdown(
            """<div style="color:grey;">2. Verweise und Links: Bei direkten oder indirekten Verweisen auf fremde Webseiten (“Hyperlinks”), die außerhalb des Verantwortungsbereichs des Autors liegen, würde eine Haftungsverpflichtung ausschließlich in dem Fall in Kraft treten, in dem der Autor von den Inhalten Kenntnis hat und es ihm technisch möglich und zumutbar wäre, die Nutzung im Falle rechtswidriger Inhalte zu verhindern.Der Autor erklärt hiermit ausdrücklich, dass zum Zeitpunkt der Linksetzung keine illegalen Inhalte auf den zu verlinkenden Seiten erkennbar waren. Auf die aktuelle und zukünftige Gestaltung, die Inhalte oder die Urheberschaft der verlinkten/verknüpften Seiten hat der Autor keinerlei Einfluss. Deshalb distanziert er sich hiermit ausdrücklich von allen Inhalten aller verlinkten /verknüpften Seiten, die nach der Linksetzung verändert wurden. Diese Feststellung gilt für alle innerhalb des eigenen Internetangebotes gesetzten Links und Verweise sowie für Fremdeinträge in vom Autor eingerichteten Gästebüchern, Diskussionsforen, Linkverzeichnissen, Mailinglisten und in allen anderen Formen von Datenbanken, auf deren Inhalt externe Schreibzugriffe möglich sind.Für illegale, fehlerhafte oder unvollständige Inhalte und insbesondere für Schäden, die aus der Nutzung oder Nichtnutzung solcherart dargebotener Informationen entstehen, haftet allein der Anbieter der Seite, auf welche verwiesen wurde, nicht derjenige, der über Links auf die jeweilige Veröffentlichung lediglich verweist.</div>""",
            True)
        st.markdown(
            """<div style="color:grey;">3. Urheber und Kennzeichnugsrecht: Der Autor ist bestrebt, in allen Publikationen die Urheberrechte der verwendeten Grafiken, Tondokumente, Videosequenzen und Texte zu beachten, von ihm selbst erstellte Grafiken, Tondokumente, Videosequenzen und Texte zu nutzen oder auf lizenzfreie Grafiken, Tondokumente, Videosequenzen und Texte zurückzugreifen. Alle innerhalb des Internetangebotes genannten und ggf. durch Dritte geschützten Marken- und Warenzeichen unterliegen uneingeschränkt den Bestimmungen des jeweils gültigen Kennzeichenrechts und den Besitzrechten der jeweiligen eingetragenen Eigentümers. Allein aufgrund der bloßen Nennung ist nicht der Schluss zu ziehen, dass Markenzeichen nicht durch Rechte Dritter geschützt sind! Das Copyright für veröffentlichte, vom Autor selbst erstellte Objekte bleibt allein beim Autor der Seiten. Eine Vervielfältigung oder Verwendung solcher Grafiken, Ton-dokumente, Videosequenzen und Texte in anderen elektronischen oder gedruckten Publikationen ist ohne ausdrückliche Zustimmung des Autors nicht gestattet.</div>""",
            True)
        st.markdown(
            """<div style="color:grey;">4. Datenschutz: Sofern innerhalb des Internetangebotes die Möglichkeit zur Eingabe persönlicher oder geschäftlicher Daten (Emailadressen, Namen, Anschriften) besteht, so erfolgt die Preisgabe dieser Daten seitens des Nutzers auf ausdrücklich freiwilliger Basis. Die Inanspruchnahme und Be-zahlung aller angebotenen Dienste ist – soweit technisch möglich und zumutbar – auch ohne Angabe solcher Daten bzw. unter Angabe anonymisierter Daten oder eines Pseudonyms gestattet. Die Nutzung der im Rahmen des Impressums oder vergleichbarer Angaben veröffentlichten Kontaktdaten wie Postanschriften, Telefon- und Faxnummern sowie Emailadressen durch Dritte zur Übersendung von nicht ausdrücklich angeforderten Informationen ist nicht gestattet. Rechtliche Schritte in jeglicher juristischer Art gegen die Versender von sogenannten Spam-Mails bei Verstössen gegen dieses Verbot sind und bleiben ausdrücklich vorbehalten.</div>""",
            True)
        st.markdown(
            """<div style="color:grey;">5. Rechtswirksamkeit und Haftungsausschluss: Dieser Haftungsausschluss ist als Teil des Internetangebotes zu betrachten, von dem aus auf diese Seite verwiesen wurde. Sofern Teile oder einzelne Formulierungen dieses Textes der geltenden Rechtslage nicht, nicht mehr oder nicht vollständig entsprechen sollten, bleiben die übrigen Teile des Dokumentes in ihrem Inhalt und ihrer Gültigkeit davon unberührt.</div>""",
            True)


if __name__ == '__main__':
    main()
