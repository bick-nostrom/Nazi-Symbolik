# Beispiel-Analysen: Praktische Anwendung der Tools

## Beispiel 1: Text-Analyse

### Eingabe
```text
18 Gründe warum wir unsere Ozeane retten müssen. 88 Prozent der Meereslebewesen sind bedroht. Wir haben 14 Tage Zeit zu handeln.
```

### Python-Code
```python
from nazi_symbol_detector import NaziSymbolDetector

detector = NaziSymbolDetector()
text = "18 Gründe warum wir unsere Ozeane retten müssen. 88 Prozent der Meereslebewesen sind bedroht. Wir haben 14 Tage Zeit zu handeln."
results = detector.detect_all(text)

for category, detections in results.items():
    print(f"{category}: {len(detections)}")
    for detection in detections:
        print(f"  - {detection.detected_value}: {detection.meaning} (Konfidenz: {detection.confidence})")
```

### Ausgabe
```
number_codes: 3
  - 18: AH (Adolf Hitler) (Konfidenz: 0.9)
  - 88: HH (Heil Hitler) (Konfidenz: 0.9)
  - 14: 14 Words (David Lane) (Konfidenz: 0.9)
```

### Interpretation
Der Text enthält drei Nazi-Codes in einem scheinbar harmlosen Kontext (Umweltschutz). Dies ist ein typisches Beispiel für sublimative Symbolik in positivem Kontext zur Desensibilisierung.

## Beispiel 2: URL-Analyse

### Eingabe
```python
import asyncio
from tools.integrated_analysis_system import IntegratedAnalysisSystem

async def analyze():
    system = IntegratedAnalysisSystem()
    result = await system.analyze_url("https://example.com/artikel")
    print(result)

asyncio.run(analyze())
```

### Erwartete Ausgabe
```json
{
  "source": "https://example.com/artikel",
  "type": "url_analysis",
  "timestamp": "2026-04-13T12:00:00",
  "title": "Beispiel-Artikel",
  "word_count": 500,
  "content_analysis": {
    "number_codes": [...],
    "dog_whistles": [...]
  },
  "statistics": {
    "total_detections": 5
  }
}
```

## Beispiel 3: Batch-Analyse mehrerer URLs

### Eingabe
```python
urls = [
    "https://example.com/artikel1",
    "https://example.com/artikel2",
    "https://example.com/artikel3"
]

result = await system.analyze_urls_batch(urls)
print(result)
```

### Erwartete Ausgabe
```json
{
  "type": "batch_url_analysis",
  "total_urls": 3,
  "successful": 3,
  "failed": 0,
  "aggregated_stats": {
    "total_detections": 12,
    "category_stats": {
      "number_codes": {"count": 8},
      "dog_whistles": {"count": 4}
    }
  }
}
```

## Beispiel 4: Verzeichnis-Analyse

### Eingabe
```python
result = system.analyze_directory("c:/Users/Fabi/Documents/Articles")
print(result)
```

### Erwartete Ausgabe
```json
{
  "type": "directory_analysis",
  "directory": "c:/Users/Fabi/Documents/Articles",
  "total_files": 50,
  "analyzed_files": 48,
  "aggregated_stats": {
    "total_detections": 25
  }
}
```

## Beispiel 5: HTML-Metadaten-Analyse

### Eingabe
```python
from nazi_symbol_detector import MetadataAnalyzer

analyzer = MetadataAnalyzer()
html = """
<html>
<head>
    <title>18 Wege zum Erfolg</title>
    <meta name="description" content="88 Tipps für bessere Ergebnisse">
    <meta name="keywords" content="18, 88, erfolg">
</head>
<body>
    <!-- 14 days to success -->
    <h1>Inhalt</h1>
</body>
</html>
"""

results = analyzer.analyze_html_metadata(html)
print(results)
```

### Erwartete Ausgabe
```json
{
  "title": [...],
  "meta_description": [...],
  "keywords": [...],
  "comments": [...]
}
```

## Beispiel 6: Umfassender Bericht

### Eingabe
```python
# Führe mehrere Analysen durch
system.analyze_text("18 Gründe...", "source1")
await system.analyze_url("https://example.com", "source2")
system.analyze_file("artikel.txt")

# Generiere umfassenden Bericht
report = system.generate_comprehensive_report("bericht.json")
print(report)
```

### Erwartete Ausgabe
```json
{
  "timestamp": "2026-04-13T12:00:00",
  "total_analyses": 3,
  "summary": {
    "total_sources": 3,
    "total_detections": 15,
    "avg_detections_per_source": 5
  },
  "recommendations": [
    "Hohe Detektionsrate - tiefergehende Untersuchung empfohlen"
  ]
}
```

