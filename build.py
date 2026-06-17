#!/usr/bin/env python3
"""
Build script for the Fur Wetting anthology project page.

Renders the hub `index.html` + 6 per-paper subpages (`<slug>/index.html`),
the README, sitemap.xml, and robots.txt from a single PAPERS list below.

Edit PAPERS or SITE and re-run; no other build step.
"""
from __future__ import annotations
import html
import os
import re
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parent

# ----------------------------------------------------------------------------
# SITE-LEVEL CONFIG
# ----------------------------------------------------------------------------
SITE = {
    "github_user": "genepatrickrible",
    "repo_name": "fur-wetting",
    "canonical_url": "https://genepatrickrible.github.io/fur-wetting/",
    "repo_url": "https://github.com/genepatrickrible/fur-wetting",
    "favicon_emoji": "\U0001F43A",  # wolf (one of the mammals studied in the fur-pelts paper)
    "body_of_work_title": "Drop Impact on Bio-inspired Fiber Arrays and Mammalian Fur",
    "tagline": "How fiber geometry, packing density, and pelt structure govern raindrop penetration.",
    "program_description": (
        "A six-paper experimental program from the Dickerson Lab at the "
        "University of Tennessee, Knoxville on how mammalian fur, and 3D-printed "
        "fiber arrays inspired by it, govern penetration by impacting drops. "
        "The papers progress from single-orientation arrays (horizontal, then "
        "vertical) through sequential impacts and cross-sectional geometry to "
        "the natural mammalian pelts that motivated the work."
    ),
    "lead_authors_plain": "Gene Patrick S. Rible, Andrew K. Dickerson",
    "lead_authors_html": (
        "<span class=\"author-block\">Gene Patrick S. Rible</span>, "
        "<span class=\"author-block\">Andrew K. Dickerson</span>"
    ),
    "affiliations_html": (
        "<span class=\"affil-block\">Department of Mechanical, Aerospace and "
        "Biomedical Engineering, University of Tennessee, Knoxville</span>"
    ),
    "contact_line_hub": (
        "<em>Contact researchers: "
        "<a href=\"mailto:grible@vols.utk.edu\" style=\"text-decoration: underline;\">"
        "grible@vols.utk.edu</a></em>"
    ),
    "lastmod_date": "2026-06-04",
    # Verification tokens populated after registering with GSC / Bing
    "gsc_token": "",
    "bing_token": "",
    # Site-wide engagement buttons (Phase 5b in the research-page-builder
    # skill). Empty string = button is not rendered. Both go in the hero
    # link-row on every subpage and the hub hero.
    "schedule_url": "https://calendar.app.google/9djYm5daK8n7TC3VA",
    "discussion_url": "https://github.com/genepatrickrible/fur-wetting/discussions",
    # Giscus widget script. Renders as an in-page comments box at the
    # bottom of every page (after Acknowledgments, before the footer).
    # `data-loading="lazy"` defers fetching the script + comments until
    # the visitor scrolls near the widget — saves bandwidth for the
    # majority of visitors who never reach the bottom of a long page.
    "giscus_html": """\
<script src="https://giscus.app/client.js"
        data-repo="genepatrickrible/fur-wetting"
        data-repo-id="R_kgDOSxn_Xw"
        data-category="Announcements"
        data-category-id="DIC_kwDOSxn_X84C-i7R"
        data-mapping="pathname"
        data-strict="0"
        data-reactions-enabled="1"
        data-emit-metadata="0"
        data-input-position="bottom"
        data-theme="preferred_color_scheme"
        data-lang="en"
        data-loading="lazy"
        crossorigin="anonymous"
        async>
</script>""",
    # Shared acknowledgments shown on the hub
    "acknowledgments_hub": (
        "We thank the many undergraduate researchers who contributed across "
        "this body of work. Funding sources are listed in each paper."
    ),
    "keywords": (
        "drop impact, fiber arrays, mammalian fur, wettability, "
        "porous media, bioinspiration, raindrop penetration, "
        "Weber number, capillary infiltration"
    ),
}

# ----------------------------------------------------------------------------
# PAPER METADATA
# ----------------------------------------------------------------------------
# Each paper: slug, title, full author list, journal metadata, abstract,
# "firsts" cards, result blocks, supplementary materials.
#
# author entries: {"name": "...", "affil_ix": 1, "is_corresponding": False}
# Citation_author meta uses "LastName, GivenNames".

