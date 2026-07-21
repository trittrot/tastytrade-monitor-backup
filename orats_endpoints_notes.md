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


## Section 200 University Cross-Reference - Additional Fields Verified

### Slope family (Core General endpoint, /datav2/cores)
slope - near-term 30-day skew steepness. Tested SPY 2026-07-20: 7.8781
slopeInf - long-dated skew steepness. Tested: 8.3362
slopeFcst - ORATS forecast of near-term slope. Tested: 8.3447
slopeFcstInf - forecast of long-dated slope. Tested: 9.0042
deriv - curvature of skew, near-term. Tested: 0.1709
derivInf - curvature, long-dated. Tested: 0.2746
slopepctile - one year percentile for slope. Tested: 73.02
slopeavg1m - trailing month average slope. Tested: 6.8251
slopeavg1y - trailing year average slope. Tested: 7.2506
slopeStdv1y - standard deviation of slope over the year. Tested: 1.03
etfSlopeRatio and variants - slope divided by sector ETF slope. Tested on SPY itself, returned 0, since SPY is the benchmark ETF, this field is only meaningful for individual stocks compared to their sector ETF, not for SPY itself.
LESSON: slopepctile and related trailing average fields live on Core General (cores endpoint), NOT on SMV Summaries, despite being documented on the same page as other slope fields.

### Earnings and implied move fields
exErnIv30d, exErnIv90d - implied volatility with earnings effect stripped out. Tested AAPL: 25.87 percent and 26.73 percent
ieeEarnEffect - market implied earnings effect. Tested: 2.5066
impliedMove - percentage stock move priced into options for next earnings. Tested AAPL: 5.49 percent
absAvgErnMv - historical average earnings day move, last 12 announcements. Tested AAPL: 2.0705 percent
ernMvStdv - standard deviation of historical earnings moves. Tested: 1.8642
fcstErnEffct - ORATS own forecast of earnings effect, comparable against market implied ieeEarnEffect. Tested: 1.4836 vs market implied 2.5066, suggesting market may be pricing a larger earnings reaction than ORATS model expects.
These fields split across two endpoints: exErnIv and impliedMove live on Summaries, while absAvgErnMv, ernMvStdv, fcstErnEffct live on Core Earn (cores endpoint).

### Forward and Flat Forward IV fields (Summaries endpoint)
fwd30_20, fwd90_30 - true forward volatility between two tenors. Tested SPY: 15.05 percent and 15.15 percent
ffwd30_20, ffwd90_30 - flat forward volatility, simpler non-compounded version. Tested: 15.49 percent and 15.40 percent
fbfwd30_20, fbfwd90_30 - ratio of flat forward divided by forward. Tested: 1.0294 and 1.0168
Per ORATS University section 203, extremes in this ratio have historically foreshadowed larger moves. Values close to 1.0 (as tested today) indicate no extreme divergence currently, this signal is quiet.

## Section 200 University Cross-Reference - FULLY COMPLETE
Every field explicitly discussed in sections 201, 202, and 203 has now been tested and confirmed working with real data, across the Summaries and Cores endpoints. Section 204 describes bulk data purchase products separate from the Data API subscription, not applicable, nothing to test there.


## ORATS University Section 300 - Backtesting (Trading Tools platform, NOT Data API)

IMPORTANT: Everything in section 300 describes ORATS Trading Tools (the Backtester, Custom Backtester, Strategy Optimizer), a separate subscription from the Data API Mike actually has. None of this is accessible through the current API subscription.

### 301 - Backtesting Methodology
Four common backtesting pitfalls: unrealistic execution prices, overfitting, path dependency, notional vs margin return confusion. ORATS uses quotes from 14 minutes before close, slippage 75 percent of bid ask for single legs down to 53 percent for four leg spreads. Database of 300 million plus precomputed backtests across 100 plus symbols and 15 strategies.

### 302 - Input Parameters
Entry criteria: DTE, strike deltas, spread yield, five technical triggers - VIX price, SMA, 14 day RSI, IV percentile 1 year, Slope percentile 1 year. Exit criteria: stop losses -25/-50/-75 percent, profit targets +25 up to +300 percent.

### 303 - Measuring Performance
37 performance metrics across four categories: Return, Risk, P&L, Others. Sharpe vs Sortino ratio explained, Sortino only penalizes downside volatility, may suit Mikes risk averse approach better. Three ranking algorithms: Best Overall Performance, Best Conservative Winner, Best Return on Risk.

### 304 - Custom Backtesting
Build fully custom backtests, not just search precomputed ones. 15 plus entry parameters, matching exit parameters. Two modes: End of Day (2007 to present) and Intraday (1 minute data, August 2020 to present). Exact slippage formula given: Buy = Bid plus (Ask minus Bid) times slippage percent. Commission 1 dollar per contract plus 0.01 per share of stock.

### 305 - Optimizing Your Strategy
Strategy Optimizer adds any of 98 proprietary ORATS indicators (includes everything tested today: slope, contango, IV percentile, forward vol) plus technical indicators (SMA, Bollinger Bands, RSI, CCI) on top of a base strategy. Uses P-value statistical validation, P less than 0.05 considered meaningful, plus permutation testing with 10000 Monte Carlo simulations to distinguish genuine edge from overfitting or luck.

## Section 300 SUMMARY
All five sections (301-305) describe the Trading Tools Backtester and Strategy Optimizer, a separate paid product from the Data API. Mike currently only has the Data API subscription. If Mike ever wants to actually RUN these backtests (not just understand the methodology), that requires the additional Trading Tools subscription, previously considered and declined in favor of API-only. Useful conceptually for understanding what a rigorous backtest looks like (execution price realism, slippage, P-value validation), which can inform Mikes own manual historical analysis approach already used successfully for contango and VIX threshold calibration.


