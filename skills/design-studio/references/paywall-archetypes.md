# Paywall archetypes

An archetype is a paywall's persuasion mechanism: the one reason it expects a
user to start a trial. A `concepts` round shows ten different archetypes; a
`concept` round shows one archetype executed ten ways, varying its **Axes**.
The slug of a name (`trial-timeline`) is the `manifest.archetype` value.
Citations point at the Sources table in `paywall-playbook.md`.

## 1. Trial timeline

**Mechanism:** naming the exact charge date and promising a reminder removes the fear of a silent charge, which is what actually blocks a trial start. [S5]
**Anatomy:** hero benefit line, then a horizontal timeline (today, mid-trial, charge date), then a reminder opt-in toggle next to the CTA, then legal.
**Wins when:** the app has a trial to sell and the audience has been burned by silent renewals before (health, finance, subscription-fatigued categories).
**Loses when:** there is no trial at all; a timeline with nothing to count down to is just clutter.
**Axes:** timeline orientation (horizontal bar, vertical steps, calendar grid) · number of milestones shown (2, 3, 4) · reminder framing (silent default, opt-in toggle, opt-out toggle) · timeline color coding (single accent color throughout, color shifts at the charge point, neutral until the final milestone) · charge-date emphasis (date only, date plus price, date plus price plus cancel link) · icon style per milestone (none, line icon, filled badge).
**Hazards:** the reminder must actually fire before charging, not just promise to; a fake or missing reminder breaks the reminder practice this archetype is built on (playbook section 2), and misstating the trial length or charge date also breaks the trial-disclosure rule and California's auto-renewal consent rule (playbook section 9). [S24][S27]
**Seen in:** BoldVoice [S37]

## 2. Testimonial wall

**Mechanism:** a dense wall of real names and quotes reads as social consensus, which the research shows matters more for a brand no one has heard of yet. [S32]
**Anatomy:** headline, then a scrollable or static grid of quote cards (name, quote, optional rating), then price and CTA below the wall.
**Wins when:** the app is new or low-recognition and needs third-party validation to close the trust gap. [S32]
**Loses when:** the app already has strong brand recognition; the wall's lift is smaller for well-known brands. [S32]
**Axes:** wall layout (grid, single-column stack, horizontal carousel) · quote count shown (3, 5, 8+) · identity shown per quote (first name, first name plus location, verified badge) · quote length (one line, two lines, short paragraph) · rating display (stars only, stars plus count, no rating) · wall position relative to CTA (above, below, interleaved).
**Hazards:** quotes and names must be real and attributable, not invented or composited; a fabricated testimonial is a deceptive-practice risk under the same honesty standard the playbook applies to dark patterns (playbook section 8).
**Seen in:** Studley [S37]

## 3. Rating hero

**Mechanism:** leading with a large star rating and review count borrows the credibility of an app-store consensus before the user reads anything else. [S12]
**Anatomy:** oversized rating number and stars at the very top, review-count subhead, then benefit copy, then price and CTA.
**Wins when:** the app has a genuinely strong, large-sample store rating to show off.
**Loses when:** the rating is new, thin, or mediocre; a small or middling number undercuts the whole mechanism.
**Axes:** rating display size (headline-scale, medium, inline with logo) · supporting proof (review count only, review count plus user count, review count plus a named publication) · star rendering (filled stars, numeric score, both) · background treatment behind the rating (flat color, gradient, blurred app screenshot) · position of the rating relative to hero art (above, overlaid, beside) · secondary proof line (none, one outcome stat, one quote).
**Hazards:** the rating and review count shown must match the current live store listing; a stale or rounded-up number is a proof-integrity risk the playbook's proof claims warn against reusing without your own real numbers. [S12]
**Seen in:** Fastic [S38]

## 4. Feature checklist

**Mechanism:** a literal checklist of what unlocks makes "pro" concrete and scannable, converting an abstract upgrade into a list of specific things the user gets. [S12]
**Anatomy:** headline naming the plan, then a vertical list of checkmarked features, then price and CTA below the list.
**Wins when:** the product has many distinct, nameable features and the buyer is evaluating capability rather than a single outcome.
**Loses when:** the product's value is really one big outcome; a long feature list dilutes a single strong benefit and a simplified single-benefit paywall has outperformed a detailed comparison chart by a wide margin. [S16]
**Axes:** list length (4, 6, 8+ items) · checkmark style (simple check, filled circle check, icon per feature) · grouping (flat list, grouped by category with subheads) · comparison mode (pro-only list, free-vs-pro two-column) · item density (icon plus one line, icon plus title plus description) · list container (plain list, card, table with divider rows).
**Hazards:** none beyond the general pricing-prominence rule in section 9: if a comparison table sits above the price, the actually-billed amount still has to be the most prominent price on screen. [S24]
**Seen in:** ClassDojo [S12]

