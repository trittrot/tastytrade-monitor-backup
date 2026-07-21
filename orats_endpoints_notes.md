# ORATS API Endpoint Reference Notes

Testing conducted on Delayed Data API ($99/mo tier), token stored in Secret Manager as orats-api-token.
Test scripts on VM: test_orats_*.py

## 1. Tickers - VERIFIED WORKING
GET /datav2/tickers
- Returns min/max available tradeDate for a ticker
- SPY: data available 2007-01-03 through 2026-06-16
- Note: max date lags about 1 month behind actual latest data

## 2. Strikes - VERIFIED WORKING
GET /datav2/strikes
- Full current option chain, filterable by dte and delta
- Tested SPY dte 40-50 delta .15-.30, returned real strikes with live bid/ask

## 3. Strikes History - VERIFIED WORKING
GET /datav2/hist/strikes
- Historical chain for a specific tradeDate
- Tested SPY on 2024-08-05, showed extreme put premiums that day

## 4. Strikes by Options - VERIFIED WORKING
GET /datav2/strikes/options
- Query by exact OCC option symbol or underlying ticker
- Tested SPY underlying, returned live stock quote

## 5. Strikes History by Options - VERIFIED WORKING, needs precise tradeDate param
GET /datav2/hist/strikes/options
- Must explicitly pass tradeDate or it defaults to something unexpected like expiry date

## 6. Monies Implied - VERIFIED WORKING
GET /datav2/monies/implied
- Smoothed IV at multiple deltas across expirations

## 7. Monies History - VERIFIED WORKING
GET /datav2/hist/monies/implied
- Tested SPY on 2024-08-05, near term IV was extremely elevated

## 8. SMV Summaries - VERIFIED WORKING
GET /datav2/summaries
- Tested SPY live, contango 0.3 confirmed present

## 9. Summaries History - VERIFIED WORKING
GET /datav2/hist/summaries
- Tested SPY on 2024-08-05, contango was -1.40, deep backwardation
- slope field not present here, only skewing - slope likely lives on Core Data only

## 10. Core Data - VERIFIED WORKING
GET /datav2/cores
- Large field set including contango slope slopepctile mktWidthVol ivPctile
- Tested SPY live, contango 0.24 to 0.25

Still to test: Core Data History, Daily Price, Historical Volatility, Dividend History, Earnings History, Stock Split History, IV Rank, IV Rank History

General lessons: always pass tradeDate explicitly for historical queries, verify fields per endpoint rather than assuming they are shared, 15 minute delay is fine for EOD workflows, requests used so far are a tiny fraction of the 20000 monthly budget


## 14. Dividend History - FAILED (403 Forbidden)
GET /datav2/hist/divs
- Tested: SPY - received HTTP 403
- Response body: "User is not authorized to access this resource with an explicit deny in an identity-based policy"
- IMPORTANT: docs.orats.io lists this endpoint with no tier restriction noted, formatted identically to other working endpoints (Strikes, Monies, Summaries, etc)
- This appears to be a genuine discrepancy between documentation and actual account permissions
- ACTION NEEDED: email support@orats.com quoting this exact error and asking them to confirm access or fix the account


## 15. Earnings History - VERIFIED WORKING
GET /datav2/hist/earnings
- Tested AAPL, returned full earnings date history through 2026-04-30 with exact announcement time of day
- Useful for avoiding accidental earnings related IV crush when scanning candidates

## 16. Stock Split History - VERIFIED WORKING
GET /datav2/hist/splits
- Tested AAPL, correctly returned both known splits, 7 for 1 in 2014 and 4 for 1 in 2020

## 17. IV Rank - VERIFIED WORKING
GET /datav2/ivrank
- Tested SPY current: iv 14.33, ivRank1m 56.19, ivPct1m 70, ivRank1y 22.41, ivPct1y 56.57
- Useful for judging whether current conditions are rich or cheap for selling premium

## 18. IV Rank History - VERIFIED WORKING
GET /datav2/hist/ivrank
- Tested SPY on 2024-08-05: iv 26.999, ivRank1m 100, ivPct1m 100, ivRank1y 100, ivPct1y 100
- Every single IV rank measure hit maximum 100 on the near miss day

FULL WALKTHROUGH COMPLETE - 18 of 18 endpoints tested
17 endpoints VERIFIED WORKING
1 endpoint FAILED - Dividend History endpoint 14, genuine 403 explicit deny, contradicts docs, needs ORATS support follow up

Summary of August 5 2024 near miss day cross validated across multiple independent ORATS metrics:
Contango negative 1.40 deep backwardation
Slope percentile 100 most extreme skew in dataset
IV percentile 1m and 1y 100 across all four IV rank measures
One day realized volatility 37.37 percent
SPY intraday range 499.75 to 512.79, open 501.10, close 506.72
Near term one day implied vol approximately 43 percent at 50 delta

This cross validation across independent metrics all agreeing on the same day being extreme gives strong confidence ORATS data is reliable and the near miss was a genuine multi sigma event not a data anomaly.
