# 🖱️ Kafka Clickstream Analytics — Streaming en Temps Réel

> Pipeline complet d'analyse comportementale en temps réel d'un site web
> avec Apache Kafka, Flask, PostgreSQL et Streamlit.

## 📋 Description

Ce projet implémente une architecture complète de **Streaming Analytics**
capable de capturer, transporter, traiter et visualiser les interactions
des utilisateurs sur un site web **en moins d'une seconde**.

Chaque clic, scroll, page vue et session est capturé par JavaScript,
transporté via Apache Kafka, stocké dans PostgreSQL et affiché
en temps réel sur un dashboard Streamlit.

---

## 🏗️ Architecture
Site Web (HTML5UP)
│
│  fetch POST (JavaScript)
▼
API Flask (port 5000)
│
│  KafkaProducer
▼
Apache Kafka — topic: clickstream (port 9093)
│
│  KafkaConsumer
▼
Consumer Python
│
├──► PostgreSQL (port 5433)
│
└──► Dashboard Streamlit (port 8501)



## ⚙️ Stack Technique

| Composant | Technologie | Version |
|-----------|-------------|---------|
| Streaming | Apache Kafka (mode KRaft) | 3.7.0 |
| API | Flask + Flask-CORS | Python 3.x |
| Consumer | kafka-python | Python 3.x |
| Base de données | PostgreSQL | 15 |
| Dashboard | Streamlit | Dernière |
| ORM | SQLAlchemy | Dernière |
| Infrastructure | Docker Compose | - |
| Frontend | HTML5UP Massively | - |


## 📁 Structure du projet
kafka-streaming/
├── docker-compose.yml    ← Kafka (KRaft) + PostgreSQL
├── api.py                ← API Flask — producteur Kafka
├── consumer.py           ← Consumer Kafka → PostgreSQL
├── dashboard.py          ← Dashboard Streamlit live
├── .gitignore
├── README.md
└── site/
├── index.html        ← Site HTML5UP + tracking JS
├── assets/
│   ├── css/
│   └── js/
└── images/

---

## 🚀 Installation et Lancement

### Prérequis

- Python 3.10+
- Docker Desktop
- Git

### 1. Cloner le projet

```bash
git clone https://github.com/VotreUsername/kafka-clickstream-analytics.git
cd kafka-clickstream-analytics
```

### 2. Créer l'environnement virtuel

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac / Linux
source venv/bin/activate
```

### 3. Installer les dépendances Python

```bash
pip install flask flask-cors kafka-python psycopg2-binary sqlalchemy pandas streamlit
```

### 4. Démarrer Kafka et PostgreSQL

```bash
docker-compose up -d
docker-compose ps    # vérifier que kafka et postgres sont Up
```

### 5. Créer les tables PostgreSQL

```bash
docker exec -it postgres psql -U admin -d streaming_db
```

```sql
CREATE TABLE IF NOT EXISTS clicks (
    id         SERIAL PRIMARY KEY,
    timestamp  TIMESTAMP DEFAULT NOW(),
    page       TEXT,
    element    TEXT,
    event_type TEXT,
    x_pos      INTEGER,
    y_pos      INTEGER,
    user_agent TEXT
);

CREATE INDEX idx_clicks_timestamp  ON clicks(timestamp);
CREATE INDEX idx_clicks_event_type ON clicks(event_type);
```

Quittez avec `\q`.

### 6. Lancer les 5 composants (5 terminaux)

```bash
# Terminal 1 
docker-compose up -d

# Terminal 2 — API Flask
python api.py

# Terminal 3 — Consumer Kafka
python consumer.py

# Terminal 4 — Dashboard Streamlit
streamlit run dashboard.py

# Terminal 5 — Site web
cd site
python -m http.server 8080
```

---

## 🌐 Accès aux services

| Service | URL |
|---------|-----|
| Site Web | http://localhost:8080 |
| API Flask | http://localhost:5000 |
| Dashboard Streamlit | http://localhost:8501 |
| Kafka broker | localhost:9093 |
| PostgreSQL | localhost:5433 |

---

## 📊 Événements capturés

| Événement | Déclencheur | Donnée capturée |
|-----------|-------------|-----------------|
| `pageview` | Chargement de la page | Titre de la page |
| `click` | Clic sur un élément | Texte de l'élément |
| `link_click` | Clic sur un lien | Texte ou URL du lien |
| `scroll` | Défilement (max 1/sec) | Profondeur en % |
| `session_end` | Fermeture de la page | Durée en secondes |
| `form_submit` | Soumission formulaire | Identifiant du formulaire |

---



## 📚 Technologies utilisées

- [Apache Kafka](https://kafka.apache.org/)
- [Flask](https://flask.palletsprojects.com/)
- [Streamlit](https://streamlit.io/)
- [PostgreSQL](https://www.postgresql.org/)
- [Docker](https://www.docker.com/)
- [HTML5UP Massively](https://html5up.net/massively)
