import json
import urllib.request

url = "https://site.api.espn.com/apis/site/v2/sports/basketball/nba/news"

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