PAPERS = [
    {
        "slug": "horizontal-fibers",
        "title": "Dynamic Drop Penetration of Horizontally Oriented Fiber Arrays",
        "tagline": "Counter to intuition, hydrophilic horizontal fiber arrays resist raindrop impact better than hydrophobic ones.",
        "authors": [
            {"name": "Gene Patrick S. Rible", "citation_name": "Rible, Gene Patrick S.", "affil_ix": 1, "is_corresponding": True},
            {"name": "Michael A. Spinazzola, III", "citation_name": "Spinazzola, Michael A.", "affil_ix": 1, "is_corresponding": False},
            {"name": "Robert E. Jones, III", "citation_name": "Jones, Robert E.", "affil_ix": 1, "is_corresponding": False},
            {"name": "Rachel U. Constantin", "citation_name": "Constantin, Rachel U.", "affil_ix": 1, "is_corresponding": False},
            {"name": "Wei Wang", "citation_name": "Wang, Wei", "affil_ix": 1, "is_corresponding": False},
            {"name": "Andrew K. Dickerson", "citation_name": "Dickerson, Andrew K.", "affil_ix": 1, "is_corresponding": False},
        ],
        "affiliations": [
            "Department of Mechanical, Aerospace and Biomedical Engineering, University of Tennessee, Knoxville, Tennessee 37996, USA",
        ],
        "contact_email": "grible@vols.utk.edu",
        "abstract": (
            "In this experimental study, we combine drop impact into porous media and onto a "
            "single fiber to study drop impact into fiber arrays inspired by mammalian fur "
            "coats. In our 3D-printed arrays, we vary the packing density, fiber alignment, "
            "strand cross-section, and wettability. Drops impact fibers fixed at both ends, "
            "penetrating over short times by momentum and laterally spreading throughout the "
            "array. Using image analysis, we measure penetration depth, and wetted width "
            "into the array. Impact Weber number and intrinsic porosity define penetration, "
            "retraction, and rebound regimes. On average, at an impact Weber number of ≈80, "
            "staggered fibers reduce penetration by 24% in hydrophilic fibers and 34% in "
            "hydrophobic fibers, and the penetration reduction percentage is expected to "
            "increase with increasing Weber number. Our results indicate that as density "
            "grows toward the density of mammalian pelts, penetration will reach a maximum "
            "value independent of drop impact velocity, thereby providing an effective rain "
            "barrier. Hydrophilicity at the densities we test, 50-150 strands/cm², aids fiber "
            "array resistance of dynamic penetration by impacting drops through the promotion "
            "of lateral drop spreading and inhibition of drop fragmentation. Conversely, "
            "hydrophobic fibers best resist low-speed wicking. The fraction of a drop that "
            "infiltrates hydrophilic and hydrophobic fibers is nearly identical for a fixed "
            "Weber number because lateral spreading restricts the penetration depth into "
            "hydrophilic fibers but does not restrict mass infiltration. Above a critical "
            "Weber number, the entire drop mass percolates fiber arrays regardless of strand "
            "wettability."
        ),
        # Video tile prepended to the Firsts grid (occupies the upper-left slot
        # so the first first-card slides into the upper-right slot).
        "firsts_video_src": "static/videos/horizontal-fibers/horizontal-fiber.mp4",
        "firsts": [
            {"icon": "fas fa-cubes", "title": "First drop impacts on 3D-printed fur-mimicking fiber arrays",
             "summary": "Drop-impact literature has long been split between three camps: solid surfaces, porous media, and single fibers. This work is the first to drop water on resin-3D-printed multi-fiber arrays sized and packed like mammalian fur, bridging the porous-media and single-fiber camps. Density, alignment, strand cross-section, and wettability are independently controlled.",
             "section": "section-staggered"},
            {"icon": "fas fa-water", "title": "Hydrophilic fibers resist dynamic penetration better than hydrophobic",
             "summary": "Counter to intuition: at the tested densities (50-150 strands/cm²), hydrophilic horizontal arrays best resist raindrop impact. They promote lateral spreading and inhibit drop fragmentation, two mechanisms hydrophobic arrays lack at dynamic velocities.",
             "section": "section-wettability"},
            {"icon": "fas fa-tachometer-alt", "title": "A critical Weber number marks the wettability crossover",
             "summary": "Below We_c, hydrophobic fibers minimize penetration (static / low-speed wicking). Above We_c, hydrophilic takes over (dynamic / raindrop). At ≈5 m/s, hydrophobic fibers shatter and let the drop fully penetrate; hydrophilic fibers stop it at finite depth.",
             "section": "section-critical-we"},
            {"icon": "fas fa-grip", "title": "Staggered arrays reduce penetration by up to 34%",
             "summary": "At We ≈ 80, staggered hydrophobic fibers cut penetration depth by 34% (24% for hydrophilic), and the benefit grows with Weber number.",
             "section": "section-staggered"},
            {"icon": "fas fa-umbrella", "title": "Density approaches a dynamic rain-barrier limit",
             "summary": "As packing density rises toward mammalian-pelt levels, penetration saturates: drop velocity no longer governs how deep the liquid reaches.",
             "section": "section-density-limit"},
        ],
        "result_sections": [
            {"id": "section-wettability", "title": "Hydrophilic fibers resist dynamic penetration better than hydrophobic",
             "pre_media": [
                 {"kind": "youtube", "youtube_id": "JqFAUE40SVI",
                  "label": "Movie S5: ≈5 m/s impacts, hydrophilic vs hydrophobic"},
                 {"kind": "youtube", "youtube_id": "DExOMbiahUk",
                  "label": "Movie S1: Impact classifications"},
             ],
             "explanation": "Modified fiber aspect ratio (AR*) versus Weber number for hydrophilic (left) and hydrophobic (right) arrays in standard (top) and bottom (bottom) orientations, colored by the number of penetrated layers. AR* is the inter-fiber spacing normalized by the drop diameter; a lower AR* means the impacting drop sees a denser array. The counter-intuitive main finding of the paper: at the tested densities (50-150 strands/cm²), hydrophilic horizontal arrays best resist raindrop impact. They do it by promoting lateral spreading (which redirects kinetic energy out across the array surface) and inhibiting drop fragmentation (which would otherwise let small daughter droplets dive deeply between strands). Hydrophobic fibers do neither; they let the drop fragment and penetrate further at dynamic velocities. In the legend, PDF stands for “penetrated drop fragmentation”: points drawn with a black outline (□) represent drops that fragmented during impact; solid markers (■) are non-fragmenting drops.",
             "figs": 1,
             "image": "static/images/horizontal-fibers/fig5.png",
             "alt": "Figure 5 from the paper: modified fiber aspect ratio versus Weber number, four-panel layout comparing hydrophilic and hydrophobic across two orientations."},
            {"id": "section-critical-we", "title": "A critical Weber number marks the wettability crossover",
             "explanation": "Normalized maximum penetration depth in hydrophobic fibers versus the same quantity in hydrophilic fibers, panel by panel for each density. Vertical lines mark the critical Weber number (We_c) at which hydrophobic penetration starts exceeding hydrophilic. Below We_c the hydrophobic case penetrates less (the static / low-speed wicking regime where hydrophobicity helps). Above We_c the hydrophilic case takes over and resists better (the dynamic / raindrop regime). The per-density We_c values are printed on each panel. At raindrop velocities (≈5 m/s, see Movie S5 below), hydrophobic arrays shatter the drop and let it fully percolate the array; hydrophilic arrays still stop it at a finite depth.",
             "figs": 1,
             "image": "static/images/horizontal-fibers/fig9.png",
             "alt": "Figure 9 from the paper: six-panel comparison of hydrophobic vs hydrophilic penetration depth with vertical dashed lines marking the critical Weber number for each density."},
            {"id": "section-staggered", "title": "3D-printing fur-inspired fiber arrays",
             "pre_media": [
                 {"kind": "local", "src": "static/videos/horizontal-fibers/horizontal-fiber.mp4",
                  "type": "video/mp4", "loop": True},
             ],
             "explanation": "Drop-impact literature has historically split into three camps: solid surfaces, porous media, and single fibers. This work bridges the porous-media and single-fiber camps by producing resin-3D-printed fiber arrays sized and packed like mammalian fur (50-150 strands/cm²) and then dropping water on the whole array rather than on a single strand. Fixing each fiber at both ends eliminates cantilever beam dynamics, isolating the wetting physics. Density, alignment, strand cross-section, and wettability are all independently controlled. Two configurations are tested: aligned (square grid) and staggered (every other row shifted by half a cell). Staggered arrangements consistently reduce penetration relative to aligned arrays of identical density, by up to 34% at We ≈ 80.",
             "figs": 1,
             "image": "static/images/horizontal-fibers/fig1.png",
             "alt": "Figure 1 from the paper: 3D-printed fiber array. Oblique view, top view, and schematic comparison of aligned vs staggered configurations."},
            {"id": "section-density-limit", "title": "Penetration saturates with density",
             "explanation": "Normalized maximum penetration depth versus Weber number for hydrophilic (left) and hydrophobic (right) arrays at three densities (about 50, 100, and 144 strands/cm squared), aligned vs staggered. As density rises toward the density of natural pelts, the curves flatten: a dynamic ceiling on penetration that natural pelts already exploit.",
             "figs": 1,
             "image": "static/images/horizontal-fibers/fig7.png",
             "alt": "Figure 7 from the paper: normalized max penetration depth vs Weber number, six panels showing the saturation behavior with density and the aligned vs staggered comparison."},
        ],
        "journal": "Langmuir",
        "journal_abbrev": "Langmuir",
        "publisher": "American Chemical Society",
        "issn": "0743-7463",
        "volume": "40",
        "issue": "26",
        "firstpage": "13339",
        "lastpage": "13354",
        "doi": "10.1021/acs.langmuir.4c00371",
        "pub_date_iso": "2024-06-12",
        "pub_year": "2024",
        "supp_pdf_source": "anthology/supplementary/la4c00371_si_006.pdf",
        # Override: link the Paper button to the lab-hosted open-access PDF
        "paper_pdf_url": "https://www.dickersonlab.com/_files/ugd/fb8f64_6e492f14c1104242bcb39ea6ec1b75cd.pdf",
        # Teaser videos rendered side-by-side between hero and abstract.
        "teaser_videos": [
            {"label": "Hydrophilic",
             "src": "static/videos/horizontal-fibers/philic_trimmed_cropped.mp4",
             "type": "video/mp4"},
            {"label": "Hydrophobic",
             "src": "static/videos/horizontal-fibers/phobic_trimmed_cropped.mp4",
             "type": "video/mp4"},
        ],
        # Override: link the Supplement button to the canonical ACS URL
        # (stripped from the UTK library proxy form `pubs-acs-org.utk.idm.oclc.org`,
        # which would only resolve for logged-in UTK users).
        "supp_pdf_url": "https://pubs.acs.org/doi/suppl/10.1021/acs.langmuir.4c00371/suppl_file/la4c00371_si_006.pdf",
        # YouTube playlist of the walkthrough + 5 supplementary movies, in
        # walkthrough -> S1 -> S5 order. Drives the hero-row "Video" button
        # and the link under the Supplementary videos heading.
        "youtube_playlist_url": "https://www.youtube.com/playlist?list=PLaxoeadWOB0rSAa_1hSGdGaYPtqpKpZR9",
        # 10-minute author walkthrough of the whole paper. Renders at the
        # very bottom of the "Firsts in this work" section as a full-width
        # YouTube embed.
        "walkthrough_youtube_id": "Xfcf5kWpkpM",
        # APS DFD 2022 conference slides, archived on Zenodo (citable DOI).
        # Drives the hero-row "Slides" button. The Zenodo record is
        # independently citable from the journal paper.
        "slides_url": "https://doi.org/10.5281/zenodo.20597232",
        "videos": [
            {"label": "Movie S1: Impact classifications", "youtube_id": "DExOMbiahUk",
             "caption": "Image sequences of all eight observed impact classifications, paired with the normalized temporal heat maps from Figure 3."},
            {"label": "Movie S2: Aligned, 144 strands/cm², U ≈ 0.5 m/s", "youtube_id": "xMrnEN9zFIA",
             "caption": "Drops impact aligned fiber arrays at packing density 144 strands per square centimeter, at an impact velocity of about 0.5 m/s."},
            {"label": "Movie S3: Aligned, 144 strands/cm², U ≈ 0.3 m/s", "youtube_id": "Ffl2BRzuVaQ",
             "caption": "Same array as Movie S2, lower impact velocity (about 0.3 m/s), for contrast in the impact regime."},
            {"label": "Movie S4: Aligned, 144 strands/cm², U ≈ 0.5 m/s", "youtube_id": "ffZa62XPKnk",
             "caption": "Movie S2 with time annotations overlaid for readers tracking each impact phase."},
            {"label": "Movie S5: ≈5 m/s impacts, hydrophilic vs hydrophobic", "youtube_id": "JqFAUE40SVI",
             "caption": "The climax of the paper: at raindrop velocities (≈5 m/s), hydrophobic fibers (right) shatter the drop into many fragments that deeply penetrate the array, whereas the hydrophilic case (left) stops the drop at finite depth. Counter to intuition, hydrophilic horizontal fibers win at raindrop speeds."},
        ],
        "videos_note": "",
        "keywords": "drop impact, fiber arrays, mammalian fur, wettability, Weber number, porosity, hydrophobic, hydrophilic, lateral spreading",
        "acknowledgments": "This research was partially funded by the National Science Foundation (CMMI 1825801 and CBET 2153740). We thank undergraduate research assistants at the Fluids and Structures Laboratory, Visalsaya Chakpuang, David Job Dooley, and Agustin Soto for bespoke code contributions, Rachel Robinette for video analysis, and Syed Jaffar Raza for editing the supplementary videos. We also give special thanks to Mohammad Alipanahrostami for coating our hydrophobic fibers.",
        "bibkey": "rible2024horizontal",
        "tagline_card": "Counter to intuition, hydrophilic horizontal fiber arrays resist dynamic drop penetration better than hydrophobic ones at the tested densities. Hydrophobic fibers only win at low Weber numbers; a critical Weber number We_c marks the crossover.",
    },
    {
        "slug": "vertical-fibers",
        "title": "Dynamic drop penetration of vertically oriented fiber arrays",
        "tagline": "An energy model for penetration depth; vertical hydrophilic arrays penetrate more than hydrophobic ones, opposite to horizontal fibers.",
        "authors": [
            {"name": "Gene Patrick S. Rible", "citation_name": "Rible, Gene Patrick S.", "affil_ix": 1, "is_corresponding": True},
            {"name": "Visalsaya Chakpuang", "citation_name": "Chakpuang, Visalsaya", "affil_ix": 1, "is_corresponding": False},
            {"name": "Aidan D. Holihan", "citation_name": "Holihan, Aidan D.", "affil_ix": 1, "is_corresponding": False},
            {"name": "Hannah P. Sebek", "citation_name": "Sebek, Hannah P.", "affil_ix": 1, "is_corresponding": False},
            {"name": "Hannah H. Osman", "citation_name": "Osman, Hannah H.", "affil_ix": 1, "is_corresponding": False},
            {"name": "Kyle R. Brown", "citation_name": "Brown, Kyle R.", "affil_ix": 1, "is_corresponding": False},
            {"name": "Wei Wang", "citation_name": "Wang, Wei", "affil_ix": 1, "is_corresponding": False},
            {"name": "Andrew K. Dickerson", "citation_name": "Dickerson, Andrew K.", "affil_ix": 1, "is_corresponding": False},
        ],
        "affiliations": [
            "Department of Mechanical, Aerospace and Biomedical Engineering, University of Tennessee, Knoxville, Tennessee 37996, USA",
        ],
        "contact_email": "grible@vols.utk.edu",
        # Looping teaser video rendered between the hero and the abstract.
        # Single-video case: the renderer wraps it in the teaser-grid flex
        # container and applies muted/autoplay/loop/playsinline automatically.
        "teaser_videos": [
            {"label": "Drop on a vertical fiber array",
             "src": "static/videos/vertical-fibers/droponverticalfiberarray_v1.mp4",
             "type": "video/mp4"},
        ],
        # Explicit cell order for the "Firsts in this work" grid. Each cell
        # is either a card, an image, or a looping video. Renderer overrides
        # the default firsts-list layout when firsts_cells is set.
        # Layout (4 rows):
        #   Row 1: VerticalFur.jpeg     | First drop-impact study of vertical fiber arrays
        #   Row 2: Energy-conservation model | Wettability inversion versus horizontal
        #   Row 3: Capillary wicking below a Bond-number threshold | capillary.mp4 loop
        #   Row 4: Liquid penetration decelerates at a constant rate (full-width)
        # The lone image cell (row 1 left) is right-aligned via CSS.
        # The row-3 video is left-aligned within its column via `align: "left"`.
        # The row-4 card spans the full row via `is_full: True`.
        "firsts_cells": [
            {"kind": "image",
             "src": "static/images/vertical-fibers/VerticalFur.jpeg",
             "alt": "Photograph of vertically oriented fur, the natural biological inspiration for the experimental fiber arrays in this paper."},
            {"kind": "card", "icon": "fas fa-arrows-up-down",
             "title": "First drop-impact study of vertical fiber arrays",
             "summary": "A systematic investigation of how vertical orientation reshapes impact dynamics compared with the horizontal case.",
             "section": "section-vertical"},
            {"kind": "card", "icon": "fas fa-calculator",
             "title": "Energy-conservation penetration model",
             "summary": "An analytical relationship between Weber number and penetration depth, validated against the experiments.",
             "section": "section-model"},
            {"kind": "card", "icon": "fas fa-droplet",
             "title": "Wettability inversion versus horizontal",
             "summary": "Vertical hydrophilic arrays penetrate MORE than hydrophobic counterparts, opposite to the horizontal case, because gravity-aligned capillarity dominates.",
             "section": "section-wettability-vert"},
            {"kind": "card", "icon": "fas fa-arrow-down",
             "title": "Capillary wicking below a Bond-number threshold",
             "summary": "When Bo ⩽ 0.11 the penetrated liquid wicks vertically along the fibers, extending the wetted footprint beyond the kinematic depth.",
             "section": "section-wicking"},
            {"kind": "video",
             "src": "static/videos/vertical-fibers/capillary.mp4",
             "type": "video/mp4",
             "align": "left"},
            {"kind": "card", "icon": "fas fa-chart-line",
             "title": "Liquid penetration decelerates at a constant rate",
             "summary": "The penetrating liquid front decelerates at a constant rate inside the array. That lets us predict the maximum penetration depth from a single measurement once the drop reaches the base. Denser arrays are more prone to rebound, contributing to a greater impact force.",
             "section": "section-deceleration",
             "is_full": True},
        ],
        "abstract": (
            "This experimental work investigates the impact dynamics of drops on vertically "
            "oriented, three-dimensional (3D)-printed fiber arrays with variations in packing "
            "density, fiber arrangement, and wettability. These fiber arrays are inspired by "
            "mammalian fur, and while not wholly representative of the entire morphological "
            "range of fur, they do reside within its spectrum. We define an aspect ratio, a "
            "modified aspect ratio relative to the drop size, that characterizes various impact "
            "regimes. Using energy conservation, we derive a model relating drop penetration "
            "depth in vertical fibers to the Weber number. In sparse fibers where the "
            "Ohnesorge number is less than 4 × 10⁻², penetration depth scales "
            "linearly with the impact Weber number. In hydrophobic fibers, density greatly "
            "reduces penetration depth when the contact angle is sufficiently high. Hydrophilic "
            "arrays have greater penetration than their hydrophobic counterparts due to "
            "capillarity, a result that contrasts with horizontal fibers. Vertical capillary "
            "infiltration of the penetrated liquid is observed whenever the Bond number is "
            "less than 0.11. For hydrophobic fibers, we predict higher density will produce "
            "complete drop penetration when the contact angle is sufficiently low. Complete "
            "infiltration by the drop is achieved at sufficient times regardless of drop "
            "impact velocity."
        ),
        "firsts": [
            {"icon": "fas fa-arrows-up-down", "title": "First drop-impact study of vertical fiber arrays", "summary": "A systematic investigation of how vertical orientation reshapes impact dynamics compared with the horizontal case.", "section": "section-vertical"},
            {"icon": "fas fa-calculator", "title": "Energy-conservation penetration model", "summary": "An analytical relationship between Weber number and penetration depth, validated against the experiments.", "section": "section-model"},
            {"icon": "fas fa-droplet", "title": "Wettability inversion versus horizontal", "summary": "Vertical hydrophilic arrays penetrate MORE than hydrophobic counterparts, opposite to the horizontal case, because gravity-aligned capillarity dominates.", "section": "section-wettability-vert"},
            {"icon": "fas fa-arrow-down", "title": "Capillary wicking below a Bond-number threshold", "summary": "When Bo ⩽ 0.11 the penetrated liquid wicks vertically along the fibers, extending the wetted footprint beyond the kinematic depth.", "section": "section-wicking"},
        ],
        "result_sections": [
            {"id": "section-vertical", "title": "Why vertical arrays behave differently",
             "explanation": "The drop now impacts fiber tips rather than fiber sides, so its kinetic energy converts to penetration through a different geometric channel. We tabulate the new impact regimes via a modified aspect ratio.",
             "pre_media": [
                 {"kind": "youtube", "youtube_id": "QUVgO2ej2Xs",
                  "label": "Movie 1: Eight impact classifications"},
                 {"kind": "image",
                  "path": "static/images/vertical-fibers/fig5.png",
                  "label": "Figure 5",
                  "alt": "Figure 5 from the paper: (a, b) Modified aspect ratio AR* vs Weber number for observed impact classifications, hydrophilic (left) and hydrophobic (right). Solid symbols mark impacts where the drop did not reach the bottom of the fiber array; symbols with a black outline mark impacts where the drop penetrated to the bottom. (c) Occurrence of drop rebound in the AR*-We spectrum in vertical fibers. (d) Theoretical maximum penetration depth predicted from a constant-deceleration model when the impacted drop reaches the base of the array."},
             ],
             "figs": 2,
             "images": [
                 {"path": "static/images/vertical-fibers/fig1.png",
                  "alt": "Figure 1 from the paper: 3D-printed vertical fiber arrays. Cross-section of a strand, aligned vs staggered top-view configurations, hydrophobic and hydrophilic contact angles, and the D0/U/dp/chi dimensional impact parameters."},
                 {"path": "static/images/vertical-fibers/fig2.png",
                  "alt": "Figure 2 from the paper: illustration of trans-fiber motions. Normal, Wave, Bisection, and Wave plus Bisection. These lateral motions are unique to vertical arrays."},
             ]},
            {"id": "section-model", "title": "An energy-conservation model for penetration depth",
             "explanation": "We balance kinetic energy at impact against the work done by drag and capillary forces on the descending liquid front. In the sparse regime (Oh < 4 × 10⁻²) the prediction is linear in We; experiments confirm.",
             "pre_media": [
                 {"kind": "youtube", "youtube_id": "70T4kgBaItM",
                  "label": "Movie 2: Contact angles, apparent vs. actual"},
                 {"kind": "youtube", "youtube_id": "wonSRuHMXi4",
                  "label": "Movie 3: Maximum drop spread at fiber tips"},
             ],
             "pre_media_layout": "row",
             "figs": 1,
             "image": "static/images/vertical-fibers/fig7.png",
             "alt": "Figure 7 from the paper: graphical accompaniment to the penetration-depth model. Cylindrical drop projection becoming a rectangular steady-state footprint inside the array, with the supporting area-projection image sequence at the bottom."},
            {"id": "section-wettability-vert", "title": "Capillarity helps hydrophilic vertical arrays penetrate",
             "explanation": "In contrast to horizontal fibers, vertical hydrophilic arrays draw additional liquid downward via capillarity, deepening the wetted column.",
             "figs": 1,
             "image": "static/images/vertical-fibers/fig8.png",
             "alt": "Figure 8 from the paper: normalized maximum penetration depth versus Weber number, hydrophilic (left) and hydrophobic (right) panels with linear k1*We + k2 fits across multiple densities. Hydrophilic curves sit above hydrophobic at low We; the wettability inversion versus horizontal fibers."},
            {"id": "section-wicking", "title": "A Bond-number criterion for capillary wicking",
             "explanation": "Whenever the Bond number of the residual drop falls below 0.11, the trapped liquid wicks vertically along the fibers, extending the effective penetration depth beyond what impact alone would predict.",
             "pre_media": [
                 {"kind": "local",
                  "src": "static/videos/vertical-fibers/capillary.mp4",
                  "type": "video/mp4",
                  "loop": True,
                  "float": "left"},
             ],
             "figs": 0},
            {"id": "section-deceleration", "title": "Liquid penetration decelerates at a constant rate",
             "explanation": "Penetration depth versus time for a drop impacting a 50 strands/cm² array at We = 15.5 shows the liquid front decelerating at a constant rate inside the array. This lets us predict the maximum penetration depth that the drop body would have achieved if the fibers had been long enough, even when the drop reaches the base mid-experiment. As fiber density rises, drops are more prone to rebound, contributing to a greater impact force. When the rate of liquid ingress reaches its maximum at τ < 1, the majority of the liquid mass still resides above the array; that mass then either rebounds, or its downward motion decelerates.",
             "pre_media": [
                 {"kind": "youtube", "youtube_id": "-skOA36BdPw",
                  "label": "Movie 4: Constant deceleration of liquid front"},
                 {"kind": "youtube", "youtube_id": "DXUviuUxWIg",
                  "label": "Movie 5: Drop deceleration above the array"},
             ],
             "pre_media_layout": "row",
             "figs": 1,
             "image": "static/images/vertical-fibers/fig6.png",
             "alt": "Figure 6 from the paper: image sequences of drops impacting vertical arrays at We = 9.4 (max spread plus lateral spread at base), We = 0.75 (low-We rebound plus capillary action, the LRC regime), and We = 8.7 (deceleration above the fiber array)."},
        ],
        "journal": "Physics of Fluids",
        "journal_abbrev": "Phys. Fluids",
        "publisher": "AIP Publishing",
        "issn": "1070-6631",
        "volume": "37",
        "issue": "2",
        "firstpage": "022108",
        "lastpage": "022108",
        "doi": "10.1063/5.0246986",
        "pub_date_iso": "2025-02-04",
        "pub_year": "2025",
        "supp_pdf_source": None,
        "videos": [
            {"label": "Movie 1: Eight impact classifications", "youtube_id": "QUVgO2ej2Xs",
             "caption": "Image sequences of all eight observed impact classifications on vertically oriented fiber arrays, paired with normalized temporal heat maps. Pairs with Fig. 3."},
            {"label": "Movie 2: Contact angles, apparent vs. actual", "youtube_id": "70T4kgBaItM",
             "caption": "The advancing contact angles appear hydrophilic due to shadowing; closer inspection shows they exceed 90°. Pairs with Fig. 4."},
            {"label": "Movie 3: Maximum drop spread at fiber tips", "youtube_id": "wonSRuHMXi4",
             "caption": "Max drop spread at the fiber tips, fiber-prevented spreading, enhanced penetration, and lateral spread at the base. Pairs with Fig. 6(a)."},
            {"label": "Movie 4: Constant deceleration of liquid front", "youtube_id": "-skOA36BdPw",
             "caption": "The penetrating liquid front decelerates at a constant rate due to drop interaction with the fiber shafts; rebound follows above the array. Pairs with Figs. 6(b) and 5(d)."},
            {"label": "Movie 5: Drop deceleration above the array", "youtube_id": "DXUviuUxWIg",
             "caption": "A We = 8.7 drop decelerates above the fiber array due to impact force without penetrating. Pairs with Fig. 6(c)."},
        ],
        "videos_note": "",
        "youtube_playlist_url": "https://www.youtube.com/playlist?list=PLaxoeadWOB0oCZIeNvpSKCT-catNuo7R8",
        # APS DFD 2023 conference slides, archived on Zenodo (citable DOI).
        "slides_url": "https://doi.org/10.5281/zenodo.20649226",
        # Override: link the Paper button to the lab-hosted open-access PDF.
        "paper_pdf_url": "https://www.dickersonlab.com/_files/ugd/fb8f64_1660b8085bac4756b340cd5a8759dae1.pdf",
        "keywords": "drop impact, vertical fibers, mammalian fur, Weber number, Ohnesorge number, capillary infiltration, Bond number, energy conservation",
        "acknowledgments": "This research was partially funded by the National Science Foundation (CMMI 1825801 and CBET 2205558). We thank undergraduate research assistants at the Fluids and Structures Laboratory, Syed Jaffar Raza for bespoke code contributions, Alexander Bottoms for editing some of the supplementary videos, and Michael Spinazzola III for fine-tuning the laser-cutting setup and parameters for our vertical fiber arrays. We also give special thanks to Mohammad Alipanahrostami for coating our samples.",
        "bibkey": "rible2025vertical",
        "tagline_card": "An energy-conservation model in which penetration scales linearly with We for sparse vertical fibers; hydrophilic vertical arrays penetrate more than hydrophobic ones (opposite to horizontal).",
    },
    {
        "slug": "sequential-impacts",
        "title": "Sequential drop impacts onto horizontal fiber arrays",
        "tagline": "Two drops in a row: fragmentation of the first limits the lateral and depth growth of the second.",
        "authors": [
            {"name": "Gene Patrick S. Rible", "citation_name": "Rible, Gene Patrick S.", "affil_ix": 1, "is_corresponding": True},
            {"name": "Agustin Soto", "citation_name": "Soto, Agustin", "affil_ix": 1, "is_corresponding": False},
            {"name": "Regina C. Shome", "citation_name": "Shome, Regina C.", "affil_ix": 2, "is_corresponding": False},
            {"name": "Andrew K. Dickerson", "citation_name": "Dickerson, Andrew K.", "affil_ix": 1, "is_corresponding": False},
        ],
        "affiliations": [
            "Department of Mechanical, Aerospace and Biomedical Engineering, University of Tennessee, Knoxville, Tennessee 37996, USA",
            "College of Computing, Georgia Institute of Technology, Atlanta, Georgia 30332, USA",
        ],
        "contact_email": "grible@vols.utk.edu",
        # Override: link the Paper button to the lab-hosted open-access PDF.
        "paper_pdf_url": "https://www.dickersonlab.com/_files/ugd/fb8f64_c902c8efda20464bbe6765f314d51e78.pdf",
        # APS DFD 2024 conference slides, archived on Zenodo (citable DOI).
        "slides_url": "https://doi.org/10.5281/zenodo.20707527",
        # Looping teaser video rendered between the hero and the abstract.
        "teaser_videos": [
            {"label": "Sequential drop impact on a horizontal fiber array",
             "src": "static/videos/sequential-impacts/h5_teaser.mp4",
             "type": "video/mp4"},
        ],
        "abstract": (
            "We experimentally investigate liquid infiltration into horizontally oriented "
            "fiber arrays imposed by sequential drop impacts. Our experimental system is "
            "inspired by mammalian fur coats, and our results provide insight into how we "
            "expect natural fibers to respond to falling drops and the structure nature gives "
            "to this hierarchic covering. Two successive drop impacts are filtered through "
            "three-dimensional printed fiber arrays with varying densities, surface "
            "wettability, and fixed fiber diameter. The penetration depth and the lateral "
            "width of drop spreading within fiber layers are functions of drop displacement "
            "relative to the liquid already within the array as well as the drop Weber "
            "number. Hydrophobic fibers more effectively prevent an increase in penetration "
            "depth by the second impacting drop at low impact Weber numbers, whereas "
            "hydrophilic fibers ensure lower liquid penetration depth into the array as the "
            "Weber number increases. Impact outcomes, such as penetration depth and lateral "
            "spreading, are insensitive to impact eccentricity between the first and second "
            "drop at high experimental Weber numbers. As expected, denser, staggered fibers "
            "reduce infiltration, preventing the entire drop mass from entering the array. "
            "Fragmentation of the first drop, which is promoted by hydrophobicity, larger "
            "inter-fiber spacing, and higher drop impact velocity, limits increases in "
            "lateral spreading and penetration depth of the liquid mass from a subsequent "
            "drop."
        ),
        "firsts": [
            {"icon": "fas fa-droplet", "title": "First two-drop study on horizontal fibers", "summary": "How an array already wetted by one drop responds to the next.", "section": "section-two-drops"},
            {"icon": "fas fa-arrows-left-right", "title": "Eccentricity matters at low We, not at high We", "summary": "Where the second drop lands relative to the first is increasingly irrelevant as impact velocity grows.", "section": "section-eccentricity"},
            {"icon": "fas fa-bomb", "title": "Initial drop fragmentation as a protective mechanism", "summary": "When the first drop fragments (more likely on hydrophobic, sparse, fast impacts), the second drop's lateral and depth growth is suppressed.", "section": "section-fragmentation"},
            {"icon": "fas fa-toggle-on", "title": "Wettability-Weber crossover", "summary": "Hydrophobic fibers best limit second-drop depth at low We; hydrophilic fibers take over at higher We.", "section": "section-crossover"},
        ],
        "result_sections": [
            {"id": "section-two-drops", "title": "Two-drop experiments on hydrophilic and hydrophobic arrays",
             "explanation": "We deliver two drops in quick succession onto 3D-printed horizontal fiber arrays with varying density and wettability, tracking how the second impact alters the wetted depth and width established by the first.",
             "pre_media": [
                 {"kind": "youtube", "youtube_id": "6268oIcFyZk",
                  "label": "Movie 3: Rebound classifications, Jet-Bulb / Jet / Little / None"},
             ],
             "figs": 2,
             "pair_layout": "stacked",
             "images": [
                 {"path": "static/images/sequential-impacts/fig1.png",
                  "alt": "Figure 1 from the paper: 3D-printed fiber arrays in staggered and aligned configurations across standard, front-and-back, and bottom orientations, plus contact-angle photos of hydrophilic and hydrophobic samples."},
                 {"path": "static/images/sequential-impacts/fig4.png",
                  "alt": "Figure 4 from the paper: classifications of supersurface retention (None / Partial / Total) and fragmentation (Whole / 0 / 1 / 2 / 3 / 4+) of liquid within the array."},
             ]},
            {"id": "section-eccentricity", "title": "Impact eccentricity loses its grip at high Weber number",
             "explanation": "At low We, offset between drops changes the outcome; at high We, the impact dynamics swamp the local detail of where the second drop lands.",
             "pre_media": [
                 {"kind": "youtube", "youtube_id": "jsPxVjN2mn0",
                  "label": "Movie 1: Drop displacement vs Weber number, image sequences"},
             ],
             "figs": 1,
             "image": "static/images/sequential-impacts/fig10.png",
             "alt": "Figure 10 from the paper: change in penetration depth within the aligned array imposed by the second drop. Top row: depth change versus the dimensionless horizontal displacement between drops. Bottom row: depth change versus impact Weber number. Colors indicate the degree of fragmentation."},
            {"id": "section-fragmentation", "title": "Fragmentation of the first drop protects against the second",
             "explanation": "Hydrophobicity, large inter-fiber spacing, and high impact velocity all promote fragmentation of the first drop, which redirects mass away from the array and limits the second drop's contribution to penetration.",
             "figs": 1,
             "image": "static/images/sequential-impacts/fig7.png",
             "alt": "Figure 7 from the paper: five-row image sequences showing how the second drop's displacement and the impact Weber number control liquid spread and penetration-depth change, including delta about 0 vs delta greater than 0 contrasts at low and high Weber numbers, plus a fragmentation case and a high-eccentricity case."},
            {"id": "section-crossover", "title": "Hydrophobic helps at low We; hydrophilic at high We",
             "explanation": "Below a Weber-number threshold, hydrophobic fibers minimize the second drop's depth increase. Above it, hydrophilic fibers do so via lateral spreading.",
             "pre_media": [
                 {"kind": "youtube", "youtube_id": "f46Ycotmya0",
                  "label": "Movie 2: Wettability crossover at low and high Weber number"},
             ],
             "figs": 1,
             "image": "static/images/sequential-impacts/fig8.png",
             "alt": "Figure 8 from the paper: (a) hydrophilic fibers allow a reduction in spread at high Weber number. (b) Hydrophobic fibers allow a reduction in penetration depth at low Weber number. The two-panel wettability crossover for sequential impacts."},
        ],
        "journal": "Physics of Fluids",
        "journal_abbrev": "Phys. Fluids",
        "publisher": "AIP Publishing",
        "issn": "1070-6631",
        "volume": "37",
        "issue": "7",
        "firstpage": "072128",
        "lastpage": "072128",
        "doi": "10.1063/5.0281512",
        "pub_date_iso": "2025-07-25",
        "pub_year": "2025",
        "supp_pdf_source": "anthology/supplementary/Supplemental Information.pdf",
        "videos": [
            {"label": "Movie 1: Drop displacement vs Weber number, image sequences", "youtube_id": "jsPxVjN2mn0",
             "caption": "Image sequences showing how the displacement of the second drop relative to the first (δ) and the impact Weber number control the change in liquid spread and penetration depth. Pairs with Fig. 7."},
            {"label": "Movie 2: Wettability crossover at low and high Weber number", "youtube_id": "f46Ycotmya0",
             "caption": "Two cases that flip with We: (a) hydrophilic fibers allow a reduction in spread of the second drop at high We; (b) hydrophobic fibers allow a reduction in penetration depth at low We. Pairs with Fig. 8."},
            {"label": "Movie 3: Rebound classifications, Jet-Bulb / Jet / Little / None", "youtube_id": "6268oIcFyZk",
             "caption": "Classifications of the rebound shape after sequential drop impacts on horizontal fiber arrays: Jet-Bulb, Jet, Little, and None. Each frame is timestamped by dimensionless time. Pairs with Fig. 11."},
        ],
        "videos_note": "",
        "youtube_playlist_url": "https://www.youtube.com/playlist?list=PLaxoeadWOB0qPAMjG2kt4fil6ploAZoFd",
        "keywords": "sequential drop impact, fiber arrays, mammalian fur, fragmentation, Weber number, eccentricity, hydrophobic",
        "acknowledgments": "This research was partially funded by the National Science Foundation (CMMI 1825801 and CBET 2205558). We thank Isabelle Garrett, an undergraduate research assistant at the Fluids and Structures Laboratory, for editing the image sequences and supplemental videos.",
        "bibkey": "rible2025sequential",
        "tagline_card": "Fragmentation of the first drop, promoted by hydrophobicity and high impact velocity, limits the second drop's lateral spreading and penetration depth.",
    },
    {
        "slug": "splash-suppression",
        "title": "Vertically oriented fiber arrays suppress splashing by restricting spreading of impacting drops",
        "tagline": "Three penetration regimes; vertical arrays suppress splash for all tested velocities, including beyond 5 m/s.",
        "authors": [
            {"name": "Gene Patrick S. Rible", "citation_name": "Rible, Gene Patrick S.", "affil_ix": 1, "is_corresponding": True},
            {"name": "Syed Jaffar Raza", "citation_name": "Raza, Syed Jaffar", "affil_ix": 1, "is_corresponding": False},
            {"name": "Joshua T. Watkins", "citation_name": "Watkins, Joshua T.", "affil_ix": 1, "is_corresponding": False},
            {"name": "Abbey Lin", "citation_name": "Lin, Abbey", "affil_ix": 1, "is_corresponding": False},
            {"name": "Visalsaya Chakpuang", "citation_name": "Chakpuang, Visalsaya", "affil_ix": 1, "is_corresponding": False},
            {"name": "Andrew K. Dickerson", "citation_name": "Dickerson, Andrew K.", "affil_ix": 1, "is_corresponding": False},
        ],
        "affiliations": [
            "Department of Mechanical, Aerospace and Biomedical Engineering, University of Tennessee, Knoxville, Tennessee 37996, USA",
        ],
        "contact_email": "grible@vols.utk.edu",
        "abstract": (
            "This experimental work builds on our previous studies on the post-impact "
            "characteristics of drops striking three-dimensional-printed fiber arrays by "
            "investigating the highly transient characteristics of impact. We measure "
            "temporal changes in drop penetration depth, lateral spreading, and drop dome "
            "height along the fiber array at the drop impacts. Liquid penetration of "
            "vertical fibers can be divided into three sequential periods with linearly "
            "approximated rates of penetration: (i) an inertial regime, where penetration "
            "dynamics are governed by inertia; (ii) a transitional regime exhibiting "
            "inertial and capillary action; and (iii) a capillary regime characterized "
            "purely by downward wicking. Horizontal fibers exhibit only the inertial and "
            "transitional stages, with wicking only observed horizontally along the "
            "direction of fibers. In horizontal hydrodynamic fiber arrays, the time duration "
            "to reach the maximum lateral deformation of the depth is proportional to We"
            "¹ᐟ⁴, as observed in drops impacting solid surfaces. There exists "
            "a critical Weber number below which the drop shows no radial deformation, and "
            "the critical value increases with decreasing fiber density. At large Weber "
            "numbers, drops splash. In contrast, vertical fibers restrict the lateral "
            "spreading of the drop, thereby suppressing a splash for all tested drop "
            "velocities, even those exceeding 5 m/s."
        ),
        "firsts": [
            {"icon": "fas fa-stopwatch", "title": "Three penetration regimes on vertical fibers", "summary": "Inertial, transitional, capillary: each with a distinct linear penetration rate.", "section": "section-three-regimes"},
            {"icon": "fas fa-chart-line", "title": "We¹ᐟ⁴ scaling for lateral deformation", "summary": "On horizontal arrays, the time to peak lateral spread scales as We¹ᐟ⁴, matching the canonical drop-on-solid result.", "section": "section-scaling"},
            {"icon": "fas fa-circle-half-stroke", "title": "Critical Weber for radial deformation", "summary": "Below a critical We, the drop does not radially deform; the critical value rises as fiber density falls.", "section": "section-critical"},
            {"icon": "fas fa-shield-halved", "title": "Splash suppression at all tested velocities", "summary": "Vertical arrays restrict lateral spreading enough that drops do not splash, even above 5 m/s.", "section": "section-splash"},
        ],
        "result_sections": [
            {"id": "section-three-regimes", "title": "Three sequential penetration regimes on vertical fibers",
             "explanation": "Time-resolved imaging reveals three linearly-approximated penetration rates: an inertial period, a transitional period (inertia plus capillarity), and a final capillary period of pure downward wicking.",
             "figs": 2,
             "pair_layout": "stacked",
             "images": [
                 {"path": "static/images/splash-suppression/fig4.png",
                  "alt": "Figure 4 from the paper: image sequence showing the characteristic temporal events in the spreading and penetration of liquid within the array for a single trial."},
                 {"path": "static/images/splash-suppression/fig6.png",
                  "alt": "Figure 6 from the paper: three regimes characterizing the penetration behavior of a drop impacting a vertical fiber array: inertial, inertial-capillary, and capillary."},
             ]},
            {"id": "section-scaling", "title": "Lateral deformation: We¹ᐟ⁴ scaling",
             "explanation": "On horizontal arrays, the time to reach maximum lateral deformation scales with We¹ᐟ⁴, mirroring drops on solid surfaces.",
             "figs": 1,
             "image": "static/images/splash-suppression/fig10.png",
             "alt": "Figure 10 from the paper: first instance of local maximum spread vs Weber number for hydrophilic horizontal fibers, with linear scaling fits across multiple densities."},
            {"id": "section-critical", "title": "A critical Weber number for radial deformation",
             "explanation": "Below this critical value the drop barely spreads; the threshold rises as fiber density drops.",
             "figs": 1,
             "image": "static/images/splash-suppression/fig12.png",
             "alt": "Figure 12 from the paper: first instance of local maximum spread vs Weber number for hydrophilic vertical fibers, with the critical Weber number printed on each panel."},
            {"id": "section-splash", "title": "Vertical arrays suppress splash",
             "explanation": "Because vertical fibers restrict lateral motion of the impacting liquid, splash is suppressed for all drop velocities we test, including impacts faster than 5 m/s.",
             "figs": 1,
             "image": "static/images/splash-suppression/fig3.png",
             "alt": "Figure 3 from the paper: image sequence of a 3 mm drop impacting at raindrop speed on a solid surface, a horizontal fiber array, a vertical fiber array, and a side-by-side comparison. Shows splash on solid and horizontal, suppression on vertical."},
        ],
        "journal": "Physics of Fluids",
        "journal_abbrev": "Phys. Fluids",
        "publisher": "AIP Publishing",
        "issn": "1070-6631",
        "volume": "37",
        "issue": "9",
        "firstpage": "092106",
        "lastpage": "092106",
        "doi": "10.1063/5.0286271",
        "pub_date_iso": "2025-09-04",
        "pub_year": "2025",
        "supp_pdf_source": None,
        "videos": [],
        "videos_note": (
            "3 supplementary movies pending upload to YouTube:\n"
            "• Movie 1: Drop on solid, horizontal, and vertical arrays at raindrop speed (pairs with Fig. 3)\n"
            "• Movie 2: Temporal events in drop spread and penetration (pairs with Fig. 4)\n"
            "• Movie 3: Three penetration regimes (inertial, inertial-capillary, capillary) (pairs with Fig. 6)"
        ),
        "keywords": "splash suppression, drop impact, vertical fibers, capillary wicking, Weber number scaling, transient penetration",
        "acknowledgments": "This research was partially funded by the National Science Foundation (CMMI 1825801 and CBET 1825801). We thank undergraduate research assistants at the Fluids and Structures Laboratory, Hadi Bhidya for bespoke code and video analysis contributions, and Aaron Matheny for performing drop impact experiments at raindrop velocities.",
        "bibkey": "rible2025splash",
        "tagline_card": "Three sequential penetration regimes (inertial, transitional, capillary) on vertical fibers; vertical arrays suppress splashing for all tested drop velocities, even beyond 5 m/s.",
    },
    {
        "slug": "cross-section-circularity",
        "title": "Cross-sectional circularity promotes dynamic drop penetration of horizontal fiber arrays",
        "tagline": "Circular fibers let drops in by 26% more than wedged ones, despite being more hydrophilic. Geometry overrides wettability.",
        "authors": [
            {"name": "Gene Patrick S. Rible", "citation_name": "Rible, Gene Patrick S.", "affil_ix": 1, "is_corresponding": True},
            {"name": "Syed Jaffar Raza", "citation_name": "Raza, Syed Jaffar", "affil_ix": 1, "is_corresponding": False},
            {"name": "Jackson H. Boger", "citation_name": "Boger, Jackson H.", "affil_ix": 1, "is_corresponding": False},
            {"name": "Hannah H. Osman", "citation_name": "Osman, Hannah H.", "affil_ix": 1, "is_corresponding": False},
            {"name": "Aidan D. Holihan", "citation_name": "Holihan, Aidan D.", "affil_ix": 1, "is_corresponding": False},
            {"name": "Braeden K. Elbers", "citation_name": "Elbers, Braeden K.", "affil_ix": 1, "is_corresponding": False},
            {"name": "Kyle R. Brown", "citation_name": "Brown, Kyle R.", "affil_ix": 1, "is_corresponding": False},
            {"name": "Christopher M. Schenck", "citation_name": "Schenck, Christopher M.", "affil_ix": 1, "is_corresponding": False},
            {"name": "Benjamin J. Reed", "citation_name": "Reed, Benjamin J.", "affil_ix": 1, "is_corresponding": False},
            {"name": "Andrew K. Dickerson", "citation_name": "Dickerson, Andrew K.", "affil_ix": 1, "is_corresponding": False},
        ],
        "affiliations": [
            "Department of Mechanical, Aerospace and Biomedical Engineering, University of Tennessee, Knoxville, Tennessee 37996, USA",
        ],
        "contact_email": "grible@vols.utk.edu",
        "abstract": (
            "In this experimental work, we compare the drop impact behavior on horizontal "
            "fiber arrays with circular and wedged fiber cross sections. Non-circular fibers "
            "are commonplace in nature, appearing on rain interfacing structures from animal "
            "fur to pine needles. Our arrays of packing densities of ≈50, 100, and 150 "
            "cm⁻² are impacted by drops falling at 0.2–1.6 m/s. A previous work "
            "has shown that hydrophilic, horizontal fiber arrays reduce dynamic drop "
            "penetration more than their hydrophobic counterparts. In this work, we show that "
            "circularity, like hydrophobicity, increases drop penetration. Despite being more "
            "hydrophilic than their non-circular counterparts, our hydrophilic circular fibers "
            "promote drop penetration by 26% more than their non-circular counterparts through "
            "suppression of lateral spreading and promotion of drop fragmentation within the "
            "array. Circular fiber cross sections induce a more circular liquid shape within "
            "the fiber array after infiltration. Using conservation of energy, we developed a "
            "model that predicts the penetration depth within the fiber array using only "
            "measurements from a single external camera above the array. We generalize our "
            "model to accommodate fibers of any convex cross-sectional geometry."
        ),
        "firsts": [
            {"icon": "fas fa-shapes", "title": "First circular-vs-wedge cross-section comparison", "summary": "A controlled experiment isolating fiber cross-section from density and wettability.", "section": "section-cross-section"},
            {"icon": "fas fa-percent", "title": "Circular fibers penetrate 26% deeper", "summary": "Despite being more hydrophilic, circular fibers let drops penetrate 26% more than wedged ones.", "section": "section-26-pct"},
            {"icon": "fas fa-camera-retro", "title": "Single-camera energy model", "summary": "An energy-conservation model that predicts penetration depth from a single external top-down camera.", "section": "section-model"},
            {"icon": "fas fa-vector-square", "title": "Generalized to any convex cross-section", "summary": "The model extends to any convex fiber geometry, not just circular and wedged.", "section": "section-convex"},
        ],
        "result_sections": [
            {"id": "section-cross-section", "title": "Why fiber shape matters separately from packing density", "explanation": "Holding wettability and density constant, we compare circular and wedge-cross-section 3D-printed fibers under identical impacts.", "figs": 2},
            {"id": "section-26-pct", "title": "Geometry overrides wettability for penetration", "explanation": "Circular fibers reduce lateral spreading and promote fragmentation inside the array, deepening the wetted column by 26% on average. Despite being more hydrophilic than the wedge case, circular fibers let drops in more readily.", "figs": 1},
            {"id": "section-model", "title": "Energy model from a single top-down camera", "explanation": "By balancing kinetic energy at impact against the work done by drag and capillary forces in the array, the depth can be inferred from a single external view, sidestepping the need for internal imaging.", "figs": 1},
            {"id": "section-convex", "title": "Generalization to any convex fiber shape", "explanation": "We recast the model in terms of geometric moments that work for any convex cross-section, opening the door to direct comparison with natural fibers (mammalian fur, pine needles, plant trichomes).", "figs": 1},
        ],
        "journal": "Physics of Fluids",
        "journal_abbrev": "Phys. Fluids",
        "publisher": "AIP Publishing",
        "issn": "1070-6631",
        "volume": "37",
        "issue": "12",
        "firstpage": "122110",
        "lastpage": "122110",
        "doi": "10.1063/5.0287633",
        "pub_date_iso": "2025-12-04",
        "pub_year": "2025",
        "supp_pdf_source": None,
        "videos": [],
        "videos_note": "Supplementary movies for this paper are pending upload to YouTube. Drop YouTube IDs into PAPERS[4]['videos'] in build.py and re-run.",
        "keywords": "fiber cross-section, drop penetration, circular fibers, wedge fibers, energy conservation, convex geometry, mammalian fur, pine needles",
        "acknowledgments": "We acknowledge support from the University of Tennessee, Knoxville and the contributions of undergraduate researchers in the Dickerson Lab.",
        "bibkey": "rible2025crosssection",
        "tagline_card": "Circular fiber cross-sections increase drop penetration by 26% over wedged ones, despite being more hydrophilic. Geometry trumps wettability.",
    },
    {
        "slug": "fur-pelts",
        "title": "Fur roughness, density, and length reduce raindrop penetration of mammalian pelts",
        "tagline": "Six pelts (zebra, grey wolf, moose, beaver, mink, sea otter): a dual-layer hydrophilic/hydrophobic structure carves a saturating dry zone under rain.",
        "authors": [
            {"name": "Gene Patrick S. Rible", "citation_name": "Rible, Gene Patrick S.", "affil_ix": 1, "is_corresponding": True},
            {"name": "John M. Wylie", "citation_name": "Wylie, John M.", "affil_ix": 1, "is_corresponding": False},
            {"name": "Braeden K. Elbers", "citation_name": "Elbers, Braeden K.", "affil_ix": 1, "is_corresponding": False},
            {"name": "David Job Dooley", "citation_name": "Dooley, David Job", "affil_ix": 1, "is_corresponding": False},
            {"name": "Cora L. Thomas", "citation_name": "Thomas, Cora L.", "affil_ix": 1, "is_corresponding": False},
            {"name": "Andrew K. Dickerson", "citation_name": "Dickerson, Andrew K.", "affil_ix": 1, "is_corresponding": False},
        ],
        "affiliations": [
            "Department of Mechanical, Aerospace and Biomedical Engineering, University of Tennessee, Knoxville, Tennessee 37996, USA",
        ],
        "contact_email": "grible@vols.utk.edu",
        "abstract": (
            "This experimental work explores the relationship between the properties and "
            "structure of mammalian fur from different habitats and the depth of water drop "
            "penetration when impacted in succession. For most mammals, water penetration "
            "depth reaches a saturation point, beyond which it no longer increases, creating "
            "a dry insulating air layer near the skin regardless of repeated water impacts. "
            "To understand this phenomenon, we define several dimensionless quantities "
            "representing fur macro-properties, such as guard hair and underfur densities, "
            "guard hair and underfur lengths, contact angles, and equivalent diameters. "
            "Additionally, we examine microscopic properties such as the aspect ratio and "
            "roughness of individual fiber scales. We establish connections between these "
            "macro- and microscopic characteristics, the thickness of the dry zone, the depth "
            "of water penetration, and the rate at which penetration depth decays "
            "exponentially. Our results show that the distal diameter influences the rate at "
            "which the penetration depth of water decays with additional impacts. Generally, "
            "a higher pelage density, larger guard hair diameter, and increased fur roughness "
            "contribute to a thicker dry zone. Using digital microscopy, we confirm that "
            "mammalian guard fur is hydrophilic, resisting dynamic penetration, whereas the "
            "finer and denser underfur is hydrophobic, resisting static penetration. This "
            "dual-layer structure allows mammals to resist wetting during a heavy rainfall."
        ),
        "firsts": [
            {"icon": "fas fa-paw", "title": "Macro–micro property catalog for six pelts", "summary": "Guard hair and underfur densities, lengths, contact angles, scale roughness, and equivalent diameters across zebra, grey wolf, moose, beaver, mink, and sea otter.", "section": "section-catalog"},
            {"icon": "fas fa-chart-line", "title": "Saturating dry zone under repeated impacts", "summary": "After enough impacts, water penetration depth saturates, leaving a permanent dry air layer next to the skin.", "section": "section-saturation"},
            {"icon": "fas fa-layer-group", "title": "Dual-layer hydrophilic–hydrophobic structure", "summary": "Guard hair is hydrophilic (resisting dynamic penetration); underfur is hydrophobic (resisting static penetration). The combination is the wetting barrier.", "section": "section-dual-layer"},
            {"icon": "fas fa-ruler-combined", "title": "Distal diameter sets the decay rate", "summary": "How fast successive impacts stop deepening the wetted column depends on the distal fiber diameter, with guard hair density and roughness setting the dry-zone thickness.", "section": "section-decay"},
        ],
        "result_sections": [
            {"id": "section-catalog", "title": "Cataloging fur across habitats", "explanation": "We sample fur from six mammals spanning terrestrial, semi-aquatic, and fully aquatic habitats. For each pelt, we quantify guard-hair and underfur length, density, contact angle, equivalent diameter, plus microscopic scale aspect ratio and roughness.", "figs": 2},
            {"id": "section-saturation", "title": "Why penetration depth saturates", "explanation": "Repeated drop impacts deepen the wetted column up to a point, after which the dry air layer near the skin remains stable. We model the exponential decay of the per-impact depth gain.", "figs": 1},
            {"id": "section-dual-layer", "title": "Two layers, two wettabilities, one barrier", "explanation": "Digital microscopy reveals that guard hair is hydrophilic (resisting dynamic penetration by spreading impact energy laterally) while underfur is hydrophobic (resisting static penetration by capillarity). Together they form the dry barrier.", "figs": 1},
            {"id": "section-decay", "title": "Distal diameter controls how fast saturation arrives", "explanation": "Among the macro variables, distal guard-hair diameter sets the decay rate of per-impact gain. Pelage density and roughness set the saturation thickness.", "figs": 1},
        ],
        "journal": "Bioinspiration & Biomimetics",
        "journal_abbrev": "Bioinspir. Biomim.",
        "publisher": "IOP Publishing",
        "issn": "1748-3190",
        "volume": "21",
        "issue": "3",
        "firstpage": "036008",
        "lastpage": "036008",
        "doi": "10.1088/1748-3190/ae66c1",
        "pub_date_iso": "2026-05-21",
        "pub_year": "2026",
        "supp_pdf_source": "anthology/supplementary/bbae66c1supp1.pdf",
        # Zenodo dataset DOI: paste the actual DOI here (without "https://doi.org/" prefix)
        "dataset_doi": "",
        "videos": [],
        "videos_note": "Supplementary movies for this paper are pending upload to YouTube. Drop YouTube IDs into PAPERS[5]['videos'] in build.py and re-run.",
        "keywords": "mammalian fur, raindrop penetration, pelage, guard hair, underfur, hydrophobic, hydrophilic, scale roughness, dry zone, thermoregulation, bioinspiration",
        "acknowledgments": "We acknowledge support from the University of Tennessee, Knoxville and the contributions of undergraduate researchers in the Dickerson Lab.",
        "bibkey": "rible2026fur",
        "tagline_card": "Six mammalian pelts: a dual-layer hydrophilic/hydrophobic guard-hair-vs-underfur structure produces a saturating dry zone under repeated rainfall.",
    },
]


