import requests
import json

from bs4 import BeautifulSoup

# main URL
url = "https://examradar.com/mcqs/se-mcq-question-answers/"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
}

response = requests.get(url, headers=headers)

soup = BeautifulSoup(response.text, 'html.parser')

topics = {}
questions = []
for row in soup.find_all('article'):
    a_tag = row.find('h3').find('a')
    a_tag_content = a_tag.text
    topics[a_tag_content] = {"link": a_tag.get('href')}

for key, value in topics.items():
    new_response = requests.get(topics[key]['link'], headers=headers)
    new_soup = BeautifulSoup(new_response.text, 'html.parser')

    for row in new_soup.find_all(class_='kensFaq_listItem'):
        if "questions" not in topics[key]:
            topics[key]['questions'] = [
                {
                    "question": row.find('h4').text,
                    "options": [option.text for option in row.find_all(class_='kensFaq_questionListItem')],
                    "answer": row.find(class_='display_answer').find('span').text
                }
            ]
        else:
            topics[key]['questions'].append({
                "question": row.find('h4').text,
                "options": [option.text for option in row.find_all(class_='kensFaq_questionListItem')],
                "answer": row.find(class_='display_answer').find('span').text
            })

        questions.append({
            "question": row.find('h4').text,
            "options": [option.text for option in row.find_all(class_='kensFaq_questionListItem')],
            "answer": row.find(class_='display_answer').find('span').text
        })
    print(key)

f = open('software.json', 'w')
json.dump(topics, f)
f.close()

f = open('questions.json', 'w')
json.dump(questions, f)
f.close()