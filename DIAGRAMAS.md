## Arquitetura de alto nível
```mermaid

graph TD

A[React Frontend] -->|HTTPS /login| B[C# Auth Service]
B -->|JWT assinado + refresh token| A

A -->|Authorization: Bearer JWT| C[Python Reservation Service]

C --> D[(PostgreSQL - Reservation DB)]
B --> E[(PostgreSQL - Auth DB)]

C --> F[Application / Domain Layer]
F --> G[Repository Layer]
G --> D

B --> H[Identity / Token Issuer]
H --> E

```

## Diagrama de Domínio e Persistência
```mermaid
classDiagram
    class BaseEntity {
        +int id
        +datetime created_at
        +datetime updated_at
    }

    class Location {
        +str name
        +str address
        +bool active
    }
    class Room {
        +str name
        +int capacity
        +int location_id
        +bool active
        +str notes
    }
    class Reservation {
        +int room_id
        +datetime start_datetime
        +datetime end_datetime
        +str responsible
        +str email
        +str phone
        +bool coffee
        +bool projector
        +int people_count
        +str description
        +str status
    }
    class ReservationConflict {
        +int reservation_id
        +str reason
    }

    BaseEntity <|-- Location
    BaseEntity <|-- Room
    BaseEntity <|-- Reservation

    Location "1" -- "0..*" Room : contém
    Room "1" -- "0..*" Reservation : contém
    Room --> Location : location_id
    Reservation --> Room : room_id
    Reservation ..> ReservationConflict : validações de sobreposição
```

## Fluxo de Autenticação e Reserva
```
[1] Usuário autentica no Frontend
    |
    | POST /login (credentials)
    v
[2] Auth Service valida identidade e emite JWT
    |
    | access token + refresh token
    v
[3] Frontend armazena sessão e anexa Bearer Token
    |
    | Authorization: Bearer <jwt>
    v
[4] Reservation Service valida assinatura, expiração e claims
    |
    | policy / authorization checks
    v
[5] Application Service executa o caso de uso
    |
    | overlap, capacity, status, auditoria
    v
[6] Repository persiste em Reservation DB
    |
    v
[7] Resposta retorna com dados consolidados e status
```