# ----------------------------------------------------------------------------
# RENDER HELPERS
# ----------------------------------------------------------------------------

def attr(s: str) -> str:
    """HTML-escape a string for use as an attribute value (quote=True)."""
    return html.escape(s, quote=True)


# --- Inline-HTML rendering for scientific prose -------------------------------
# Subscript shortcut: <var>_<sub> -> <i>var</i><sub>sub</sub>
_SUB_VARS_RE = r"(?:d|D|U|t|We|Re|Oh|Bo|AR\*?|τ|χ|ρ|μ|σ|θ)"
_SUB_PATTERN = re.compile(rf"\b({_SUB_VARS_RE})_([A-Za-z0-9]{{1,4}})\b")
# "We" italicization: only when followed (within whitespace) by a math operator,
# exponent, terminal punctuation, or end-of-string. Avoids the pronoun "We"
# followed by a verb. Note: "<" / ">" have already been escaped to &lt; / &gt;
# by html.escape, so we match the entity forms.
_WE_MATH = re.compile(
    r"\bWe(?=\s*(?:[≈=≪≫≤≥·×/^,.;:!?)\]]"
    r"|&lt;|&gt;|<sub>|<sup>|[⁰¹²³⁴⁵⁶⁷⁸⁹ᐟ]|$))"
)
# Other multi-letter dimensionless groups have no English-word conflicts.
# Lookahead `(?![A-Za-z])` (rather than `\b`) lets the optional `*` at the
# end of "AR*" / "Re*" match correctly — `\b` fails between `*` and a space.
_OTHER_DIM = re.compile(r"\b(AR\*?|Re\*?|Oh|Bo)(?![A-Za-z])")
# Lowercase Greek letters used as physics variables.
_GREEK = re.compile(r"([ρμσθχτφλα])")


