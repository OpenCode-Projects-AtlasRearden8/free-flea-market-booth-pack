# Free Flea-Market Booth Pack

Free, unbranded, print-at-home printables for running a tidy flea-market
booth — the vendor kind, where you set up a blanket or table at a public
market and sell to shoppers all day. **Not** a home garage-sale kit (see the
"Who this is for" note below).

Everything here is plain HTML/CSS that builds to clean US-Letter PDFs with one
local script. No accounts, no tracking, no server, no secrets: run it on your
own machine and print what you need.

## The eight printables

| # | Sheet | What it solves | Prints |
|---|-------|----------------|--------|
| 1 | **Blanket Layout Map** | Where the blanket, till, and item zones go — decided at home, not at 6 a.m. | 1 page |
| 2 | **Big Readable Price Signs** | $1 / $2 / $5 / $10 table signs plus fill-a-bag, make-an-offer, cash-only banners | 2 pages |
| 3 | **Price Stickers & Tag Strips** | Round stickers at tag size plus cut-apart item/size/price tag strips | 3 pages |
| 4 | **Cash Tally Log** | One line per sale; count-up to honest profit at day's end | 1 page |
| 5 | **Change-Counting Card** | Float planner, denomination quick math, till scratch space | 1 page |
| 6 | **"Sold" Ticket Stubs** | Twin half-stubs for sales and time-boxed holds | 2 pages |
| 7 | **Rain Plan Checklist** | Tarps and tubs packed, booth moves when it pours, go/no-go decided early | 1 page |
| 8 | **Load-In / Load-Out Sheet** | Box tracker, booth kit, and the day timeline with two sweeps | 2 pages, landscape |

Unbranded PDFs land in `printables/` — no logos, no watermarks, nothing
reminding you who built them mid-transaction.

## Build it (local, no accounts)

You need Python 3.10+ and [WeasyPrint](https://weasyprint.org/):

```sh
pip install weasyprint          # system deps per WeasyPrint docs
python3 build.py                # build all 8 sheets into printables/
python3 build.py cash-tally     # build one sheet
python3 build.py --clean        # wipe printables/ first
```

Outputs: `printables/<sheet-name>.pdf`.

## Test it

```sh
python3 -m pytest tests -q      # builds every sheet; checks each PDF
```

35 tests verify every sheet builds a valid, US-Letter, text-extractable,
unbranded PDF.

## Editing the sheets

- Sources live in `sheets/*.html` with one shared `sheets/shared.css`.
- Edit any sheet, re-run `python3 build.py <name>`, and open the PDF.
- `setup/<sheet-name>.md` holds a short setup article for each sheet: how to
  use it, when to use it, and what it pairs with.
- No web fonts: everything uses system fonts, so your build works offline.

## Setup articles

Each sheet has a getting-started article in `setup/` — a warm, plain-English
read: what the sheet is for, how to use it at the booth, and which other
sheets it pairs with. Start with `setup/load-sheet.md` if you want the
whole-day routine story, or `setup/blanket-layout.md` if you are fresh out of
a parking spot and a stack of boxes.

## Who this is for

For flea-market and vendor-booth sellers — first-timers, occasional sellers,
and anyone whose booth deserves to be tidy: prices on things, change counted,
rain handled. **This pack is deliberately distinct from a home garage-sale
kit** (a home yard sale has neighbors and your own driveway, not a paid
market slot and an aisle of competitor booths).

Built and maintained by **Asdale Dynamics, LLC** as part of a set of
beginner-friendly, plain-English, local-first tools. If you know someone
selling their first day at a flea market, send them this folder — this pack
is free; their early mistakes do not have to be.

## License

MIT — see `LICENSE`. Copyright (c) 2026 Asdale Dynamics, LLC.
