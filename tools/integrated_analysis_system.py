#!/usr/bin/env python3
"""
Integriertes Analyse-System für Nazi-Symbolik-Forschung
Kombiniert alle Tools in einem einheitlichen System
"""

import asyncio
import json
from typing import Dict, List, Optional
from datetime import datetime
from pathlib import Path
import sys

# Importiere unsere Module
from nazi_symbol_detector import NaziSymbolDetector, MetadataAnalyzer, ReportGenerator
from web_scraper import WebScraper, ScrapedArticle


class IntegratedAnalysisSystem:
    """
    Integriertes System für komplette Analyse-Workflows
    """
    
    def __init__(self):
        self.detector = NaziSymbolDetector()
        self.metadata_analyzer = MetadataAnalyzer()
        self.results = []
    
    def analyze_text(self, text: str, source: str = "unknown") -> Dict:
        """
        Analysiere Text auf Nazi-Symbolik
        
        Args:
            text: Zu analysierender Text
            source: Quelle des Textes
            
        Returns:
            Analyse-Ergebnis
        """
        print(f"Analysiere Text aus: {source}")
        
        results = self.detector.detect_all(text)
        
        return {
            'source': source,
            'type': 'text_analysis',
            'timestamp': datetime.now().isoformat(),
            'results': {k: [r.__dict__ for r in v] for k, v in results.items()},
            'statistics': self._calculate_stats(results)
        }
    
    def analyze_file(self, file_path: str) -> Dict:
        """
        Analysiere Datei auf Nazi-Symbolik
        
        Args:
            file_path: Pfad zur Datei
            
        Returns:
            Analyse-Ergebnis
        """
        print(f"Analysiere Datei: {file_path}")
        
        result = self.detector.analyze_file(file_path)
        self.results.append(result)
        
        return result
    
    async def analyze_url(self, url: str) -> Dict:
        """
        Analysiere URL auf Nazi-Symbolik
        
        Args:
            url: Zu analysierende URL
            
        Returns:
            Analyse-Ergebnis
        """
        print(f"Analysiere URL: {url}")
        
        async with WebScraper() as scraper:
            article = await scraper.scrape_article(url)
            
            if article:
                # Analysiere Content
                content_analysis = self.detector.detect_all(article.content)
                
                # Analysiere Metadaten
                metadata_analysis = self.metadata_analyzer.analyze_html_metadata(
                    f"<title>{article.title}</title>"
                )
                
                result = {
                    'source': url,
                    'type': 'url_analysis',
                    'timestamp': datetime.now().isoformat(),
                    'title': article.title,
                    'word_count': article.word_count,
                    'content_analysis': {k: [r.__dict__ for r in v] for k, v in content_analysis.items()},
                    'metadata_analysis': metadata_analysis,
                    'statistics': self._calculate_stats(content_analysis)
                }
                
                self.results.append(result)
                return result
            else:
                return {
                    'source': url,
                    'type': 'url_analysis',
                    'error': 'Failed to scrape URL',
                    'timestamp': datetime.now().isoformat()
                }
    
    async def analyze_urls_batch(self, urls: List[str]) -> Dict:
        """
        Analysiere mehrere URLs parallel
        
        Args:
            urls: Liste der URLs
            
        Returns:
            Aggregiertes Analyse-Ergebnis
        """
        print(f"Analysiere {len(urls)} URLs im Batch...")
        
        tasks = [self.analyze_url(url) for url in urls]
        results = await asyncio.gather(*tasks)
        
        successful = [r for r in results if 'error' not in r]
        
        return {
            'type': 'batch_url_analysis',
            'timestamp': datetime.now().isoformat(),
            'total_urls': len(urls),
            'successful': len(successful),
            'failed': len(urls) - len(successful),
            'results': successful,
            'aggregated_stats': self._aggregate_stats(successful)
        }
    
    def analyze_directory(self, directory: str) -> Dict:
        """
        Analysiere alle Dateien in einem Verzeichnis
        
        Args:
            directory: Verzeichnispfad
            
        Returns:
            Aggregiertes Analyse-Ergebnis
        """
        print(f"Analysiere Verzeichnis: {directory}")
        
        path = Path(directory)
        files = list(path.glob('*.txt')) + list(path.glob('*.md')) + list(path.glob('*.html'))
        
        results = []
        for file_path in files:
            try:
                result = self.analyze_file(str(file_path))
                results.append(result)
            except Exception as e:
                print(f"Fehler bei {file_path}: {e}")
        
        return {
            'type': 'directory_analysis',
            'timestamp': datetime.now().isoformat(),
            'directory': directory,
            'total_files': len(files),
            'analyzed_files': len(results),
            'results': results,
            'aggregated_stats': self._aggregate_stats(results)
        }
    
    def generate_comprehensive_report(self, output_path: Optional[str] = None) -> Dict:
        """
        Generiere umfassenden Bericht aller Analysen
        
        Args:
            output_path: Optionaler Ausgabepfad für JSON
            
        Returns:
            Umfassender Bericht
        """
        print("Generiere umfassenden Bericht...")
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'total_analyses': len(self.results),
            'results': self.results,
            'summary': self._generate_summary(),
            'recommendations': self._generate_recommendations()
        }
        
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            print(f"Bericht gespeichert: {output_path}")
        
        return report
    
    def _calculate_stats(self, results: Dict) -> Dict:
        """Berechne Statistiken für eine Analyse"""
        stats = {}
        total_detections = 0
        
        for category, detections in results.items():
            if detections:
                count = len(detections)
                total_detections += count
                avg_confidence = sum(d.confidence for d in detections) / count
                stats[category] = {
                    'count': count,
                    'avg_confidence': avg_confidence
                }
        
        stats['total_detections'] = total_detections
        return stats
    
    def _aggregate_stats(self, results: List[Dict]) -> Dict:
        """Aggregiere Statistiken über mehrere Analysen"""
        aggregated = {
            'total_sources': len(results),
            'total_detections': 0,
            'category_stats': {}
        }
        
        for result in results:
            if 'statistics' in result:
                aggregated['total_detections'] += result['statistics'].get('total_detections', 0)
                
                for category, stats in result['statistics'].items():
                    if category != 'total_detections':
                        if category not in aggregated['category_stats']:
                            aggregated['category_stats'][category] = {
                                'count': 0,
                                'avg_confidence': 0
                            }
                        aggregated['category_stats'][category]['count'] += stats.get('count', 0)
        
        return aggregated
    
    def _generate_summary(self) -> Dict:
        """Generiere Zusammenfassung aller Ergebnisse"""
        if not self.results:
            return {'message': 'Keine Ergebnisse vorhanden'}
        
        total_sources = len(self.results)
        total_detections = sum(
            r.get('statistics', {}).get('total_detections', 0) 
            for r in self.results
        )
        
        return {
            'total_sources': total_sources,
            'total_detections': total_detections,
            'avg_detections_per_source': total_detections / total_sources if total_sources > 0 else 0
        }
    
    def _generate_recommendations(self) -> List[str]:
        """Generiere Empfehlungen basierend auf Ergebnissen"""
        recommendations = []
        
        if not self.results:
            return ['Keine Empfehlungen - keine Ergebnisse vorhanden']
        
        summary = self._generate_summary()
        
        if summary['avg_detections_per_source'] > 5:
            recommendations.append('Hohe Detektionsrate - tiefergehende Untersuchung empfohlen')
        
        if summary['avg_detections_per_source'] > 10:
            recommendations.append('Sehr hohe Detektionsrate - sofortige Maßnahme empfohlen')
        
        if summary['avg_detections_per_source'] < 1:
            recommendations.append('Niedrige Detektionsrate - keine akute Handlung erforderlich')
        
        return recommendations


