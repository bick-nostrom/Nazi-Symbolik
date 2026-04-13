# Nazi-Symbolik Forschungsprojekt - Agent Guidelines

## Projektbeschreibung

Dies ist ein Forschungs- und Aufdeckungsprojekt zur Identifikation und Dokumentation von Nazi-Symbolik in Medien-Artikeln, Webseiten und anderen Quellen. Nazi-Symbolik kann auf vielfältige Weise versteckt sein und systematisch aufgedeckt werden.

## Arten von Nazi-Symbolik

### Zahlen-Symbolik
- **18**: AH (Adolf Hitler - 1. Buchstabe=1, 8. Buchstabe=H)
- **88**: HH (Heil Hitler)
- **14**: "14 Words" (David Lane's Slogan)
- **28**: BH (Blood & Honour)
- **44**: DD (Deutschland)
- **1919**: Gründungsjahr der NSDAP
- **1923**: Hitlerputsch
- **1933**: Machtergreifung
- **1938**: Reichspogromnacht
- **1945**: Ende des Zweiten Weltkriegs
- Kombinationen wie 188, 1488, etc.

### Zeichen-Symbolik
- Runen (z.B. Odal-Rune, Sig-Rune, Tyr-Rune)
- Schwarze Sonne
- Hakenkreuz-Variationen
- Wolfsangel
- Triskele
- Keltenkreuz in neonazistischem Kontext
- Zahlen als Codes (oben genannte)

### Versteckte Symbolik
- Geburtsdaten von Nazi-Größen
- Historische Daten in URLs, Timestamps
- Textcodierungen
- Quelltext-Kommentare
- Metadaten
- Bildpixel-Werte
- Hash-Werte

## Methodik

### MCP Tools für Recherchen

**Playwright (io.windsurf/mcp-playwright)**
- Webseiten navigieren und analysieren
- Vollständige Seiteninhalte extrahieren
- Netzwerk-Requests untersuchen
- Screenshots für Dokumentation
- JavaScript für tiefe Analyse

**Cloudflare-Dokumentation (io.windsurf/cloudflare-docs)**
- Bei Bedarf für technische Analysen

**Memory (io.windsurf/memory)**
- Wissensgraph für Mustererkennung
- Beziehungen zwischen Symbolen und Funden

### Arbeitsablauf

1. **Zieldefinition**
   - Welche Quelle wird untersucht?
   - Welche Art von Symbolik wird gesucht?

2. **Datenerhebung**
   - Playwright: Webseite navigieren (`mcp2_browser_navigate`)
   - Snapshot erstellen (`mcp2_browser_snapshot`)
   - Inhalt analysieren (`mcp2_browser_evaluate`)
   - Netzwerk-Requests prüfen (`mcp2_browser_network_requests`)

3. **Analyse**
   - Text auf Zahlen-Muster prüfen
   - URLs auf versteckte Codes untersuchen
   - Metadaten analysieren
   - Quelltext auf versteckte Symbole durchsuchen

4. **Dokumentation**
   - Funde in `findings/` dokumentieren
   - Screenshots speichern
   - Kontext und Beweise anhängen
   - Muster in `patterns/` katalogisieren

5. **Validierung**
   - Funde kritisch prüfen
   - Fehlinterpretationen ausschließen
   - Kontext berücksichtigen

## Verzeichnisstruktur

```
/
├── research/          # Aktive Recherchen
├── findings/          # Dokumentierte Funde
├── patterns/          # Bekannte Muster
├── sources/           # Quellenmaterial
├── analysis/          # Detaillierte Analysen
└── reports/           # Zusammenfassende Berichte
```

## Dokumentationsstandards

### Funde dokumentieren
Jeder Fund muss enthalten:
- **Quelle**: URL, Publikation, Datum
- **Symbol**: Art der Symbolik
- **Kontext**: Wie wurde das Symbol verwendet?
- **Beweise**: Screenshots, Zitate, Daten
- **Analyse**: Warum ist dies Nazi-Symbolik?
- **Unklarheiten**: Was ist noch zu klären?

### Dateinamenskonvention
- `findings/YYYY-MM-DD-quelle-symbol.md`
- `patterns/symbol-kategorie.md`

## Wichtige Hinweise

- **Kontext ist entscheidend**: Nicht jede Zahl 18 oder 88 ist Nazi-Symbolik
- **Falsch-Positive vermeiden**: Zufällige Übereinstimmungen ausschließen
- **Quellenkritik**: Verlässlichkeit der Quellen prüfen
- **Rechtliche Aspekte**: Dokumentation vs. Verbreitung beachten
- **Ethik**: Forschungszwecke vs. Propaganda unterscheiden

## Playwright-Beispiel

```javascript
// Webseite analysieren auf versteckte Zahlen
async (page) => {
  const content = await page.content();
  const numbers = content.match(/\b\d{2,4}\b/g);
  // Analyse der Zahlen auf Nazi-Codes
  return numbers;
}
```

## Muster-Erkennung

Regelmäßige Überprüfung auf:
- Häufige Zahlenkombinationen
- Wiederkehrende Zeichen
- Strukturelle Ähnlichkeiten
- Geografische Häufungen

## Weiterführende Arbeit

- Automatisierte Scans mit Playwright
- Pattern-Matching-Algorithmen
- KI-gestützte Erkennung
- Datenbank für Muster
- Zusammenarbeit mit Forschungseinrichtungen
