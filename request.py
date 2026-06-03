import json
import urllib.request

sport = input("Enter the sport (e.g., 'basketball', 'football', 'baseball'): ").strip().lower()
if sport != "basketball" and sport != "football" and sport != "baseball":
    print("Invalid sport. Please enter 'basketball', 'football', or 'baseball'.")
    exit()

league = input("Enter the league (e.g., 'nba', 'nfl', 'mlb'): ").strip().lower()
if league != "nba" and league != "nfl" and league != "mlb":
    print("Invalid league. Please enter 'nba', 'nfl', or 'mlb'.")
    exit()

resource = input("Enter the resource (e.g., 'news', 'scores'): ").strip().lower()
if resource != "news" and resource != "scores":
    print("Invalid resource. Please enter 'news' or 'scores'.")
    exit()

league_names = {
    "nba": "NBA",
    "nfl": "NFL",
    "mlb": "MLB",
}

def get_display_name(sport, league):
    fleague = league_names.get(league, league.upper())
    fsport = sport.capitalize()
    return f"{fleague}"

def fix_score_name(resource):
    if resource == "scores":
        return "scoreboard"
    else:
        return resource

def build_url(sport, league, api_resource):
    base_url = "https://site.api.espn.com/apis/site/v2/sports"
    return f"{base_url}/{sport}/{league}/{api_resource}"

def news(url):
    with urllib.request.urlopen(url) as response:
        if response.status == 200:
            raw_data = response.read().decode('utf-8')
            data = json.loads(raw_data)

            for article in data.get('articles', []):
                title = article.get('headline', 'No Title Available')

                title

                # author = article.get('byline', 'Unknown Author')
                
                # print(f"{title} ({author})")
                print(title)
                return title
        else:
            print(f"Failed to retrieve data. {response.status}")
    

def scores(url):
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
                    
                    print(f"{team1} {score1} - {team2} {score2}")
                else:
                    print("No score data available for this event.")
        else:
            print(f"Failed to retrieve data. {response.status}")

api_resource = fix_score_name(resource)
url = build_url(sport, league, api_resource)

print(f"Fetching {get_display_name(sport, league)} {resource}...")

items = news(url)
for item in items:
    print(item)

if api_resource == "news":
    news(url)
elif api_resource == "scoreboard":
    scores(url)
else:
    print(f"Invalid choice: '{resource}'. Please enter 'news' or 'scores'.")

# NEXT STEPS:
# 1. Return structured data from fetch functions
#    - change news(url) so it collects titles into a list and returns that list
#    - change scores(url) so it collects score items and returns them instead of printing directly
#    - this makes the functions reusable for a sidebar UI later
#
# 2. Use a small config object for valid input
#    - replace the repeated if checks with a dict like:
#      valid_leagues = {"basketball":["nba"], "football":["nfl"], "baseball":["mlb"]}
#    - translate resource names using a map like:
#      resource_map = {"news":"news", "scores":"scoreboard"}
#
# 3. Add network error handling
#    - wrap urllib.request.urlopen(url) in try/except
#    - catch urllib.error.HTTPError and urllib.error.URLError
#    - print a friendly message and return an empty list on failure
#
# 4. Separate input/selection from fetch logic
#    - keep the CLI choice code separate from the URL builder and parser
#    - later the same news(url)/scores(url) functions can be called from a sidebar UI