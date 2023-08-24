from pymed import PubMed
from pprint import pprint
import json

def pubMedSearch(search):
    email = "myemail@gmail.com"
    pubmed = PubMed(tool="PubMedSearcher", email=email)

    #Carries out the Search through Pubmed API
    results = pubmed.query(search, max_results=30)
    articleList = []
    articleInfo = []

    for article in results:
    # Print the type of object we've found (can be either PubMedBookArticle or PubMedArticle).
    # We need to convert it to dictionary with available function
        articleDict = article.toDict()
        articleList.append(articleDict)

    # Generate list of dict records which will hold all article details that could be fetch from PUBMED API
    for article in articleList:
    #Sometimes article['pubmed_id'] contains list separated with comma - take first pubmedId in that list - thats article pubmedId
        pubmedId = article['pubmed_id'].partition('\n')[0]
        # Append article info to dictionary
        articleInfo.append({u'pubmed_id':pubmedId,
                        u'title':article['title'],
                        u'abstract':article['abstract'],
                        u'conclusions':article['conclusions'],
                        u'results': article['results'],
                    })
    #print articleInfo to a json file for ease of viewing
    with open('articleInfo.json', 'w') as articles_file:
        json.dump(articleInfo, articles_file, indent = 4)
    
    return articleInfo

