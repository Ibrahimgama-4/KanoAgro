import json
from pathlib import Path
_DATA = json.loads((Path(__file__).resolve().parent.parent.parent / "data" / "crop_calendar.json").read_text(encoding="utf-8"))
MONTHS = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

def calendar(crop_slug=None) -> dict:
    entries = [e for e in _DATA["entries"] if not crop_slug or e["crop_slug"] == crop_slug]
    for e in entries:
        e["months_label"] = "–".join(MONTHS[m - 1] for m in (e["months"][0], e["months"][-1])) if e.get("months") else None
    return {"banner": _DATA["banner"], "entries": entries}
