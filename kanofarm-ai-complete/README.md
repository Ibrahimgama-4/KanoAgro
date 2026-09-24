# 🌾 KanoFarm AI — Smart Farming. Better Decisions. Higher Productivity.

Installable web app (PWA) for Kano State farmers: real weather-based farm advice, farm records and timeline,
alerts, plant photo checks, IPM guidance, soil/irrigation guidance, expert review, and an optional AI assistant.
Built around one rule: **no fabricated data.** Where verified data does not exist, the app says so.

## Honest status
| Area | Status |
|---|---|
| Weather + advisories (Open-Meteo, modelled) | Working. Live call verified only by `scripts/smoke_weather.py` on your machine |
| Accounts, profile, farms, crops, timeline, alerts, history | Implemented (Supabase Auth + RLS). Needs your Supabase project |
| Rainfall since planting + rain/temperature charts | Implemented (Open-Meteo historical reanalysis + recent model days, labelled per source; partial totals flagged). Live API call not run in the authoring sandbox |
| Irrigation, soil & fertilizer guidance | Implemented, **general guidance only**, no dosages/volumes |
| Plant Doctor | Full pipeline (photo quality gate, confidence gate, IPM, product lookup, storage, expert review). **No trained model ships.** Until you train and deploy one it says the model is unavailable |
| Pesticide information | Registry + admin entry + expiry logic. **Empty** until verified records are added (NAFDAC bulk access not confirmed) |
| Crop calendar | **Draft** entries from secondary sources, labelled and not Kano-reviewed. No growth-stage calendar yet |
| Hausa | Architecture + draft crop names only. Message translations empty until reviewed by a native-speaking agronomist |
| AI assistant | Optional. Off unless `ANTHROPIC_API_KEY` is set (paid) |
| Not built | Farm map/boundaries, push/SMS/WhatsApp, flood/pest/disease risk models, on-device AI, Capacitor/Play Store, full admin (users, farms, guides, model registry UI) |

Tested here: 79 unit tests (pure logic). Endpoint tests (`tests_api/`) and app startup run in GitHub Actions because
the authoring sandbox had no network or FastAPI. The browser UI was syntax-checked but **not clicked through**;
expect some first-run fixes and please report them.

## Deploy (GitHub → Vercel + Supabase, no local machine)
1. **Supabase**: create a project → SQL editor → run `database/migrations/0001_core.sql`, `0002_features.sql`, `0003_reference_crops.sql` in order.
   Authentication → Providers → Email. For a quick MVP turn **off "Confirm email"**; otherwise configure SMTP so confirmation emails arrive.
2. **GitHub**: create a repo and push this folder (root must contain `index.py`). Use GitHub Desktop or `git push`; browser upload skips dotfiles like `.github/`.
   Check the **Actions** tab: CI must be green.
3. **Vercel**: Add New → Project → import the repo. Keep auto-detected settings. Add environment variables from `.env.example`
   (`SUPABASE_URL`, `SUPABASE_ANON_KEY` at minimum). Deploy.
4. Open `https://YOUR-APP.vercel.app/api/health` → `{"status":"ok"}`, then open the site on Android Chrome → Install app.
5. Sign up in the app. To become an admin: Supabase SQL editor →
   `insert into user_roles (user_id, role) values ('<your id from Authentication → Users>', 'admin');`
6. Optional: train the Plant Doctor (`ml/README.md`), deploy `ml/serving`, set `AI_MODEL_ENDPOINT`/`AI_MODEL_TOKEN`.
7. Add verified pesticide records in **More → Expert / Admin** only when you have a citable source.

## Local development (optional)
```bash
pip install -r requirements-dev.txt
python -m unittest discover -s tests -t .          # pure-logic tests
python -m unittest discover -s tests_api -t .      # endpoint tests
uvicorn index:app --reload                         # http://localhost:8000
python scripts/smoke_weather.py                    # live Open-Meteo check
```

## Layout
`index.py` Vercel entrypoint · `kanofarm/` API + services + knowledge · `static/` mobile web app + PWA ·
`database/` migrations · `data/` crop calendar + data sources · `ml/` training, evaluation, serving ·
`tests/`, `tests_api/` · `docs/`

## Security model
Farmer requests carry the farmer's own Supabase JWT to Postgres, so **Row Level Security** enforces ownership; the backend holds no
service-role key. Uploads are size-limited and type-checked by content. Images are stored only if the farmer opts in.
Farm GPS is visible only to its owner. Rate limits are in-memory (per instance). Technical errors are logged, never shown.

## Licensing and cost warnings
* Open-Meteo free tier and Vercel Hobby are **non-commercial**. See `docs/COSTS.md` and `docs/DATA_SOURCES.md`.
* PlantDoc is CC BY 4.0 (attribution). PlantVillage license must be checked at your source.
* Choose and add your own project `LICENSE` before publishing.

## Limitations you must communicate to users
Weather is modelled at ~11 km. Alert thresholds are unreviewed defaults. Any future model is unvalidated for Nigerian field
conditions until tested on expert-labelled Nigerian images. Not a replacement for extension officers.
