- MySQL Database: armazena dados de Video, Genre, CastMember, Category.
- Kafka Connect: conecta o MySQL com o Kafka para replicar dados via Debezium MySQL
  - Copia dados do MySQL Database via connector
  - Envia dados para ElasticSearch (Sink ElasticSearch)
  - [ ] Apache Kafka (Message Broker): ???
- Database API Catálogo: ElasticSearch
- API Catálogo de Vídeos: endpoints para navegação e playback dos vídeos (?)


## Libs
- GraphQL: https://strawberry.rocks/
- FastAPI: https://fastapi.tiangolo.com/
- ElasticSearch: https://elasticsearch-py.readthedocs.io/en/latest/
- Kafka


## File structure

```
src/
├── use_cases/                   # Business logic and application use cases
│   ├── video/                   # Use cases specific to video management
│   │   ├── save_video.py        # Save video data to Elasticsearch via a database gateway
│   │   └── list_videos.py
│   ├── category/                # Use cases for category management
│   │   ├── save_category.py
│   │   └── list_categories.py
│   ├── genre/                   # Use cases for genre management
│   │   ├── save_genre.py
│   │   └── list_genres.py
│   └── cast_member/             # Use cases for cast member management
│       ├── save_cast_member.py
│       └── list_cast_members.py
├── domain/                      # Domain models (similar to DTOs with limited business rules)
│   ├── video.py                 # Praticamente só regras de validação? Talvez assumir dados válidos para evitar repetições
│   ├── category.py
│   ├── genre.py
│   └── cast_member.py
├── controller/                  # Controllers for interfacing with the outer world (HTTP, GraphQL)
│   ├── graphql/                 # GraphQL specific controllers
│   └── fastapi/                 # FastAPI specific controllers (RESTful API)
└── gateway (infra?)/            # Abstractions for external component integrations
    ├── elasticsearch/           # Elasticsearch integration logic
    └── kafka/                   # Kafka integration logic (listeners)
```
