# Paywall playbook: what converts, and the sources

How to read this. Every claim names its evidence: `benchmark` (aggregate data
across many apps), `case study` (one app's reported result) or `practice`
(practitioner consensus with no published number). A number without a source
never appears here. Use it three ways: to plan a round (which levers a
variation pulls), to judge one (the rubric in section 11), and to plan an A/B
set (section 10).

## 1. Order: value before price

**Claim.** The recommended paywall content order, top to bottom, is hero image or video, then benefit copy, then pricing options, then the purchase button, then legal links (terms, restore). [S10] (practice)
**Do:** lead with the outcome and only reveal price after value has been shown.
**Don't:** open on a price or plan grid before the user has seen what they're buying.

**Claim.** Adding video to a paywall drove a large revenue increase for a fitness app (about 80% revenue increase after adding paywall video), and moving a paywall before onboarding with video sharply increased reach for another app (+50% paywall views, install-to-trial conversion doubled). [S17][S33] (case study)
**Do:** test a short, outcome-demonstrating video as the hero element.
**Don't:** credit video alone for the second result; that test also moved the paywall's position.

**Claim.** Multi-page (multi-step) onboarding paywalls convert 37% better than single-page paywalls (12.41% vs 9.07%, across 40M+ onboarding paywall opens). [S13] (benchmark)
**Do:** consider spreading hero, proof and plan choice across a few steps before the price screen.
**Don't:** assume a single long page is automatically simpler for the user; test the split.

**Claim.** A radically simplified single-page paywall (image, headline, CTA) beat a detailed feature-comparison-chart paywall by 111% higher conversion. [S16] (case study)
**Do:** default to a simple hero and CTA, and add detail only once it's tested.
**Don't:** assume more information always helps; here it lost by a wide margin.

**Claim.** A free-vs-pro feature comparison table on a paywall lifts both trial starts (+18%) and paid conversion (+15%); 52% of top 100 apps use one. [S34] (benchmark)
**Do:** test a comparison table where users need to see what "pro" unlocks.
**Don't:** treat this and the simplicity result above as settled in the same direction: one case study found removing detail winning, one benchmark found a comparison table winning. Test both structures rather than assuming either wins by default.

## 2. Trial framing

**Claim.** A trial-timeline design that states the trial length, the cancel-by date and promises a reminder before billing increased trial signups 23%, raised reminder opt-in from 6% to 74%, and cut related support complaints 55%. [S5] (case study)
**Do:** show the exact date billing starts, and offer an opt-in reminder next to the CTA.
**Don't:** leave the charge date implicit or assume users remember the trial length unprompted.

**Claim.** Practitioner tooling defaults the pre-billing reminder to one day before a trial ends, on the reasoning that a warned user can cancel cleanly instead of disputing the charge afterward. [S8][S9][S21] (practice)
**Do:** send or surface a reminder before the trial converts, and make the lead time configurable.
**Don't:** let the first notice of billing be the charge itself.

**Claim.** Letting users toggle the free trial on or off themselves, rather than always defaulting them into it, is a practitioner-recommended testable variant. [S11] (practice)
**Do:** add a trial on/off control beside the plan choice.
**Don't:** assume toggle-on always wins; no isolated lift number for this lever alone has been published.

**Claim.** Longer free trials convert better, peaking in the 17 to 32 day range (45.7% median trial-to-paid conversion). [S3] (benchmark)
**Do:** test trial lengths in the multi-week range rather than defaulting to something very short.
**Don't:** assume one universal optimal length; no source gives a single best length across categories.

**Claim.** Trials longer than 4 days show conversion rates exceeding 60% for top-quartile apps. [S15] (practice)
**Do:** consider a trial length above 4 days when the offer supports it.
**Don't:** expect a typical (non-top-quartile) app to hit that conversion rate just by lengthening the trial. [S15]

**Claim.** Adding a short free trial to a weekly plan sharply increased that plan's lifetime value versus the same plan with no trial: $7.40 to $54.50 (+636%). [S7] (benchmark)
**Do:** pair a trial with whichever plan most needs an LTV boost, not only the annual plan.
**Don't:** assume this lift generalizes to every plan type without testing it there too.

**Claim.** Roughly three in ten annual subscribers cancel within their first month, which argues for setting trial and billing expectations clearly up front. [S3] (benchmark)
**Do:** restate what's billed and when at the moment of purchase, not only during the trial.
**Don't:** treat the sale as won once the trial starts.

## 3. Plan structure and anchoring

**Claim.** Two-plan paywalls are the dominant layout across app categories (41 to 60% of paywalls show exactly two plans), though single- and multi-plan adoption vary sharply by vertical: Shopping shows 40% single-plan, Health & Fitness shows 60% multi-plan. [S2][S31] (benchmark)
**Do:** default to two plans unless your category's own numbers say otherwise.
**Don't:** copy another vertical's plan count without checking category norms first.

**Claim.** Offering more pricing options increases conversion with diminishing returns: 2 products beat 1 by 61%, and 3 beat 2 by 44%, across 32M+ paywall interactions. [S14] (benchmark)
**Do:** test adding a second and third plan before concluding one plan is enough.
**Don't:** keep adding plans past three expecting the same rate of lift; it diminishes.

**Claim.** Among paywall A/B test categories, changing the number of plans shown is the single highest-win-rate lever for lifetime value (57.1% win rate). [S7] (benchmark)
**Do:** prioritize a plan-count test early in a testing roadmap.
**Don't:** rank plan-count below cosmetic levers like color or icon choice.

**Claim.** One documented high-converting price-anchoring setup pairs a monthly plan at $18.99 against a cheap weekly plan at $5.99 as the anchor. [S7] (benchmark)
**Do:** show the anchor plan alongside the target plan so the price contrast reads visually.
**Don't:** anchor against a plan so cheap that it becomes the obvious pick instead of the decoy.

**Claim.** Practitioner pattern: price the monthly plan deliberately high, not to sell it, but to make the annual plan look cheap by comparison. [S12] (case study)
**Do:** set the monthly price high enough that the annual plan reads as an obvious discount.
**Don't:** price the monthly plan so high it looks punitive or damages trust in the offer.

**Claim.** Cheap annual plans retain subscribers far better than expensive monthly plans over a year (36.0% vs 6.7% one-year retention). [S3] (benchmark)
**Do:** weigh annual-plan retention, not just paywall conversion, when picking the default plan.
**Don't:** optimize only for which plan converts more clicks at the paywall.

**Claim.** Preselecting the default plan is one of the strongest levers on which plan people buy, but the cheapest-looking default can win conversion while reducing total revenue. [S36] (practice)
**Do:** choose the default deliberately for the metric you're optimizing, and name that choice in notes.
**Don't:** default to the cheapest plan just because it wins clicks.

**Claim.** Price-only A/B tests rarely move conversion (28.3% win rate), and only a small minority of apps use promotional or discount offers on their paywall at all (9.3%). [S7][S4] (benchmark)
**Do:** treat a bare price change as a low-priority test; spend test budget on plan count, trial and layout first.
**Don't:** expect a price-only change to reliably move conversion.

**Claim.** Win-rate ranking of monetization test types by LTV uplift: localization ranks highest (62.3% win rate), then trial structure (59.6%), plan duration (58.7%), price (45.5%), with visual and copy tests ranking lowest (34.6%). [S7] (benchmark)
**Do:** prioritize trial-structure and plan-duration tests over visual-only or copy-only tests when optimizing for lifetime value.
**Don't:** treat this 45.5% LTV win-rate figure for price as the same number as the 28.3% price-conversion win-rate above; they measure different outcomes (LTV vs conversion) from the same source and shouldn't be combined into one figure. [S7]

**Claim.** Offer/plan-matrix changes, price, trial and plan mix changed together, are described as the single biggest paywall lever (10 to 40% range, "sometimes much more"). [S32] (practice)
**Do:** when testing budget is limited, bundle plan, trial and price changes into one offer-matrix test rather than isolating one variable.
**Don't:** expect to cleanly attribute the resulting lift to any single element; this claim bundles price, trial and plan changes together.

## 4. Proof

**Claim.** High-revenue app paywalls use specific, large user-count and star-rating proof rather than vague claims: Speak cites 5 million users and a 4.8-star rating from 140,000+ reviews, alongside Flo and YAZIO using testimonials and ratings. [S12] (case study)
**Do:** use your own real numbers, refreshed as they grow, instead of vague claims like "loved by users."
**Don't:** invent or round a proof number you can't stand behind.

**Claim.** Social-proof tests (testimonial or rating) move conversion more for unknown brands than for well-known ones, with a successful lift of 5 to 15%. [S32] (practice)
**Do:** weight proof heavily for a new or low-recognition app.
**Don't:** assume a well-known brand needs the same proof investment as a newcomer.

**Claim.** Leading a food/diet app's paywall with a 5-star review plus a specific outcome stat (86% of users improved their diet) raised trial conversion 72%. [S6] (case study)
**Do:** pair a rating with one concrete, checkable outcome statistic.
**Don't:** use an outcome stat you can't source or that isn't representative of typical users.

**Claim.** Redesigning a driver-license-prep app's paywall with a trial toggle and real App Store reviews as social proof raised ARPU 17.02%. [S6] (case study)
**Do:** pull actual store reviews rather than written testimonials when they're available.
**Don't:** attribute this ARPU lift to proof alone; the redesign changed the trial toggle at the same time.

**Claim.** In Japan and other Asia-market paywalls, social proof, testimonials and trust indicators are treated as essential because users look for third-party validation before purchasing. [S15] (practice)
**Do:** raise proof density for markets where third-party validation is expected.
**Don't:** ship one global proof density without checking market norms.

**Claim.** A recurring carousel or "stories"-style hero pattern, auto-advancing through benefits or reviews, appears on production paywalls, observed in ROI and Pestle. [S22] (practice)
**Do:** consider an auto-advancing hero as a proof-delivery format, not only a static block.
**Don't:** auto-advance so fast that a reader can't finish a claim.

## 5. Risk reversal

**Claim.** Cancel-anytime risk-reversal copy is treated as a low-cost, broadly applicable paywall addition, described as nearly effortless to add. [S16] (case study)
**Do:** add plain "cancel anytime" language (or equivalent) near the CTA by default.
**Don't:** skip it as minor; it costs little and is treated as broadly beneficial.

**Claim.** Cal AI's paywall reassures users with prominent "No Payment Due Now" copy placed near the CTA, alongside "Cancel anytime" microcopy. [S12] (case study)
**Do:** state when, or whether, the card is charged directly next to the action button.
**Don't:** bury payment timing in fine print far from the CTA.

## 6. The call to action

**Claim.** Simplifying the CTA button from a plan-specific label to a single word ("Continue") improved conversion 10% over plan-name CTAs. [S16] (case study)
**Do:** test a generic action word against a plan-specific label.
**Don't:** assume more descriptive CTA copy always helps; here it lost.

**Claim.** Superwall's own recommended CTA-copy test set is "Start free trial" vs. "Continue" vs. "Try [product] free for 7 days," offered as a suggested test rather than a reported result. [S12] (case study)
**Do:** run this three-way test before inventing new CTA copy from scratch.
**Don't:** present it as a proven winner; the source calls it a suggested test, not a result.

**Claim.** CTA copy and offer-framing tests produce smaller but compounding gains, with a successful lift of 2 to 10%. [S32] (practice)
**Do:** stack small CTA-copy wins across many tests rather than expecting one big win.
**Don't:** expect a CTA copy change alone to fix a weak paywall.

## 7. Personalisation

**Claim.** Adding a single onboarding question that builds credibility (for example "How did you hear about us?" with options like doctor, TV, friend, scientific article) before the paywall raised conversion for a health app roughly 10%. [S20] (case study)
**Do:** add one credibility-building question ahead of the paywall, tied to your category's trust signals.
**Don't:** add many onboarding questions expecting a proportionally bigger effect; only this one is sourced.

**Claim.** A two-person team built a fitness and calorie app with an extensive personalized onboarding flow (25-plus cards) before its paywall and scaled it to over 15 million downloads and over 30 million dollars in ARR in under two years before acquisition (Cal AI, acquired by MyFitnessPal). [S20] (case study)
**Do:** treat a long, personalized onboarding as a viable strategy, not just a UX cost.
**Don't:** assume scale alone proves the personalization, and not the product, drove the result; this is one case study.

**Claim.** Redesigning onboarding (trimmed copy, a clearer value proposition) ahead of the paywall, without personalizing per answer, drove ARPU up 102% and total revenue up 50% over four months, with activation revenue up 414%. [S18] (case study)
**Do:** try clarity and brevity first; this result came from onboarding changes, not per-answer personalization.
**Don't:** conflate "personalized onboarding" with "shorter, clearer onboarding"; they're different levers with different evidence.

**Claim.** Running dozens of paywall A/B tests (packaging, billing cycle, intro offers, win-back) without engineering support doubled revenue over a year (42 tests, 2x revenue in 12 months). [S19] (case study)
**Do:** budget for a steady cadence of small tests rather than one big personalization project.
**Don't:** expect a single redesign to match a year of compounding tests.

**Claim.** Headline and value-proposition changes are one of the higher-leverage single-element paywall tests, with a successful lift of 5 to 20%. [S32] (practice)
**Do:** name the user's outcome in the headline plainly, and test that before decoration.
**Don't:** read this 5 to 20% figure [S32] as support for per-answer headline personalization specifically; that tactic is practice-level guidance only, with no published lift number (the research could not source one).

## 8. Urgency, delays and dark patterns

A delayed close, a countdown or a "one time offer" can slide from urgency into a dark pattern the moment it stops being honest or becomes hard to exit.

**Claim.** Delaying the close ("X") button for a few seconds after the paywall appears is a recognized practitioner tactic to increase read-through and subscription likelihood, with no published number isolating its effect. [S35] (practice)
**Do:** cap the delay at a few seconds and always reveal the close control afterward.
**Don't:** hide the close control indefinitely, or disguise it as something else.

**Claim.** FTC staff have flagged countdown timers implying a purchase deadline as a recognized dark pattern: "countdown timers designed to make consumers believe they only have a limited time." [S29] (practice)
**Do:** only run a countdown for a genuinely time-bound offer, and let it expire honestly.
**Don't:** run a countdown that resets on reload or that never actually expires.

**Claim.** FTC staff and a live enforcement case both flag deliberately hard-to-find or multi-step cancellation flows as a dark pattern: "made it extremely difficult to cancel free trials and subscription plans." [S29][S30] (practice)
**Do:** make cancellation as easy to find as the purchase path itself.
**Don't:** interpose multiple retention offers between a user and completing cancellation: FTC v. Amazon challenged exactly this ("redirected to multiple pages that presented several offers to continue the subscription"). [S30]

**Claim.** A checkout button that failed to clearly disclose it also enrolled the consumer in a paid subscription was found deceptive by the FTC. [S30] (practice)
**Do:** state on or beside the CTA that tapping it starts a paid subscription.
**Don't:** let a generic "Continue" or "Get Started" label silently start billing.

Flag any variation that uses one; the pick question names it.

## 9. Rules that bind every paywall

**Apple 3.1.1: in-app purchase required.** Content or functionality unlocked in the app must be sold through Apple's in-app purchase, not an outside mechanism: "you must use in-app purchase." [S23] Apps may not use license keys, QR codes, crypto wallets or similar workarounds to unlock paid content instead of IAP: "Apps may not use their own mechanisms to unlock content or functionality." [S23]

**The US storefront exception, 3.1.1(a).** In the US storefront, apps do not need Apple's external-link entitlement to include external purchase buttons, links or calls to action: "not required for developers to include buttons, external links, or other calls to action." [S23] Outside that exception, developers can apply for an entitlement to link to their own site for these purchases: "may apply for entitlements to provide a link in their app." [S23]

**Apple 3.1.2(a) and (c): subscription terms.** Auto-renewable subscriptions are permitted in any app category: "Apps may offer auto-renewable in-app purchase subscriptions, regardless of category." [S23] The subscription period must last at least seven days and work across the user's devices: "the subscription period must last at least seven days and be available across." [S23] Before asking someone to subscribe, the app must clearly describe what they get for the price: "you should clearly describe what the user will get for the price." [S23]

**Trial disclosure.** A free trial's length, and the price charged once it ends, must be clearly stated before purchase: "Clearly indicate how long the free trial lasts and the price billed." [S24]

**Billed amount is the most prominent price (Apple subscription guidance).** On a subscription purchase screen, the total amount to be billed must be the single most visually prominent price shown: "amount that will be billed must be the most prominent pricing element." [S24] Any discount or per-period comparison price must be smaller and subordinate: "should be displayed in a subordinate position and size to the annual price." [S24]

**Google Play subscription policy.** Developers must clearly and explicitly disclose offer terms, subscription cost and billing-cycle frequency: "clearly and explicitly disclosing your offer terms, the cost of your subscription." [S25] Apps must not mislead users about any subscription service or content offered: "must not mislead users about any subscription services or content." [S25] A subscription's name must not misrepresent the offer, for example it cannot be called "Free Trial": "don't name your subscription 'Free Trial'." [S26] Terms must be visible without an extra tap to reveal them: "Users should not have to perform any additional action to review the information." [S26]

**Auto-renewal disclosure near the consent button, California ARL (BPC section 17602).** California requires automatic-renewal or continuous-service terms be shown clearly and conspicuously before the deal is completed: "in a clear and conspicuous manner." [S27] Those terms must sit in visual proximity to the button the consumer uses to consent: "in visual proximity to the request for consent to the offer." [S27] A business must get the consumer's affirmative consent to the auto-renewal terms before charging their card: "without first obtaining the consumer's affirmative consent to the agreement." [S27]

**FTC negative-option rule, status as of 2026.** The FTC's 2024 "click-to-cancel" negative-option rule has been struck down in full and is not currently in force: "we grant the petitions for review and vacate the Rule." [S28] The Eighth Circuit vacated it only for a procedural defect, not on the underlying consumer-protection merits: "the procedural deficiencies of the Commission's rulemaking process are fatal here." [S28] The FTC is redoing this rulemaking from scratch rather than the vacated rule being back in effect: "issuing an advance notice of proposed rulemaking." [S28]

## 10. A/B levers, ranked

1. **Single vs multi-page.** Vary whether the paywall is one screen or a short sequence of steps before pricing: multi-page onboarding paywalls convert 37% better than single-page (12.41% vs 9.07%). [S13]
2. **Plan layout.** Vary plan count and arrangement: a second and third plan lift conversion 61% and 44% over the prior count, two plans is the dominant layout industry-wide, and plan-duration tests rank among the higher-win-rate categories for LTV (58.7%). [S14][S2][S31][S7]
3. **Trial length display.** Vary whether the trial timeline (length, charge date, reminder) is shown explicitly: doing so raised trial signups 23% in one case study, and trial-structure tests as a category rank second-highest for LTV win rate (59.6%), just behind localization. [S5][S7]
4. **Trial toggle.** Vary whether the trial is on by default or user-selected: a trial-structure lever, the category S7 rates second-highest for LTV win rate (59.6%); no isolated lift number for the toggle alone is published. [S7][S11]
5. **Default plan.** Vary which plan is preselected: a plan-related lever in the category S7 rates 58.7% for LTV win rate; no clean isolated percentage for default-plan preselection specifically is published, and the cheapest-looking default can win conversion while cutting revenue. [S7][S36]
6. **Proof type.** Vary which proof leads (rating, review, outcome stat): a rating plus a specific outcome stat raised trial conversion 72% in one case study. [S6][S12]
7. **CTA copy.** Vary the button label: simplifying to a single word lifted conversion 10% in one case study, and copy/framing tests compound 2 to 10% more broadly; visual and copy tests are the lowest-win-rate category for LTV (34.6%), which is why this sits below the trial and plan levers above. [S16][S32][S7]
8. **Headline.** Vary the outcome named in the headline: headline and value-proposition changes are a higher-leverage single-element test, 5 to 20% successful lift, though visual and copy tests as a category rank lowest for LTV win rate (34.6%). [S32][S7]
9. **Close delay.** Vary how long the close (X) button is disabled: a recognized practitioner tactic to raise read-through, with no published isolated lift. [S35]
10. **Proof position.** Vary whether proof sits above or below the CTA/price. (practice) No reported result was found for position in isolation; treat it as untested.
11. **Price display (billed vs per-period).** Vary only the subordinate per-period breakdown; the billed amount's prominence is fixed by Apple's rule (section 9). (practice) No conversion-tested lift was found for the display format itself.

## 11. Scoring rubric

Answer each for every variation; the count of yes is its score. `agentPick`
is the highest score; ties go to the variation whose archetype or lever has
the better live number in `performance.md`. The pick question cites the line
that decided it.

1. Value is clear before the price: the headline names the outcome, not the product.
2. The billed amount is the most prominent price; breakdowns are smaller and subordinate.
3. There is one primary action; any second purchase path is visibly secondary.
4. Trial terms (length, what is charged, when) sit next to the CTA.
5. Proof is specific and real (from the proof list) and sits before the price or beside the CTA.
6. Risk reversal is in plain words near the CTA.
7. The default plan is the one the offer wants chosen, and the selected state is unmistakable.
8. The first viewport holds headline, value or proof, price and CTA without scrolling.
9. Dismissing is visible from the first frame; any delay is flagged per section 8.
10. Nothing fails section 9: renewal terms, restore, terms and privacy are present and legible.

## Sources

| id | Source | URL | Date | Strength |
|---|---|---|---|---|
| S2 | State of Subscription Apps 2026 — Business report (RevenueCat) (accessed 2026-09) | https://www.revenuecat.com/state-of-subscription-apps-2026-business/ | 2026-09 | benchmark |
| S3 | State of Subscription Apps 2025 (RevenueCat) | https://www.revenuecat.com/state-of-subscription-apps-2025 | 2025-03-14 | benchmark |
| S4 | "2.1% vs 10.7%: the paywall data that changes the strategy" (Neoads, citing RevenueCat 2026 data) | https://neoads.substack.com/p/hard-paywalls-convert-less-but-earn | 2026-03-13 | benchmark |
| S5 | "How Solving Our Biggest Customer Complaint at Blinkist Led to a 23% Increase in Conversion" (Growth.Design case study) | https://growth.design/case-studies/trial-paywall-challenge | 2021-01-19 | case study |
| S6 | "How four paywall redesigns boosted conversions and revenue" (RevenueCat blog) | https://www.revenuecat.com/blog/growth/paywall-redesigns-case-studies | 2025-03-27 | case study |
| S7 | "What does a high-performing paywall look like in 2026?" (Adapty, State of In-App Subscriptions 2026) | https://adapty.io/blog/high-performing-paywall-2026/ | 2026-03-13 | benchmark |
| S8 | Superwall docs — "Free Trials" (accessed 2026-09) | https://superwall.com/docs/framework/trials | 2026-09 | practice |
| S9 | Superwall — "Free Trial Reminders" feature page (accessed 2026-09) | https://superwall.com/features/free-trial-reminders | 2026-09 | practice |
| S10 | "How to Design a Perfect Paywall for a Mobile App" (Airbridge) | https://www.airbridge.io/blog/perfect-mobile-paywall | 2022-12-21 | practice |
| S11 | "Subscription App Onboarding: Get 100% of Users to Your Paywall" (Airbridge) | https://www.airbridge.io/en/blog/subscription-app-onboarding | 2023-02-16 | practice |
| S12 | "5 Paywall Patterns Used By Million-Dollar Apps" (Superwall blog) | https://superwall.com/blog/5-paywall-patterns-used-by-million-dollar-apps | 2025-08-15 | case study |
| S13 | "Multi-page onboarding paywalls convert 37% better than single-page. Here's why" (Superwall blog) | https://superwall.com/blog/new-postmulti-page-onboarding-paywalls-convert-37-better-than-single-page-heres-why | 2026-05-26 | benchmark |
| S14 | "How many products should you offer on your paywall?" (Superwall blog) | https://superwall.com/blog/how-many-products-should-you-offer-on-your-paywall | 2022-11-14 | benchmark |
| S15 | "The essential guide to mobile paywalls for subscription apps" (RevenueCat blog) | https://www.revenuecat.com/blog/growth/guide-to-mobile-paywalls-subscription-apps | 2024-12-05 | practice |
| S16 | "The paywall tactics behind $100K/month apps" (Superwall blog) | https://superwall.com/blog/the-paywall-tactics-behind-usd100k-month-apps | 2026-02-12 | case study |
| S17 | "Video Paywalls for Subscription Apps: How to Increase Conversion" (RevenueCat blog) | https://www.revenuecat.com/blog/growth/video-paywalls | 2025-11-25 | case study |
| S18 | "How onboarding & pricing tests doubled revenue per user" (Adapty case study) (accessed 2026-09) | https://adapty.io/case-studies/travel-app/ | 2026-09 | case study |
| S19 | "How Feeld doubled revenue with paywall A/B testing" (Adapty case study) (accessed 2026-09) | https://adapty.io/case-studies/feeld/ | 2026-09 | case study |
| S20 | "How to personalize app onboarding and paywalls" (Adapty blog) (accessed 2026-09) | https://adapty.io/blog/how-to-personalize-onboarding-and-paywalls-in-your-mobile-app/ | 2026-09 | case study |
| S21 | "How to add trial notifications to your subscriptions" (RevenueCat blog) (accessed 2026-09) | https://www.revenuecat.com/blog/engineering/how-to-add-trial-notifications-to-your-subscriptions | 2026-09 | practice |
| S22 | "20 live iOS paywalls and what to learn from them" (Superwall blog) | https://superwall.com/blog/20-ios-paywalls-in-production | 2024-03-12 | practice |
| S23 | App Review Guidelines (Apple) (accessed 2026-09) | https://developer.apple.com/app-store/review/guidelines/ | 2026-09 | practice |
| S24 | App Store Subscriptions — design guidance (Apple) (accessed 2026-09) | https://developer.apple.com/app-store/subscriptions/ | 2026-09 | practice |
| S25 | Subscriptions policy (Google Play Console Help) | https://support.google.com/googleplay/android-developer/answer/9900533 | 2025-10 | practice |
| S26 | Create and manage subscriptions (Google Play Console Help) (accessed 2026-09) | https://support.google.com/googleplay/android-developer/answer/140504 | 2026-09 | practice |
| S27 | California Business and Professions Code § 17602 (accessed 2026-09) | https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=BPC&sectionNum=17602 | 2026-09 | practice |
| S28 | Custom Communications, Inc. v. FTC, No. 24-3137 (8th Cir.) | https://ecf.ca8.uscourts.gov/opndir/25/07/243137P.pdf | 2025-07-08 | practice |
| S29 | FTC Staff Report — "Bringing Dark Patterns to Light" | https://www.ftc.gov/system/files/ftc_gov/pdf/P214800%20Dark%20Patterns%20Report%209.14.2022%20-%20FINAL.pdf | 2022-09-14 | practice |
| S30 | FTC Press Release — "FTC Takes Action Against Amazon" | https://www.ftc.gov/news-events/news/press-releases/2023/06/ftc-takes-action-against-amazon-enrolling-consumers-amazon-prime-without-consent-sabotaging-their | 2023-06 | practice |
| S31 | State of Subscription Apps 2026 — report landing page (RevenueCat) (accessed 2026-09) | https://www.revenuecat.com/state-of-subscription-apps | 2026-09 | benchmark |
| S32 | "The Paywall Growth Lever Framework" (Superwall blog) | https://superwall.com/blog/the-paywall-growth-lever-framework-how-to-build-smarter-experiments-faster | 2026-05-29 | practice |
| S33 | "8 paywall test ideas to grow app revenue" (RevenueCat blog) | https://www.revenuecat.com/blog/growth/paywall-tests-grow-app-revenue | 2023-09-15 | case study |
| S34 | "10 types of mobile app paywalls and conversion hacks they use" (Adapty blog) | https://adapty.io/blog/the-10-types-of-mobile-app-paywalls/ | 2025-12-18 | benchmark |
| S35 | "How to Successfully Optimize Paywall Conversion Rates with UX?" (Momentum blog) | https://www.themomentum.ai/blog/how-to-successfully-optimize-paywall-conversion-rates-with-ux | 2023-03-13 | practice |
| S36 | "Paywall experiments playbook: What to test first, second, third" (Adapty blog) (accessed 2026-09) | https://adapty.io/blog/paywall-experiments-playbook/ | 2026-09 | practice |
