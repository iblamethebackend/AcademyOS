# CampusOS — India-first K–12 School SaaS Blueprint

Prepared 10 November 2026. CampusOS is a working product name.

## Deliverables

- **CampusOS-School-SaaS-Blueprint.pdf** — 71 pages with searchable vector text, 71 bookmarks, clickable contents and official source links.
- **CampusOS-Requirements.csv** — 144 functional requirements across 24 modules, with priorities, owners, business rules, module acceptance checks and screen references. Opens in Excel or Google Sheets.
- **CampusOS-Screen-Gallery.jpg** — overview of all 23 screen concepts.
- **screens/** — full-page PNG exports of every screen concept (including three mobile journeys with three views each).
- **source/** — editable requirements and PDF drawing source.
- **verification-report.json** — document completeness and layout checks.
- **page-map.json** — complete page index.

## PDF navigation

- Pages 3–8: scope, roles, authorization, navigation, journeys and SaaS packaging.
- Pages 9–32: functional catalogue.
- Pages 33–44: architecture, data contracts, APIs, security, quality, operations, testing and delivery.
- Page 45: visual system.
- Pages 46–68: screen designs.
- Pages 69–71: state patterns, design traceability and sources.

## Rebuild

This version was generated with Python on Windows. The source references Windows Segoe UI font files in C:/Windows/Fonts. Fonts are not bundled; use licensed local fonts and update the registration paths when porting to another environment.

Install the versions in source/requirements.txt, then run from the project root:

    python deliverables/source/build_blueprint.py
    python deliverables/source/verify_and_export.py

The verification script exports the screen PNGs and gallery. Optional internal preview rendering:

    python deliverables/source/preview.py

## Scope and assumptions

The PDF is a product and implementation blueprint, with static screen designs. It is not a running SaaS application. All school identities, people, figures and UI data are fictional. P0/P1/P2 are proposed implementation priorities. Capacity, performance targets, staffing and delivery windows are planning assumptions for validation with pilot schools.

Schools must validate their board-specific templates, finance/payroll policies, retention and current legal obligations. Government API availability is not assumed. Official references are linked on page 71.

## Verification

Checked all 71 pages for text bounds and completeness; verified 144 unique requirement IDs, 23 screen concepts, bookmarks and links. Reviewed full-document contact sheets and selected full-resolution pages. Paragraph-fit checks report no overflow. These are document checks, not application tests or proof of production compliance.

