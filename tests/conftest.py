import sys, os
from pathlib import Path

# add project root to sys.path (…/MECH_SHOP_DEPLOYMENT_CICD)
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# ensure test env is present (CI or local)
os.environ.setdefault("FLASK_APP", "app")
os.environ.setdefault("FLASK_ENV", "testing")
os.environ.setdefault("DATABASE_URL", "sqlite:///ci.db")
os.environ.setdefault("CACHE_TYPE", "SimpleCache")
os.environ.setdefault("RATE_LIMIT_DEFAULT", "100/hour")
