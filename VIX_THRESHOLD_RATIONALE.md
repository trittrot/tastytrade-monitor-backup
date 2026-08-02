# VIX Alert Threshold Design Rationale

Last updated: 2026-08-02

## History of Changes

### Original design: percentage-based thresholds
The VIX monitor originally used percentage moves from the days open, e.g. plus or minus 10, 15, 20, 25, 30 percent. This was intuitive but had two flaws discovered through use.

### Change 1: Reference point corrected to industry standard
Originally the reference (days open) was set at midnight UK, the first tick after the calendar date changed. Since VIX is calculated across a wider window than just US cash market hours, this meant the reference could be an arbitrary overnight value with no relationship to when VIX options are actually tradeable.

Researched and confirmed the genuine industry standard convention, used by CNBC, Bloomberg, Yahoo Finance: percentage change compares current VIX to the PRIOR DAYS OFFICIAL CLOSE at 4.15pm ET, which is 21.15 UK during BST. VIX and SPX options continue calculating for 15 minutes after regular equity markets close at 4.00pm ET.

Fixed the reference point to reset at 21.15 UK, fetching the genuine prior close from CBOE own published VIX_History.csv data rather than using whatever price happened to be live at the moment the script started or restarted. This was directly validated by comparing our calculated percentage change against Tastytrade own live displayed percentage figure, which matched exactly (1.23 percent both sources).

### Change 2: Switched from percentage to points (handles)
Mike was advised that professional VIX traders use points or handles, not percentage moves, since percentage change of an already-abstract volatility measure is a second order concept. Raw point moves correspond directly to real tradeable dollar amounts on VIX futures and options, and to standard deviation based risk framing.

Switched the alert system entirely from percentage thresholds to point thresholds: 3, 5, 8, and 15 points, corresponding approximately to 1, 2, an intermediate tier, and 3 standard deviation moves respectively. This was Mikes own explicit specification, based on the round number heuristic that a 3 point VIX move is approximately 1 standard deviation and a 5 point move is approximately 2 standard deviations.

### Change 3: Regime adjusted thresholds
A genuine limitation was identified in the fixed point system: a given point move means something very different depending on the starting VIX level, because VIX is non-linear and mean reverting.

In a low volatility regime (VIX around 12 to 15), a 2 point move represents roughly a 15 percent relative expansion, statistically very notable, often signaling the end of a calm period.
In a high volatility regime (VIX around 30 to 40), a 2 point move is routine noise, roughly 5 percent. In these environments a move needs to be 5 to 8 points to be considered significant.
Historical backtests referenced show that daily spikes of 4 plus points, greater than 3 standard deviations, exhibit strong mean reversion, with VIX tending to partially pull back over the following 1 to 5 trading sessions.

To address this, the system now uses 4 regime buckets based on the days starting reference VIX level, each with its own scaled point thresholds:

Low vol regime, reference under 15: thresholds 2, 3, 4, 6 points
Normal regime, reference 15 to 25: thresholds 3, 5, 8, 15 points (the original fixed values, since most trading days fall in this range)
Elevated regime, reference 25 to 35: thresholds 5, 8, 12, 20 points
Extreme or crisis regime, reference 35 plus: thresholds 8, 12, 18, 25 points

The regime is determined automatically each day based on the genuine prior close reference price (see Change 1), and the appropriate threshold set is selected before the day begins monitoring.

Note as of this writing, downward move thresholds use the same regime buckets and values as upward moves. Mike has indicated he will likely want to differentiate downward thresholds in the future, since downward VIX moves relate to long premium hedge management rather than short premium risk.

## Design Philosophy
All changes described here emerged from genuine evidence and reasoning, not arbitrary choices: real historical CBOE data, cross validation against Tastytrade own live displayed figures, and specific guidance Mike researched and brought to the conversation about professional trader conventions and regime relativity. This is consistent with the broader systems approach throughout this project: prefer evidence based calibration over assumption wherever possible.