def science_text(s: str) -> str:
    """Convert authored plain text into inline HTML for scientific prose.

    - Escapes &, <, > first.
    - Subscript shortcut: ``We_c`` -> ``We_c``.
    - Italicizes ``AR``, ``AR*``, ``Re``, ``Oh``, ``Bo`` unconditionally.
    - Italicizes ``We`` only when followed by a math indicator or terminal
      punctuation (so the pronoun "We measure" stays upright, but "We ≈ 80",
      "We¹ᐟ⁴", "critical We," and "We < 50" all italicize).
    - Italicizes lowercase Greek symbols.
    Subscripts and superscripts themselves stay upright (the convention).
    """
    s = html.escape(s)
    s = _SUB_PATTERN.sub(
        lambda m: f"<i>{m.group(1)}</i><sub>{m.group(2)}</sub>", s
    )
    s = _WE_MATH.sub(r"<i>We</i>", s)
    s = _OTHER_DIM.sub(r"<i>\1</i>", s)
    s = _GREEK.sub(r"<i>\1</i>", s)
    return s


def doi_url(doi: str) -> str:
    return f"https://doi.org/{doi}"


def short_authors(authors, max_n=3):
    names = [a["name"] for a in authors]
    if len(names) <= max_n + 1:
        return ", ".join(names)
    return ", ".join(names[:max_n]) + f", …, {names[-1]}"


