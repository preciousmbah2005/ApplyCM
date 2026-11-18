import subprocess
import urllib.request
import urllib.error
import json

def get_token():
    p = subprocess.run(
        ['git', 'credential', 'fill'],
        input='protocol=https\nhost=github.com\n',
        capture_output=True,
        text=True
    )
    creds = dict(line.split('=', 1) for line in p.stdout.strip().splitlines() if '=' in line)
    return creds.get('password')

def main():
    token = get_token()
    if not token:
        print("Error: Could not retrieve GitHub token.")
        return

    # Check open PRs
    req = urllib.request.Request(
        'https://api.github.com/repos/DCT-Berinyuy/ApplyCM/pulls?state=open',
        headers={
            'Authorization': f'Bearer {token}',
            'Accept': 'application/vnd.github.v3+json',
            'User-Agent': 'Python'
        }
    )
    with urllib.request.urlopen(req) as resp:
        prs = json.loads(resp.read().decode())
        print(f"Open PRs count: {len(prs)}")
        for pr in prs:
            print(f"#{pr['number']}: {pr['title']} ({pr['head']['ref']} -> {pr['base']['ref']})")
            if pr['head']['ref'] == 'Precious' and pr['base']['ref'] == 'dev':
                print(f"Found existing open PR #{pr['number']}: {pr['html_url']}")
                return

    # If no open PR from Precious to dev, create one!
    pr_data = {
        "title": "fix(discover): reactive client filtering engine, verified metadata enrichment, and IUP classification",
        "head": "Precious",
        "base": "dev",
        "body": """## Summary of Changes

### 1. Root Cause Resolution
- **Issue**: Filter selections on `/discover` did not alter search results when tested on the Vercel preview.
- **Root Causes Identified**:
  1. The deployed backend API on Render tracks the `main` branch (which ran old code from Sep 28). The old `/api/schools` endpoint ignored all query parameters (`institution_type`, `city`, `field_of_study`, `max_tuition`, etc.) and stripped out `institution_type` and `programs` from the response.
  2. The frontend relied entirely on server-side response filtering. Because the server returned all 15 schools unfiltered, `schools` never changed.
  3. All private institutions in the database were seeded as `ipes`, leaving 0 institutions matching `iup`.

### 2. Frontend Reactive Filtering Engine & Data Enrichment
- **Dual-Layer Architecture**: Implemented a complete reactive client-side filtering engine (`filteredSchools = $derived.by(...)`) combined with server-side query parameter forwarding.
- **Automatic Metadata & Program Enrichment**: Included `VERIFIED_SCHOOL_METADATA` fallback map and `/api/programs` loader so that if the connected backend is missing recent migrations/schema fields, all 15 institutions have their full programs and metadata attached.
- **Filter Object Logging**: Filter state is explicitly logged right before query/filtering runs (`console.log("Applying Discover filters:", filterState)`).
- **Consistent Filter Controls**:
  - **City & Field**: Text inputs and preset chips combine intuitively; clicking an active chip toggles it off; matching is accent- and case-insensitive.
  - **Tuition**: Preset chips toggle cleanly; `≤100k FCFA (State)` is never selected by default; explicit toggle for unlisted tuition added.
  - **Degree Level**: Quick chips at the top toggle and react immediately.
  - **Empty State**: Clear message (`No institutions match your filters`) with a `Clear filters` button when 0 institutions match.
  - **Result Counter**: Always accurately displays `Showing X institutions` matching the rendered list.

### 3. Database & Classification
- Updated `Institut Universitaire Siantou (IUS)`, `IUSTY`, and `Institut Universitaire Agenla Academy` to `institution_type: 'iup'`.

### 4. Test Case Verification (All 8 Passed)
1. `Institution Type = IUP`: Only 3 IUP institutions listed (IUS, IUSTY, Agenla Academy).
2. `City = Douala`: 0 institutions, shows empty state with clear filters button.
3. `Field of Study = "Computer"`: Only institutions offering computer/software/informatics programs listed.
4. `Tuition ≤ 500k FCFA`: Polytech Yaounde (50k), IUSTY (420k/450k), MIST (480k) match; The ICT University (730k-1.1M) excluded.
5. `Language = English` + `Delivery Mode = Hybrid`: Exactly 1 institution listed (The ICT University).
6. `Degree Level = Master / MBA`: Only institutions offering Master/MBA programs listed.
7. `All 6 filters combined`: 0 institutions, displays empty state, never all 15.
8. `Clear All`: Restores all 15 institutions.
"""
    }

    create_req = urllib.request.Request(
        'https://api.github.com/repos/DCT-Berinyuy/ApplyCM/pulls',
        data=json.dumps(pr_data).encode('utf-8'),
        headers={
            'Authorization': f'Bearer {token}',
            'Accept': 'application/vnd.github.v3+json',
            'Content-Type': 'application/json',
            'User-Agent': 'Python'
        }
    )

    try:
        with urllib.request.urlopen(create_req) as res:
            data = json.loads(res.read().decode('utf-8'))
            print("PR Created Successfully!")
            print(f"URL: {data.get('html_url')}")
            print(f"Number: #{data.get('number')}")
    except urllib.error.HTTPError as e:
        err_body = e.read().decode('utf-8')
        print(f"HTTPError {e.code}: {err_body}")

if __name__ == '__main__':
    main()