## 5. Free vs Pro table

**Mechanism:** a side-by-side comparison table lets the user see exactly what they lose by staying free, which the research ties to a real lift in both trial starts and paid conversion. [S34]
**Anatomy:** two-column header (Free, Pro), then a row per feature with check/cross or value per column, then price and CTA under the Pro column.
**Wins when:** the app already has a real free tier worth comparing against, and the buyer is feature-literal (productivity, fitness tracking, utility apps).
**Loses when:** there's no meaningful free tier, or the list would be mostly crosses under "Free," which reads as punitive rather than motivating.
**Axes:** row count (5, 8, 12+) · row value type (check/cross, numeric limit vs. unlimited, short text) · column emphasis (equal-weight columns, Pro column highlighted/wider) · table style (full-width table, card-per-row, accordion) · header treatment (plain labels, Pro column badge like "Recommended") · value icon style (checkmark/cross glyphs, colored dot indicators, text-only "Yes"/"No").
**Hazards:** none beyond the pricing-prominence rule in section 9 (the actually-billed price must outrank any per-row or per-period figure in visual weight). [S24]
**Seen in:** Hevy [S37]

## 6. Personalised plan

**Mechanism:** reflecting the user's own onboarding answers back as "your plan" builds credibility because the offer now looks built for them specifically, not generic; this is practice reasoning, not a sourced claim, since the research covers a single credibility-building onboarding question, not per-answer paywall personalization.
**Anatomy:** headline referencing the user's stated goal, a plan visual built from their inputs (chart, schedule, or summary card), then price and CTA.
**Wins when:** onboarding already collects goal- or preference-level answers (weight, habit, skill-level) that can be reflected back convincingly.
**Loses when:** onboarding is thin or generic; a "personalized" plan built from one shallow question reads as a gimmick rather than a real reflection of the user.
**Axes:** personalization depth (one input reflected, two to three combined, full profile summary) · plan visual (text summary, chart, calendar/schedule) · reflection framing ("Your plan" vs. "Recommended for you" vs. named-goal headline) · confidence signal (none, "based on N answers," a small quiz-recap strip) · edit affordance (none, "change your answers" link) · plan length shown (single duration, multiple duration options).
**Hazards:** the reflected data must be true to what the user actually answered; inventing or exaggerating a personalization signal that wasn't really used is a deceptive-design risk in the same family as the playbook's dark-pattern honesty standard (playbook section 8).
**Seen in:** Noom [S39]

## 7. Outcome projection

**Mechanism:** projecting a future result on a chart or timeline turns an abstract benefit into a visualized, dated outcome, which is a stronger motivator than a list of features.
**Anatomy:** headline naming the outcome, a projection chart or date marker (goal line, target date), supporting stat, then price and CTA.
**Wins when:** the category has a natural quantifiable trajectory to show (weight, sleep, savings, skill progress) and the app collected a baseline during onboarding.
**Loses when:** the product has no measurable trajectory to project; forcing a chart onto a qualitative benefit looks fabricated.
**Axes:** chart type (line trending to goal, bar comparison, calendar countdown to target date) · timeframe shown (weeks, months, a fixed target date) · baseline source (user-entered, estimated default, none shown) · supporting stat (one outcome percentage, none, a comparison to "average users") · goal marker style (dot plus label, shaded target zone, milestone flags) · color treatment (single accent line, gradient fill under curve, neutral line with highlighted goal point).
**Hazards:** any projected outcome or comparison stat must be sourced or clearly framed as an estimate, not a guarantee; the playbook's own proof guidance says not to use an outcome stat you can't source (playbook section 4) [S6], and presenting a projection as certain rather than an estimate risks the same not-misleading-users rule Google Play applies to subscription offers (playbook section 9). [S25]
**Seen in:** MyFitnessPal [S40]

## 8. Coach or mascot-led

