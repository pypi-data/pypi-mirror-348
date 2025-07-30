import asyncio
from pubstomp.core import main  # from your original script's main()

def cli():
    asyncio.run(main())
