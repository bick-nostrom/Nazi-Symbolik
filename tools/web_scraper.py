#!/usr/bin/env python3
"""
Web Scraper für systematische Analyse von Medieninhalten auf Nazi-Symbolik
"""

import asyncio
import aiohttp
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
import json
import re
from urllib.parse import urljoin, urlparse
import time
from nazi_symbol_detector import NaziSymbolDetector, MetadataAnalyzer


@dataclass
class ScrapedArticle:
    """Datenstruktur für gescrapte Artikel"""
    url: str
    title: str
    content: str
    metadata: Dict
    analysis: Dict
    timestamp: str
    word_count: int


class WebScraper:
    """
    Web Scraper für systematische Medienanalyse
    """
    
    def __init__(self, delay: float = 1.0):
        """
        Initialisiere Scraper
        
        Args:
            delay: Verzögerung zwischen Requests (Sekunden)
        """
        self.delay = delay
        self.detector = NaziSymbolDetector()
        self.metadata_analyzer = MetadataAnalyzer()
        self.session = None
        
        # User-Agent für Requests
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    async def __aenter__(self):
        """Async Context Manager Entry"""
        self.session = aiohttp.ClientSession(headers=self.headers)
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async Context Manager Exit"""
        if self.session:
            await self.session.close()
    
    async def scrape_article(self, url: str) -> Optional[ScrapedArticle]:
        """
        Scrape einen einzelnen Artikel
        
        Args:
            url: URL des Artikels
            
        Returns:
            ScrapedArticle oder None bei Fehler
        """
        try:
            # Rate Limiting
            await asyncio.sleep(self.delay)
            
            async with self.session.get(url) as response:
                if response.status != 200:
                    print(f"Error: Status {response.status} for {url}")
                    return None
                
                html = await response.text()
            
            # Parse HTML
            soup = BeautifulSoup(html, 'html.parser')
            
            # Extrahiere Titel
            title = self._extract_title(soup)
            
            # Extrahiere Content
            content = self._extract_content(soup)
            
            # Extrahiere Metadaten
            metadata = self._extract_metadata(soup, url)
            
            # Analysiere Content
            content_analysis = self.detector.detect_all(content)
            
            # Analysiere Metadaten
            metadata_analysis = self.metadata_analyzer.analyze_html_metadata(html)
            
            # Wortzahl
            word_count = len(content.split())
            
            return ScrapedArticle(
                url=url,
                title=title,
                content=content,
                metadata=metadata,
                analysis={
                    'content': {k: [asdict(r) for r in v] for k, v in content_analysis.items()},
                    'metadata': metadata_analysis
                },
                timestamp=datetime.now().isoformat(),
                word_count=word_count
            )
        
        except Exception as e:
            print(f"Error scraping {url}: {str(e)}")
            return None
    
    def _extract_title(self, soup: BeautifulSoup) -> str:
        """Extrahiere Titel aus HTML"""
        # Verschiedene Methoden für Titel
        title = soup.find('h1')
        if title:
            return title.get_text(strip=True)
        
        title = soup.find('title')
        if title:
            return title.get_text(strip=True)
        
        return "No Title Found"
    
    def _extract_content(self, soup: BeautifulSoup) -> str:
        """Extrahiere Hauptinhalt aus HTML"""
        # Entferne nicht-relevante Elemente
        for element in soup(['script', 'style', 'nav', 'footer', 'header', 'aside']):
            element.decompose()
        
        # Versuche verschiedene Content-Selektoren
        content_selectors = [
            'article',
            '[role="main"]',
            'main',
            '.content',
            '.article-content',
            '.post-content',
            '#content',
        ]
        
        for selector in content_selectors:
            content = soup.select_one(selector)
            if content:
                return content.get_text(separator=' ', strip=True)
        
        # Fallback: Body
        return soup.body.get_text(separator=' ', strip=True) if soup.body else ""
    
    def _extract_metadata(self, soup: BeautifulSoup, url: str) -> Dict:
        """Extrahiere Metadaten"""
        metadata = {
            'url': url,
            'domain': urlparse(url).netloc,
        }
        
        # Meta Tags
        for meta in soup.find_all('meta'):
            name = meta.get('name') or meta.get('property')
            content = meta.get('content')
            if name and content:
                metadata[name] = content
        
        # Datum
        date_selectors = [
            'time[datetime]',
            '[datetime]',
            '.date',
            '.published',
            '.timestamp'
        ]
        
        for selector in date_selectors:
            date_elem = soup.select_one(selector)
            if date_elem:
                metadata['publish_date'] = date_elem.get('datetime') or date_elem.get_text(strip=True)
                break
        
        # Autor
        author_selectors = [
            '[rel="author"]',
            '.author',
            '.byline',
            '.writer'
        ]
        
        for selector in author_selectors:
            author_elem = soup.select_one(selector)
            if author_elem:
                metadata['author'] = author_elem.get_text(strip=True)
                break
        
        return metadata
    
    async def scrape_multiple(self, urls: List[str]) -> List[ScrapedArticle]:
        """
        Scrape mehrere Artikel parallel
        
        Args:
            urls: Liste der URLs
            
        Returns:
            Liste der gescrapten Artikel
        """
        tasks = [self.scrape_article(url) for url in urls]
        results = await asyncio.gather(*tasks)
        return [r for r in results if r is not None]
    
    def generate_report(self, articles: List[ScrapedArticle]) -> Dict:
        """
        Generiere aggregierten Bericht über mehrere Artikel
        
        Args:
            articles: Liste der gescrapten Artikel
            
        Returns:
            Aggregierter Bericht
        """
        total_articles = len(articles)
        total_detections = 0
        detection_stats = {}
        domain_stats = {}
        
        for article in articles:
            # Content-Detektionen
            for category, detections in article.analysis['content'].items():
                if detections:
                    total_detections += len(detections)
                    if category not in detection_stats:
                        detection_stats[category] = 0
                    detection_stats[category] += len(detections)
            
            # Domain-Statistiken
            domain = article.metadata['domain']
            if domain not in domain_stats:
                domain_stats[domain] = {
                    'count': 0,
                    'detections': 0
                }
            domain_stats[domain]['count'] += 1
            domain_stats[domain]['detections'] += sum(
                len(d) for d in article.analysis['content'].values()
            )
        
        return {
            'timestamp': datetime.now().isoformat(),
            'total_articles': total_articles,
            'total_detections': total_detections,
            'detection_rate': total_detections / total_articles if total_articles > 0 else 0,
            'detection_stats': detection_stats,
            'domain_stats': domain_stats,
            'articles': [asdict(article) for article in articles]
        }


class SitemapScraper(WebScraper):
    """
    Scraper für Sitemaps (automatische Entdeckung von URLs)
    """
    
    async def scrape_sitemap(self, sitemap_url: str) -> List[str]:
        """
        Scrape eine Sitemap und extrahiere URLs
        
        Args:
            sitemap_url: URL der Sitemap
            
        Returns:
            Liste der URLs
        """
        try:
            await asyncio.sleep(self.delay)
            
            async with self.session.get(sitemap_url) as response:
                if response.status != 200:
                    print(f"Error: Status {response.status} for sitemap {sitemap_url}")
                    return []
                
                xml = await response.text()
            
            # Parse XML
            soup = BeautifulSoup(xml, 'xml')
            
            # Extrahiere URLs
            urls = []
            for loc in soup.find_all('loc'):
                url = loc.get_text(strip=True)
                urls.append(url)
            
            return urls
        
        except Exception as e:
            print(f"Error scraping sitemap {sitemap_url}: {str(e)}")
            return []
    
    async def discover_and_scrape(self, base_url: str, max_articles: int = 100) -> List[ScrapedArticle]:
        """
        Entdecke automatisch URLs über Sitemaps und scrape sie
        
        Args:
            base_url: Basis-URL der Webseite
            max_articles: Maximale Anzahl zu scrapender Artikel
            
        Returns:
            Liste der gescrapten Artikel
        """
        # Versuche Sitemap zu finden
        sitemap_urls = [
            f"{base_url}/sitemap.xml",
            f"{base_url}/sitemap_index.xml",
            f"{base_url}/robots.txt"
        ]
        
        all_urls = []
        
        for sitemap_url in sitemap_urls:
            if sitemap_url.endswith('.txt'):
                # robots.txt
                urls = await self._scrape_robots_txt(sitemap_url)
            else:
                # XML Sitemap
                urls = await self.scrape_sitemap(sitemap_url)
            
            if urls:
                all_urls.extend(urls)
                break
        
        if not all_urls:
            print("Keine Sitemap gefunden, keine URLs")
            return []
        
        # Limitiere Anzahl
        all_urls = all_urls[:max_articles]
        
        print(f"Scraping {len(all_urls)} URLs...")
        return await self.scrape_multiple(all_urls)
    
    async def _scrape_robots_txt(self, robots_url: str) -> List[str]:
        """Scrape robots.txt für Sitemap-URLs"""
        try:
            await asyncio.sleep(self.delay)
            
            async with self.session.get(robots_url) as response:
                if response.status != 200:
                    return []
                
                content = await response.text()
            
            # Extrahiere Sitemap-URLs
            urls = []
            for line in content.split('\n'):
                line = line.strip()
                if line.lower().startswith('sitemap:'):
                    url = line.split(':', 1)[1].strip()
                    urls.append(url)
            
            # Wenn Sitemaps gefunden, scrappe diese
            all_urls = []
            for sitemap_url in urls:
                sitemap_urls = await self.scrape_sitemap(sitemap_url)
                all_urls.extend(sitemap_urls)
            
            return all_urls
        
        except Exception as e:
            print(f"Error scraping robots.txt: {str(e)}")
            return []


async def main():
    """
    Hauptfunktion für CLI-Nutzung
    """
    import argparse
    
    parser = argparse.ArgumentParser(description='Web Scraper für Nazi-Symbolik-Erkennung')
    parser.add_argument('url', help='URL oder Sitemap')
    parser.add_argument('--output', '-o', help='Ausgabedatei für JSON-Bericht')
    parser.add_argument('--max', '-m', type=int, default=100, help='Maximale Anzahl Artikel')
    parser.add_argument('--sitemap', '-s', action='store_true', help='Als Sitemap behandeln')
    
    args = parser.parse_args()
    
    async with SitemapScraper() as scraper:
        if args.sitemap or 'sitemap' in args.url:
            articles = await scraper.discover_and_scrape(args.url, args.max)
        else:
            article = await scraper.scrape_article(args.url)
            articles = [article] if article else []
        
        if articles:
            report = scraper.generate_report(articles)
            
            if args.output:
                with open(args.output, 'w', encoding='utf-8') as f:
                    json.dump(report, f, indent=2, ensure_ascii=False)
                print(f"Bericht gespeichert: {args.output}")
            else:
                print(json.dumps(report, indent=2, ensure_ascii=False))
        else:
            print("Keine Artikel gefunden")


if __name__ == '__main__':
    asyncio.run(main())
