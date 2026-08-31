# Heart of Gold Bottle — WAITING (owner instruction, 2026-08-31)

Insulated pink water bottle, gold heart, bamboo lid. Submitted with two owner
photographs and **no brand and no manufacturer item number**. Owner instructed
on 2026-08-31: *"Запази този елемент в изчакване."* — hold, do not publish.

**No `PM-###` is allocated.** The next free id stays available for whatever
publishes first.

## Why it is not published

The two owner photographs never reached the working container. Attachments
earlier in the session did land on disk (the PM-042…044 package and the HOME
`.rar` were both read from `/root/.claude/uploads/`), but that directory was
lost when the container recycled at 11:41 on 2026-08-31 and was not recreated
for later attachments. The images are visible in the conversation and absent
from the filesystem, so they cannot be hashed, converted, committed, or checked
by the publication regression, which verifies every frame by SHA-256.

Media was not reconstructed from the rendered images. A published frame has to
be the owner's file, byte for byte.

## Staged record, ready to publish unchanged

| Field | Value |
|---|---|
| name | `Heart of Gold Bottle` |
| slug | `heart-of-gold-bottle` |
| category | `home` |
| brand | *omitted — none supplied* |
| manufacturerItemNo | *omitted — none supplied* |
| color | `Pink` |
| composition | `Неръждаема стомана, бамбуков капак` |
| priceEUR | `22` |
| oldPriceEUR | `null` |
| selectedBy | `null` |
| availability | `{"ONE SIZE": "available"}` |
| media.fit | `contain` |
| media.ph | `home` |
| media.field | `blush` |
| newUntil | publication date + 14 days |

Description:

> Розова термо бутилка със златно сърце и бамбуков капак. 0,5 л, двойни стени —
> топло до 12 часа, студено до 24.

Media contract — **two frames only**, by explicit owner instruction
(*"Използвай само тези две снимки"*). Precedent: PM-041 published below the
usual three-to-five frame count under the same kind of owner exception.

| Slot | Frame | Alt text |
|---|---|---|
| `media.image` | whole bottle, front | Розова термо бутилка Heart of Gold със златно сърце и бамбуков капак, цял продукт |
| `gallery[0]` | detail, heart and dotted bands | Детайл на розовата термо бутилка Heart of Gold със златно сърце и бели точковидни ленти |

The name was created for PINK MALL at the owner's request; it is not a
manufacturer model name and must not be presented as one.

`0,5 л`, `12 часа` and `24 часа` are owner-stated facts. They appear in the
description only, never as verified product fields.

## What unblocks it

The two image files reaching the container by any route that is not the
attachment channel: committed to this branch, or fetchable from a URL. On
arrival this publishes in one pass with no further questions.