def authors_html(authors):
    parts = []
    for a in authors:
        star = "<sup>*</sup>" if a.get("is_corresponding") else ""
        parts.append(
            f"<span class=\"author-block\">{html.escape(a['name'])}{star}</span>"
        )
    return ", ".join(parts)


def citation_author_tags(authors) -> str:
    return "\n  ".join(
        f"<meta name=\"citation_author\" content=\"{attr(a['citation_name'])}\">"
        for a in authors
    )


def affiliations_html(affils) -> str:
    if len(affils) == 1:
        return f"<span class=\"affil-block\">{html.escape(affils[0])}</span>"
    parts = []
    for i, af in enumerate(affils, 1):
        parts.append(
            f"<span class=\"affil-block\"><sup>{i}</sup>{html.escape(af)}</span>"
        )
    return "<br>".join(parts)


def contact_line(paper) -> str:
    email = paper["contact_email"]
    return (
        f"<em><sup>*</sup>Contact researchers: "
        f"<a href=\"mailto:{email}\" style=\"text-decoration: underline;\">{email}</a></em>"
    )


def journal_badge(paper) -> str:
    j = paper["journal"]
    return f"{html.escape(j)}&nbsp;<strong>{paper['volume']}</strong>, "\
           f"{paper['firstpage']} ({paper['pub_year']})"


def pages_field(paper) -> str:
    if paper.get("lastpage") and paper["lastpage"] != paper["firstpage"]:
        return f"{paper['firstpage']}–{paper['lastpage']}"
    return paper["firstpage"]


def bibtex(paper) -> str:
    auths = " and ".join(a["citation_name"] for a in paper["authors"])
    return textwrap.dedent(f"""\
        @article{{{paper['bibkey']},
          author  = {{{auths}}},
          title   = {{{paper['title']}}},
          journal = {{{paper['journal']}}},
          volume  = {{{paper['volume']}}},
          number  = {{{paper['issue']}}},
          pages   = {{{pages_field(paper).replace('–', '--')}}},
          year    = {{{paper['pub_year']}}},
          doi     = {{{paper['doi']}}}
        }}""")


def citation_text_plain(paper) -> str:
    # "LastName, GivenInitials." per author, separated by commas, "and" before last
    parts = []
    for a in paper["authors"]:
        last, given = a["citation_name"].split(", ", 1)
        initials = "".join(
            p[0] + "."
            for p in given.replace("-", " ").split()
            if p
        )
        parts.append(f"{last}, {initials}")
    if len(parts) > 1:
        authors_str = ", ".join(parts[:-1]) + ", and " + parts[-1]
    else:
        authors_str = parts[0]
    return (
        f"{authors_str} ({paper['pub_year']}). {paper['title']}. "
        f"{paper['journal']}, {paper['volume']}({paper['issue']}), "
        f"{pages_field(paper)}. {doi_url(paper['doi'])}"
    )


