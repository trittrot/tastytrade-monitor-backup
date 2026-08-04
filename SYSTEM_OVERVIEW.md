# Tastytrade Monitoring System - Complete Reference

Last updated: 2026-08-04

## Scheduled (cron) Alerts, UK times

| Time | Script | Description |
|------|--------|-------------|
| 07:30 | heartbeat.py | Confirms system is alive, always alerts |
| 07:35 | es_gap_check.py | Compares ES to prior close, gap up/down, points prominent over percent |
| 14:31 | es_gap_check.py | Same check, midday |
| 21:16 | sp500_two_stage_scan.py | S&P 500 two-stage scan - Stage 1 confidence (80/90 percent tiers), Stage 2 ivPct1y IV percentile filter on Stage 1 qualifiers, SMS plus email |
| 20:55 | es_gap_check.py | Same check, EOD |
| 21:16 | orats_contango_monitor.py | SPY contango, day over day change plus 10 day moving average deviation, CAUTION and SIGNIFICANT tiers |
| 21:16 | etf_two_stage_scan.py | 21 Liquid ETFs two-stage scan - Stage 1 confidence (80 percent), Stage 2 ivPct1y IV percentile filter on Stage 1 qualifiers, SMS plus email |
| 21:16 | spy_term_structure_alert.py | Full SPY term structure snapshot with commentary, SMS plus email |
| 22:00 | es_close_capture.py | Captures ES close for next gap comparison, silent unless failing |
| 23:00 Sunday only | es_sunday_reopen_check.py | Compares Sunday reopen to Friday close |

## Continuous Background Services (systemd)

| Service | Description |
|---------|-------------|
| vix_live_monitor.py | Regime-adjusted staged point (handle) VIX alerts: low vol under 15 uses 2/3/4/6, normal 15-25 uses 3/5/8/15, elevated 25-35 uses 5/8/12/20, extreme 35 plus uses 8/12/18/25 (added 2026-08-02). Reference point is prior day's genuine 21:15 UK official CBOE close, not midnight |
| es_iv_live_monitor.py | Two tier ES IV percentile monitor, 80 percent and 90 percent high priority tier (added 2026-07-28), each tier tracked independently, checked every 60 seconds |

## On-Demand Commands

| Command | Purpose | Delivery |
|---------|---------|----------|
| mw-liq-etfs | Run 21 Liquid ETFs two-stage scan (confidence then ivPct1y) | Real SMS plus email every time run |
| confidence-all | Full S&P 500 two-stage scan (confidence then ivPct1y) | Real SMS plus email every time run |
| confidence SYMBOL | Single symbol confidence check | Real SMS only every time run |
| contango SYMBOL | Live contango reading, defaults to SPY if no symbol given | Screen only |
| term SYMBOL | Full term structure snapshot with commentary, defaults to SPY | Screen only |
| trend SYMBOL | Bullish, neutral, or bearish determination using 20d, 50d, 100d moving averages, defaults to SPY | Screen only |
| price SYMBOL | Live bid, ask, mid quote with change vs prior close, defaults to SPY, supports futures like /ES | Screen only |

Note: commands marked Real SMS or email trigger genuine alerts every single time they are run manually, not just on schedule.

## Design Philosophy
Monitoring and alerting only, never autonomous trade execution. All trade decisions and execution are made manually by Mike via the Tastytrade platform. EOD or near EOD decision making preferred over intraday reactivity, based on Mikes self acknowledged history of poor intraday decisions and shaped by the August 2024 volatility near miss.

All SMS alerts include UK time and date as the first line, added 2026-07-30, applied universally via the shared send_alert function in alerts.py.

See DISASTER_RECOVERY.md for full rebuild instructions, orats_endpoints_notes.md and orats_university_notes.md for ORATS API reference material, VIX_THRESHOLD_RATIONALE.md for VIX alert design history, SOSNOFF_TASTYLIVE_STRATEGIES.md for tastylive strategy reference, IN_CASE_OF_EMERGENCY.md for family and executor guidance.
