import json
from auth import authenticate_production

session = authenticate_production()
data = session._get('/public-watchlists')

for w in data['items']:
    if w['name'] == 'S&P 500':
        print(json.dumps(w, indent=2)[:2000])
