# Statistische Signifikanztests: Anleitung und Beispiele

## Überblick

Anleitung für die Durchführung statistischer Signifikanztests für die Analyse von Nazi-Symbolik, basierend auf der validierten Methodik.

## 1. Grundlagen

### 1.1 Nullhypothese

**Definition:**
Die Nullhypothese (H0) besagt, dass kein Zusammenhang zwischen der beobachteten Häufigkeit eines Codes und der erwarteten Häufigkeit im zufälligen Kontext besteht.

**Beispiel:**
H0: Die Häufigkeit des Codes "88" im analysierten Text ist nicht signifikant höher als im zufälligen Kontext.

### 1.2 Alternativhypothese

**Definition:**
Die Alternativhypothese (H1) besagt, dass ein signifikanter Zusammenhang zwischen der beobachteten Häufigkeit eines Codes und der erwarteten Häufigkeit im zufälligen Kontext besteht.

**Beispiel:**
H1: Die Häufigkeit des Codes "88" im analysierten Text ist signifikant höher als im zufälligen Kontext.

### 1.3 Signifikanzniveau

**Definition:**
Das Signifikanzniveau (α) ist die Wahrscheinlichkeit, die Nullhypothese fälschlicherweise abzulehnen (Fehler 1. Art).

**Wert:**
Typischerweise wird α = 0.05 (5%) verwendet.

## 2. Häufigkeitsanalyse

### 2.1 Chi-Quadrat-Test

**Zweck:**
Testung, ob die beobachtete Häufigkeit eines Codes signifikant von der erwarteten Häufigkeit abweicht.

**Formel:**
χ² = Σ ((O - E)² / E)

Dabei:
- O = Beobachtete Häufigkeit
- E = Erwartete Häufigkeit

**Beispiel:**
- Beobachtete Häufigkeit von "88" im analysierten Text: 50
- Erwartete Häufigkeit von "88" im zufälligen Kontext: 10
- χ² = ((50 - 10)² / 10) = 160

**Interpretation:**
- χ² = 160 ist hoch
- p < 0.001 (sehr signifikant)
- Die Nullhypothese wird abgelehnt

### 2.2 Binomial-Test

**Zweck:**
Testung, ob die beobachtete Häufigkeit eines Codes signifikant höher als die erwartete Häufigkeit ist.

**Formel:**
P(X = k) = (n choose k) * p^k * (1-p)^(n-k)

Dabei:
- n = Gesamtzahl der Beobachtungen
- k = Beobachtete Häufigkeit des Codes
- p = Erwartete Wahrscheinlichkeit des Codes

**Beispiel:**
- n = 1000 (Gesamtzahl der Wörter)
- k = 50 (beobachtete Häufigkeit von "88")
- p = 0.01 (erwartete Wahrscheinlichkeit von "88")

**Interpretation:**
- P(X = 50) ist sehr klein
- p < 0.001 (sehr signifikant)
- Die Nullhypothese wird abgelehnt

## 3. Assoziationsanalyse

### 3.1 Fisher's Exact Test

**Zweck:**
Testung, ob zwei Codes signifikant miteinander assoziiert sind.

**Formel:**
Der Test berechnet die exakte Wahrscheinlichkeit der beobachteten Kontingenztabelle unter der Annahme der Unabhängigkeit.

**Beispiel:**
Kontingenztabelle für "88" und "18":

|          | "18" vorhanden | "18" nicht vorhanden | Summe |
|----------|----------------|---------------------|-------|
| "88" vorhanden | 40 | 10 | 50 |
| "88" nicht vorhanden | 5 | 945 | 950 |
| Summe | 45 | 955 | 1000 |

**Interpretation:**
- Fisher's Exact Test zeigt signifikante Assoziation
- p < 0.001 (sehr signifikant)
- Die Nullhypothese der Unabhängigkeit wird abgelehnt

### 3.2 Odds Ratio

**Zweck:**
Bestimmung der Stärke der Assoziation zwischen zwei Codes.

**Formel:**
OR = (a * d) / (b * c)

Dabei:
- a = Häufigkeit von beiden Codes
- b = Häufigkeit von Code A ohne Code B
- c = Häufigkeit von Code B ohne Code A
- d = Häufigkeit von keinem Code

**Beispiel:**
- a = 40 (beide Codes)
- b = 10 (nur "88")
- c = 5 (nur "18")
- d = 945 (kein Code)
- OR = (40 * 945) / (10 * 5) = 756

**Interpretation:**
- OR = 756 ist sehr hoch
- Starke Assoziation zwischen "88" und "18"
- Die Wahrscheinlichkeit, beide Codes zu finden, ist 756-mal höher als erwartet

## 4. Multiple-Testing-Korrektur

### 4.1 Bonferroni-Korrektur

**Zweck:**
Korrektur für multiple Tests, um die Fehlerwahrscheinlichkeit zu kontrollieren.

**Formel:**
α_korrigiert = α / n

Dabei:
- α = Ursprüngliches Signifikanzniveau (z.B. 0.05)
- n = Anzahl der Tests

