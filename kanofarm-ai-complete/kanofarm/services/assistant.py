"""Optional AI assistant grounded in the farmer's context. Needs ANTHROPIC_API_KEY (paid API).
Privacy: sends LGA/ward (no name, phone or GPS) to the third-party model."""
import json, urllib.request
from typing import Callable

SYSTEM = """You are the KanoFarm AI assistant for smallholder farmers in Kano State, Nigeria.
Rules:
- Use simple, practical language. Keep answers short. If the farmer writes in Hausa, answer in Hausa only if you are confident; otherwise answer simply in English and say Hausa support is limited.
- Use the FARM CONTEXT provided (weather advisories, crop, days after planting). If information is missing, say so. Never invent weather, statistics, prevalence, or local recommendations.
- Never recommend a specific pesticide product, dose, or registration number. Suggest integrated pest management first (prevention, cultural, mechanical, biological), and say chemical control needs a registered product verified with an extension officer and the product label.
- You cannot diagnose from text alone. Give possible causes, how to tell them apart, and advise using Scan Plant or an extension officer.
- Be honest about uncertainty. You do not replace qualified agricultural extension professionals."""

def build_context(profile: dict, farm: dict | None, crops: list, advisories: list) -> str:
    lines = [f"Language preference: {profile.get('language', 'en')}"]
    if farm:
        lines.append(f"Farm area: LGA={farm.get('lga') or 'unknown'}, ward={farm.get('ward') or 'unknown'} (Kano State)")
    for c in crops:
        lines.append(f"Crop: {c['name']}, planted {c['planting_date']}, {c['days_after_planting']} days after planting")
    for a in advisories:
        lines.append(f"Weather advisory: {a['message_key']} evidence={json.dumps(a['evidence'])}")
    if not farm: lines.append("No farm selected: weather context unavailable.")
    return "FARM CONTEXT\n" + "\n".join(lines)

def build_request(model: str, context: str, message: str) -> dict:
    return {"model": model, "max_tokens": 600, "system": SYSTEM + "\n\n" + context,
            "messages": [{"role": "user", "content": message}]}

def _post(key, payload, timeout=30):
    req = urllib.request.Request("https://api.anthropic.com/v1/messages", data=json.dumps(payload).encode(), method="POST",
        headers={"x-api-key": key, "anthropic-version": "2023-06-01", "content-type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:   # nosec - fixed https URL
        return json.loads(r.read().decode())

def ask(api_key: str, payload: dict, post: Callable = _post) -> str:
    resp = post(api_key, payload)
    text = "".join(b.get("text", "") for b in resp.get("content", []) if b.get("type") == "text").strip()
    if not text: raise ValueError("empty reply")
    return text
