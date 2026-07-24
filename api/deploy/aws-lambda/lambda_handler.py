"""
lambda_handler.py  -  AWS Lambda entrypoint for the HS Writing G9-12 grader.

Wraps the existing FastAPI app (api/main.py) with Mangum so the SAME service that runs on Render/uvicorn runs
unchanged behind a Lambda function URL. No app code changes: the /score ExternalApiScore endpoint, the vendored
grader_engine, and the keyless /score + /timeback exemptions are all reused as-is.

WHY LAMBDA: Timeback's QTI grader allowlist (validateCustomOperatorUrls) accepts *.lambda-url.*.on.aws and
*.execute-api.*.amazonaws.com but NOT *.onrender.com (empirically verified 2026-07-24). A Lambda function URL
is an approved host with zero allowlist request, and it doubles as the planned AWS migration.

DEPLOY: this file must sit next to (or import-path-reach) api/main.py. The zip/container root should contain
main.py, external_score.py, grader_engine/, and this handler. Set Lambda handler = "lambda_handler.handler".
See README.md in this folder for the full step list.
"""
import os
import sys

# Ensure the api/ root (two levels up from deploy/aws-lambda/) is importable so `import main` resolves.
_API_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if _API_ROOT not in sys.path:
    sys.path.insert(0, _API_ROOT)

from mangum import Mangum   # noqa: E402  (added to requirements-lambda.txt)
from main import app        # noqa: E402  the existing FastAPI app (unchanged)

# Mangum translates Lambda function-URL / API-Gateway events <-> ASGI. api_gateway_base_path="/" keeps the
# route as POST /score (the wirer bakes .../score?grain=...). lifespan="auto" runs the app's Anthropic-client
# startup on cold start.
handler = Mangum(app, lifespan="auto")