async def main():
    """
    Hauptfunktion für CLI-Nutzung
    """
    import argparse
    
    parser = argparse.ArgumentParser(description='Integriertes Nazi-Symbolik Analyse-System')
    parser.add_argument('--text', '-t', help='Text analysieren')
    parser.add_argument('--file', '-f', help='Datei analysieren')
    parser.add_argument('--url', '-u', help='URL analysieren')
    parser.add_argument('--directory', '-d', help='Verzeichnis analysieren')
    parser.add_argument('--urls', '-U', nargs='+', help='Mehrere URLs analysieren')
    parser.add_argument('--output', '-o', help='Ausgabedatei für Bericht')
    parser.add_argument('--report', '-r', action='store_true', help='Umfassenden Bericht generieren')
    
    args = parser.parse_args()
    
    system = IntegratedAnalysisSystem()
    
    if args.text:
        result = system.analyze_text(args.text, "command_line")
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif args.file:
        result = system.analyze_file(args.file)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif args.url:
        result = await system.analyze_url(args.url)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif args.urls:
        result = await system.analyze_urls_batch(args.urls)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif args.directory:
        result = system.analyze_directory(args.directory)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    if args.report or args.output:
        report = system.generate_comprehensive_report(args.output)
        if not args.output:
            print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    asyncio.run(main())
