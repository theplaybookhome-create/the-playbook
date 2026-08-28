# Google Play Data safety answers — THE PLAYBOOK

Use these exact answers in Play Console → App content → Data safety.
Review them once before you submit.

## Does your app collect or share user data?
Yes — optional account + published Community posts + purchase unlock flag.
Daily tracking logs stay on the device and are NOT collected by you.

## Data collected
- Personal info: Email address (optional account)
- Personal info: Name (optional display name)
- App activity: Other user-generated content (Community posts the user publishes)
- App info and performance: none required
- Financial: Purchase history is handled by Google Play if you use Play Billing; for the web Stripe Payment Link, declare Purchase history collected by Stripe if you also wrap the web paywall. Prefer listing the Play app as FREE and collecting no financial data in-app.
- Photos / location / contacts / health: No (do not declare health — logs are user notes, not Health Connect data)

## Data shared
- Shared with Stripe only if the Android app still opens the Stripe Payment Link.
- Shared with Supabase for account email and Community posts.

## Security
- Data is encrypted in transit (HTTPS).
- Users can request deletion.
- You may commit to Independent security review: No.

## Data deletion
Yes. In-app: Today → Your data → Delete my data.
Account: email Theplaybookhome@gmail.com
URL: https://theplaybook.cloud/support.html

## Families / Designed for Children
Do NOT declare Designed for Children.
Target age: 18+
Reason: the user is the parent or carer. Children are subjects of notes written by an adult.
