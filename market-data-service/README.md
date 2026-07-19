# Dhan Feed Limits

| Feed Type | WebSocket URL | Max Instruments per Connection | Max Instruments per Subscribe Message |
|-----------|---------------|-------------------------------|----------------------------------------|
| Ticker / Quote / Full (5-level) | api-feed.dhan.co | 5000 | 100 |
| 20-level Market Depth | depth-api-feed.dhan.co/twentydepth | 50 | 50 |
| 200-level Market Depth | full-depth-api.dhan.co/twohundreddepth | 1 | 1 |


`
{'InstrumentCount': 1, 'InstrumentList': [{'ExchangeSegment': 'NSE_EQ', 'SecurityId': '1333'}], 'RequestCode': 15}
`