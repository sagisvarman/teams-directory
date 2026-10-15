# Teams Directory

Search directory for SBP school basketball team names. Type a team, school, school code or alumni name and the school it belongs to comes up with all its team names and alumni groups.

Single static page, no build step to view it: open `index.html`.

## Updating the data

The source sheets are in `source/`. After editing them (or `source/template.html` for the design), rebuild with one command:

```
python3 source/build.py
```

This regenerates `index.html`. Commit and push to `main` and Vercel redeploys automatically.
