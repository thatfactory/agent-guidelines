# Animations

Motion should make a change understandable and an interaction feel continuous. Apply these experience requirements to app and game interfaces regardless of implementation framework. Use [User Experience](UX.md) to decide whether a change should interrupt the user and [SwiftUI animation](../Swift/SwiftUI.md#animation) for implementation policy.

These are ThatFactory quality requirements informed by Apple's [motion guidance](https://developer.apple.com/design/human-interface-guidelines/motion). They describe observable behavior without prescribing a particular layout technique, animation curve, or duration.

## Move a visual unit together

- When a surface slides, moves, or resizes as one object, its title, body, icons, background, border, and other attached decoration must remain visually attached throughout the transition. A button's label must not arrive ahead of its background or continue travelling after the button settles.
- Coordinate the surrounding layout with the content it reveals or hides. A container that grows to reveal a button should resize as the button enters; avoid expanding an empty area first and then starting a separate entrance animation. Apply the same continuity when content disappears.
- Preserve the intended visual relationship throughout intermediate frames, including when motion reverses. Matching only the start and end states is insufficient.
- Use staggered or independently moving elements only for an explicit interaction or communication purpose. Document that purpose in the consumer's design guidance; accidental differences in timing are defects, not choreography.

## Respect concealment and boundaries

- When content appears to move from behind another surface or back into a concealed region, preserve that depth relationship for its entire path. No unintended edge, stroke, text, or background may protrude beyond the concealing surface or intended reveal area.
- Check both entrance and exit, including partial visibility and rapid reversal. For example, a button sliding away beneath a field must not leave its upper outline visible above the field.
- Keep intentional shadows, focus treatment, and readable content intact. Fix the particular reveal or concealment boundary without indiscriminately cutting off valid decoration or neighbouring content.

## Reverse and interrupt gracefully

- Give the return to an earlier state the same care as the initial change. If selection smoothly introduces a checkmark or changes color, font weight, or width, deselection must remove that feedback smoothly too. Do not animate the new choice while abruptly resetting the previous one.
- For a reversible slide reveal, return content toward the concealed origin it came from. A different exit path needs an explicit interaction purpose; do not change direction accidentally between entrance and exit.
- Coordinate all visible attributes that belong to that state change. A fading checkmark does not compensate for a snapping width, background, or label position.
- If input changes before motion finishes, continue smoothly from the currently displayed state toward the latest state. Do not jump back to a starting pose, play stale queued transitions, or force the user to wait for an obsolete animation.
- A graceful reversal need not literally replay identical frames or use identical timing. Preserve the spatial relationship and continuity while keeping the response prompt. Intentional immediate feedback remains valid when it serves the interaction; record the reason instead of leaving an unexplained snap.
- Keep actions and functional state responsive throughout motion, following the framework's implementation guidance. Animation must not delay selection, cancellation, or another valid action.

## Keep unaffected surroundings stable

- A local state change must not make unchanged neighbouring controls or labels jump or drift. For example, selecting one option must not nudge an unselected option's label sideways as a checkmark appears elsewhere.
- When a change legitimately requires surrounding layout to move, make that reflow coherent with the initiating change. Distinguish intended reflow from incidental jitter; do not freeze all layout or compromise adaptation to longer text and different content sizes to hide a defect.
- Check the outgoing element, incoming element, and unchanged neighbours together. A polished animation on the selected control alone does not establish that the interaction is polished.

## Acceptance scenarios

Observe the actual interaction at normal speed, then use recordings and intermediate-frame inspection to diagnose suspected sequencing, separation, or boundary defects. Record the platform/OS, app revision, scenario, actions, and result. A source-code animation modifier, successful build, static screenshot, or settled-state comparison does not prove correct motion.

| Scenario | Required outcome |
| --- | --- |
| Reveal and hide a compound control | Attached content travels as one unit; required container resizing is coordinated |
| Move content behind a field, card, or other surface | No unintended edge or content leaks outside the concealment boundary in either direction |
| Select one option, then another | Both incoming and outgoing feedback transition smoothly; unchanged neighbours stay stable |
| Type and delete rapidly or reverse selection before motion finishes | Motion stays continuous, follows the latest state, and settles correctly without stale playback |
| Repeat with relevant longer labels and supported content sizes | Composition, concealment, and necessary reflow remain coherent |

Apply the existing [Reduce Motion policy](../Swift/SwiftUI.md#reduce-motion) to affected motion; preserve the same information and task outcome with the appropriate adaptation. Missing applicable interaction evidence or an unresolved violation above prevents [audit completion](../../.agents/skills/agent-guidelines-audit/SKILL.md#audit-animation-and-image-rendering). Documentation-only changes use scenario walkthroughs, without claiming consumer runtime verification.
