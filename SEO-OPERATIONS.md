# Search and AI discovery

This release adds nine canonical pages, including three original research guides, a guide index, company information, and dedicated product pages. Research guides link back to the Revision B schematics, explain assumptions, and cite primary sources. Product pages provide direct routes to the Fawn product, Functioning Faith web demo, and the supplied TestFlight invitation.

## Maintain and verify

Edit `content/pages.json` for metadata and question/answer pairs; edit `content/*.html` for guide and product copy. Update modified dates only when content materially changes. The architecture source remains `scripts/build_architecture.py`.

```sh
python scripts/build_site.py
python scripts/verify_seo.py
python scripts/preview.py
```

The preview serves clean URLs at http://127.0.0.1:8766. It is a local content preview, not a Cloudflare header emulator. The verifier checks the page inventory, canonical metadata, JSON-LD, visible FAQ parity, local links and fragments, image alt attributes, robots, and sitemap. Browser checks should also cover image decoding, mobile overflow, JavaScript-disabled content, video playback, and motion controls. Fonts are locally hosted under their included SIL Open Font Licenses; the DM Sans file is a variable font covering weights 400–700.

## Production checks

- Check the commit-specific Cloudflare Pages result on GitHub.
- Confirm all nine sitemap URLs return the expected page with HTTP 200.
- Confirm `/robots.txt` is plain text and `/sitemap.xml` is XML. Previously these paths returned the homepage as HTML.
- Confirm a nonexistent URL returns HTTP 404. The root `404.html` prevents Pages' default SPA fallback from creating soft 404s.
- Confirm `.html` URLs redirect to the clean canonical path and alternate hostname redirects work.
- `functions/_middleware.js` redirects only the public www and production pages.dev hostnames to the apex, preserving paths and query strings. All other requests continue to static assets; commit preview hostnames remain available for review. Hostname redirects are not supported by Pages `_redirects` files.
- Confirm source content and internal build notes have `X-Robots-Tag: noindex`; they are not search landing pages.
- Inspect live rendered content, fonts, images, metadata and mobile performance. Local timing is not field Core Web Vitals.

## Search reporting still requires verified accounts

In Google Search Console and Bing Webmaster Tools, verify ownership and submit `https://goldstarorbital.com/sitemap.xml`. Check indexing, selected canonicals, crawl errors, query impressions and landing-page clicks. No account verification, sitemap submission, indexing, or ranking is implied by publishing this repository.

Use the site's analytics provider, once configured, to compare AI referral sources (for example ChatGPT, Perplexity and Copilot), landing pages, and onward clicks. Referral headers can be absent; report observed referrals rather than attributing all direct visits to AI. Product buttons include `data-conversion` labels for future event integration, but this release does not collect conversion events or add a tracking service. Check provider consent and retention settings before enabling one.

`robots.txt` permits search crawlers, including OAI-SearchBot. Cloudflare account-level bot rules can still affect genuine crawlers; check their requests and OpenAI's published IP ranges if discovery fails. A successful request with a bot user-agent is only an endpoint check, not proof that real bot IP addresses pass the firewall.

## Supported markup and limits

The static JSON-LD graph describes Organization, Person, WebSite, WebPage, BreadcrumbList, TechArticle, the guide ItemList, and the Functioning Faith SoftwareApplication. FAQPage entries mirror visible questions and answers. No ratings, reviews, prices, hardware validation, or search endorsements are invented.

Google no longer displays FAQ rich results as of May 2026. FAQ content is still useful to readers, but the markup is not a promise of rich-result eligibility. Google's AI-search guidance recommends the same useful content, crawlability, and technical fundamentals as search; it does not require `llms.txt`. Rankings and AI citations depend on external systems and cannot be guaranteed.

References: [Google AI search guidance](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide), [Google documentation updates](https://developers.google.com/search/updates), [OpenAI crawler documentation](https://developers.openai.com/api/docs/bots), [Cloudflare Pages routing](https://developers.cloudflare.com/pages/configuration/serving-pages/).
