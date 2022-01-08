import requests

#Specify a URL that resolves to your workspace
URL = "http://127.0.0.1/"



#Call each API endpoint and store the responses
response1 = requests.get('http://127.0.0.1:8000/scoring').content
response2 = requests.get('http://127.0.0.1:8000/summarystats').content
response3 = requests.get('http://127.0.0.1:8000/diagnostics').content
response4 = requests.post('http://127.0.0.1:8000/prediction?file=finaldata.csv',).content

#combine all API responses
responses = [response1, response2, response3, response4]

print(responses)
#write the responses to your workspace
with open('apireturns.txt', 'w') as f:
    for resp in responses:
        f.write(resp.decode("utf-8"))
        f.write('\n')
