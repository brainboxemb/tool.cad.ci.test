import json
import os
from pathlib import Path

out = Path(os.environ["CAD_CI_OUTPUT"])
out.mkdir(parents=True, exist_ok=True)
active = json.loads(os.environ["CAD_CI_ACTIVE_DEPENDENTS_JSON"])
(out / "active.json").write_text(json.dumps(active) + "\n", encoding="utf-8")
