from pymed import PubMed
from pprint import pprint
import json
import openai

def pubMedSearch(search):
    email = "myemail@gmail.com"
    pubmed = PubMed(tool="PubMedSearcher", email=email)

    #Carries out the Search through Pubmed API
    results = pubmed.query(search, max_results=5)
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

def get_answer(question,knowledge):
    openai.api_key = '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'

    prompt = f"Answer the following question based on the knowledge I am providing. Don't answer from what you have been trained. If you can't answer from the knowledge given, tell that you don't have enough information to answer the same: {question} Knowledge: {knowledge} \nAnswer:"

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=[
            {"role": "system", "content": "You are a physicians assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message["content"].strip()

def main():
    #Take user Input
    search = input("Enter your MedGPT Query: ")
    #Search for the articles in PubMed
    articles = pubMedSearch(search)

    #Get a response from chatGPT
    response = get_answer(search, articles)
    print(response)

main()
