        # Drop Impact on Bio-inspired Fiber Arrays and Mammalian Fur

        Source for the project landing page that aggregates six experimental papers
        on drop impact, fiber arrays, and mammalian fur from the Dickerson Lab at
        the University of Tennessee, Knoxville.

        Live at **https://genepatrickrible.github.io/fur-wetting/**.

        ## The six papers

        | Paper | Venue | DOI |
        | ----- | ----- | --- |
        | [Dynamic Drop Penetration of Horizontally Oriented Fiber Arrays](horizontal-fibers/) | Langmuir 40, 13339 (2024) | [10.1021/acs.langmuir.4c00371](https://doi.org/10.1021/acs.langmuir.4c00371) |
| [Dynamic drop penetration of vertically oriented fiber arrays](vertical-fibers/) | Physics of Fluids 37, 022108 (2025) | [10.1063/5.0246986](https://doi.org/10.1063/5.0246986) |
| [Sequential drop impacts onto horizontal fiber arrays](sequential-impacts/) | Physics of Fluids 37, 072128 (2025) | [10.1063/5.0281512](https://doi.org/10.1063/5.0281512) |
| [Vertically oriented fiber arrays suppress splashing by restricting spreading of impacting drops](splash-suppression/) | Physics of Fluids 37, 092106 (2025) | [10.1063/5.0286271](https://doi.org/10.1063/5.0286271) |
| [Cross-sectional circularity promotes dynamic drop penetration of horizontal fiber arrays](cross-section-circularity/) | Physics of Fluids 37, 122110 (2025) | [10.1063/5.0287633](https://doi.org/10.1063/5.0287633) |
| [Fur roughness, density, and length reduce raindrop penetration of mammalian pelts](fur-pelts/) | Bioinspiration & Biomimetics 21, 036008 (2026) | [10.1088/1748-3190/ae66c1](https://doi.org/10.1088/1748-3190/ae66c1) |

        ## Repository layout

        ```
        fur-wetting/
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
