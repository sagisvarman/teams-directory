# Teams Directory

Search directory for SBP school basketball team names. Type a team, school, school code or alumni name and the school it belongs to comes up with all its team names and alumni groups.

Single static page, no build step to view it: open `index.html`.

## Updating the data

The source sheets are in `source/`. To rebuild after editing them:

```
cd source
python3 build_data.py        # writes data.json
```

then inject `data.json` into `template.html` (replace `/*__DATA__*/`) and save the result as `../index.html`.
