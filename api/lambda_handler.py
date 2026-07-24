"""
lambda_handler.py  -  AWS Lambda entrypoint for the HS Writing G9-12 grader (ROOT of the deploy package).

Lives at the api/ root (NOT in deploy/aws-lambda/, whose hyphen makes it un-importable as a Lambda module).
The Lambda handler setting is simply:  lambda_handler.handler

Wraps the existing FastAPI app (main.py) with Mangum so the SAME service that runs on Render/uvicorn runs
unchanged behind a Lambda function URL. No app-logic changes: the keyless /score ExternalApiScore endpoint,
the vendored grader_engine, and the auth exemptions are all reused as-is.

WHY LAMBDA: Timeback's QTI grader allowlist accepts *.lambda-url.*.on.aws (verified 2026-07-24) but NOT
*.onrender.com. A Lambda function URL is an approved host with no allowlist request, and it doubles as the
planned AWS migration.
"""
from mangum import Mangum   # ASGI<->Lambda adapter (in requirements-lambda.txt)
from main import app        # the existing FastAPI app, unchanged (zip root is on sys.path)

# Mangum translates Lambda function-URL / API-Gateway events <-> ASGI. lifespan="auto" runs the app's
# Anthropic-client startup on cold start. Route stays POST /score (the wirer bakes .../score?grain=...).
handler = Mangum(app, lifespan="auto")
