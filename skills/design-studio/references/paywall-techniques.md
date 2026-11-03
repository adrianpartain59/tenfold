# Paywall techniques: what real paywalls put on screen

The visual and structural techniques subscription apps and paywall vendors
use, each with a real app or a source. Read with `paywall-craft.md` ("Visual
first", "Flows"). Plan every screen of a flow by naming the technique that
carries its visual. Researched 2026-11; anything marked **[unverified]** is
practice without a primary source. Sources at the bottom.

## The default anatomy

Superwall's lead paywall designer (4,500+ paywalls) names one default that
"performs well across categories": a value headline, a few bullets, social
proof and a big CTA. Comparison tables underperform bullets and video, and
native-looking designs often beat custom ones. [T1]

| Zone | What goes there |
|---|---|
| Top 40–55% | The hero visual: product screenshots or "UI chunks", a device shot, a video of the app in use, a photo of real people, an illustration. About 90% of paywalls lead with a banner, slider or video instead of text. [T2] |
| Headline | Concrete, one or two lines, readable in about 3 seconds ("Unlock exclusive recipes", not "Go Pro"). [T2][T3] |
| Benefits | 3–5 one-line bullets with icons. Checklists outnumber benefit carousels about 2:1 in a 1,204-paywall corpus. [T4][T5] |
| Proof | One concrete rating or count beats stacked generic claims; only ~6% of paywalls show any. [T6] |
| Plans | Two plans (shorter period + annual) is the most common layout (51.5%); the recommended plan is preselected and visually dominant. [T7] |
| CTA | Sticky bottom, high contrast. A plain "Continue" beat a descriptive CTA by +111% in one test; a "No payment now / cancel anytime" line sits right by it. [T1][T8] |
| Footer | Restore, Terms, Privacy, the billed price line. Most paywall mistakes live here: repeated plan names and clutter. [T1] |

Total copy: the only explicit budget found is under 100–150 words for a whole
paywall [T3]; three of four winning redesigns in RevenueCat's case studies
moved from long-form to short-form [T9]. The skill's budgets
(`paywall-craft.md`) are tighter per screen because a flow spreads the words
over several screens.

## Flows

Multi-page onboarding paywalls converted at 12.41% against 9.07% for
single-page across 40M+ opens (Feb–May 2026, observational): +37%. The
recommended order is value, then expectations (how the trial works), then
pricing. [T10] Real flows:

- **Finch:** a warm first-person team line ("Finch is free to use. But we'd
  love for you to try Finch Plus…") → an offer beat → the timeline paywall. [T11]
- **Adobe Express:** trial timeline → feature list → plans. [T12]
- **Duolingo:** value carousel before the paywall; benefits walkthrough after. [T13]
- **Cal AI, Noom:** quiz → "building your plan" loader → plan-ready result →
  paywall (Noom: goal-date projection curve). Loaders that show
  personalisation and testimonials are "generally net positive". [T14][T15]
- **Exit sequences:** the main paywall, then one offer on close (Bend,
  Pushscroll). Never chain more than one. [T12]

Steps move forward with one Continue each; carousel dots belong to pagers
inside a screen.

## Catalog

Each entry: what it is · a real example · the `visual` it gives a screen.

1. **Illustrated trial timeline.** Today / reminder / charge-day nodes with
   icons. Blinkist's honest timeline with a real reminder: +23% trial
   conversion, −55% complaints [T13][T16]. Used by Opal, BoldVoice, Finch and
   Strava; only ~3% of paywalls use one [T17]. Draw the nodes as objects
   (calendar pages, day tiles), not a bulleted list. A reminder node only when
   the reminder really fires.
2. **"No payment due now" line** under the plans or CTA. Cal AI; Lose It!
   gives a whole screen to how the trial works. [T8] Only where it is true for
   the selected plan.
3. **Rating + count stack or laurel badge.** Speak: "5M+ users · 4.8★ · 140K
   reviews"; Stoic leads with "App of the Day". [T8][T6] Draw it as a badge
   (laurel branches around the number), big enough to be the visual.
4. **Testimonial card.** Flo; YAZIO stacks starred reviews under the offer.
   Real store reviews were part of redesigns with +72% install-to-trial and
   +17% ARPU. [T8][T9] One or two short quotes, never a wall.
5. **Review marquee.** An auto-scrolling row of short review cards; vendor
   components exist (Purchasely, RevenueCat). **[unverified]** as a measured
   pattern.
6. **Benefit pager / stories.** One frame per benefit, 3–4 frames, most
   valuable first, swipe cue visible, no fast auto-advance (ROI, Pestle,
   Peachy). [T2][T5]
7. **UI chunks / screenshot hero.** Real fragments of the app as the hero:
   Goalkit, Sunlitt's widget preview. [T5]
8. **Device video or device shot.** The app in motion inside a device frame,
   among the best converters per Superwall's designer. [T1] A tilted or
   floating device is a still version.
9. **App behind a sheet.** The real app, dimmed or blurred, with the offer as
   a sheet over it. **[unverified]**; closest documented: BitePal's locked
   features. [T12]
10. **Free vs Pro table.** Hevy. Underperforms bullets [T1]; only with a real
    free tier.
11. **Personal plan / projection.** Noom's goal-date curve; Runna names the
    user's plan. [T12][T15] Only from answers that really reach the paywall.
12. **Before / after story.** Fasting App, above the yearly plan. [T12]
13. **Sale hero.** A price chart or "SALE" callout with the regular price
    marked: +20% (2.7% → 3.24%) in one redesign. [T9] Only for a real sale.
14. **Offer ticket on exit.** A coupon or ticket object with the real regular
    price beside the offer (Bend, Captions). [T8][T12] No fake expiry.
15. **Spin / gift reveal.** YAZIO, Cal AI (part of a 123-experiment program
    that raised trial-to-paid 31%; no isolated lift). [T18] Only for a real
    discount everyone gets.
16. **Illustration or mascot.** A party-game redesign with illustrations and
    a playful headline: +31% install-to-trial, +64% revenue. [T9]
17. **Bottom fade.** A gradient at the fold that hints there is more (Outside). [T5]
18. **Personal note from the team.** A short first-person letter staged as
    an object: a card on a quiet ground, a polaroid of the team, an envelope,
    a chat thread, a handwritten card. Finch opens its paywall flow in a team
    voice [T11]; an indie app sets a founder note in a handwriting font with a
    sign-off [T19]. No source reports results for the pattern
    **[unverified]**; treat it as a test arm unless the project has its own
    result. Conventions [unverified]: 40–120 words, a team photo or avatars,
    a signature line, first screen of the flow, plans after it.

## Apple 3.1.2 and these visuals

- A hero or CTA that promotes the trial more conspicuously than the billed
  amount is rejected ("Try for Free" CTA, Aug 2026). [T20] A giant "FREE"
  headline needs the price at the same weight in the same element.
- Trial toggles are rejected since January 2026; use a trial-bearing plan
  card or a timeline. [T21]
- A timeline's charge node shows the real billed amount; the CTA area repeats it.

## Sources

| Id | Source |
|---|---|
| T1 | Jonathan Parra (Superwall), 4,000 paywalls: https://app-dev-and-marketing.pages.dev/4000-paywalls-jonathan-parra |
| T2 | Adapty, designing effective paywalls: https://adapty.io/blog/markdown/designing-effective-paywalls-for-mobile-apps.md |
| T3 | Apphud, high-converting paywalls: https://blog.apphud.com/design-high-converting-subscription-app-paywalls |
| T4 | Lazyweb, checklists vs carousels: https://design.lazyweb.com/blog/do-paywalls-use-feature-checklists-or-benefit-carousels |
| T5 | Superwall, 20 iOS paywalls in production: https://superwall.com/blog/20-ios-paywalls-in-production |
| T6 | Lazyweb, social proof share: https://design.lazyweb.com/blog/what-percent-of-paywalls-show-social-proof.md |
| T7 | Lazyweb, plan counts: https://design.lazyweb.com/blog/how-many-plan-options-do-mobile-paywalls-show |
| T8 | Superwall, 5 paywall patterns: https://superwall.com/blog/5-paywall-patterns-used-by-million-dollar-apps |
| T9 | RevenueCat, paywall redesign case studies: https://www.revenuecat.com/blog/growth/paywall-redesigns-case-studies.md |
| T10 | Superwall, multi-page paywalls convert 37% better: https://superwall.com/blog/new-postmulti-page-onboarding-paywalls-convert-37-better-than-single-page-heres-why |
| T11 | Botsi, Finch flow: https://www.botsi.com/resources/flows/apps/finch |
| T12 | ScreensDesign, paywall examples 2026: https://screensdesign.com/articles/mobile-app-paywall-design-examples-2026/ |
| T13 | RevenueCat, how top apps approach paywalls: https://www.revenuecat.com/blog/growth/how-top-apps-approach-paywalls.md |
| T14 | Retention.blog, 10 onboarding tests: https://www.retention.blog/p/10-tests-for-onboarding |
| T15 | RevenueCat, web-to-app funnel: https://www.revenuecat.com/blog/growth/web-to-app-onboarding-funnel |
| T16 | Blinkist paywall write-up: https://b2bpricinginsights.substack.com/p/4-min-read-how-blinkists-new-paywall |
| T17 | Lazyweb, trial timeline prevalence: https://experiments.lazyweb.com/research/paywall-trial-timeline-ui-prevalence.md |
| T18 | Superwall, Cal AI case study: https://superwall.com/case-studies/cal-ai |
| T19 | SonoBuddy founder note: https://github.com/aminayawork-tech/Sonobuddy/pull/316 |
| T20 | Apple Developer Forums 841626: https://developer.apple.com/forums/thread/841626 |
| T21 | RevenueCat, RIP toggle paywall: https://www.revenuecat.com/blog/growth/rip-toggle-paywall |