def citation_text_html(paper) -> str:
    parts = []
    for a in paper["authors"]:
        last, given = a["citation_name"].split(", ", 1)
        initials = "".join(
            p[0] + "."
            for p in given.replace("-", " ").split()
            if p
        )
        parts.append(f"{html.escape(last)}, {html.escape(initials)}")
    if len(parts) > 1:
        authors_str = ", ".join(parts[:-1]) + ", and " + parts[-1]
    else:
        authors_str = parts[0]
    return (
        f"{authors_str} ({paper['pub_year']}). {html.escape(paper['title'])}. "
        f"<i>{html.escape(paper['journal'])}</i>, "
        f"<b>{paper['volume']}</b>({paper['issue']}), {pages_field(paper)}. "
        f"<a href=\"{doi_url(paper['doi'])}\">{doi_url(paper['doi'])}</a>"
    )


def firsts_cards(paper, base_path=""):
    """base_path: '' for subpage (anchor stays on same page), or 'slug/' for hub.

    Two layout modes:

    1. New explicit-cells mode (`firsts_cells` set on the paper):
       The cells list contains image/video/card cells in exact display order.
       Each cell occupies one Bulma `.column is-half` slot in the grid.

    2. Legacy mode (`firsts` + optional `firsts_video_src`):
       Renders the firsts list as cards, optionally prepended with a video
       tile in the upper-left. Falls back to lone-last-centering when the
       resulting cell count is odd.
    """
    cells = []

    # New mode: explicit firsts_cells
    if paper.get("firsts_cells"):
        n = len(paper["firsts_cells"])
        for i, c in enumerate(paper["firsts_cells"]):
            # Full-width cell? Otherwise apply lone-last centering when the
            # half-width count is odd.
            if c.get("is_full"):
                col_class = "column is-full"
            else:
                is_lone_last = (n % 2 == 1) and (i == n - 1)
                col_class = "column is-half is-offset-one-quarter" if is_lone_last else "column is-half"
            if c["kind"] == "image":
                align_class = " align-left" if c.get("align") == "left" else ""
                cells.append(textwrap.dedent(f"""\
                    <div class="{col_class}">
                      <div class="first-card first-card-image{align_class}">
                        <img class="firsts-image" src="../{c['src']}" alt="{attr(c.get('alt', ''))}">
                      </div>
                    </div>"""))
            elif c["kind"] == "video":
                type_attr = f' type="{attr(c["type"])}"' if c.get("type") else ""
                align_class = " align-left" if c.get("align") == "left" else ""
                cells.append(textwrap.dedent(f"""\
                    <div class="{col_class}">
                      <div class="first-card first-card-video{align_class}">
                        <video class="firsts-video" muted autoplay loop playsinline preload="metadata">
                          <source src="../{c['src']}"{type_attr}>
                        </video>
                      </div>
                    </div>"""))
            elif c["kind"] == "card":
                href = f"{base_path}#{c['section']}"
                cells.append(textwrap.dedent(f"""\
                    <div class="{col_class}">
                      <a class="first-card-link" href="{href}">
                        <div class="first-card">
                          <span class="icon has-text-info"><i class="{c['icon']} fa-lg"></i></span>
                          <h3 class="is-size-5 has-text-weight-bold">{html.escape(c['title'])}</h3>
                          <p>{science_text(c['summary'])}</p>
                        </div>
                      </a>
                    </div>"""))
        return "\n".join(cells)

    # Legacy mode: firsts list + optional video src
    video_src = paper.get("firsts_video_src")
    if video_src:
        cells.append(textwrap.dedent(f"""\
            <div class="column is-half">
              <div class="first-card first-card-video">
                <video class="firsts-video" muted autoplay loop playsinline preload="metadata">
                  <source src="../{video_src}" type="video/mp4">
                </video>
              </div>
            </div>"""))
    n = len(paper["firsts"]) + (1 if video_src else 0)
    for i, f in enumerate(paper["firsts"]):
        href = f"{base_path}#{f['section']}"
        cell_index = i + (1 if video_src else 0)
        is_lone_last = (n % 2 == 1) and (cell_index == n - 1)
        col_class = "column is-half is-offset-one-quarter" if is_lone_last else "column is-half"
        cells.append(textwrap.dedent(f"""\
            <div class="{col_class}">
              <a class="first-card-link" href="{href}">
                <div class="first-card">
                  <span class="icon has-text-info"><i class="{f['icon']} fa-lg"></i></span>
                  <h3 class="is-size-5 has-text-weight-bold">{science_text(f['title'])}</h3>
                  <p>{science_text(f['summary'])}</p>
                </div>
              </a>
            </div>"""))
    return "\n".join(cells)


def render_pre_media(items, layout="stacked"):
    """Render a section's pre-figure media block (YouTube embeds or local
    videos). Returns "" if items is empty.

    layout="stacked" (default): each item full-width, one above the next.
    layout="row": wrap each item in a Bulma is-half column and arrange
    side-by-side in a single .columns row.
    """
    if not items:
        return ""
    blocks = []
    for m in items:
        if m["kind"] == "youtube":
            blocks.append(textwrap.dedent(f"""\
                <div class="pre-figure-media">
                  <h4 class="is-size-6 has-text-weight-bold has-text-centered">{html.escape(m.get('label', ''))}</h4>
                  <div class="video-embed">
                    <iframe src="https://www.youtube.com/embed/{m['youtube_id']}" title="{attr(m.get('label', ''))}"
                            frameborder="0"
                            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                            allowfullscreen></iframe>
                  </div>
                </div>"""))
        elif m["kind"] == "image":
            # Static figure rendered inline among the pre-figure media.
            # Useful when a section wants a video plus an auxiliary figure
            # above the main figure block.
            label_html = (
                f'<h4 class="is-size-6 has-text-weight-bold has-text-centered">{html.escape(m["label"])}</h4>'
                if m.get("label") else ""
            )
            blocks.append(textwrap.dedent(f"""\
                <div class="pre-figure-media">
                  {label_html}
                  <figure class="image">
                    <img src="../{m['path']}" alt="{attr(m.get('alt', ''))}">
                  </figure>
                </div>"""))
        elif m["kind"] == "local":
            loop_attr = " loop" if m.get("loop") else ""
            type_attr = f' type="{attr(m["type"])}"' if m.get("type") else ""
            # Optional float lets the explanation paragraph wrap text around
            # the video. CSS handles sizing + margin for the floated variant.
            float_class = f' float-{m["float"]}' if m.get("float") in ("left", "right") else ""
            blocks.append(textwrap.dedent(f"""\
                <div class="pre-figure-media{float_class}">
                  <video class="pre-figure-video" muted autoplay{loop_attr} playsinline preload="metadata">
                    <source src="../{m['src']}"{type_attr}>
                  </video>
                </div>"""))
    if layout == "row" and len(blocks) > 1:
        cols = "\n".join(
            f'<div class="column is-half">\n{b}\n</div>' for b in blocks
        )
        return (
            '<div class="columns is-multiline pre-figure-row">\n'
            f'{cols}\n'
            '</div>'
        )
    return "\n".join(blocks)


def result_blocks(paper):
    blocks = []
    for r in paper["result_sections"]:
        # Subpages resolve static/ via "../" because the page lives at "/<slug>/".
        if r.get("image"):
            fig_html = textwrap.dedent(f"""\
                <figure class="image">
                  <img src="../{r['image']}" alt="{attr(r.get('alt', ''))}">
                </figure>""")
        elif r.get("images"):  # paired panel: list of {path, alt}
            if r.get("pair_layout") == "stacked":
                # Render each image on its own row, full-width.
                stacked = []
                for img in r["images"]:
                    stacked.append(textwrap.dedent(f"""\
                        <figure class="image">
                          <img src="../{img['path']}" alt="{attr(img.get('alt', ''))}">
                        </figure>"""))
                fig_html = "\n".join(stacked)
            else:
                # Default: side-by-side columns.
                cols = []
                for img in r["images"]:
                    cols.append(textwrap.dedent(f"""\
                        <div class="column">
                          <figure class="image">
                            <img src="../{img['path']}" alt="{attr(img.get('alt', ''))}">
                          </figure>
                        </div>"""))
                fig_html = '<div class="columns is-vcentered figure-pair">\n' + "\n".join(cols) + "\n</div>"
        elif r.get("figs", 1) == 0:
            # No figure at all (e.g. a section whose visual content is
            # entirely pre_media videos above the explanation).
            fig_html = ""
        elif r.get("figs", 1) == 2:
            hints = r.get("placeholder_hints", ["", ""])
            left_hint = (f'<p class="is-size-7 placeholder-hint">{html.escape(hints[0])}</p>'
                         if len(hints) > 0 and hints[0] else "")
            right_hint = (f'<p class="is-size-7 placeholder-hint">{html.escape(hints[1])}</p>'
                          if len(hints) > 1 and hints[1] else "")
            fig_html = textwrap.dedent(f"""\
                <div class="columns is-vcentered figure-pair">
                  <div class="column">
                    <div class="placeholder-box placeholder-16x9">
                      <div class="placeholder-label">
                        <p><strong>Figure placeholder</strong></p>
                        {left_hint}
                        <p class="is-size-7">Drop into <code>static/images/{paper['slug']}/</code> and replace.</p>
                      </div>
                    </div>
                  </div>
                  <div class="column">
                    <div class="placeholder-box placeholder-16x9">
                      <div class="placeholder-label">
                        <p><strong>Figure placeholder</strong></p>
                        {right_hint}
                        <p class="is-size-7">Drop into <code>static/images/{paper['slug']}/</code> and replace.</p>
                      </div>
                    </div>
                  </div>
                </div>""")
        else:
            hint = r.get("placeholder_hint", "")
            hint_html = (f'<p class="is-size-7 placeholder-hint">{html.escape(hint)}</p>'
                         if hint else "")
            fig_html = textwrap.dedent(f"""\
                <div class="placeholder-box placeholder-wide">
                  <div class="placeholder-label">
                    <p><strong>Figure placeholder</strong></p>
                    {hint_html}
                    <p class="is-size-7">Drop into <code>static/images/{paper['slug']}/</code> and replace.</p>
                  </div>
                </div>""")
        # explanation is treated as trusted inline HTML so we can use
        # <sub>, <sup>, <i>, <b>, etc. The metadata is author-authored.
        pre_html = render_pre_media(
            r.get("pre_media", []),
            layout=r.get("pre_media_layout", "stacked"),
        )
        pre_block = (pre_html + "\n") if pre_html else ""
        blocks.append(textwrap.dedent(f"""\
            <div class="result-block" id="{r['id']}">
              <h3 class="title is-4">{science_text(r['title'])}</h3>
              {pre_block}{fig_html}
              <p class="content">{science_text(r['explanation'])}</p>
            </div>"""))
    return "\n".join(blocks)


def video_tiles(paper):
    if not paper["videos"]:
        # Allow videos_note to be a multi-line string with bullet points.
        # Each '\n' becomes a <br>; the placeholder box widens to a wide
        # aspect so the bulleted list has room to breathe.
        note_html = html.escape(paper["videos_note"]).replace("\n", "<br>")
        return textwrap.dedent(f"""\
            <div class="column is-full">
              <div class="placeholder-box placeholder-wide videos-pending">
                <div class="placeholder-label">
                  <span class="icon is-large"><i class="fab fa-youtube fa-2x"></i></span>
                  <p class="videos-note">{note_html}</p>
                </div>
              </div>
            </div>""")
    tiles = []
    n = len(paper["videos"])
    for i, v in enumerate(paper["videos"]):
        # If the count is odd, center the last tile by offsetting it a quarter.
        is_lone_last = (n % 2 == 1) and (i == n - 1)
        col_class = "column is-half is-offset-one-quarter" if is_lone_last else "column is-half"
        tiles.append(textwrap.dedent(f"""\
            <div class="{col_class}">
              <h3 class="is-size-5 has-text-weight-bold has-text-centered">{html.escape(v['label'])}</h3>
              <div class="video-embed">
                <iframe src="https://www.youtube.com/embed/{v['youtube_id']}" title="{attr(v['label'])}"
                        frameborder="0"
                        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                        allowfullscreen></iframe>
              </div>
              <p class="has-text-centered is-size-7">{science_text(v['caption'])}</p>
            </div>"""))
    return "\n".join(tiles)


def teaser_videos_section(paper) -> str:
    """Render a side-by-side teaser-video block. Empty string if not configured."""
    vids = paper.get("teaser_videos") or []
    if not vids:
        return ""
    # Use Bulma columns. Subpages resolve static/ via "../".
    n = len(vids)
    cols = []
    for v in vids:
        type_attr = f' type="{attr(v["type"])}"' if v.get("type") else ""
        cols.append(textwrap.dedent(f"""\
            <div class="column has-text-centered">
              <video class="teaser-video" muted autoplay loop playsinline preload="metadata"
                     aria-label="{attr(v.get('label', ''))}">
                <source src="../{v['src']}"{type_attr}>
              </video>
            </div>"""))
    return textwrap.dedent("""\
        <section class="section teaser-section">
          <div class="container is-max-desktop">
            <div class="columns is-vcentered teaser-grid">
        {cols}
            </div>
          </div>
        </section>""").format(cols="\n".join(cols))


