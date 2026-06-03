import json
import urllib.request

sport = input("Enter the sport (e.g., 'basketball', 'football', 'baseball'): ").strip().lower()

if sport != "basketball" and sport != "football" and sport != "baseball":
    print("Invalid sport. Please enter 'basketball', 'football', or 'baseball'.")

league = input("Enter the league (e.g., 'nba', 'nfl', 'mlb'): ").strip().lower()
resource = input("Enter the resource (e.g., 'news', 'scores'): ").strip().lower()

league_names = {
    "nba": "NBA",
    "nfl": "NFL",
    "mlb": "MLB",
}

def get_display_name(sport, league):
    fleague = league_names.get(league, league.upper())
    fsport = sport.capitalize()
    return f"{fleague}"

def build_url(sport, league, resource):
    base_url = "https://site.api.espn.com/apis/site/v2/sports"
    return f"{base_url}/{sport}/{league}/{resource}"

def news():
    news_url = build_url(sport, league, resource)
    with urllib.request.urlopen(news_url) as response:
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
    scores_url = build_url(sport, league, resource)
    with urllib.request.urlopen(scores_url) as response:
        if response.status == 200:
            raw_data = response.read().decode('utf-8')
            data = json.loads(raw_data)

            for event in data.get('events', []):
                competitions = event.get('competitions', [])
                if not competitions:
                    continue

                competitors = competitions[0].get('competitors', [])
                if len(competitors) >= 2:
                    team1 = competitors[0]['team'].get('abbreviation', 'Unknown')
                    score1 = competitors[0].get('score', '0')
                    
                    team2 = competitors[1]['team'].get('abbreviation', 'Unknown')
                    score2 = competitors[1].get('score', '0')
                    
                    print(f"{team1} {score1} - {team2} {score2}")
                else:
                    print("No score data available for this event.")
        else:
            print(f"Failed to retrieve data. {response.status}")

print(f"Fetching {get_display_name(sport, league)} {resource}...")

if resource == "news":
    news()
elif resource == "scores":
    resource = "scoreboard"
    scores()
else:
    print(f"Invalid choice: '{resource}'. Please enter 'news' or 'scores'.")