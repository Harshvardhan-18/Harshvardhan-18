# Setup

## 1. Create the special repo
On GitHub, create a new **public** repo named exactly your username (e.g. `HV18`).
GitHub auto-detects this and shows its README on your profile page.

## 2. Push these files to it
```
dark.svg
light.svg
update.py
ascii_yo_svg.py
photo_to_ascii.py
portrait.txt
portrait_tspan.txt
requirements.txt
.github/workflows/main.yml
README.md   <- paste profile-readme-snippet.md contents into this
```
`cache/` will be created automatically by the workflow on first run — no need to push it empty.

## 3. Add the token
Settings → Secrets and variables → Actions → New repository secret:
- Name: `ACCESS_TOKEN`
- Value: a GitHub fine-grained PAT with (per the comment at the top of `update.py`):
  Account: `read:Followers`, `read:Starring`, `read:Watching`
  Repository: `read:Commit statuses`, `read:Contents`, `read:Issues`, `read:Metadata`, `read:Pull Requests`

`USER_NAME` doesn't need a secret — the workflow passes it automatically from `github.repository_owner`.

## 4. Set your birthday (optional)
`update.py` currently has a placeholder date of birth:
```python
age_data, age_time = perf_counter(daily_readme, datetime.datetime(2004, 1, 1))
```
Change `2004, 1, 1` to your actual DOB, or swap it for `acc_date` (your GitHub account creation date, already fetched at the top of `__main__`) if you'd rather not publish your birthday.

## 5. Run it
Actions tab → "Update profile SVGs" → Run workflow. It also runs daily via cron and on every push to `main`.

## Regenerating the portrait
If you swap the photo later:
```
python3 photo_to_ascii.py     # photo.jpeg -> portrait.txt
python3 ascii_yo_svg.py       # portrait.txt -> portrait_tspan.txt
python3 build_svg.py          # rebuilds dark.svg / light.svg with the new tspans
```

## Note on the original script
`update.py` had one small gap: `svg_overwrite()` received `age_data` as a parameter but never
wrote it into the SVG (`justify_format` was never called for it). I added that one line so
"Coding Since" actually populates — everything else is unchanged from what you gave me.
