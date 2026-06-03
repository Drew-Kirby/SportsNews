import json
import urllib.request
import urllib.error

league_names = {
    "nba": "NBA",
    "nfl": "NFL",
    "mlb": "MLB",
}

valid_leagues = {
    "basketball": ["nba"],
    "football": ["nfl"],
    "baseball": ["mlb"]
}

resource_names = {
    "news": "news",
    "scores": "scoreboard"
}

sport = input("Enter the sport (e.g., 'basketball', 'football', 'baseball'): ").strip().lower()
if sport not in valid_leagues:
    print("Invalid sport. Please enter 'basketball', 'football', or 'baseball'.")
    exit()

league = input("Enter the league (e.g., 'nba', 'nfl', 'mlb'): ").strip().lower()
if league not in valid_leagues.get(sport, []):
    print("Invalid league. Please enter 'nba', 'nfl', or 'mlb'.")
    exit()

resource = input("Enter the resource (e.g., 'news', 'scores'): ").strip().lower()
if resource not in resource_names:
    print("Invalid resource. Please enter 'news' or 'scores'.")
    exit()

def get_display_name(sport, league):
    fleague = league_names.get(league, league.upper())
    fsport = sport.capitalize()
    return f"{fleague}"

def build_url(sport, league, api_resource):
    base_url = "https://site.api.espn.com/apis/site/v2/sports"
    return f"{base_url}/{sport}/{league}/{api_resource}"

def news(url):
    titles = []

    try:
        with urllib.request.urlopen(url) as response:
            if response.status == 200:
                raw_data = response.read().decode('utf-8')
                data = json.loads(raw_data)

                for article in data.get('articles', []):
                    title = article.get('headline', 'No Title Available')

                    titles.append(title)

                    # author = article.get('byline', 'Unknown Author')
                    
                    # print(f"{title} ({author})")
                return titles
            else:
                print(f"Failed to retrieve data. {response.status}")
                return []
    except urllib.error.HTTPError as e:
        print(f"HTTP Error: {e}")
        return []
    except urllib.error.URLError as e:
        print(f"URL Error: {e}")
        return []

def scores(url):
    scoresList = []

    try:
        with urllib.request.urlopen(url) as response:
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
                        
                        scoresList.append(f"{team1} {score1} - {team2} {score2}")
                    else:
                        print("No score data available for this event.")
                return scoresList    
            else:
                print(f"Failed to retrieve data. {response.status}")
                return []
    except urllib.error.HTTPError as e:
        print(f"HTTP Error: {e}")
        return []
    except urllib.error.URLError as e:
        print(f"URL Error: {e}")
        return []

api_resource = resource_names.get(resource)
url = build_url(sport, league, api_resource)

print(f"Fetching {get_display_name(sport, league)} {resource}...")

if api_resource == "news":
    items = news(url)
    for item in items:
        print(item)
elif api_resource == "scoreboard":
    items = scores(url)
    for item in items:
        print(item)
else:
    print(f"Invalid choice: '{resource}'. Please enter 'news' or 'scores'.")

# NEXT STEPS:
# 4. Separate input/selection from fetch logic
#    - keep the CLI choice code separate from the URL builder and parser
#    - later the same news(url)/scores(url) functions can be called from a sidebar UI