def link_buttons(paper, canonical_subpage_url):
    """Hero buttons. Only render those with real targets."""
    btns = []
    # Paper PDF: override > DOI URL.
    paper_pdf = paper.get("paper_pdf_url") or doi_url(paper["doi"])
    btns.append(textwrap.dedent(f"""\
        <span class="link-block">
          <a href="{paper_pdf}" class="button is-dark is-rounded" target="_blank" rel="noopener">
            <span class="icon"><i class="fas fa-file-pdf"></i></span><span>Paper</span>
          </a>
        </span>"""))
    btns.append(textwrap.dedent(f"""\
        <span class="link-block">
          <a href="{doi_url(paper['doi'])}" class="button is-dark is-rounded" target="_blank" rel="noopener">
            <span class="icon"><i class="ai ai-doi"></i></span><span>DOI</span>
          </a>
        </span>"""))
    if paper.get("supp_pdf_source") or paper.get("supp_pdf_url"):
        # Supplement URL: override > locally-hosted copy.
        supp_url = paper.get("supp_pdf_url") or f"../static/pdfs/{paper['slug']}/supplementary.pdf"
        btns.append(textwrap.dedent(f"""\
            <span class="link-block">
              <a href="{supp_url}" class="button is-dark is-rounded" target="_blank" rel="noopener">
                <span class="icon"><i class="fas fa-file-lines"></i></span><span>Supplement</span>
              </a>
            </span>"""))
    if paper.get("dataset_doi"):
        btns.append(textwrap.dedent(f"""\
            <span class="link-block">
              <a href="https://doi.org/{paper['dataset_doi']}" class="button is-dark is-rounded" target="_blank" rel="noopener">
                <span class="icon"><i class="ai ai-zenodo"></i></span><span>Data</span>
              </a>
            </span>"""))
    # Video (YouTube playlist of supplementary movies)
    if paper.get("youtube_playlist_url"):
        btns.append(textwrap.dedent(f"""\
            <span class="link-block">
              <a href="{paper['youtube_playlist_url']}" class="button is-dark is-rounded" target="_blank" rel="noopener">
                <span class="icon"><i class="fab fa-youtube"></i></span><span>Video</span>
              </a>
            </span>"""))
    # Slides (conference deck, e.g. archived on Zenodo with its own DOI)
    if paper.get("slides_url"):
        btns.append(textwrap.dedent(f"""\
            <span class="link-block">
              <a href="{paper['slides_url']}" class="button is-dark is-rounded" target="_blank" rel="noopener">
                <span class="icon"><i class="fas fa-display"></i></span><span>Slides</span>
              </a>
            </span>"""))
    # Cite dropdown
    btns.append(textwrap.dedent(f"""\
        <span class="link-block">
          <div class="dropdown cite-dropdown">
            <div class="dropdown-trigger">
              <button class="button is-dark is-rounded" aria-haspopup="true" aria-controls="cite-menu">
                <span class="icon"><i class="fas fa-quote-right"></i></span>
                <span>Cite</span>
                <span class="icon is-small"><i class="fas fa-angle-down"></i></span>
              </button>
            </div>
            <div class="dropdown-menu" id="cite-menu" role="menu">
              <div class="dropdown-content">
                <a href="#" class="dropdown-item" data-cite-text
                   data-citation-text="{attr(citation_text_plain(paper))}"
                   data-citation-html="{attr(citation_text_html(paper))}">
                  <span class="icon"><i class="fas fa-copy"></i></span><span class="cite-label">Copy as text</span>
                </a>
                <a href="#citation" class="dropdown-item">
                  <span class="icon"><i class="fas fa-code"></i></span><span>BibTeX (.bib)</span>
                </a>
              </div>
            </div>
          </div>
        </span>"""))
    # Note: Schedule + Discussion are intentionally NOT appended here.
    # They render in their own `.publication-links.engagement-row` block in
    # the template, so they always sit on a visually distinct second row
    # below the per-paper buttons regardless of viewport width.
    return "\n".join(btns)


def engagement_buttons():
    """Schedule + Discussion buttons; rendered on subpages and on the hub.
    Each is omitted if its URL is empty in SITE.
    """
    out = []
    if SITE.get("schedule_url"):
        out.append(textwrap.dedent(f"""\
            <span class="link-block">
              <a href="{SITE['schedule_url']}" class="button is-dark is-rounded" target="_blank" rel="noopener">
                <span class="icon"><i class="fas fa-calendar-check"></i></span><span>Schedule</span>
              </a>
            </span>"""))
    if SITE.get("discussion_url"):
        out.append(textwrap.dedent(f"""\
            <span class="link-block">
              <a href="{SITE['discussion_url']}" class="button is-dark is-rounded" target="_blank" rel="noopener">
                <span class="icon"><i class="fas fa-comments"></i></span><span>Discussion</span>
              </a>
            </span>"""))
    return out


def jsonld_subpage(paper) -> str:
    canonical = SITE["canonical_url"] + paper["slug"] + "/"
    authors_jsonld = ",\n      ".join(
        f'{{"@type": "Person", "name": "{html.escape(a["name"])}", '
        f'"affiliation": {{"@type": "Organization", "name": "{html.escape(paper["affiliations"][a["affil_ix"]-1])}"}}}}'
        for a in paper["authors"]
    )
    return textwrap.dedent(f"""\
        {{
          "@context": "https://schema.org",
          "@type": "ScholarlyArticle",
          "headline": "{html.escape(paper['title'])}",
          "name": "{html.escape(paper['title'])}",
          "author": [
            {authors_jsonld}
          ],
          "datePublished": "{paper['pub_date_iso']}",
          "publisher": {{"@type": "Organization", "name": "{html.escape(paper['publisher'])}"}},
          "isPartOf": {{
            "@type": "PublicationIssue",
            "issueNumber": "{paper['issue']}",
            "isPartOf": {{
              "@type": "PublicationVolume",
              "volumeNumber": "{paper['volume']}",
              "isPartOf": {{
                "@type": "Periodical",
                "name": "{html.escape(paper['journal'])}",
                "issn": "{paper['issn']}"
              }}
            }}
          }},
          "pageStart": "{paper['firstpage']}",
          "identifier": "doi:{paper['doi']}",
          "url": "{canonical}",
          "sameAs": "{doi_url(paper['doi'])}",
          "abstract": "{attr(paper['abstract'])}"
        }}""")


# ----------------------------------------------------------------------------
# PAGE RENDERERS
# ----------------------------------------------------------------------------

SUBPAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">

  <title>{title}</title>
  <meta name="description" content="{description}">
  <meta name="keywords" content="{keywords}">
  <meta name="author" content="{authors_plain}">

  <link rel="canonical" href="{canonical}">

  <meta name="google-site-verification" content="{gsc_token}">
  <meta name="msvalidate.01" content="{bing_token}">

  <!-- Google Scholar citation_* metadata -->
  <meta name="citation_title" content="{title}">
  {citation_author_tags}
  <meta name="citation_publication_date" content="{pub_date_slash}">
  <meta name="citation_journal_title" content="{journal}">
  <meta name="citation_journal_abbrev" content="{journal_abbrev}">
  <meta name="citation_publisher" content="{publisher}">
  <meta name="citation_issn" content="{issn}">
  <meta name="citation_volume" content="{volume}">
  <meta name="citation_issue" content="{issue}">
  <meta name="citation_firstpage" content="{firstpage}">
  <meta name="citation_doi" content="{doi}">
  <meta name="citation_abstract_html_url" content="{doi_url}">
  <meta name="citation_pdf_url" content="{citation_pdf_url}">

  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{description}">
  <meta property="og:type" content="article">
  <meta property="og:url" content="{canonical}">
  <meta property="og:image" content="{canonical_root}static/images/teaser-social.png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="{og_image_alt}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:image" content="{canonical_root}static/images/teaser-social.png">

  <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>{favicon_emoji}</text></svg>">

  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bulma@0.9.4/css/bulma.min.css">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.2/css/all.min.css">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/jpswalsh/academicons@1/css/academicons.min.css">
  <link rel="stylesheet" href="../static/css/index.css">

  <script type="application/ld+json">
  {jsonld}
  </script>
</head>
<body>

<section class="hero is-light">
  <div class="hero-body">
    <div class="container is-max-desktop">
      <div class="columns is-centered">
        <div class="column has-text-centered">
          <p class="is-size-7"><a href="../">← Back to the anthology</a></p>
          <h1 class="title is-2 publication-title">{title}</h1>
          <p class="subtitle is-5 tagline">{tagline}</p>
          <div class="is-size-5 publication-authors">{authors_html}</div>
          <div class="is-size-6 publication-affiliations">
            {affiliations_html}
            <br>
            {contact_line}
          </div>
          <p class="publication-venue">
            <a class="tag is-dark is-medium venue-link"
               href="{doi_url}"
               target="_blank" rel="noopener">
              {journal_badge}
            </a>
          </p>
          <div class="publication-links">
            {link_buttons}
          </div>
          <div class="publication-links engagement-row">
            {engagement_buttons}
          </div>
        </div>
      </div>
    </div>
  </div>
</section>

{teaser_section}

<section class="section">
  <div class="container is-max-desktop">
    <div class="columns is-centered has-text-justified">
      <div class="column is-four-fifths">
        <h2 class="title is-3 has-text-centered">Abstract</h2>
        <div class="content"><p>{abstract}</p></div>
      </div>
    </div>
  </div>
</section>

<section class="section has-background-light">
  <div class="container is-max-desktop">
    <h2 class="title is-3 has-text-centered">Firsts in this work</h2>
    <p class="subtitle is-6 has-text-centered firsts-sub">
      New experimental tools and observations from this paper.
    </p>
    {firsts_intro_image_html}
    <div class="columns is-multiline">
      {firsts_cards}
    </div>
    {walkthrough_block}
  </div>
</section>

<section class="section">
  <div class="container is-max-desktop">
    <h2 class="title is-3 has-text-centered">How it works and what we found</h2>
    {result_blocks}
  </div>
</section>

<section class="section has-background-light">
  <div class="container is-max-desktop">
    <h2 class="title is-3 has-text-centered">Supplementary videos</h2>
    {video_playlist_link}
    <div class="columns is-multiline">
      {video_tiles}
    </div>
  </div>
</section>

<section class="section" id="citation">
  <div class="container is-max-desktop">
    <h2 class="title is-3 has-text-centered">Citation</h2>
    <div class="content"><pre class="bibtex"><code>{bibtex_block}</code></pre></div>
  </div>
</section>

<section class="section has-background-light">
  <div class="container is-max-desktop">
    <h2 class="title is-4 has-text-centered">Acknowledgments</h2>
    <div class="content has-text-centered"><p>{acknowledgments}</p></div>
  </div>
</section>

<section class="section" id="discussion">
  <div class="container is-max-desktop">
    <h2 class="title is-3 has-text-centered">Discussion</h2>
    <p class="subtitle is-6 has-text-centered firsts-sub">
      Questions, comments, and follow-up work. Sign in with GitHub to post.
    </p>
    <div class="giscus-wrap">
{giscus_html}
    </div>
  </div>
</section>

<footer class="footer">
  <div class="container is-max-desktop has-text-centered">
    <p class="is-size-7">
      <a href="{repo_url}" target="_blank" rel="noopener">Source for this page</a>
      &nbsp;&middot;&nbsp;
      Template adapted from
      <a href="https://github.com/nerfies/nerfies.github.io" target="_blank" rel="noopener">Nerfies</a>,
      used under
      <a href="http://creativecommons.org/licenses/by-sa/4.0/" target="_blank" rel="noopener">CC&nbsp;BY-SA&nbsp;4.0</a>.
    </p>
  </div>
</footer>

