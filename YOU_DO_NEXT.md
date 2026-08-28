# What you still need to do
I finished the pieces that can be done in the project files. Everything below needs you (or a developer account only you can open).

## Do this week — web launch (recommended first)
1. Hard-refresh https://theplaybook.cloud after this deploy and check Privacy, Terms and Support in the footer.
2. In the app, open Today, scroll to Your data, tap Delete my data once on a test device and confirm logs vanish but unlock stays.
3. Export a backup, then import it, to prove recovery still works.
4. Email yourself from Theplaybookhome@gmail.com so you know support mail is live.
5. In Stripe Dashboard → Payment Links, confirm the success URL is `https://theplaybook.cloud/?unlocked=1`.
6. Freeze UI changes until after the first real users. Stop theme patching mid-launch.
7. Put the privacy URL in any Facebook / TikTok / X bio: https://theplaybook.cloud/privacy.html

## Play Store — only you can do
8. Create a Google Play developer account ($25 one-time) at https://play.google.com/console
9. Decide billing BEFORE you wrap the app:
   - A) Play listing is free. People unlock on the website with Stripe. Safest.
   - B) Charge £2.99 inside the Play app using Play Billing (Digital Goods API). Needed if the unlock button stays in the Android build.
10. On your laptop, install Java + Bubblewrap and wrap https://theplaybook.cloud as a Trusted Web Activity. Package name suggestion: `cloud.theplaybook.app`
11. After the first AAB is signed, copy the **SHA-256** of the Play App Signing cert into `.well-known/assetlinks.json` (replace REPLACE_WITH_PLAY_APP_SIGNING_SHA256) and push it.
12. Upload the AAB to a Closed testing track.
13. Paste listing copy from STORE_LISTING.md. Upload feature-graphic-1024x500.png, icon-512.png, and at least two phone screenshots.
14. Complete Content rating, Data safety (see DATA_SAFETY.md), target audience (18+, not Designed for Children), and the privacy policy URL.
15. Add 12 real testers (Gmail accounts). They must tap the opt-in link and install from Play. Keep 12 opted-in for 14 continuous days.
16. Then apply for production access.

## Legal / family-data (you confirm)
17. Read privacy.html and terms.html. Change the operator name if you trade as a limited company.
18. If you ever sync daily logs to the cloud, update the privacy page BEFORE you ship that.
19. For account deletion requests, delete the Supabase Auth user and any community_posts rows for that email.

## Nice-to-have, not blockers for web
20. Custom email domain instead of Gmail.
21. Support page is live at /support.html — share that link in bios if you want.
22. Crash-free pass on a cheap Android phone and an iPhone in Safari Add to Home Screen.
