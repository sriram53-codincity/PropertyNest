# PropertyNest — Architecture

## System Architecture Diagram

```mermaid
graph TB
    subgraph CLIENT["🌐 Client Browser"]
        REACT["React 18<br/>React Router<br/>AuthContext"]
    end

    subgraph NGINX["🔀 Nginx Reverse Proxy"]
        STATIC["Static Files<br/>(React Build)"]
        PROXY["/api → FastAPI"]
    end

    subgraph BACKEND["⚙️ FastAPI Backend"]
        MAIN["main.py<br/>(App Entrypoint)"]
        AUTH["auth.py<br/>(JWT + bcrypt)"]
        
        subgraph ROUTES["Routes Layer (Waiter)"]
            R1["auth_routes"]
            R2["property_routes"]
            R3["application_routes"]
            R4["seller_request_routes"]
            R5["lease_routes"]
            R6["maintenance_routes"]
            R7["appointment_routes"]
        end
        
        subgraph SCHEMAS["Schemas Layer (Menu Checker)"]
            S1["Pydantic Models"]
            S2["Request Validation"]
            S3["Response Shapes"]
        end
        
        subgraph SERVICES["Services Layer (Chef)"]
            SV1["auth_service"]
            SV2["property_service"]
            SV3["application_service"]
            SV4["seller_request_service"]
            SV5["lease_service"]
            SV6["maintenance_service"]
            SV7["appointment_service"]
        end
    end

    subgraph DATABASES["🗄️ Databases"]
        PG["PostgreSQL 15<br/>(Relational Data)<br/>───────────<br/>users, properties,<br/>applications, leases,<br/>maintenance_requests,<br/>appointments,<br/>seller_requests"]
        MONGO["MongoDB 6<br/>(Document Data)<br/>───────────<br/>PropertyDetails:<br/>descriptions,<br/>amenities,<br/>image_urls,<br/>inspection_reports"]
    end

    subgraph DEVOPS["🔧 DevOps"]
        GH["GitHub Actions CI"]
        PYTEST["pytest (8 tests)"]
        VERIFY["verify_requirements.sh"]
    end

    REACT -->|"HTTP Requests"| NGINX
    NGINX -->|"/ (static)"| STATIC
    NGINX -->|"/api/*"| PROXY
    PROXY -->|"Proxy Pass"| MAIN
    MAIN --> ROUTES
    ROUTES -->|"Validates Input"| SCHEMAS
    SCHEMAS -->|"Clean Data"| SERVICES
    SERVICES -->|"SQLAlchemy<br/>Async Queries"| PG
    SERVICES -->|"Beanie ODM<br/>Document Ops"| MONGO
    AUTH -.->|"JWT Token<br/>Verification"| ROUTES
    GH -->|"On Push to main"| PYTEST
    GH -->|"On Push to main"| VERIFY
```

## Data Flow — How a Request Travels

```mermaid
sequenceDiagram
    participant U as User Browser
    participant N as Nginx
    participant R as Routes (Waiter)
    participant S as Schemas (Menu Checker)
    participant SV as Services (Chef)
    participant PG as PostgreSQL
    participant MG as MongoDB

    U->>N: POST /api/applications/
    N->>R: Proxy to FastAPI
    R->>R: Check JWT Token (auth.py)
    R->>R: Check User Role (require_roles)
    R->>S: Validate request body
    S-->>R: ✅ Data is valid
    R->>SV: create_application(body, user_id, db)
    SV->>PG: SELECT property WHERE id = ?
    PG-->>SV: Property found
    SV->>PG: SELECT application WHERE duplicate?
    PG-->>SV: No duplicate
    SV->>PG: INSERT INTO applications
    PG-->>SV: ✅ Saved (id=42)
    SV-->>R: {"message": "Application submitted", "id": "42"}
    R-->>N: 200 OK + JSON
    N-->>U: Display success
```

## Database Schema — PostgreSQL

```mermaid
erDiagram
    USERS ||--o{ USER_ROLES : has
    USERS ||--o{ PROPERTIES : owns
    USERS ||--o{ APPLICATIONS : submits
    USERS ||--o{ APPOINTMENTS : books
    USERS ||--o{ SELLER_REQUESTS : submits
    PROPERTIES ||--o{ APPLICATIONS : receives
    PROPERTIES ||--o{ LEASES : generates
    PROPERTIES ||--o{ APPOINTMENTS : linked_to
    APPLICATIONS ||--o| LEASES : creates
    LEASES ||--o{ MAINTENANCE_REQUESTS : has

    USERS {
        int id PK
        text full_name
        text email UK
        text password
        bool is_active
        datetime created_at
    }

    USER_ROLES {
        int id PK
        int user_id FK
        text role
    }

    PROPERTIES {
        int id PK
        int owner_id FK
        text title
        text city
        text property_type
        int bedrooms
        int bathrooms
        numeric monthly_rent
        text status
        bool is_available
    }

    APPLICATIONS {
        int id PK
        int property_id FK
        int applicant_id FK
        text full_name
        text email
        date date_of_birth
        text marital_status
        text employment_type
        date move_in_date
        int lease_duration
        text status
    }

    LEASES {
        int id PK
        int property_id FK
        int tenant_id FK
        int owner_id FK
        int application_id FK
        date start_date
        date end_date
        numeric monthly_rent
        text status
    }

    MAINTENANCE_REQUESTS {
        int id PK
        int lease_id FK
        int property_id FK
        int tenant_id FK
        text title
        text category
        text priority
        text status
    }

    APPOINTMENTS {
        int id PK
        int user_id FK
        int property_id FK
        int owner_id FK
        text purpose
        date preferred_date
        text status
        text meet_url
    }

    SELLER_REQUESTS {
        int id PK
        int user_id FK
        text full_name
        text property_title
        text district
        text status
    }
```

## MongoDB Document Structure

```json
{
  "_id": "ObjectId",
  "property_id": "42",
  "description": "Spacious 2BHK apartment with city view...",
  "amenities": ["WiFi", "Parking", "Gym", "Swimming Pool"],
  "image_urls": ["/uploads/property_images/uuid_photo.jpg"],
  "inspection_reports": []
}
```

> **Why two databases?**  
> PostgreSQL stores structured, relational data (users, properties, leases) where strict schemas and foreign key relationships matter.  
> MongoDB stores flexible, variable-length data (property descriptions, amenities lists, image galleries) where each property may have wildly different content.
