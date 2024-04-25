from pymed import PubMed
from pprint import pprint
import json
import openai
openai.api_key = ''
def pubMedSearch(query):
    email = "myemail@gmail.com"
    pubmed = PubMed(tool="PubMedSearcher", email=email)

    #Carries out the Search through Pubmed API
    results = pubmed.query(query, max_results=5)
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
    # with open('articleInfo.json', 'w') as articles_file:
    #     json.dump(articleInfo, articles_file, indent = 4)
    
    return articleInfo

def get_query(question):

    query = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a research assistant that makes pubmed queries from user input."},
            {"role": "user", "content": f"{question}?"},
        ],
        functions=[
            {
                "name": "pubMedSearch",
                "description": "Get research documents from pubmed database matching our query",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "Query": {
                            "type": "string",
                            "description": "The query using keywords that will bring related information from pubmed database for the task asked"
                        }
                    },
                    "required": ["Query"]
                }
            }
        ]
    )

    return query['choices'][0]['message']['function_call']

def get_answer(question,knowledge):
    prompt = f"Answer the following question based on the knowledge i am providing. Dont answer from what you have been trained. if you cant answer from the knowledge given tell that you dont have enough information to answer the same: {question} Knowledge: {knowledge} \nAnswer:"
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=[
            {"role": "system", "content": "You are a research assistant that takes in data from pubmed articles and does what the user asks only using the knowledge the user provides to you. Do not use your own trained data."},
            {"role": "user", "content": f"Question: {question}  Knowledge: {knowledge}"},
        ],
    )
    
    answer = response.choices[0] if response.choices else "No answer found"
    return answer
    

def main():
    #Take user Input
    search = input("Enter your MedGPT Query: ")
    #Search for the articles in PubMed
    #Get a response from chatGPT
    response = get_query(search)
    print(response['arguments'])
    data = pubMedSearch(response['arguments'])
    answer = get_answer(search, data)
    print(answer['message']['content'])

main()
