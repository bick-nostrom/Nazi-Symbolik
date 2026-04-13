# Tools für Nazi-Symbolik-Forschung

## Überblick

Dieses Verzeichnis enthält praktische Tools für die systematische Analyse von Nazi-Symbolik in Medieninhalten.

## Verfügbare Tools

### 1. Nazi Symbol Detector (`nazi_symbol_detector.py`)

Automatische Erkennung von Nazi-Symbolik in Texten und Metadaten.

**Funktionen:**
- Erkennung von Zahlen-Codes (18, 88, 14, etc.)
- Erkennung von Dog-Whistles
- Erkennung historischer Daten
- URL-Analyse
- Akrostichon-Erkennung
- HTML-Metadaten-Analyse
- JSON- und Text-Bericht-Generierung

**Installation:**
```bash
pip install beautifulsoup4 aiohttp
```

**Nutzung:**
```bash
# Einzelne Datei analysieren
python nazi_symbol_detector.py artikel.txt --text

# JSON-Bericht generieren
python nazi_symbol_detector.py artikel.txt -o bericht.json
```

**Python API:**
```python
from nazi_symbol_detector import NaziSymbolDetector

detector = NaziSymbolDetector()
results = detector.detect_all("18 Gründe für den Erfolg")
print(results)
```

### 2. Web Scraper (`web_scraper.py`)

Systematisches Web-Scraping für Medienanalyse.

**Funktionen:**
- Scraping einzelner Artikel
- Batch-Scraping mehrerer URLs
- Sitemap-basierte URL-Entdeckung
- Automatische Content-Extraktion
- Metadaten-Extraktion
- Integrierte Symbolik-Erkennung
- Aggregierte Berichte

**Installation:**
```bash
pip install beautifulsoup4 aiohttp
```

**Nutzung:**
```bash
# Einzelnen Artikel scrapen
python web_scraper.py https://example.com/artikel

# Sitemap scrapen
python web_scraper.py https://example.com/sitemap.xml --sitemap --max 50

# Bericht speichern
python web_scraper.py https://example.com -o bericht.json
```

**Python API:**
```python
import asyncio
from web_scraper import WebScraper

async def scrape():
    async with WebScraper() as scraper:
        article = await scraper.scrape_article("https://example.com")
        print(article.analysis)

asyncio.run(scrape())
```

## Best Practices

### 1. Ethische Nutzung
- Nur für Forschungszwecke verwenden
- Datenschutzgesetze beachten
- Robots.txt respektieren
- Rate Limiting implementieren

### 2. Datenqualität
- Ergebnisse manuell validieren
- Kontext berücksichtigen
- False Positives ausschließen
- Quellen dokumentieren

### 3. Skalierung
- Batch-Verarbeitung für große Datenmengen
- Asynchrone Verarbeitung nutzen
- Caching implementieren
- Datenbank für persistente Speicherung

### 4. Sicherheit
- Input-Validierung
- SQL-Injection verhindern
- XSS-Schutz
- Secure Coding Practices

## Erweiterungsmöglichkeiten

### 1. Bild-Analyse
```python
# Bild auf visuelle Nazi-Symbolik analysieren
from PIL import Image
import cv2

def analyze_image(image_path):
    # Implementierung der Bildanalyse
    pass
```

### 2. Video-Analyse
```python
# Video-Frames auf Nazi-Symbolik analysieren
def analyze_video(video_path):
    # Implementierung der Videoanalyse
    pass
```

### 3. Audio-Analyse
```python
# Audio auf versteckte Codes analysieren
def analyze_audio(audio_path):
    # Implementierung der Audioanalyse
    pass
```

### 4. Social Media Integration
```python
# Social Media Posts analysieren
def analyze_social_media(platform, query):
    # Implementierung der Social Media Analyse
    pass
```

## Datenbank-Integration

### SQLite Beispiel
```python
import sqlite3

def store_results(results, db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Tabelle erstellen
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS detections (
            id INTEGER PRIMARY KEY,
            url TEXT,
            symbol_type TEXT,
            detected_value TEXT,
            confidence REAL,
            timestamp TEXT
        )
    ''')
    
    # Ergebnisse speichern
    for detection in results:
        cursor.execute('''
            INSERT INTO detections (url, symbol_type, detected_value, confidence, timestamp)
            VALUES (?, ?, ?, ?, ?)
        ''', (detection['url'], detection['symbol_type'], 
              detection['detected_value'], detection['confidence'], 
              detection['timestamp']))
    
    conn.commit()
    conn.close()
```

## Monitoring und Alerting

### E-Mail Alerts
```python
import smtplib
from email.mime.text import MIMEText

def send_alert(results):
    if results['total_detections'] > threshold:
        msg = MIMEText(f"High detection rate: {results['total_detections']}")
        msg['Subject'] = 'Nazi Symbolik Alert'
        msg['From'] = 'monitor@example.com'
        msg['To'] = 'admin@example.com'
        
        with smtplib.SMTP('smtp.example.com') as server:
            server.send_message(msg)
```

## Performance-Optimierung

### 1. Caching
```python
from functools import lru_cache

@lru_cache(maxsize=1000)
def detect_cached(text):
    return detector.detect_all(text)
```

### 2. Parallelisierung
```python
from concurrent.futures import ThreadPoolExecutor

def parallel_scrape(urls):
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(scrape_article, urls))
    return results
```

### 3. Batch-Verarbeitung
```python
def batch_process(files, batch_size=100):
    for i in range(0, len(files), batch_size):
        batch = files[i:i+batch_size]
        process_batch(batch)
```

## Fehlerbehandlung

### Robustes Scraping
```python
async def robust_scrape(url, max_retries=3):
    for attempt in range(max_retries):
        try:
            return await scrape_article(url)
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            await asyncio.sleep(2 ** attempt)  # Exponential backoff
```

## Rechtliche Hinweise

- **Datenschutz:** DSGVO und andere Datenschutzgesetze beachten
- **Urheberrecht:** Nur für Forschungszwecke verwenden
- **Terms of Service:** Nutzungsbedingungen der Websites respektieren
- **Haftung:** Keine Garantie für Korrektheit der Ergebnisse

## Support und Contributing

Für Fragen, Probleme oder Contributions bitte:
- Issues im GitHub-Repository erstellen
- Pull Requests einreichen
- Diskussionen starten

## Lizenz

Diese Tools sind für Forschungszwecke entwickelt. Bitte nutzen Sie sie verantwortungsvoll und ethisch korrekt.
