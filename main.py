from config import spreadsheet, range 
from google.oauth2 import service_account
from googleapiclient.discovery import build
import random


# Sheets config
credentials = service_account.Credentials.from_service_account_file("key.json", scopes=["https://www.googleapis.com/auth/spreadsheets"])
service = build("sheets", "v4", credentials=credentials)
sheet = service.spreadsheets()
result = sheet.values().get(spreadsheetId=spreadsheet, range=range).execute()
values = result.get("values", [])

# Setup research demo
roster = [v[1] for v in values]
participants = []
p1_topics = []
p2_topics = []
common_topics = []
sent_topics = []
exp_active = True

def choose_participants():
  p1_input = input("Please enter participant 1's first and last name: ")
  if p1_input not in roster:
    print("Participant not found. Please try again.")
    exit()
  p2_input = input("Please enter participant 2's first and last name name: ")
  if p2_input not in roster:
    print("Participant not found. Please try again.")
    exit()
  participants.append(p1_input)
  participants.append(p2_input)

def clean_topics(topics):
    topics = topics.split(',')
    return topics

# Extract topics 
def extract_topics(participants):
    for row in values:
       if row[1] == participants[0]:
            topics = clean_topics(row[2])
            for t in topics:
                t = t.strip()
                p1_topics.append(t)
       if row[1] == participants[1]:
            topics = clean_topics(row[2])
            for t in topics:
                t = t.strip()
                p2_topics.append(t)
              
# Build topic suggestion
def build_common_topics(p1_topics, p2_topics):
  for topic in p1_topics:
    if topic in p2_topics:
        if topic not in common_topics:
          common_topics.append(topic)

def get_topic_suggestion(common_topics):
    while True:
       topic = random.choice(common_topics)
       if topic not in sent_topics:
          break
    sent_topics.append(topic)
    body = 'Common topic: {topic}'.format(topic=topic)
    return body

def main():
    choose_participants()
    extract_topics(participants)
    build_common_topics(p1_topics, p2_topics)
    print(get_topic_suggestion(common_topics))
    while True:
       x = input('Press enter for another common topic...')
       if len(common_topics)-1 == len(sent_topics):
          print(get_topic_suggestion(common_topics))
          print("No more common topics.")
          break
       else:
          print(get_topic_suggestion(common_topics))

if __name__ == '__main__':
   main()
