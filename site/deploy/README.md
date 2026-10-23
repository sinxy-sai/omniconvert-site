# Static deployment

1. Run the CI verification locally:

   ```powershell
   python -m pytest tests -q
   npm run build
   python tools/verify_artifacts.py dist/releases/latest.json
   ```

2. Copy the contents of `dist/` to `/srv/omniconvert-site` on the HTTPS host.
3. Adapt `nginx-omniconvert.conf.example` to the host certificate paths and enable it.
4. Keep `/app/service-worker.js` uncached so clients receive cache policy updates promptly.
5. Serve `/app/manifest.webmanifest` and all release downloads over HTTPS.

The GitHub Actions `publish` job creates an attested static artifact on pushes to `main`. The example Nginx configuration is intentionally deployment-neutral; certificate management remains with the host.
