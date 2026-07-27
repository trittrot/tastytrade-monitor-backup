import json
from auth import authenticate_production

session = authenticate_production()
data = session._get('/public-watchlists')

combined_symbols = set()
for w in data['items']:
    if w['name'] in ('S&P 500', 'NASDAQ 100'):
        entries = w.get('watchlist-entries', [])
        for e in entries:
            combined_symbols.add(e.get('symbol'))
        print(w['name'] + ': ' + str(len(entries)) + ' symbols')

combined_list = sorted(combined_symbols)
print()
print('Combined unique symbols: ' + str(len(combined_list)))

with open('broad_universe_symbols.txt', 'w') as f:
    for s in combined_list:
        f.write(s + '\n')
print('Saved to broad_universe_symbols.txt')
