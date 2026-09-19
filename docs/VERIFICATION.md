# Verification · 2026-09-19

[Back to project](../README.md)

## Implemented and checked

- 15 Python tests: five label examples plus API validation, provider failures, malformed scores and privacy/security headers.
- Chromium and WebKit: success, 503, network failure, malformed response, cancellation after editing, reset, POST payload and five widths (320–1440 px).
- Pylint `server.py`: 10.00/10. A lint score is not a security certification.
- Browser tests mock model responses. Screenshots capture the real interface in its idle state.

Run `python -m unittest discover -v` and `pylint server.py`. For browser checks, install Playwright 1.56.1 in a separate directory, install its Chromium and WebKit browsers, start `python server.py`, and run `node test_browser.cjs` with `PLAYWRIGHT_MODULE` pointing to that installation.

## Boundaries

No live Watson inference, model accuracy, clinical validity or production hosting was established by these tests. The optional external-provider course examples remain separate from the mandatory deterministic gate. POST avoids text in URLs; it does not make the external provider private or authorize sensitive input. The compatibility GET endpoint still accepts query text. Production authentication, rate limiting and deployment controls remain separate work.
