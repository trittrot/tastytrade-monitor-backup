# ORATS University Notes - Volatility Surface (Sections 200-204)

Summarized from https://orats.com/university on 2026-07-20, for reference in future sessions.

## 201 - Volatility Surface
The volatility surface is implied volatility across every strike and expiration for one stock. Two useful slices: term structure (at-the-money IV across expirations) and skew (IV across strikes for one expiration).

Contango: short-term IV lower than long-term IV, the normal state. Backwardation: short-term IV higher than long-term, the reverse, associated with stress.

Skew typically forms a U shape, called the smile. Slope measures the steepness or lopsidedness of the skew, drawn as a tangent line at the 50 delta.

## 202 - Volatility Around Earnings
IV rises heading into earnings because the market prices in extra uncertainty from the announcement. ORATS mathematically isolates this earnings effect to calculate ex-earnings IV, which allows fair comparison across time and between stocks with different earnings calendars.

Implied earnings move is the percent move priced into options ahead of an announcement, comparable against the actual historical move to judge whether straddles or strangles were good value.

Inter-earnings IV and HV compares historical volatility over the last three calendar months to the IV priced in for the upcoming quarter, both measured right after an announcement, to see if upcoming IV is overshooting recent realized volatility.

## 203 - Predictive Indicators
Ex-earnings IV is best judged versus a related ETF, versus ORATS forecast, and versus its own 1 year percentile.

Slope is best judged relative to its own recent trend, not in isolation. A slope higher than recent levels favors risk reversal strategies. A slope lower than recent levels favors collar strategies.

Contango measures the slope of at-the-money ex-earnings IV for expirations under 45 days. Contango is positively related to stock performance. IMPORTANT: ORATS explicitly states contango should be compared against its own 10 day moving average, not just day to day. When contango flips from positive to negative, ORATS states this can be a bad sign for the market.

Forward and Flat Forward IV are additional measures. ORATS states extremes in the ratio of flat forward to forward IV have historically foreshadowed larger moves in the underlying. Not yet built into Mikes system as of this note.

## 204 - Historical Data
ORATS sells three separate raw bulk data products, distinct from the Data API subscription Mike uses: near end-of-day FTP files since 2007, 1-minute intraday data since August 2020, and physical hard drive delivery for the full intraday archive. Not currently relevant to Mikes system, noted for reference only if deeper independent research is ever needed.

## Practical implication for Mikes system
As of this note, orats_contango_monitor.py compares todays contango only to the previous days reading. ORATS own documentation recommends comparing against a 10 day moving average instead, as a signal of regime change. This is a planned enhancement, see the live script and git history for current implementation status.
