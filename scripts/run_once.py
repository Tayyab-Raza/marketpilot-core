import asyncio, json
from app.services.research import run_research
print(json.dumps(asyncio.run(run_research()),indent=2,default=str))