<script src="../static/js/index.js" defer></script>
</body>
</html>
"""


HUB_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">

  <title>{body_of_work_title}</title>
  <meta name="description" content="{description}">
  <meta name="keywords" content="{keywords}">
  <meta name="author" content="{lead_authors_plain}">

  <link rel="canonical" href="{canonical}">
  <meta name="google-site-verification" content="{gsc_token}">
  <meta name="msvalidate.01" content="{bing_token}">

  <!-- Google Scholar citation_* metadata for the most recent paper in this body of work -->
  <meta name="citation_title" content="{latest_title}">
  {latest_citation_author_tags}
  <meta name="citation_publication_date" content="{latest_pub_date_slash}">
  <meta name="citation_journal_title" content="{latest_journal}">
  <meta name="citation_journal_abbrev" content="{latest_journal_abbrev}">
  <meta name="citation_publisher" content="{latest_publisher}">
  <meta name="citation_issn" content="{latest_issn}">
  <meta name="citation_volume" content="{latest_volume}">
  <meta name="citation_issue" content="{latest_issue}">
  <meta name="citation_firstpage" content="{latest_firstpage}">
  <meta name="citation_doi" content="{latest_doi}">
  <meta name="citation_abstract_html_url" content="{latest_doi_url}">

  <meta property="og:title" content="{body_of_work_title}">
  <meta property="og:description" content="{description}">
  <meta property="og:type" content="website">
  <meta property="og:url" content="{canonical}">
  <meta property="og:image" content="{canonical}static/images/teaser-social.png">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:image" content="{canonical}static/images/teaser-social.png">

  <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>{favicon_emoji}</text></svg>">

  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bulma@0.9.4/css/bulma.min.css">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.2/css/all.min.css">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/jpswalsh/academicons@1/css/academicons.min.css">
  <link rel="stylesheet" href="static/css/index.css">

  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "Collection",
    "name": "{body_of_work_title}",
    "description": "{description}",
    "url": "{canonical}",
    "hasPart": [
      {hub_collection_parts}
    ]
  }}
  </script>
</head>
<body>

<section class="hero is-light">
  <div class="hero-body">
    <div class="container is-max-desktop">
      <div class="columns is-centered">
        <div class="column has-text-centered">
          <h1 class="title is-2 publication-title">{body_of_work_title}</h1>
          <p class="subtitle is-5 tagline">{tagline}</p>
          <div class="is-size-5 publication-authors">{lead_authors_html}</div>
          <div class="is-size-6 publication-affiliations">
            {affiliations_html}
            <br>
            {contact_line_hub}
          </div>
          <div class="publication-links">
            <span class="link-block">
              <a href="#papers" class="button is-dark is-rounded">
                <span class="icon"><i class="fas fa-list"></i></span><span>The papers</span>
              </a>
            </span>
            <span class="link-block">
              <a href="#citation" class="button is-dark is-rounded">
                <span class="icon"><i class="fas fa-quote-right"></i></span><span>Cite all six</span>
              </a>
            </span>
          </div>
          <div class="publication-links engagement-row">
            {engagement_buttons}
          </div>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container is-max-desktop">
    <div class="columns is-centered has-text-justified">
      <div class="column is-four-fifths">
        <h2 class="title is-3 has-text-centered">About this research program</h2>
        <div class="content"><p>{program_description}</p></div>
      </div>
    </div>
  </div>
</section>

<section class="section has-background-light" id="papers">
  <div class="container is-max-desktop">
    <h2 class="title is-3 has-text-centered">Papers</h2>
    <p class="subtitle is-6 has-text-centered firsts-sub">
      Each card links to a per-paper page with the abstract, key findings, figures, and citation.
    </p>
    <div class="columns is-multiline">
      {hub_paper_cards}
    </div>
  </div>
</section>

<section class="section" id="citation">
  <div class="container is-max-desktop">
    <h2 class="title is-3 has-text-centered">Citation (BibTeX)</h2>
    <p class="subtitle is-6 has-text-centered firsts-sub">
      All six entries in chronological order.
    </p>
    <div class="content"><pre class="bibtex"><code>{combined_bibtex}</code></pre></div>
  </div>
</section>

<section class="section has-background-light">
  <div class="container is-max-desktop">
    <h2 class="title is-4 has-text-centered">Acknowledgments</h2>
    <div class="content has-text-centered"><p>{acknowledgments}</p></div>
  </div>
</section>

<section class="section" id="discussion">
  <div class="container is-max-desktop">
    <h2 class="title is-3 has-text-centered">Discussion</h2>
    <p class="subtitle is-6 has-text-centered firsts-sub">
      Questions, comments, and follow-up work. Sign in with GitHub to post.
    </p>
    <div class="giscus-wrap">
{giscus_html}
    </div>
  </div>
</section>

<footer class="footer">
  <div class="container is-max-desktop has-text-centered">
    <p class="is-size-7">
      <a href="{repo_url}" target="_blank" rel="noopener">Source for this page</a>
      &nbsp;&middot;&nbsp;
      Template adapted from
      <a href="https://github.com/nerfies/nerfies.github.io" target="_blank" rel="noopener">Nerfies</a>,
      used under
      <a href="http://creativecommons.org/licenses/by-sa/4.0/" target="_blank" rel="noopener">CC&nbsp;BY-SA&nbsp;4.0</a>.
    </p>
  </div>
</footer>

<script src="static/js/index.js" defer></script>
</body>
</html>
"""


def render_subpage(paper):
    canonical = SITE["canonical_url"] + paper["slug"] + "/"
    description = f"{paper['title']}. {paper['journal']} ({paper['pub_year']}). " \
                  f"Lead author: Gene Patrick S. Rible."
    pub_date_slash = paper["pub_date_iso"].replace("-", "/")
    # citation_pdf_url should be the actual PDF if available; Google Scholar uses it.
    citation_pdf = paper.get("paper_pdf_url") or doi_url(paper["doi"])
    return SUBPAGE_TEMPLATE.format(
        title=html.escape(paper["title"]),
        description=attr(description),
        keywords=attr(paper["keywords"]),
        authors_plain=attr(", ".join(a["name"] for a in paper["authors"])),
        canonical=canonical,
        canonical_root=SITE["canonical_url"],
        gsc_token=SITE["gsc_token"],
        bing_token=SITE["bing_token"],
        citation_author_tags=citation_author_tags(paper["authors"]),
        pub_date_slash=pub_date_slash,
        journal=html.escape(paper["journal"]),
        journal_abbrev=html.escape(paper["journal_abbrev"]),
        publisher=html.escape(paper["publisher"]),
        issn=paper["issn"],
        volume=paper["volume"],
        issue=paper["issue"],
        firstpage=paper["firstpage"],
        doi=paper["doi"],
        doi_url=doi_url(paper["doi"]),
        citation_pdf_url=citation_pdf,
        og_image_alt=attr(f"Teaser for {paper['title']}"),
        favicon_emoji=SITE["favicon_emoji"],
        jsonld=jsonld_subpage(paper),
        tagline=science_text(paper["tagline"]),
        authors_html=authors_html(paper["authors"]),
        affiliations_html=affiliations_html(paper["affiliations"]),
        contact_line=contact_line(paper),
        journal_badge=journal_badge(paper),
        link_buttons=link_buttons(paper, canonical),
        engagement_buttons="\n".join(engagement_buttons()),
        teaser_section=teaser_videos_section(paper),
        abstract=science_text(paper["abstract"]),
        firsts_cards=firsts_cards(paper),
        firsts_intro_image_html=(
            textwrap.dedent(f"""\
                <figure class="image firsts-intro-image">
                  <img src="../{paper['firsts_intro_image']['src']}"
                       alt="{attr(paper['firsts_intro_image'].get('alt', ''))}">
                </figure>""")
            if paper.get("firsts_intro_image") else ""
        ),
        walkthrough_block=(
            textwrap.dedent(f"""\
                <div class="walkthrough-block">
                  <h3 class="title is-4 has-text-centered walkthrough-title">Watch the 10-minute walkthrough</h3>
                  <div class="video-embed walkthrough-embed">
                    <iframe src="https://www.youtube.com/embed/{paper['walkthrough_youtube_id']}"
                            title="Author walkthrough of {attr(paper['title'])}"
                            frameborder="0"
                            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                            allowfullscreen></iframe>
                  </div>
                </div>""")
            if paper.get("walkthrough_youtube_id") else ""
        ),
        result_blocks=result_blocks(paper),
        video_tiles=video_tiles(paper),
        video_playlist_link=(
            f'<p class="subtitle is-6 has-text-centered firsts-sub">'
            f'<a href="{paper["youtube_playlist_url"]}" target="_blank" rel="noopener">'
            f'Watch all of them as a playlist on YouTube &rarr;</a></p>'
            if paper.get("youtube_playlist_url") else ""
        ),
        bibtex_block=html.escape(bibtex(paper)),
        acknowledgments=html.escape(paper["acknowledgments"]),
        giscus_html=SITE.get("giscus_html", ""),
        repo_url=SITE["repo_url"],
    )


def hub_paper_cards():
    cards = []
    for p in PAPERS:
        cards.append(textwrap.dedent(f"""\
            <div class="column is-half">
              <a class="first-card-link" href="{p['slug']}/">
                <div class="first-card">
                  <h3 class="is-size-5 has-text-weight-bold">{html.escape(p['title'])}</h3>
                  <p class="is-size-7" style="color:#777;margin-top:0.4rem;">{html.escape(short_authors(p['authors']))}</p>
                  <p class="is-size-7" style="color:#777;margin-bottom:0.6rem;"><em>{html.escape(p['journal'])}</em> <strong>{p['volume']}</strong>, {p['firstpage']} ({p['pub_year']})</p>
                  <p>{science_text(p['tagline_card'])}</p>
                </div>
              </a>
            </div>"""))
    return "\n".join(cards)


def render_hub():
    latest = max(PAPERS, key=lambda p: p["pub_date_iso"])
    hub_collection = []
    for p in PAPERS:
        hub_collection.append(
            '{{"@type": "ScholarlyArticle", "name": "{title}", '
            '"url": "{url}", "sameAs": "{doi}"}}'.format(
                title=html.escape(p["title"]),
                url=SITE["canonical_url"] + p["slug"] + "/",
                doi=doi_url(p["doi"]),
            )
        )
    combined = "\n\n".join(bibtex(p) for p in PAPERS)
    description = (
        "A six-paper experimental program from the Dickerson Lab on how mammalian "
        "fur and bio-inspired fiber arrays govern raindrop penetration."
    )
    return HUB_TEMPLATE.format(
        body_of_work_title=html.escape(SITE["body_of_work_title"]),
        description=attr(description),
        keywords=attr(SITE["keywords"]),
        lead_authors_plain=attr(SITE["lead_authors_plain"]),
        canonical=SITE["canonical_url"],
        gsc_token=SITE["gsc_token"],
        bing_token=SITE["bing_token"],
        latest_title=html.escape(latest["title"]),
        latest_citation_author_tags=citation_author_tags(latest["authors"]),
        latest_pub_date_slash=latest["pub_date_iso"].replace("-", "/"),
        latest_journal=html.escape(latest["journal"]),
        latest_journal_abbrev=html.escape(latest["journal_abbrev"]),
        latest_publisher=html.escape(latest["publisher"]),
        latest_issn=latest["issn"],
        latest_volume=latest["volume"],
        latest_issue=latest["issue"],
        latest_firstpage=latest["firstpage"],
        latest_doi=latest["doi"],
        latest_doi_url=doi_url(latest["doi"]),
        favicon_emoji=SITE["favicon_emoji"],
        hub_collection_parts=",\n      ".join(hub_collection),
        tagline=science_text(SITE["tagline"]),
        lead_authors_html=SITE["lead_authors_html"],
        affiliations_html=SITE["affiliations_html"],
        contact_line_hub=SITE["contact_line_hub"],
        program_description=html.escape(SITE["program_description"]),
        engagement_buttons="\n".join(engagement_buttons()),
        hub_paper_cards=hub_paper_cards(),
        combined_bibtex=html.escape(combined),
        acknowledgments=html.escape(SITE["acknowledgments_hub"]),
        giscus_html=SITE.get("giscus_html", ""),
        repo_url=SITE["repo_url"],
    )


def render_sitemap():
    urls = [SITE["canonical_url"]] + [
        SITE["canonical_url"] + p["slug"] + "/" for p in PAPERS
    ]
    parts = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        priority = "1.0" if u == SITE["canonical_url"] else "0.9"
        parts.append(
            "  <url>\n"
            f"    <loc>{u}</loc>\n"
            f"    <lastmod>{SITE['lastmod_date']}</lastmod>\n"
            "    <changefreq>monthly</changefreq>\n"
            f"    <priority>{priority}</priority>\n"
            "  </url>"
        )
    parts.append("</urlset>")
    return "\n".join(parts) + "\n"


def render_robots():
    return f"User-agent: *\nAllow: /\n\nSitemap: {SITE['canonical_url']}sitemap.xml\n"


def render_readme():
    paper_rows = "\n".join(
        f"| [{p['title']}]({p['slug']}/) | {p['journal']} {p['volume']}, {p['firstpage']} ({p['pub_year']}) | "
        f"[{p['doi']}]({doi_url(p['doi'])}) |"
        for p in PAPERS
    )
    return textwrap.dedent(f"""\
        # {SITE['body_of_work_title']}

        Source for the project landing page that aggregates six experimental papers
        on drop impact, fiber arrays, and mammalian fur from the Dickerson Lab at
        the University of Tennessee, Knoxville.

        Live at **{SITE['canonical_url']}**.

        ## The six papers

        | Paper | Venue | DOI |
        | ----- | ----- | --- |
        {paper_rows}

        ## Repository layout

        ```
        {SITE['repo_name']}/
        index.html                      hub landing page
        <slug>/index.html               one per paper (6 subpages)
        static/css/index.css            shared styles
        static/js/index.js              shared Cite-dropdown behavior
        static/images/<slug>/           per-paper figures (placeholders for now)
        static/pdfs/<slug>/             supplementary PDFs (3 of 6 papers)
        sitemap.xml                     hub + 6 subpages
        robots.txt                      allows all crawlers
        build.py                        regenerates all pages from PAPERS metadata
        ```

        ## Regenerating the pages

        ```bash
        python3 build.py
        ```

        Edit the `PAPERS` list in `build.py` to update titles, abstracts,
        author lists, firsts, YouTube IDs, dataset DOIs, then re-run.

        ## Preview locally

        ```bash
        python3 -m http.server 8000
        # open http://localhost:8000
        ```

        ## SEO

        - Google Scholar `citation_*` meta tags (per subpage, one author each).
        - Schema.org `ScholarlyArticle` JSON-LD per subpage; `Collection` on the hub.
        - Canonical URLs, keywords, search-engine verification tags.
        - 1200x630 OG image (`static/images/teaser-social.png` to be generated).
        - `sitemap.xml` and `robots.txt` at the repo root.

        ## Credits

        Page template adapted from [Nerfies](https://github.com/nerfies/nerfies.github.io),
        used under [CC BY-SA 4.0](http://creativecommons.org/licenses/by-sa/4.0/).
        """)


# ----------------------------------------------------------------------------
# DRIVER
# ----------------------------------------------------------------------------

def main():
    for p in PAPERS:
        target = ROOT / p["slug"] / "index.html"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(render_subpage(p), encoding="utf-8")
        print(f"wrote {target.relative_to(ROOT)}")
    (ROOT / "index.html").write_text(render_hub(), encoding="utf-8")
    print("wrote index.html")
    (ROOT / "sitemap.xml").write_text(render_sitemap(), encoding="utf-8")
    print("wrote sitemap.xml")
    (ROOT / "robots.txt").write_text(render_robots(), encoding="utf-8")
    print("wrote robots.txt")
    (ROOT / "README.md").write_text(render_readme(), encoding="utf-8")
    print("wrote README.md")


if __name__ == "__main__":
    main()
