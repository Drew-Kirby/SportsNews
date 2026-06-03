import json
import urllib.request
import urllib.error

league_names = {
    "nba": "NBA", "wnba": "WNBA", "mens-college-basketball": "Men's College Basketball",
    "womens-college-basketball": "Women's College Basketball", "fiba": "FIBA",
    "nfl": "NFL", "college-football": "College Football", "mlb": "MLB", "college-baseball": "College Baseball",
    "college-softball": "College Softball", "nhl": "NHL", "mens-college-hockey": "Men's College Hockey",
    "fifa.world": "FIFA World Cup", "uefa.champions": "UEFA Champions League", "fifa.wwc": "FIFA Women's World Cup",
    "pga": "PGA Tour", "liv": "LIV Golf", "lpga": "LPGA Tour", "champions-tour": "Champions Tour",
    "f1": "F1", "nascar-premier": "NASCAR Premier"
}

valid_leagues = {
    "basketball": ["nba", "wnba", "mens-college-basketball", "womens-college-basketball", "fiba"],
    "football": ["nfl", "college-football"],
    "baseball": ["mlb", "college-baseball", "college-softball"],
    "hockey": ["nhl", "mens-college-hockey"], 
    "soccer": ["fifa.world", "uefa.champions", "fifa.wwc"], 
    "golf": ["pga", "lpga", "liv", "champions-tour"], 
    "racing": ["f1", "nascar-premier"]
}

resource_names = {
    "news": "news",
    "scores": "scoreboard",
    "standings": "standings",
    "rankings": "rankings"
}

def build_url(sport, league, api_resource):
    base_url = "https://site.api.espn.com/apis/site/v2/sports"
    if api_resource == "standings":
        return f"https://site.api.espn.com/apis/v2/sports/{sport}/{league}/standings"
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

def standings(url):
    standingsByConference = {}

    try:
        with urllib.request.urlopen(url) as response:
            if response.status == 200:
                raw_data = response.read().decode('utf-8')
                data = json.loads(raw_data)

                all_conferences = []
                for item in data.get('children', []):
                    if 'children' in item:
                        all_conferences.extend(item.get('children', []))
                    else:
                        all_conferences.append(item)

                for conference in all_conferences:
                    conf_name = conference.get('name', 'Unknown Conference')
                    standingsByConference[conf_name] = []
                    
                    standings_obj = conference.get('standings', {})
                    for entry in standings_obj.get('entries', []):
                        team_name = entry.get('team', {}).get('abbreviation', 'Unknown')
                        if not team_name:
                            continue

                        wins = '0'
                        losses = '0'

                        for stat in entry.get('stats', []):
                            if stat.get('name') == 'wins':
                                wins = stat.get('displayValue', '0')
                            elif stat.get('name') == 'losses':
                                losses = stat.get('displayValue', '0')
                        standingsByConference[conf_name].append(f"{team_name}: {wins}-{losses}")
                return standingsByConference
            else:
                print(f"Failed to retrieve data. {response.status}")
                return {}
    except urllib.error.HTTPError as e:
        print(f"HTTP Error: {e}")
        return {}
    except urllib.error.URLError as e:
        print(f"URL Error: {e}")
        return {}
    
def rankings(url):
    top25 = []

    try:
        with urllib.request.urlopen(url) as response:
            if response.status == 200:
                raw_data = response.read().decode('utf-8')
                data = json.loads(raw_data)

                rankings_list = data.get('rankings', [])
                if not rankings_list:
                    return[]

                primary_poll = rankings_list[0]
                for entry in primary_poll.get('ranks', []):
                   rank = entry.get('current', 0)
                   team_info = entry.get('team', {})
                   team_name = team_info.get('abbreviation', 'Unknown')
                   points = entry.get('points', '0')

                   top25.append(f"#{rank} {team_name} ({points} points)")
                return top25
            else:
                print(f"Failed to retrieve data. {response.status}")
                return []
    except urllib.error.HTTPError as e:
        print(f"HTTP Error: {e}")
        return []
    except urllib.error.URLError as e:
        print(f"URL Error: {e}")
        return []

def get_user_choices():
    sport = input("Enter the sport (e.g., 'basketball', 'football', 'baseball'): ").strip().lower()
    if sport not in valid_leagues:
        print("Invalid sport. Please enter a valid sport.")
        exit()

    league = input(f"Enter the league (e.g., {', '.join(valid_leagues.get(sport, []))}): ").strip().lower()
    if league not in valid_leagues.get(sport, []):
        print("Invalid league. Please enter a valid league for the selected sport.")
        exit()

    resource = input("Enter the resource (e.g., 'news', 'scores'): ").strip().lower()
    if resource not in resource_names:
        print("Invalid resource. Please enter a valid resource type.")
        exit()
    return(sport, league, resource)

def get_display_name(sport, league):
    fleague = league_names.get(league, league.upper())
    fsport = sport.capitalize()
    return f"{fleague}"
    
def explore_api(url):
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode('utf-8'))
        print(json.dumps(data, indent=2))  # Pretty-print it

if __name__ == "__main__":
    sport, league, resource = get_user_choices()

    api_resource = resource_names.get(resource)
    url = build_url(sport, league, api_resource)
    #explore_api(url)

    print(f"Fetching {get_display_name(sport, league)} {resource}...")

    if api_resource == "news":
        items = news(url)
        for item in items:
            print(item)
    elif api_resource == "scoreboard":
        items = scores(url)
        for item in items:
            print(item)
    elif api_resource == "standings":
        items=standings(url)
        for conference, teams in items.items():
            print(conference)
            sorted_teams = sorted(teams, key=lambda x: int(x.split(": ")[1].split("-")[0]), reverse=True)
            for team in sorted_teams:
                print(team)
            
    elif api_resource == "rankings":
        items = rankings(url)
        for item in items:
            print(item)
    else:
        print(f"Invalid choice: '{resource}'. Please enter a valid resource type.")