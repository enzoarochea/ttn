# Claims to confirm before launch: Teltech Networks, S.A. (v2)

Source: the current site grupottn.com, crawled in full for this redesign.
Items in section A are **not** on the new site. Items in section B **are**
on the site (they come from grupottn.com) and need a final client OK.

## A. Kept off the site until the client confirms

| # | Claim (as found on grupottn.com) | Status on the new site | Question for the client |
|---|---|---|---|
| 1 | **"SOC 24/7"** behind the cybersecurity offer | Not mentioned. "Ciberseguridad y Monitoreo" only describes managed security under an SLA. | Do you operate a SOC? Is it yours or Born Digital's? What hours does it actually cover? |
| 2 | **"Cumplimiento normativo (ISO 27001, NIST, etc.)"** | Not mentioned. | Certified, or only aligned? Certificate scope and expiry? |
| 3 | **"Líderes en soluciones tecnológicas de alto nivel"** | Not used. A leadership claim needs a basis. | Is there a ranking, award or market data behind it? |
| 4 | **"En alianza estratégica con Born Digital"** (cybersecurity) and **"Born Digital IO" footer credit** | Neither is used. BornDigitalIA appears only as a partner name. | Confirm the alliance wording and whether it can be published. |
| 5 | **Partner marketing figures**: "Coro automatiza hasta el 97 %", "100+ clientes B2B en 7 países", Wix figures (6.5M empresas, 99.99 % uptime, SOC 2, PCI DSS...) | Not used. They are the partners' claims, not Teltech's. | None, unless you want partner pages. |
| 6 | **Free offers**: "Análisis de Riesgos de Ciberseguridad Gratis", "Prueba de 30 días" | Not used as offers. "Evaluación de riesgos de ciberseguridad" appears only as a meeting type, with no price. | Are these offers current? Under what conditions? |
| 7 | **"Encriptación de nivel Empresarial o Militar"** | Not used. | Marketing wording; confirm or drop. |
| 8 | **AI demo line "Llama a Brenda" +1 (414) 420-9902** | Not used. It looks like a Born Digital demo number. | Should Teltech publish it? |
| 9 | **Wix listed as a "partner"** | Removed. Wix is the site builder. | Confirm. |
| 10 | **Past events** (Jul 2025 – Jan 2026: LATAM cybersecurity panels, CORO partner sessions, BDIO) | Not listed. Most look like partner-run events. | Which events were organized by Teltech? Should a past-events archive be published? |
| 11 | **Team, intermediate history milestones, certifications, values** | Placeholders marked "Pendiente: contenido del cliente". | Supply verified content. |
| 12 | **Social media** (LinkedIn and Facebook icons on the current site) | Not linked: the URLs could not be verified. | Provide the official profile URLs. |
| 13 | **Pricing, client logos, case studies, any other numbers** | None on the site. | Provide only figures you can substantiate. |

## B. On the new site, taken from grupottn.com: please confirm

- **Founded in 2013**, with head office in Ciudad de Guatemala (the "Compañía" page of the current site). Shown in the hero eyebrow, stats, header and Compañía.
- **Operations in El Salvador, Nicaragua, Costa Rica and Miami.** Shown on the globe, in the location chips and on the Compañía map. The globe and map mark each country at its **capital city** as a representative point; the current site does not say which cities. Confirm or give the real office cities.
- **Opening hours: Monday to Friday, 8:00–17:00.** Shown in the footer, Contacto, Compañía and Reserva. The booking form offers "Mañana (8:00 a 12:00)" and "Tarde (12:00 a 17:00)"; that split is ours.
- **Logo:** the vector logo from the current site is used in the header, footer, intro and favicon. **It reads "TTN".** The original brief said not to use "TTN" on the page. All site text says "Teltech Networks, S.A.", but the mark itself shows TTN. The brand decision is the client's: keep this logo, or supply a "Teltech Networks" version.
- **Manufacturer logos:** Hikvision, Hanwha, Cambium Networks, Mitel, Hewlett Packard Enterprise, Zoom, Optoma, EZVIZ and Ruijie, shown in white in the "Tecnología que integramos" marquee. Confirm that each relationship is current and that you may display their trademarks.
- **Ecosystem partners:** Searchlight Cyber (the brief said "Light Cyber"; the current site says "Search Light Cyber", so we used the official name), Coro, Guardz and BornDigitalIA. Each is shown with a one-word category only (Ciberseguridad or Inteligencia artificial).
- **Meeting types** in Reserva, all 30 minutes, copied from the current booking page: five advisory sessions; discovery meetings for Coro, Guardz, Searchlight Cyber, AI and **Kommo CRM**; and "Convertirte en partner de red". Confirm that Kommo CRM should be listed.
- **Service sub-items** in Soluciones and in the home "Ecosistema" panels come from the current service pages and have been rewritten. "Análisis predictivo en seguridad" now appears only under Ciberseguridad; the current site also puts it under Seguridad and Audio y Video.
- **Which verticals each service serves** (the "Para quién" chips) is our mapping. Please review it.

## C. Decisions needed before launch

- **Form backends:** contact, booking and newsletter forms validate and show success, but send nothing. Each form has `data-endpoint="TODO-…"`, plus a TODO in `js/main.js`.
- **Privacy policy:** the current site has `/privacy-policy`. Migrate it so the consent checkboxes can link to it.
- **Map embed** on Contacto: the placeholder needs a provider choice.
- **Domain and email:** the site uses info@grupottn.com while the brand is Teltech Networks. Confirm the final domain.
