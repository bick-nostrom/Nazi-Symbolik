#!/usr/bin/env python3
"""
Erweiterter Nazi-Symbolik Detector mit ML-Unterstützung
"""

import re
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from collections import Counter
import math


@dataclass
class AdvancedDetectionResult:
    """Erweitertes Erkennungsergebnis mit ML-Scores"""
    symbol_type: str
    detected_value: str
    context: str
    confidence: float
    ml_score: float
    pattern_score: float
    combined_score: float
    position: Optional[Tuple[int, int]] = None


class AdvancedNaziSymbolDetector:
    """
    Erweiterter Detector mit Pattern-Recognition und ML-Scoring
    """
    
    def __init__(self):
        # Basierend auf original detector
        self.number_codes = {
            '18': 'AH (Adolf Hitler)',
            '88': 'HH (Heil Hitler)',
            '14': '14 Words (David Lane)',
            '28': 'BH (Blood & Honour)',
            '44': 'DD (Deutschland)',
            '1488': '14 + 88 kombiniert',
        }
        
        # Pattern-Recognition
        self._compile_patterns()
        
        # ML-Training-Daten (simuliert)
        self.pattern_weights = self._init_pattern_weights()
    
    def _compile_patterns(self):
        """Kompiliere erweiterte Patterns"""
        # Kombinierte Patterns
        self.combined_pattern = re.compile(
            r'\b(\d{1,3})\s*[/\-\.]\s*(\d{1,3})\b'
        )
        
        # Sequenzen
        self.sequence_pattern = re.compile(
            r'\b(\d{2,4})\b.*?\b(\d{2,4})\b.*?\b(\d{2,4})\b'
        )
        
        # Wiederholungen
        self.repetition_pattern = re.compile(
            r'(\b\d{2}\b).*?\1'
        )
    
    def _init_pattern_weights(self) -> Dict:
        """Initialisiere Pattern-Gewichte für ML-Scoring"""
        return {
            'number_code': 0.9,
            'combined_code': 0.8,
            'sequence': 0.7,
            'repetition': 0.6,
            'proximity': 0.5,
            'frequency': 0.4
        }
    
    def detect_with_ml(self, text: str) -> Dict[str, List[AdvancedDetectionResult]]:
        """
        Erweiterte Erkennung mit ML-Scoring
        
        Args:
            text: Zu analysierender Text
            
        Returns:
            Erweiterte Erkennungsergebnisse
        """
        results = {
            'number_codes': self._detect_number_codes_ml(text),
            'combined_codes': self._detect_combined_codes_ml(text),
            'sequences': self._detect_sequences_ml(text),
            'repetitions': self._detect_repetitions_ml(text)
        }
        
        return results
    
    def _detect_number_codes_ml(self, text: str) -> List[AdvancedDetectionResult]:
        """Erkenne Zahlen-Codes mit ML-Scoring"""
        results = []
        
        for code, meaning in self.number_codes.items():
            pattern = re.compile(r'\b' + re.escape(code) + r'\b')
            
            for match in pattern.finditer(text):
                # ML-Scoring basierend auf Kontext
                ml_score = self._calculate_ml_score(text, match.start(), match.end())
                
                # Pattern-Scoring
                pattern_score = self._calculate_pattern_score(text, match.start(), match.end())
                
                # Kombinierter Score
                combined_score = (ml_score + pattern_score) / 2
                
                results.append(AdvancedDetectionResult(
                    symbol_type='number_code',
                    detected_value=code,
                    meaning=meaning,
                    context=self._get_context(text, match.start(), match.end()),
                    confidence=0.9,
                    ml_score=ml_score,
                    pattern_score=pattern_score,
                    combined_score=combined_score,
                    position=(match.start(), match.end())
                ))
        
        return results
    
    def _detect_combined_codes_ml(self, text: str) -> List[AdvancedDetectionResult]:
        """Erkenne kombinierte Codes mit ML-Scoring"""
        results = []
        
        for match in self.combined_pattern.finditer(text):
            code1, code2 = match.groups()
            combined = f"{code1}/{code2}"
            
            # Prüfe ob beide Codes relevant sind
            if code1 in self.number_codes or code2 in self.number_codes:
                ml_score = self._calculate_ml_score(text, match.start(), match.end())
                pattern_score = 0.8  # Kombinierte Codes haben hohe Pattern-Relevanz
                combined_score = (ml_score + pattern_score) / 2
                
                results.append(AdvancedDetectionResult(
                    symbol_type='combined_code',
                    detected_value=combined,
                    meaning=f'Kombination: {code1} + {code2}',
                    context=self._get_context(text, match.start(), match.end()),
                    confidence=0.7,
                    ml_score=ml_score,
                    pattern_score=pattern_score,
                    combined_score=combined_score,
                    position=(match.start(), match.end())
                ))
        
        return results
    
    def _detect_sequences_ml(self, text: str) -> List[AdvancedDetectionResult]:
        """Erkenne Sequenzen von Codes mit ML-Scoring"""
        results = []
        
        for match in self.sequence_pattern.finditer(text):
            numbers = match.groups()
            
            # Prüfe ob Sequenz Nazi-Codes enthält
            nazi_codes = [n for n in numbers if n in self.number_codes]
            
            if len(nazi_codes) >= 2:
                sequence = '-'.join(numbers)
                ml_score = self._calculate_ml_score(text, match.start(), match.end())
                pattern_score = 0.7  # Sequenzen haben hohe Pattern-Relevanz
                combined_score = (ml_score + pattern_score) / 2
                
                results.append(AdvancedDetectionResult(
                    symbol_type='sequence',
                    detected_value=sequence,
                    meaning=f'Sequenz mit {len(nazi_codes)} Nazi-Codes',
                    context=self._get_context(text, match.start(), match.end()),
                    confidence=0.6,
                    ml_score=ml_score,
                    pattern_score=pattern_score,
                    combined_score=combined_score,
                    position=(match.start(), match.end())
                ))
        
        return results
    
    def _detect_repetitions_ml(self, text: str) -> List[AdvancedDetectionResult]:
        """Erkenne Wiederholungen von Codes mit ML-Scoring"""
        results = []
        
        # Zähle Häufigkeiten aller Zahlen
        numbers = re.findall(r'\b(\d{2,4})\b', text)
        counter = Counter(numbers)
        
        # Finde wiederholte Nazi-Codes
        for code, count in counter.items():
            if code in self.number_codes and count >= 2:
                ml_score = min(count * 0.1, 1.0)  # Häufigkeit erhöht Score
                pattern_score = 0.6
                combined_score = (ml_score + pattern_score) / 2
                
                # Finde alle Positionen
                positions = []
                for match in re.finditer(r'\b' + re.escape(code) + r'\b', text):
                    positions.append(match.start())
                
                for pos in positions:
                    results.append(AdvancedDetectionResult(
                        symbol_type='repetition',
                        detected_value=code,
                        meaning=f'{count} Wiederholungen von {code}',
                        context=self._get_context(text, pos, pos + len(code)),
                        confidence=0.5,
                        ml_score=ml_score,
                        pattern_score=pattern_score,
                        combined_score=combined_score,
                        position=(pos, pos + len(code))
                    ))
        
        return results
    
    def _calculate_ml_score(self, text: str, start: int, end: int) -> float:
        """
        Berechne ML-Score basierend auf Kontext-Features
        
        Args:
            text: Vollständiger Text
            start: Startposition des Match
            end: Endposition des Match
            
        Returns:
            ML-Score (0-1)
        """
        context = self._get_context(text, start, end, 100)
        
        score = 0.0
        
        # Feature 1: Nähe zu anderen Zahlen
        nearby_numbers = len(re.findall(r'\b\d{2,4}\b', context))
        if nearby_numbers > 0:
            score += 0.2 * min(nearby_numbers / 3, 1.0)
        
        # Feature 2: Politische Wörter im Kontext
        political_words = ['politik', 'system', 'eliten', 'global', 'kampf']
        political_count = sum(1 for word in political_words if word.lower() in context.lower())
        if political_count > 0:
            score += 0.3 * min(political_count / 2, 1.0)
        
        # Feature 3: Emotionale Wörter im Kontext
        emotional_words = ['wut', 'angst', 'hass', 'liebe', 'stolz']
        emotional_count = sum(1 for word in emotional_words if word.lower() in context.lower())
        if emotional_count > 0:
            score += 0.2 * min(emotional_count / 2, 1.0)
        
        # Feature 4: Historische Referenzen
        historical_words = ['geschichte', 'historisch', 'tradition', 'erbe']
        historical_count = sum(1 for word in historical_words if word.lower() in context.lower())
        if historical_count > 0:
            score += 0.3 * min(historical_count / 2, 1.0)
        
        return min(score, 1.0)
    
    def _calculate_pattern_score(self, text: str, start: int, end: int) -> float:
        """
        Berechne Pattern-Score basierend auf Position und Umgebung
        
        Args:
            text: Vollständiger Text
            start: Startposition des Match
            end: Endposition des Match
            
        Returns:
            Pattern-Score (0-1)
        """
        score = 0.5  # Basis-Score
        
        # Feature 1: Position im Text
        relative_pos = start / len(text)
        if relative_pos < 0.1 or relative_pos > 0.9:
            score += 0.2  # Anfang oder Ende erhöht Score
        
        # Feature 2: Satz-Anfang oder -Ende
        sentence_start = text.rfind('.', 0, start) + 1
        sentence_end = text.find('.', end)
        if sentence_end == -1:
            sentence_end = len(text)
        
        sentence = text[sentence_start:sentence_end]
        words = sentence.split()
        
        if start - sentence_start < 20:  # Nahe am Satzanfang
            score += 0.2
        
        if sentence_end - end < 20:  # Nahe am Satzende
            score += 0.2
        
        # Feature 3: Alleinstehend (nicht Teil von längerer Zahl)
        if start > 0 and not text[start-1].isdigit():
            score += 0.1
        
        return min(score, 1.0)
    
    def _get_context(self, text: str, start: int, end: int, context_length: int = 50) -> str:
        """Extrahiere Kontext um einen Match"""
        context_start = max(0, start - context_length)
        context_end = min(len(text), end + context_length)
        return text[context_start:context_end]
    
    def calculate_risk_score(self, text: str) -> Dict:
        """
        Berechne Gesamtrisiko-Score für einen Text
        
        Args:
            text: Zu analysierender Text
            
        Returns:
            Risiko-Analyse
        """
        results = self.detect_with_ml(text)
        
        total_detections = sum(len(detections) for detections in results.values())
        
        # Berechne durchschnittlichen combined_score
        all_scores = []
        for detections in results.values():
            all_scores.extend([d.combined_score for d in detections])
        
        avg_score = sum(all_scores) / len(all_scores) if all_scores else 0.0
        
        # Risiko-Kategorien
        if avg_score >= 0.8:
            risk_level = "SEHR HOCH"
        elif avg_score >= 0.6:
            risk_level = "HOCH"
        elif avg_score >= 0.4:
            risk_level = "MITTEL"
        elif avg_score >= 0.2:
            risk_level = "NIEDRIG"
        else:
            risk_level = "SEHR NIEDRIG"
        
        return {
            'total_detections': total_detections,
            'average_score': avg_score,
            'risk_level': risk_level,
            'recommendation': self._get_recommendation(risk_level, total_detections),
            'detailed_results': results
        }
    
    def _get_recommendation(self, risk_level: str, detections: int) -> str:
        """Generiere Empfehlung basierend auf Risiko"""
        if risk_level == "SEHR HOCH":
            return "SOFORTIGE MANNAHMEN ERFORDERLICH - Tiefergehende Untersuchung"
        elif risk_level == "HOCH":
            return "MANNAHMEN EMPFOHLEN - Detaillierte Analyse"
        elif risk_level == "MITTEL":
            return "ÜBERWACHUNG EMPFOHLEN - Regelmäßige Prüfung"
        elif risk_level == "NIEDRIG":
            return "KEINE AKUTE MASSNAHMEN - Monitoring beibehalten"
        else:
            return "KEINE MASSNAHMEN ERFORDERLICH"


def main():
    """Hauptfunktion für CLI-Nutzung"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Erweiterter Nazi-Symbolik Detector mit ML')
    parser.add_argument('text', help='Zu analysierender Text')
    parser.add_argument('--risk', '-r', action='store_true', help='Risiko-Analyse durchführen')
    
    args = parser.parse_args()
    
    detector = AdvancedNaziSymbolDetector()
    
    if args.risk:
        result = detector.calculate_risk_score(args.text)
        print(f"Risiko-Level: {result['risk_level']}")
        print(f"Empfehlung: {result['recommendation']}")
        print(f"Durchschnittlicher Score: {result['average_score']:.2f}")
    else:
        results = detector.detect_with_ml(args.text)
        for category, detections in results.items():
            print(f"{category}: {len(detections)}")
            for detection in detections[:5]:  # Zeige erste 5
                print(f"  - {detection.detected_value}: {detection.combined_score:.2f}")


if __name__ == '__main__':
    main()
