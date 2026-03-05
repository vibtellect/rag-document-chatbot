# RAG-Dokumenten-Chatbot (PoC)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![GitHub](https://img.shields.io/badge/GitHub-vibtellect/rag--document--chatbot-blue?logo=github)](https://github.com/vibtellect/rag-document-chatbot)

DE-first README. English version: [README_EN.md](./README_EN.md)

## 3-Minuten-Ergebnis

Diese Demo liefert einen lauffaehigen RAG-Stack fuer Unternehmensdokumente:

`PDF/Markdown Upload -> Chunking + Embeddings -> Qdrant -> Quellenbasierte Antwort`

**Proof-of-Concept**: Schnell einsatzbereit, ideal zum Lernen und Experimentieren. Fuer produktiven Einsatz siehe [Naechste Schritte](#naechste-schritte).

## Problem

Wissen steckt in vielen internen Dokumenten und ist schwer auffindbar.

## Loesung

Ein FastAPI-Backend mit Qdrant und Bedrock beantwortet Fragen auf Basis hochgeladener Inhalte, inkl. Quellenhinweisen.

## Architektur

- **Frontend**: React + Vite (Web-UI fuer Upload + Chat)
- **Backend**: FastAPI (Ingestion, Retrieval, LLM-Integration)
- **Vector Store**: Qdrant (In-Memory oder persistent)
- **Modelle**: AWS Bedrock (Claude 3.5 Sonnet + Titan Embeddings)
- **Containerisierung**: Docker Compose

## Quickstart

### 1) Setup

```bash
make setup
```

Dann `.env` aus `.env.example` kopieren und fuellen:

```bash
AWS_ACCESS_KEY_ID=AKIAXXXXXXXXXXXXXXXX
AWS_SECRET_ACCESS_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
AWS_REGION=eu-central-1
```

### 2) Start (Docker Compose)

```bash
make up
```

Frontend erreichbar unter `http://localhost:3000`, API unter `http://localhost:8000`.

### 3) Smoke-Test

```bash
make smoke
```

Erwartung:
- API Health `http://localhost:8000/health` erreichbar
- Frontend `http://localhost:3000` erreichbar

### 4) Stop

```bash
make down
```

## Demo-Nutzung {#demo}

### 1) Demo-Dokumente hochladen

5 Unternehmensdokumente stehen in `demo-docs/` bereit:

```bash
# Alle Demo-Dokumente hochladen
for doc in demo-docs/*.md; do
  curl -X POST http://localhost:8000/api/upload \
    -F "file=@$doc" -F "tenant_id=demo"
done
```

### 2) Fragen stellen (cURL)

```bash
# IT-Sicherheit
curl -X POST http://localhost:8000/api/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "Wie viele Zeichen muss ein Passwort mindestens haben?", "tenant_id": "demo"}'

# Reisekosten
curl -X POST http://localhost:8000/api/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "Wie hoch ist die Hotelkostenpauschale in Muenchen?", "tenant_id": "demo"}'

# Homeoffice
curl -X POST http://localhost:8000/api/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "Wie viele Tage pro Woche darf ich im Homeoffice arbeiten?", "tenant_id": "demo"}'

# Onboarding
curl -X POST http://localhost:8000/api/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "Was muss ich in der ersten Woche als neuer Mitarbeiter erledigen?", "tenant_id": "demo"}'
```

### 3) UI-basiert

Frontend unter `http://localhost:3000` oeffnen:
1. Documents hochladen (Drag-and-Drop oder Button)
2. Fragen stellen im Chat-Interface
3. Quellen anzeigen und validieren

## API-Endpunkte

- `POST /api/upload` (PDF oder Markdown)
- `POST /api/ask`
- `GET /api/documents`
- `DELETE /api/documents/{doc_id}`
- `GET /health`

## Projektstruktur

```text
.
|-- Makefile
|-- docker-compose.yml
|-- .env.example
|-- backend/
|-- frontend/
`-- demo-docs/
    |-- it-sicherheitsrichtlinie.md
    |-- urlaubsregelung.md
    |-- onboarding-checkliste.md
    |-- reisekostenrichtlinie.md
    `-- homeoffice-regelung.md
```

## Kosten (Richtwert)

Abhaengig von Tokenvolumen und Dokumentmenge, typischerweise im niedrigen zweistelligen USD-Bereich fuer kleine PoCs.

Bedrock-Pricing: https://aws.amazon.com/de/bedrock/pricing/

## Grenzen des PoC

- Kein Auth-/Rechtemodell
- Kein Langzeit-Monitoring/Observability
- Retrieval-Strategie ist bewusst einfach gehalten
- Nicht fuer direkten Produktivbetrieb ausgelegt

## Naechste Schritte fuer Produktivbetrieb

1. **Sicherheit**: Secret Management, Authentifizierung/Autorisierung, TLS
2. **Retrieval**: Reranking, Hybrid Search, Query-Expansion
3. **Betriebsbetrieb**: Logging, Monitoring, Alerting, Datenhaltung
4. **Skalierung**: Load-Balancing, Database-Backup, Disaster-Recovery

Siehe [SECURITY.md](./SECURITY.md) fuer Mindestanforderungen.

## Lizenz

MIT License - siehe [LICENSE](./LICENSE)

## Contributing

Contributions sind willkommen! Siehe [CONTRIBUTING.md](./CONTRIBUTING.md) fuer Details.

---

## Weitere Ressourcen

- **Portfolio**: [bojatschkin.de](https://bojatschkin.de) – Cloud Engineer mit KI-Integration
- **Blogpost**: [RAG-Chatbot mit Bedrock – Praxiswissen aus Unternehmensdokumenten](https://bojatschkin.de/blog/rag-chatbot-bedrock?utm_source=github&utm_medium=readme&utm_campaign=rag-chatbot-demo)
- **Kontakt**: Wenn du den PoC in einen produktiven Wissensassistenten mit sauberem Betriebskonzept ueberfuehren willst → [Kostenloses Erstgesprach buchen](https://bojatschkin.de?utm_source=github&utm_medium=readme&utm_campaign=rag-chatbot-contact)

---

Built by [vibtellect](https://github.com/vibtellect) – Cloud Engineering & AI Integration