## ORATS University Section 400 - Implementation, Risk, Review (Trading Tools platform, NOT Data API)

IMPORTANT: Like section 300, the entire 400 series describes Trading Tools features, not the Data API. Actual section count is 401-405, not 406 as originally assumed.

### 401 - Stock Scanning
Scans 5000 plus tickers comparing indicators to own history (moving averages), forecasts, and related equities. Over 30 sector ETF benchmarks suffixed underscore C, e.g. XLK_C for tech, SPY_C for SPY itself.
TWO SCAN TEMPLATES DIRECTLY RELEVANT to Mikes future scanning system:
Put-call skew cheap: slope lower than recent levels, low slope percentile, high slope forecast vs current - candidate for COLLAR strategy
Put-call skew rich: slope higher than recent levels, high slope percentile, low slope forecast vs current - candidate for RISK REVERSAL strategy
These use exactly the fields already tested and confirmed working: slope, slopepctile, slopeFcst. Could be replicated in Mikes own scanner without needing Trading Tools subscription.
Other templates: unusual call/put volume, earnings this week, high/low IV30d, hard-to-borrow.

### 402 - Option Scanning
Three theoretical edges once a stock is scanned: Distribution edge (D%) based on 15 plus years historical price move probability, Forecast edge (F%) based on ORATS volatility surface forecast, Smoothed edge (S%) based on proprietary SMV pricing. Plus 20 filterable columns: Greeks, POP%, reward risk, market width, DTE, breakevens, open interest, volume.

### 403 - Trade Ideas and Signals
Central dashboard aggregating four sources: Backtest Finder (matches current conditions against 300 million plus historical backtests), Curated Strategies (ORATS team optimized), My Strategies (own saved), Option Scans. Plus market intelligence: Time and Sales, Top Movers, Unusual Volume, Earnings/Dividends calendar, Macro Calendar.

### 404 - Placing Orders
Profit attribution breaks price changes into 8 factors: Delta, Gamma, Vega, Prior/Current Marks, Theta, Slope, Unknown. Payoff diagrams with what-if scenarios for IV change and DTE change. Five exit alert types: Trade, Event, Indicator, Leg, Time-based - conceptually similar to alerts already built for Mikes system. Broker connections: Tradier, TradeStation, Interactive Brokers - NOTE Tastytrade is not listed as a supported broker connection in Trading Tools.

### 405 - Review
Trade Journal for automated position tracking, works with ORATS paper trading accounts or CSV import for Interactive Brokers. Performance visualization, behavioral pattern detection, validates whether live results matched backtest expectations.

## Section 400 SUMMARY
All five sections (401-405) describe Trading Tools features, not the Data API. Most directly relevant to Mikes own build: the 401 put-call skew cheap/rich scan logic, which uses fields already tested and working (slope, slopepctile, slopeFcst) and could be replicated in a custom scanner script without needing the Trading Tools subscription.

## ORATS UNIVERSITY FULLY COMPLETE
All sections 200 through 400 (201-204, 301-305, 401-405) have been read in full and summarized as of 2026-07-20. Section 100 (101-103, Introduction) was not covered as it was not requested.


## SPY Term Structure Analysis - Complete Field Taxonomy (verified 2026-07-21)

Correction to earlier work: iv30d_orHvXern20d is NOT a real field name. The genuine field for IV vs HV ratio concept is ivHvXernRatio, located on Core General (cores endpoint), not Summaries. Lesson repeated again: field availability is strictly endpoint-specific even when documentation groups fields together on one page.

### On Summaries endpoint (/datav2/summaries)
Spot ex-earnings IV curve, 7 tenors: exErnIv10d, exErnIv20d, exErnIv30d, exErnIv60d, exErnIv90d, exErnIv6m, exErnIv1y
contango - near term slope summary, already built into live monitor
Forward curve: fwd30_20, fwd60_30, fwd90_60, fwd180_90, fwd90_30
Flat forward and ratio: ffwd and fbfwd variants for same tenor pairs, extremes in fbfwd ratio historically foreshadow larger moves per ORATS University 203
confidence - data quality indicator
iv30d - tested SPY 2026-07-21: 0.138 (13.8 percent)
rSlp30 - tested same date: 7.8398, confirmed this is the Summaries-endpoint name for the same concept as slope on Cores

### On Cores endpoint (/datav2/cores)
slope, slopeInf, slopeFcst, slopeFcstInf - full slope family
slopepctile - one year percentile for slope
ivPctile1y - percentile of current orIv vs year range
ivHvXernRatio - tested SPY 2026-07-21: 1.11, this is the genuine IV vs HV ratio field (implied vol divided by historical vol, ex-earnings)
orHvXern20d - tested same date: 12.84 percent, the actual 20-day historical volatility ex-earnings component used in the ratio above
deriv, derivInf - curvature of skew

### Recommended approach for full term structure analysis (not just contango alone)
1. Pull full exErnIv curve across all 7 tenors daily, not just contango, to see the whole curve shape rather than just the near-term slope
2. Use contango as a fast daily alert trigger (already built)
3. Layer in the forward curve (fwd fields) to see what the market expects BETWEEN future dates, which can be more revealing than spot levels alone
4. Watch fbfwd ratios for extremes as an anomaly check per ORATS guidance
5. GAP: unlike slope, contango has no built-in percentile field (no contangopctile exists) - would need manual historical calculation for percentile context on the full curve, same approach already used for the 10-day moving average work
