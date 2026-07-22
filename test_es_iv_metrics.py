import asyncio
import json
from auth import authenticate_production

async def check_es_metrics():
    session = authenticate_production()
    data = session._get('/market-metrics?symbols=/ES')
    print(json.dumps(data, indent=2, default=str))

asyncio.run(check_es_metrics())
