# JEE prep site - pipeline starter

A minimal scaffold whose only job is to prove the GitHub to Vercel pipeline
works, before any real features get built on top of it.

- `index.html` - static frontend test page
- `api/hello.py` - Python serverless function test

## Deploy

1. Push this folder to a new GitHub repository.
2. Go to vercel.com and sign in with GitHub.
3. Click "Add New" -> "Project" and import the repo.
4. Leave all settings on default and click Deploy.
5. Visit your `*.vercel.app` URL, then `*.vercel.app/api/hello`.

If both load, the frontend, the Python backend, and the auto-deploy pipeline
are all confirmed working.
