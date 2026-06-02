import json
import urllib.request

userin = input("Enter 'news' for news or 'scores' for scores: ")

def news():
    url = (f"https://site.api.espn.com/apis/site/v2/sports/basketball/nba/news")
    with urllib.request.urlopen(url) as response:
        if response.status == 200:
            raw_data = response.read().decode('utf-8')
            data = json.loads(raw_data)

            for article in data.get('articles', []):
                title = article.get('headline', 'No Title Available')

                # author = article.get('byline', 'Unknown Author')
                
                # print(f"{title} ({author})")
                
                print(title)
        else:
            print(f"Failed to retrieve data. {response.status}")

def scores():
    scores_url = f"https://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard"
    with urllib.request.urlopen(scores_url) as response:
        if response.status == 200:
            raw_data = response.read().decode('utf-8')
            data = json.loads(raw_data)

            for event in data.get('events', []):
                competitors = event.get('competitors', [])
                
                if len(competitors) >= 2:
                    team1 = competitors[0]['team'].get('abbreviation', 'Unknown')
                    score1 = competitors[0].get('score', '0')
                    
                    team2 = competitors[1]['team'].get('abbreviation', 'Unknown')
                    score2 = competitors[1].get('score', '0')
                    
                    print(f"{team1} {score1} - {team2} {score2}")
        else:
            print(f"Failed to retrieve data. {response.status}")

user_choice = userin.strip().lower()

if user_choice == "news":
    news()
elif user_choice == "scores":
    scores()
else:
    print(f"Invalid choice: '{user_choice}'. Please enter 'news' or 'scores'.")

