#!/usr/bin/env python3
"""
Nazi Symbolik Detector - Automatische Erkennung von Nazi-Symbolik in Texten und Metadaten
"""

import re
import json
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
import hashlib


@dataclass
class DetectionResult:
    """Ergebnis einer Symbolik-Erkennung"""
    symbol_type: str
    detected_value: str
    context: str
    confidence: float
    position: Optional[Tuple[int, int]] = None
    metadata: Optional[Dict] = None


class NaziSymbolDetector:
    """
    Hauptklasse zur Erkennung von Nazi-Symbolik
    """
    
    def __init__(self):
        # Nazi-Codes Datenbank
        self.number_codes = {
            '18': 'AH (Adolf Hitler)',
            '88': 'HH (Heil Hitler)',
            '14': '14 Words (David Lane)',
            '28': 'BH (Blood & Honour)',
            '44': 'DD (Deutschland)',
            '1488': '14 + 88 kombiniert',
            '1988': 'Jahr mit 88 versteckt',
            '311': 'KKK',
            '5': 'S (Sieg/SS)',
            '7': 'G (Gott/Germanien)',
            '12': 'A (Angriff/Adolf)',
            '13': 'B (Blut/Bund)',
            '23': 'W (Wehrmacht/Weiße)',
        }
        
        # Dog-Whistles Datenbank
        self.dog_whistles = [
            'globalisten',
            'eliten',
            'system',
            'mainstream',
            'lügenpresse',
            'umvolkung',
            'großer austausch',
            'kulturremarxismus',
            'genderismus',
        ]
        
        # Historische Daten
        self.historical_dates = {
            '1919': 'Gründung NSDAP',
            '1923': 'Hitlerputsch',
            '1933': 'Machtergreifung',
            '1938': 'Reichspogromnacht',
            '1945': 'Ende Zweiter Weltkrieg',
        }
        
        # Kompilierte Regex Patterns
        self._compile_patterns()
    
    def _compile_patterns(self):
        """Kompiliere Regex Patterns für Effizienz"""
        # Zahlen-Codes
        self.number_pattern = re.compile(
            r'\b(' + '|'.join(re.escape(code) for code in self.number_codes.keys()) + r')\b'
        )
        
        # Kombinierte Zahlen
        self.combined_pattern = re.compile(
            r'\b(\d{1,3})\s*[/\-]\s*(\d{1,3})\b'
        )
        
        # Dog-Whistles (case-insensitive)
        self.dog_whistle_pattern = re.compile(
            r'\b(' + '|'.join(re.escape(dw) for dw in self.dog_whistles) + r')\b',
            re.IGNORECASE
        )
        
        # Historische Daten
        self.date_pattern = re.compile(
            r'\b(' + '|'.join(re.escape(date) for date in self.historical_dates.keys()) + r')\b'
        )
        
        # URL-Patterns
        self.url_pattern = re.compile(
            r'https?://[^\s<>"]+|www\.[^\s<>"]+'
        )
        
        # Akrostichon-Pattern
        self.acrosticon_pattern = re.compile(
            r'^([A-Z])', re.MULTILINE
        )
    
    def detect_number_codes(self, text: str) -> List[DetectionResult]:
        """
        Erkenne Nazi-Zahlen-Codes im Text
        
        Args:
            text: Zu analysierender Text
            
        Returns:
            Liste der erkannten Codes
        """
        results = []
        
        # Direkte Codes
        for match in self.number_pattern.finditer(text):
            code = match.group()
            results.append(DetectionResult(
                symbol_type='number_code',
                detected_value=code,
                meaning=self.number_codes[code],
                context=self._get_context(text, match.start(), match.end()),
                confidence=0.9,
                position=(match.start(), match.end())
            ))
        
        # Kombinierte Codes
        for match in self.combined_pattern.finditer(text):
            code1, code2 = match.groups()
            combined = f"{code1}/{code2}"
            if code1 in self.number_codes or code2 in self.number_codes:
                results.append(DetectionResult(
                    symbol_type='combined_code',
                    detected_value=combined,
                    meaning=f'Kombination: {code1} + {code2}',
                    context=self._get_context(text, match.start(), match.end()),
                    confidence=0.7,
                    position=(match.start(), match.end())
                ))
        
        return results
    
    def detect_dog_whistles(self, text: str) -> List[DetectionResult]:
        """
        Erkenne Dog-Whistles im Text
        
        Args:
            text: Zu analysierender Text
            
        Returns:
            Liste der erkannten Dog-Whistles
        """
        results = []
        
        for match in self.dog_whistle_pattern.finditer(text):
            whistle = match.group().lower()
            results.append(DetectionResult(
                symbol_type='dog_whistle',
                detected_value=whistle,
                meaning='Dog-Whistle für rechtsextreme Positionen',
                context=self._get_context(text, match.start(), match.end()),
                confidence=0.6,
                position=(match.start(), match.end())
            ))
        
        return results
    
    def detect_historical_dates(self, text: str) -> List[DetectionResult]:
        """
        Erkenne historische Nazi-Daten im Text
        
        Args:
            text: Zu analysierender Text
            
        Returns:
            Liste der erkannten historischen Daten
        """
        results = []
        
        for match in self.date_pattern.finditer(text):
            date = match.group()
            results.append(DetectionResult(
                symbol_type='historical_date',
                detected_value=date,
                meaning=self.historical_dates[date],
                context=self._get_context(text, match.start(), match.end()),
                confidence=0.5,
                position=(match.start(), match.end())
            ))
        
        return results
    
    def detect_urls(self, text: str) -> List[DetectionResult]:
        """
        Erkenne URLs mit potenziellen Nazi-Codes
        
        Args:
            text: Zu analysierender Text
            
        Returns:
            Liste der verdächtigen URLs
        """
        results = []
        
        for match in self.url_pattern.finditer(text):
            url = match.group()
            
            # Überprüfe URL auf Nazi-Codes
            url_codes = self.detect_number_codes(url)
            
            if url_codes:
                results.append(DetectionResult(
                    symbol_type='url_code',
                    detected_value=url,
                    meaning=f'URL enthält Nazi-Codes: {[code.detected_value for code in url_codes]}',
                    context=self._get_context(text, match.start(), match.end()),
                    confidence=0.8,
                    position=(match.start(), match.end())
                ))
        
        return results
    
    def detect_acrosticons(self, text: str) -> List[DetectionResult]:
        """
        Erkenne Akrosticha (versteckte Botschaften in Satzanfängen)
        
        Args:
            text: Zu analysierender Text
            
        Returns:
            Liste der erkannten Akrosticha
        """
        results = []
        
        # Extrahiere erste Buchstaben von Sätzen/Absätzen
        first_letters = []
        for match in self.acrosticon_pattern.finditer(text):
            first_letters.append(match.group(1))
        
        # Suche nach Mustern
        letter_string = ''.join(first_letters)
        
        # Überprüfe auf bekannte Muster
        patterns = ['AH', 'HH', 'SS', 'NS']
        for pattern in patterns:
            if pattern in letter_string:
                results.append(DetectionResult(
                    symbol_type='acrosticon',
                    detected_value=pattern,
                    meaning=f'Akrostichon: {pattern}',
                    context=f'Erste Buchstaben: {letter_string[:50]}...',
                    confidence=0.4,
                    metadata={'full_letters': letter_string}
                ))
        
        return results
    
    def detect_all(self, text: str) -> Dict[str, List[DetectionResult]]:
        """
        Führe alle Erkennungen durch
        
        Args:
            text: Zu analysierender Text
            
        Returns:
            Dictionary mit allen Erkennungsergebnissen
        """
        return {
            'number_codes': self.detect_number_codes(text),
            'dog_whistles': self.detect_dog_whistles(text),
            'historical_dates': self.detect_historical_dates(text),
            'urls': self.detect_urls(text),
            'acrosticons': self.detect_acrosticons(text),
        }
    
    def _get_context(self, text: str, start: int, end: int, context_length: int = 50) -> str:
        """
        Extrahiere Kontext um einen Match
        
        Args:
            text: Originaltext
            start: Startposition des Match
            end: Endposition des Match
            context_length: Länge des Kontexts
            
        Returns:
            Kontext-String
        """
        context_start = max(0, start - context_length)
        context_end = min(len(text), end + context_length)
        return text[context_start:context_end]
    
    def analyze_file(self, file_path: str) -> Dict:
        """
        Analysiere eine Datei
        
        Args:
            file_path: Pfad zur Datei
            
        Returns:
            Analyse-Ergebnisse
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            results = self.detect_all(content)
            
            # Berechne Statistiken
            total_detections = sum(len(detections) for detections in results.values())
            
            return {
                'file_path': file_path,
                'timestamp': datetime.now().isoformat(),
                'total_detections': total_detections,
                'detections': {k: [asdict(r) for r in v] for k, v in results.items()},
                'statistics': self._calculate_statistics(results)
            }
        
        except Exception as e:
            return {
                'file_path': file_path,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def _calculate_statistics(self, results: Dict[str, List[DetectionResult]]) -> Dict:
        """
        Berechne Statistiken über die Erkennungen
        
        Args:
            results: Erkennungsergebnisse
            
        Returns:
            Statistiken
        """
        stats = {}
        
        for category, detections in results.items():
            if detections:
                avg_confidence = sum(d.confidence for d in detections) / len(detections)
                stats[category] = {
                    'count': len(detections),
                    'avg_confidence': avg_confidence,
                    'most_common': self._get_most_common(detections)
                }
        
        return stats
    
    def _get_most_common(self, detections: List[DetectionResult]) -> str:
        """
        Finde den häufigsten erkannten Wert
        
        Args:
            detections: Liste der Erkennungen
            
        Returns:
            Häufigster Wert
        """
        from collections import Counter
        values = [d.detected_value for d in detections]
        return Counter(values).most_common(1)[0][0] if values else None


class MetadataAnalyzer:
    """
    Analysiert Metadaten auf Nazi-Symbolik
    """
    
    def __init__(self):
        self.detector = NaziSymbolDetector()
    
    def analyze_html_metadata(self, html_content: str) -> Dict:
        """
        Analysiere HTML-Metadaten
        
        Args:
            html_content: HTML-Inhalt
            
        Returns:
            Analyse-Ergebnisse
        """
        results = {
            'title': [],
            'meta_description': [],
            'keywords': [],
            'comments': []
        }
        
        # Extrahiere Title
        title_match = re.search(r'<title>(.*?)</title>', html_content, re.IGNORECASE)
        if title_match:
            results['title'] = self.detector.detect_all(title_match.group(1))
        
        # Extrahiere Meta Description
        desc_match = re.search(r'<meta[^>]*name=["\']description["\'][^>]*content=["\'](.*?)["\']', 
                              html_content, re.IGNORECASE)
        if desc_match:
            results['meta_description'] = self.detector.detect_all(desc_match.group(1))
        
        # Extrahiere Keywords
        kw_match = re.search(r'<meta[^>]*name=["\']keywords["\'][^>]*content=["\'](.*?)["\']',
                            html_content, re.IGNORECASE)
        if kw_match:
            results['keywords'] = self.detector.detect_all(kw_match.group(1))
        
        # Extrahiere HTML-Kommentare
        comments = re.findall(r'<!--(.*?)-->', html_content, re.DOTALL)
        for comment in comments:
            results['comments'].append(self.detector.detect_all(comment.strip()))
        
        return results
    
    def analyze_url(self, url: str) -> Dict:
        """
        Analysiere eine URL auf Nazi-Codes
        
        Args:
            url: Zu analysierende URL
            
        Returns:
            Analyse-Ergebnisse
        """
        results = self.detector.detect_urls(url)
        
        # Extrahiere Pfad-Parameter
        from urllib.parse import urlparse, parse_qs
        parsed = urlparse(url)
        
        path_analysis = self.detector.detect_all(parsed.path)
        param_analysis = {}
        
        for key, value in parse_qs(parsed.query).items():
            param_analysis[key] = self.detector.detect_all(value[0])
        
        return {
            'url': url,
            'path_analysis': [asdict(r) for r in path_analysis],
            'parameter_analysis': {k: [asdict(r) for r in v] for k, v in param_analysis.items()},
            'direct_detection': [asdict(r) for r in results]
        }


class ReportGenerator:
    """
    Generiert Berichte aus Analyse-Ergebnissen
    """
    
    @staticmethod
    def generate_json(results: Dict, output_path: str):
        """
        Generiere JSON-Bericht
        
        Args:
            results: Analyse-Ergebnisse
            output_path: Ausgabepfad
        """
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
    
    @staticmethod
    def generate_text_report(results: Dict) -> str:
        """
        Generiere Text-Bericht
        
        Args:
            results: Analyse-Ergebnisse
            
        Returns:
            Text-Bericht
        """
        report = []
        report.append("=" * 60)
        report.append("Nazi Symbolik Detektion Bericht")
        report.append("=" * 60)
        report.append(f"Zeitstempel: {results.get('timestamp', 'N/A')}")
        report.append(f"Datei: {results.get('file_path', 'N/A')}")
        report.append(f"Gesamtdetektionen: {results.get('total_detections', 0)}")
        report.append("")
        
        if 'detections' in results:
            for category, detections in results['detections'].items():
                if detections:
                    report.append(f"{category.upper()}:")
                    report.append("-" * 40)
                    for detection in detections:
                        report.append(f"  - Wert: {detection['detected_value']}")
                        report.append(f"    Bedeutung: {detection['meaning']}")
                        report.append(f"    Konfidenz: {detection['confidence']:.2f}")
                        report.append(f"    Kontext: {detection['context'][:50]}...")
                        report.append("")
        
        if 'statistics' in results:
            report.append("STATISTIKEN:")
            report.append("-" * 40)
            for category, stats in results['statistics'].items():
                report.append(f"{category}:")
                report.append(f"  Anzahl: {stats['count']}")
                report.append(f"  Durchschnittliche Konfidenz: {stats['avg_confidence']:.2f}")
                if stats['most_common']:
                    report.append(f"  Häufigster: {stats['most_common']}")
                report.append("")
        
        return "\n".join(report)


def main():
    """
    Hauptfunktion für CLI-Nutzung
    """
    import argparse
    
    parser = argparse.ArgumentParser(description='Nazi Symbolik Detector')
    parser.add_argument('file', help='Zu analysierende Datei')
    parser.add_argument('--output', '-o', help='Ausgabedatei für JSON-Bericht')
    parser.add_argument('--text', '-t', action='store_true', help='Text-Bericht ausgeben')
    
    args = parser.parse_args()
    
    detector = NaziSymbolDetector()
    results = detector.analyze_file(args.file)
    
    if args.output:
        ReportGenerator.generate_json(results, args.output)
        print(f"Bericht gespeichert: {args.output}")
    
    if args.text or not args.output:
        print(ReportGenerator.generate_text_report(results))


if __name__ == '__main__':
    main()