**Beispiel:**
- α = 0.05
- n = 10 Tests
- α_korrigiert = 0.05 / 10 = 0.005

**Interpretation:**
- Nur p-Werte < 0.005 sind signifikant
- Strikteres Signifikanzniveau zur Kontrolle für multiple Tests

### 4.2 False Discovery Rate (FDR)

**Zweck:**
Kontrolle der erwarteten Proportion falscher positiver Ergebnisse.

**Formel:**
Benjamini-Hochberg-Prozedur

**Beispiel:**
- Sortierung der p-Werte in aufsteigender Reihenfolge
- Berechnung des kritischen Wertes für jeden p-Wert
- Ablehnung aller Hypothesen mit p-Werten unter dem kritischen Wert

**Interpretation:**
- Kontrolliert die erwartete Proportion falscher positiver Ergebnisse
- Weniger konservativ als Bonferroni-Korrektur

## 5. Effektgrößen

### 5.1 Cramér's V

**Zweck:**
Bestimmung der Effektgröße für Chi-Quadrat-Tests.

**Formel:**
V = sqrt(χ² / (n * min(r-1, c-1)))

Dabei:
- χ² = Chi-Quadrat-Wert
- n = Gesamtzahl der Beobachtungen
- r = Anzahl der Zeilen
- c = Anzahl der Spalten

**Beispiel:**
- χ² = 160
- n = 1000
- r = 2
- c = 2
- V = sqrt(160 / (1000 * 1)) = 0.4

**Interpretation:**
- V = 0.4 (mittlere Effektgröße)
- 0.1 = kleine Effektgröße
- 0.3 = mittlere Effektgröße
- 0.5 = große Effektgröße

### 5.2 Cohen's d

**Zweck:**
Bestimmung der Effektgröße für Unterschiede zwischen zwei Gruppen.

**Formel:**
d = (M1 - M2) / SD

Dabei:
- M1 = Mittelwert Gruppe 1
- M2 = Mittelwert Gruppe 2
- SD = Gepoolte Standardabweichung

**Beispiel:**
- M1 = 50 (Häufigkeit von "88" in Texten mit Nazi-Symbolik)
- M2 = 10 (Häufigkeit von "88" in Texten ohne Nazi-Symbolik)
- SD = 20
- d = (50 - 10) / 20 = 2.0

**Interpretation:**
- d = 2.0 (sehr große Effektgröße)
- 0.2 = kleine Effektgröße
- 0.5 = mittlere Effektgröße
- 0.8 = große Effektgröße

## 6. Implementierung in Python

### 6.1 Chi-Quadrat-Test

```python
from scipy.stats import chi2_contingency

# Kontingenztabelle
observed = [[50, 950], [10, 990]]

# Chi-Quadrat-Test
chi2, p, dof, expected = chi2_contingency(observed)

print(f"Chi-Quadrat-Wert: {chi2}")
print(f"p-Wert: {p}")
print(f"Freiheitsgrade: {dof}")
```

### 6.2 Fisher's Exact Test

```python
from scipy.stats import fisher_exact

# Kontingenztabelle
table = [[40, 10], [5, 945]]

# Fisher's Exact Test
oddsratio, p = fisher_exact(table)

print(f"Odds Ratio: {oddsratio}")
print(f"p-Wert: {p}")
```

### 6.3 Binomial-Test

```python
from scipy.stats import binom_test

# Parameter
n = 1000
k = 50
p = 0.01

# Binomial-Test
p_value = binom_test(k, n, p)

print(f"p-Wert: {p_value}")
```

## 7. Empfehlungen

### 7.1 Durchführung der Tests

**Schritt 1:**
- Bestimmung der Basisrate für jeden Code
- Bestimmung der beobachteten Rate im analysierten Text

**Schritt 2:**
- Durchführung des Chi-Quadrat-Tests
- Durchführung des Binomial-Tests
- Durchführung von Fisher's Exact Test für Assoziationen

**Schritt 3:**
- Multiple-Testing-Korrektur durchführen
- Berechnung der Effektgrößen
- Interpretation der Ergebnisse

### 7.2 Berichterstattung

**Bericht:**
- Bericht aller p-Werte (korrigiert und unkorrigeriert)
- Bericht aller Effektgrößen
- Bericht aller Konfidenzintervalle
- Transparente Darstellung aller Methoden

**Interpretation:**
- Nur Ergebnisse mit p < 0.05 (korrigiert) als signifikant berichten
- Effektgrößen berichten, um die praktische Relevanz zu bewerten
- Limitationen und Unsicherheiten offenlegen

## 8. Fazit

**Empfehlung:**
Alle Analysen sollten mit statistischen Signifikanztests durchgeführt werden, um evidenzbasierte Ergebnisse zu gewährleisten und Halluzinationen oder an den Haaren herbeigezogene Evidenzen zu vermeiden.

---

*Diese Anleitung dient der Durchführung statistischer Signifikanztests für die Analyse von Nazi-Symbolik.*

*Erstellungsdatum: 13. April 2026*
*Status: Anleitung erstellt*
