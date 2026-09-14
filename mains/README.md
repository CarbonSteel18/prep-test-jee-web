# papers/mains

Drop JEE Main PDF papers in this folder, then list each one in `/mains/index.html`.

## Adding a paper

1. Upload the PDF here (on GitHub: **Add file -> Upload files**, while you're
   inside this folder). Give it a filename with no spaces, for example
   `2026-01-24-shift1.pdf`.
2. Open `/mains/index.html` and add a line for it. Copy the example block
   shown in the HTML comment near the bottom of that file.
3. Commit the changes. Vercel redeploys automatically within a minute.

## Link format

Each entry links to the shared viewer:

`/viewer/?file=/papers/mains/<your-file>.pdf&title=<Your-Title-With-Hyphens>`

Use hyphens instead of spaces in the title. The viewer converts them back to
spaces automatically when it displays the title.
