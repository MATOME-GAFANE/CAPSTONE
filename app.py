# AI researchers are based at South Africa’s
# 26 public universities and other research-based organisations. They publish the results of their research in
# a variety of venues, including journals, conference proceedings and workshop proceedings. The
# application will draw from and consolidate data from multiple public research data sources, including the
# researcher rating system used by the National Research Foundation (NRF) and Microsoft Academic
# Graph (MAG). A web based interface must be provided for users to perform queries and visualise
# information about the research community including: a) dominant research areas/topics, publications
# venues, collaborations (co-authors) and impact (citations) (b) in which
# researchers are based (c) finding interesting trends and patterns over time, (c) appropriate metrics to
# assess and analyse the community and network structure, and (d) manual update and synchronisation
# functionality with MAG, the NRF and other public data sources.
from flask import Flask, render_template, request

from Google_data import Google_data
from Webpage_builder import Webpage_builder
from googleScholarOperations import handle_query
from test import notdash

app = Flask(__name__)


@app.route("/", methods=["POST", "GET"])
def index():
    return pages.homepage()


@app.route("/callback_topics_data", methods=["GET"])
def topics_data():
    return pages.graph_callback()

@app.route("/trendsAndAnalysis", methods=["GET"])
def trendsAndAnalysis():
    return pages.TrendsAndAnalysis_page()
@app.route("/publications", methods=["POST", "GET"])
def publications():
    return pages.publications_page()


@app.route("/researchers", methods=["GET"])
def researchers():
    return pages.researchers_page()

@app.route("/institutions", methods=["GET"])
def institutions():
    return pages.institutions_page()

@app.route("/inst_<institution>")
def render_institution(institution):
    return pages.render_institution_page(institution)

@app.route("/researcher_<RID>")
def render_researcher(RID):
    return pages.render_researcher_page(RID)

@app.route("/search_results")
def search_researchers():
    return pages.search_researchers()

@app.route("/inst_search_results")
def search_Institutions():
    return pages.search_institutions(request.method, request.args.get("Institution_search"))

@app.route("/publications")
def publications_page(self):
        if request.method == "POST":
            query = request.form["query"]
            queryType = request.form.get('Querytype')
            handle_query(queryType, query)
            return handle_query(queryType, query)

        return render_template("publications.html")

@app.route("/Citations")
def Ciations():
   return render_template('TrendsAndAnalysisGoogle.html', graphJSON=notdash( ))

@app.route("/about")
def About():
   return render_template('about.html')


if __name__ == '__main__':
    google_Data = Google_data("Data/Database.db")

    pages = Webpage_builder(google_Data)
    app.run(debug=True)
