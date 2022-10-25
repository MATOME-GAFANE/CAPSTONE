import sqlite3
from serpapi import GoogleSearch
from urllib.parse import urlsplit, parse_qsl

class Google_data:
    def __init__(self, DB_name):
        self.DB_name = DB_name
        self.citations = []
        self.api_key = ""
        self.read_api_key()
        self.api_calls_remaining = 0
        self.read_remaining_API_calls()

        # To stop the program from trying to reach Google Scholar when it can't
        self.enabled_google_comms = True

    def write_remaining_API_calls(self, write=0):
        file = open("Data/API Calls Remaining.txt", "w")
        if write == 0:
            file.write(str(self.api_calls_remaining-1))
        else:
            file.write(str(write))
        file.close()
        self.read_remaining_API_calls()

    def read_remaining_API_calls(self):
        file = open("Data/API Calls Remaining.txt", "r")
        self.api_calls_remaining = int(file.readline())
        if self.api_calls_remaining == 0:
            self.get_new_api_key()
            self.write_remaining_API_calls(100)
        file.close()

    def read_api_key(self):
        file = open("Data/API Keys.txt", "r")
        self.api_key = str(file.readline())
        file.close()

    def get_new_api_key(self):
        # If error occurs then there are no more API keys or its file has been corrupted, or is missing.
        # Either way, Google Scholar can't be reached. Thus, communication gets disabled.
        try:
            with open('Data/API Keys.txt', 'r') as fin:
                data = fin.read().splitlines(True)
            with open('Data/API Keys.txt', 'w') as fout:
                fout.writelines(data[1:])
            self.read_api_key()
        except:
            print("Could not get new api key!")
            self.enabled_google_comms = False
            return -1
        return 0

    def check_Google_enable(self):
        return self.enabled_google_comms

    def find_best_fit(self, query, initials, surname, institution, primary_research, secondary_research,
                      specializations):
        best_fit = None
        maxim = 0
        primary_fields = primary_research.split(";")
        secondary_fields = secondary_research.split(";")
        specs = specializations.split(";")
        profiles = self.get_profiles(query)
        for profile in profiles:
            hits = 0

            # Some attributes are more important than others
            if surname in profile.get("name"):
                hits += 1000

            names = profile.get("name").split(" ")
            for i in range(len(names)):
                if names[i][0] == initials:
                    hits += 100

            if institution in profile.get("affiliations"):
                hits += 10

            for i in range(len(primary_fields)):
                if profile.get("interests") is not None:
                    for interest in profile.get("interests"):
                        if primary_fields[i].lower().strip() == interest.get("title").lower().strip():
                            hits += 5

            for i in range(len(secondary_fields)):
                if profile.get("interests") is not None:
                    for interest in profile.get("interests"):
                        if secondary_fields[i].lower().strip() == interest.get("title").lower().strip():
                            hits += 5

            for i in range(len(specs)):
                if profile.get("interests") is not None:
                    for interest in profile.get("interests"):
                        if specs[i].lower().strip() == interest.get("title").lower().strip():
                            hits += 5

            if hits > maxim:
                best_fit = profile
                maxim = hits
        return best_fit, maxim  # Maxim: Maximum and is used to measure the degree of certainty.

    def get_profiles(self, search_query):
        if self.enabled_google_comms:
            params = {
                "api_key": self.api_key,
                "engine": "google_scholar_profiles",  # profile results search engine
                "mauthors": search_query  # search query
            }
            search = GoogleSearch(params)
            self.write_remaining_API_calls()
            profile_results_data = []
            profiles_is_present = True
            while profiles_is_present:
                profile_results = search.get_dict()
                for profile in profile_results.get("profiles", []):
                    name = profile.get("name")
                    author_id = profile.get("author_id")
                    affiliations = profile.get("affiliations")
                    interests = profile.get("interests")
                    profile_results_data.append({
                        "name": name,
                        "author_id": author_id,
                        "affiliations": affiliations,
                        "interests": interests
                    })

                if "next" in profile_results.get("pagination", []):
                    search.params_dict.update(
                        dict(parse_qsl(urlsplit(profile_results.get("pagination").get("next")).query)))
                else:
                    profiles_is_present = False
            return profile_results_data

    def author_results(self, author_id):
        if not self.enabled_google_comms:
            author_results_data = []
            params = {
                "api_key": self.api_key,      # SerpApi API key
                "engine": "google_scholar_author",    # author results search engine
                "author_id": author_id,  # search query
                "hl": "en"
            }
            search = GoogleSearch(params)
            self.write_remaining_API_calls()
            results = search.get_dict()

            if results is not None:
                name = results.get("author").get("name")
                affiliations = results.get("author").get("affiliations")
                interests = results.get("author").get("interests")
                cited_by_graph = results.get("cited_by", {}).get("graph")
                total_citations = results.get("cited_by", {}).get("table")[0].get("citations").get("all")
                co_authors = results.get("co_authors")
                author_results_data.append({
                    "name": name,
                    "affiliations": affiliations,
                    "interests": interests,
                    "cited_by_graph": cited_by_graph,
                    "co_authors": co_authors,
                    "total_citations" : total_citations

                })
            else:
                author_results_data.append({
                    "name": "",
                    "affiliations": "",
                    "interests": "",
                    "cited_by_graph": "",
                    "co_authors": "",
                    "total_citations": ""

                })

            return author_results_data
        return None

    def all_author_articles(self, author_id):
        if not self.enabled_google_comms:
            author_article_results_data = []
            params = {
                "api_key": self.api_key,     # SerpApi API key
                "engine": "google_scholar_author",   # author results search engine
                "hl": "en",                          # language
                "sort": "pubdate",                   # sort by year
                "author_id": author_id  # search query
            }
            search = GoogleSearch(params)
            self.write_remaining_API_calls()
            articles_is_present = True
            while articles_is_present:
                results = search.get_dict()
                for article in results.get("articles", []):
                    title = article.get("title")
                    authors = article.get("authors")
                    publication = article.get("publication")
                    cited_by_value = article.get("cited_by", {}).get("value")
                    year = article.get("year")
                    author_article_results_data.append({
                        "article_title": title,
                        "article_year": year,
                        "article_authors": authors,
                        "article_publication": publication,
                        "article_cited_by_value": cited_by_value,
                        })
                if "next" in results.get("serpapi_pagination", []):
                    search.params_dict.update(dict(parse_qsl(urlsplit(results.get("serpapi_pagination").
                                                                      get("next")).query)))
                else:
                    articles_is_present = False
            return author_article_results_data
        return None

    def get_citations(self):
        return self.citations

    def populate_citations(self):
        try:
            temp_citations = []
            conn = sqlite3.connect(self.DB_name)
            cursor = conn.cursor()
            cursor.execute("SELECT author_id from Researcher_IDS")
            author_ids = cursor.fetchall()
            for author_id in author_ids:

                if author_id is not None:
                    result_dictionary = self.author_results(author_id[0])
                    temp_citations.append({"author_id" : author_id,
                                           "citations": result_dictionary[0].get("total_citations"),
                                           "cited_by_graph" : result_dictionary[0].get("cited_by_graph")})
                else :
                    temp_citations.append({"author_id" : "",
                                           "citations": 0,
                                           "cited_by_graph" : {}})

                self.citations = temp_citations
        except:
            print("Couldn't populate citations")

    def populate_user_ids(self):
        try:
            conn = sqlite3.connect(self.DB_name)
            cursor = conn.cursor()

            cursor.execute("Drop table if exists Researchers_IDS")
            cursor.execute("CREATE TABLE IF NOT EXISTS Researchers_IDS (ID Primary key, Author_ID)")
            cursor.execute("Select id ,initials, surname, institution, primaryResearch, secondaryResearch,"
                           " specializations from researchers")
            conn.commit()
            rows = cursor.fetchall()

            profiles = []
            for row in rows:
                search_query = row[1][0] + " " + row[2]
                profiles.append(self.find_best_fit(search_query, row[1], row[2], row[3], row[4], row[5], row[6]))

            for i in range(len(rows)):
                query = "Insert into Researchers_IDS (author_id, id) values (?,?)"

                if profiles[i][0] is not None:
                    print(profiles[i][0].get("author_id"))
                    cursor.execute(query, (profiles[i][0].get("author_id"), rows[i][0]))
                else:
                    cursor.execute(query, ("", rows[0]))
            conn.commit()
            conn.close()
        except:
            print("Couldn't populate user ids")
