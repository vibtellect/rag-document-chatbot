# IT-Sicherheitsrichtlinie

**Gültig ab:** 01.01.2026  
**Version:** 2.0  
**Verantwortlich:** IT-Abteilung

---

## 1. Passwort-Policy

### 1.1 Anforderungen

Alle Mitarbeiter müssen folgende Passwort-Richtlinien einhalten:

- **Mindestlänge:** 12 Zeichen
- **Komplexität:** Groß- und Kleinbuchstaben, Zahlen, Sonderzeichen
- **Änderungsintervall:** 90 Tage
- **Wiederverwendung:** Letzte 5 Passwörter dürfen nicht verwendet werden
- **Speicherung:** Keine Passwörter auf Papier oder unverschlüsselt digital

### 1.2 Multi-Faktor-Authentifizierung (MFA)

Für folgende Systeme ist MFA verpflichtend:

- VPN-Zugang
- E-Mail (externer Zugriff)
- Cloud-Speicher (OneDrive, SharePoint)
- Remote Desktop

---

## 2. VPN-Zugang

### 2.1 Berechtigte Personen

VPN-Zugang wird gewährt für:

- Mitarbeiter im Homeoffice
- Externe Dienstleister (zeitlich begrenzt)
- Geschäftsführung

### 2.2 Verbindungsdaten

- **Server:** vpn.unternehmen.de
- **Protokoll:** IKEv2/IPSec
- **Port:** 500/4500

### 2.3 Sicherheitshinweise

- VPN nur für geschäftliche Zwecke nutzen
- Bei Nichtgebrauch trennen
- Keine Weitergabe von Zugangsdaten

---

## 3. Datenschutz und Datensicherheit

### 3.1 Klassifizierung von Daten

| Klasse             | Beispiele                          | Schutzmaßnahmen       |
| ------------------ | ---------------------------------- | --------------------- |
| Öffentlich         | Webseite, Broschüren               | Standard              |
| Intern             | Organigramme, interne Mitteilungen | Zugangskontrolle      |
| Vertraulich        | Kundendaten, Verträge              | Verschlüsselung       |
| Streng vertraulich | Finanzdaten, Personalakten         | Verschlüsselung + MFA |

### 3.2 E-Mail-Verschlüsselung

E-Mails mit vertraulichen Inhalten müssen verschlüsselt werden:

- **Intern:** TLS-Verschlüsselung
- **Extern:** S/MIME oder PGP

---

## 4. Incident Response

### 4.1 Meldepflicht

Folgende Vorfälle müssen sofort an die IT gemeldet werden:

- Verdacht auf Malware-Infektion
- Phishing-E-Mails
- Verlust mobiler Geräte
- Unautorisierter Datenzugriff

### 4.2 Meldewege

- **E-Mail:** security@unternehmen.de
- **Telefon:** +49 123 456789-99 (24/7)
- **Internes Ticket:** Service Desk

### 4.3 Eskalation

1. **Level 1:** IT-Helpdesk (Erstbewertung)
2. **Level 2:** IT-Security (Analyse)
3. **Level 3:** Externe Forensik (bei schweren Vorfällen)

---

## 5. Schulung

### 5.1 Pflichtschulungen

- **Einführung:** Bei Arbeitsantritt
- **Auffrischung:** Jährlich
- **Spezialthemen:** Bei neuen Bedrohungen

### 5.2 Inhalte

- Phishing-Erkennung
- Passwort-Sicherheit
- Umgang mit vertraulichen Daten
- Verhalten bei Sicherheitsvorfällen

---

**Unterschrift:**

Mit meiner Unterschrift bestätige ich, die IT-Sicherheitsrichtlinie gelesen und verstanden zu haben.

Name: ************\_************

Datum: ************\_************

Unterschrift: ************\_************