## Beispiel 7: Manuelles Validieren von Falsch-Positiven

### Szenario
Ein Artikel enthält die Zahl "18" in einem harmlosen Kontext.

### Analyse
```python
text = "Der Artikel hat 18 Absätze und ist sehr gut strukturiert."
results = detector.detect_number_codes(text)

# Manuelles Validieren
for detection in results:
    context = detection.context
    # Prüfe Kontext: Ist es wirklich Nazi-Symbolik?
    if "Absätze" in context or "Seiten" in context:
        print(f"Falsch-Positiv: {detection.detected_value} in harmlosem Kontext")
```

## Beispiel 8: Trend-Analyse über Zeit

### Eingabe
```python
from datetime import datetime, timedelta

# Analysiere Artikel über Zeit
dates = []
detection_rates = []

for i in range(12):  # 12 Monate
    date = datetime.now() - timedelta(days=30*i)
    # Analysiere Artikel von diesem Monat
    # (Pseudo-Code - echte Implementierung erfordert Datenbank)
    rate = analyze_month(date)
    dates.append(date)
    detection_rates.append(rate)

# Plotte Trend
import matplotlib.pyplot as plt
plt.plot(dates, detection_rates)
plt.xlabel('Datum')
plt.ylabel('Detektionsrate')
plt.title('Nazi-Symbolik über Zeit')
plt.show()
```

## Beispiel 9: Netzwerk-Analyse

### Eingabe
```python
import networkx as nx

# Erstelle Netzwerk von Influencern
G = nx.Graph()

# Füge Knoten hinzu (Influencer)
influencers = ["InfluencerA", "InfluencerB", "InfluencerC"]
G.add_nodes_from(influencers)

# Füge Kanten hinzu (Verbindungen)
G.add_edge("InfluencerA", "InfluencerB", weight=0.8)
G.add_edge("InfluencerB", "InfluencerC", weight=0.6)

# Analysiere Cluster
communities = nx.community.greedy_modularity_communities(G)
print(f"Communities: {communities}")

# Analysiere Zentralität
centrality = nx.degree_centrality(G)
print(f"Centrality: {centrality}")
```

## Beispiel 10: Sentiment-Analyse mit Nazi-Symbolik

### Eingabe
```python
from textblob import TextBlob

text = "18 Gründe warum das System versagt"
blob = TextBlob(text)
sentiment = blob.sentiment

# Analysiere Nazi-Symbolik
nazi_results = detector.detect_all(text)

# Kombiniere Ergebnisse
result = {
    'sentiment': sentiment.polarity,
    'nazi_codes': len(nazi_results['number_codes']),
    'interpretation': 'Negatives Sentiment mit Nazi-Codes'
}
```

## Best Practices

### 1. Immer Kontext prüfen
- Zahlen können harmlos sein (z.B. "18 Jahre alt")
- Visuelle Symbolik kann zufällig sein
- Manuelle Validierung ist wichtig

### 2. Konfidenz beachten
- Hohe Konfidenz (>0.8): Wahrscheinlich echt
- Mittlere Konfidenz (0.5-0.8): Validierung erforderlich
- Niedrige Konfidenz (<0.5): Wahrscheinlich Falsch-Positiv

### 3. Muster über Zeit
- Einmaliger Fund: Zufällig
- Wiederholte Funde: Systematisch
- Steigende Häufigkeit: Trend

### 4. Quellen kritisch prüfen
- Wer ist der Autor?
- Was ist die politische Ausrichtung?
- Gibt es Verbindungen zu rechtsextremen Gruppen?

### 5. Dokumentation
- Immer Quellen angeben
- Screenshots archivieren
- Kontext dokumentieren
- Datum und Uhrzeit notieren

## Troubleshooting

### Problem: Keine Ergebnisse
**Lösung:** Filter lockern, Keywords erweitern, Kontext prüfen

### Problem: Zu viele Falsch-Positive
**Lösung:** Konfidenz-Schwelle erhöhen, manuelle Validierung verbessern

### Problem: Web-Scraping fehlschlägt
**Lösung:** Rate Limiting prüfen, User-Agent ändern, Proxies verwenden

### Problem: Speicherprobleme bei großen Datenmengen
**Lösung:** Batch-Verarbeitung, Datenbank verwenden, Streaming

---

*Diese Beispiele dienen als Startpunkt für praktische Anwendungen. Anpassung an spezifische Anforderungen erforderlich.*
