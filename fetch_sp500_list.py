import urllib.request
import csv
import io

def fetch_sp500_symbols():
    url = 'https://raw.githubusercontent.com/datasets/s-and-p-500-companies/main/data/constituents.csv'
    with urllib.request.urlopen(url) as response:
        csv_text = response.read().decode('utf-8')
    reader = csv.DictReader(io.StringIO(csv_text))
    symbols = [row['Symbol'] for row in reader]
    return symbols

if __name__ == "__main__":
    symbols = fetch_sp500_symbols()
    print("Total S&P 500 tickers fetched:", len(symbols))
    with open('sp500_symbols.txt', 'w') as f:
        for s in symbols:
            f.write(s + '\n')
    print("Saved to sp500_symbols.txt")
