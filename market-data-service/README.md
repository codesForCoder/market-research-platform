# Market Data Service

## Dhan Feed Limits

| Feed Type                             | WebSocket URL                            | Max Instruments / Connection | Max Instruments / Subscribe Request |
|---------------------------------------|------------------------------------------|-----------------------------:|------------------------------------:|
| Ticker / Quote / Full (5-Level Depth) | `api-feed.dhan.co`                       |                        5,000 |                                 100 |
| 20-Level Market Depth                 | `depth-api-feed.dhan.co/twentydepth`     |                           50 |                                  50 |
| 200-Level Market Depth                | `full-depth-api.dhan.co/twohundreddepth` |                            1 |                                   1 |

---

# Subscribe to Market Feed

```bash
curl -X POST "http://localhost:8001/api/instruments/subscribe/feed" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{
    "instruments": [
      {
        "security_id": 100000,
        "exchange": "NSE",
        "segment": "D"
      },
      {
        "security_id": 100001,
        "exchange": "NSE",
        "segment": "D"
      },
      {
        "security_id": 100002,
        "exchange": "NSE",
        "segment": "D"
      },
      {
        "security_id": 100040,
        "exchange": "NSE",
        "segment": "D"
      },
      {
        "security_id": 100044,
        "exchange": "NSE",
        "segment": "D"
      },
      {
        "security_id": 100046,
        "exchange": "NSE",
        "segment": "D"
      },
      {
        "security_id": 100048,
        "exchange": "NSE",
        "segment": "D"
      }
    ]
  }'
```

---

# Subscribe to Market Depth

```bash
curl -X POST "http://localhost:8001/api/instruments/subscribe/depth" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{
    "instruments": [
      {
        "instrument": {
          "security_id": 100000,
          "exchange": "NSE",
          "segment": "D"
        },
        "depth": 20
      },
      {
        "instrument": {
          "security_id": 100001,
          "exchange": "NSE",
          "segment": "D"
        },
        "depth": 20
      },
      {
        "instrument": {
          "security_id": 100040,
          "exchange": "NSE",
          "segment": "D"
        },
        "depth": 20
      },
      {
        "instrument": {
          "security_id": 100044,
          "exchange": "NSE",
          "segment": "D"
        },
        "depth": 200
      },
      {
        "instrument": {
          "security_id": 100046,
          "exchange": "NSE",
          "segment": "D"
        },
        "depth": 200
      }
    ]
  }'
```