**Mechanism:** a recurring character delivering the pitch personifies the product, which lowers the sales feeling by making the ask feel like encouragement from a familiar guide rather than a corporate upsell.
**Anatomy:** mascot or coach illustration/animation at top, speech-bubble or first-person benefit copy, then price and CTA presented as the coach's suggestion.
**Wins when:** the app already has an established mascot or coach character the user has met earlier in onboarding or daily use (language learning, habit coaching, kids' apps).
**Loses when:** there's no existing character; introducing one for the first time at the paywall feels like a costume rather than a relationship.
**Axes:** character presentation (static illustration, looping animation, short video) · copy voice (first-person as the character, third-person about the character) · character expression/pose (celebratory, encouraging, concerned-about-losing-you) · CTA framing (character "suggests" the plan vs. neutral button copy) · background setting (plain color, in-app scene, character-branded pattern) · presence of a secondary human proof element (none, alongside a testimonial, alongside a rating).
**Hazards:** none beyond the general urgency rule in section 8 if the character is used to pressure rather than encourage (e.g., a mascot expressing manufactured disappointment to guilt a decline).
**Seen in:** Duolingo [S41]

## 9. Video or carousel hero

**Mechanism:** a short outcome-demonstrating video or an auto-advancing carousel shows the product working rather than describing it, and video heroes have driven large reported revenue increases in fitness apps specifically. [S17]
**Anatomy:** full-bleed video or carousel as the hero, progress dots if a carousel, benefit copy below, then price and CTA.
**Wins when:** the product has a visually demonstrable outcome or workflow (fitness, cooking, creative tools) and can produce a short, polished clip.
**Loses when:** there's nothing visually compelling to show, or only a low-quality clip is available; a weak video can hurt more than a strong static image would.
**Axes:** hero type (single looping video, multi-slide carousel, video-then-carousel hybrid) · overlay treatment (no overlay, gradient scrim for text legibility, full color-wash overlay) · slide count if carousel (3, 5, 7) · caption style (none, short caption per slide, testimonial-style caption) · frame shape (full-bleed edge-to-edge, contained card with rounded corners, split-screen before/after) · controls visibility (hidden, visible on tap, always-visible progress bar).
**Hazards:** an auto-advancing hero must not out-pace what a reader can finish reading, and it must not be the mechanism used to visually crowd out or delay the close control (playbook section 8).
**Seen in:** FitnessAI [S33]

## 10. Single-plan hero

**Mechanism:** collapsing to one plan and one simply presented price follows the same radical-simplicity approach that beat a detailed feature-comparison-chart paywall in one case study, though that test compared page complexity (a simple hero vs. a detailed chart), not the number of plans shown. [S16]
**Anatomy:** hero benefit statement, single price line, one CTA; no plan grid or comparison at all.
**Wins when:** the brand is strong enough that a single well-priced offer doesn't need to be justified by comparison, or the goal is to remove decision friction entirely.
**Loses when:** the audience is price-sensitive or unfamiliar with the brand; the clearest benchmark on plan count runs the other way, two plans convert 61% better than one across 32M+ paywall interactions, so this archetype gives up a well-documented lever and should be tested against a two-plan version before it's trusted. [S14]
**Axes:** price presentation (per-period only, per-period plus total, total only) · layout structure (price stacked above the CTA, price and CTA side by side, price folded into the CTA button label) · CTA copy (generic "Continue," price-inclusive, benefit-named) · risk-reversal placement (directly under CTA, directly under price, both) · hero art (product screenshot, lifestyle image, abstract brand pattern) · secondary link visibility ("see other plans" link present or absent).
**Hazards:** none beyond the general billed-amount-prominence rule in section 9, which still applies even with only one plan on screen. [S24]
**Seen in:** Calm [S34]

## 11. Plan cards

**Mechanism:** presenting plans as parallel cards with one visually marked "best value" uses anchoring and a preselected default to steer the choice without hiding the other options. [S36]
**Anatomy:** two or three plan cards side by side or stacked, one badge-marked as recommended, price and cadence per card, single CTA below the cards.
**Wins when:** there are 2-3 real plan options worth comparing and a clear default the offer wants chosen.
**Loses when:** there's only one plan, or the plans are priced too close together to anchor visually against each other.
**Axes:** card count (2, 3) · layout (side-by-side, stacked vertical) · default selection (cheapest preselected, best-value preselected, none preselected) · badge treatment on the recommended card (ribbon, border highlight, background color fill) · price framing per card (total price, per-period equivalent, both) · savings callout (percent-off badge, dollar-savings line, none).
**Hazards:** the per-period breakdown shown on each card must stay visually subordinate to the actual billed total, the part of this pattern the billed-price-prominence rule actually governs (playbook section 9). [S24]
**Seen in:** Quizlet [S37]

## 12. Exit ticket

**Mechanism:** offering a discount only when the user tries to leave targets the most price-sensitive moment, recovering some users who would otherwise convert to zero.
**Anatomy:** the original paywall, then an intercept screen on close/back showing a one-time discounted offer with its own CTA and its own close control.
**Wins when:** the base offer already converts reasonably and the goal is to recover marginal price-sensitive users without discounting everyone up front.
**Loses when:** the base paywall hasn't been tested on its own yet, since an exit offer can mask a weak primary paywall instead of fixing it.
**Axes:** intercept form (full-screen takeover, bottom sheet, centered modal card) · hero visual on the intercept (product screenshot, single benefit icon, plain color field) · price display (strikethrough original price beside the new price, new price only, percent-off badge with the original price small) · offer duration shown (untimed, honestly time-boxed with a visible countdown) · number of exit steps (single intercept, one retention offer then exit) · visual urgency (plain card, accented/red treatment, animated attention grabber).
**Hazards:** must not chain multiple retention offers between the user and actually leaving, and any countdown on the offer must be real and not reset on reload; both are dark patterns the FTC has specifically challenged (playbook section 8, and the FTC v. Amazon complaint). [S29][S30]
**Seen in:** Bend [S37]

## 13. Friend gift

**Mechanism:** letting a subscriber give the app to a friend for free turns the paywall into a shareable, goodwill-driven action instead of a pure purchase ask, extending reach through the existing user base.
**Anatomy:** headline framing the gift, a friend-selection or share-link step, confirmation of what the friend receives, and the subscriber's own price/CTA nearby or on a following screen.
**Wins when:** the product has strong existing word-of-mouth or a social use case (wellness, meditation, shared habits) where gifting fits naturally.
**Loses when:** the product isn't naturally shareable or social; a bolted-on referral flow can distract from the core purchase decision without a real motivation to gift.
**Axes:** gift mechanism (referral link, in-app friend picker, redeemable code) · gift visual presentation (wrapped-gift icon and animation, plain text card, illustrated friend-pair graphic) · framing (holiday/seasonal gift, everyday referral, milestone-triggered) · visibility of the giver's own offer (shown together with the gift, shown after, separate screen entirely) · social proof of past gifting (none, "N people gifted this week") · reciprocity messaging (none, "you'll get a reward too").
**Hazards:** the terms of what the friend actually receives must be stated as clearly as the subscriber's own trial terms (playbook section 9's trial-disclosure rule applies to any complimentary access granted, not only the direct purchase).
**Seen in:** Headspace [S42]

