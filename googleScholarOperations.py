import random
from ast import literal_eval

import requests


def validate_enrich_query(querytype, query):
    
    if querytype == 'Researchers':
        query = 'author:' + query
    return query

def query_url(query):
    url = "https://serpapi.com/search?engine=google_scholar&q=" + query + "&apikey=cb34ab2c9bfb16e1e30db561d8a0cfc62643bddd40834a87e2321c67a4fd2a2b"
    payload = {}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    # print(response.text)
    return response


def handle_query(querytype,query):
    query=validate_enrich_query(querytype,query)
    results = literal_eval(query_url(query).text)
    # print(querytype)
    m = f"<table> <caption>Search Results</caption><th>Number</th><th>Title of the Paper</th><th>Author</th> <th>Institution</th>"
    # print(len(response['response']['docs']))
    r = 1;
    for searchResult in results['organic_results']:
        title = str(searchResult['title'])
        authors=" "
        if(querytype=='Researchers'):
            authors=querytype
        for attribute in searchResult['publication_info']:
            if attribute == 'authors':
                authors_list=[]
                for x in searchResult['publication_info']['authors']:
                    authors_list.append(x['name'])
                #print(type(searchResult['publication_info']['authors']))
                authors = str(authors_list)
        
        if (querytype == 'Institutions'):
            instution = querytype
        m = m + f"<tr><td style=\"background-color:#DC143C;\">{r}</td> <td style=\"background-color:powderblue;\">{title} </td> <td style=\"background-color:#42DBDE;\">{authors}</td> </td>  </tr>"
        r += 1
    m += "</table>"

    # print(m)
    return f"<p>{m}</p>"