## 14. Countdown offer

**Mechanism:** a visible countdown timer on a discount implies the price will change soon; the research does not measure whether this makes people buy faster, only that the FTC flags the pattern as a dark pattern the moment the deadline isn't real, so its use here is a practitioner tactic, not a proven lever. [S29]
**Anatomy:** offer headline, a live countdown clock, discounted price and CTA, standard legal below.
**Wins when:** the offer is genuinely time-bound (a real limited window, a real end-of-trial deadline) and the countdown reflects an actual, enforced expiration.
**Loses when:** there's no real deadline behind it; a fake or resetting countdown is exactly the pattern flagged as deceptive. [S29]
**Axes:** countdown format (digital clock, progress bar draining, calendar date only) · timer placement (top banner, floating badge near the CTA, inline within the price block) · price display (strikethrough original beside the discounted price, discounted price only, percent-off badge with the original price shown small) · expiration behavior (offer disappears entirely, reverts to standard price and stays visible, re-offered later at a different depth) · CTA styling (standard button, accent-colored button, pulsing/animated button) · background urgency treatment (neutral background, accent color wash, pulsing/animated background).
**Hazards:** Urgency ethics apply (playbook section 8): the timer must expire honestly and must not reset on reload or reappear identically on the next visit, or it becomes the countdown-timer dark pattern the FTC has explicitly named. [S29]
**Seen in:** Noom [S39]
