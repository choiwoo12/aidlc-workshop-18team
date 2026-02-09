# Table Order Backend

테이블오더 서비스의 Backend API 서버입니다.

## Tech Stack

- **Language**: Java 17
- **Framework**: Spring Boot 3.2.0
- **Database**: H2 In-Memory
- **Data Access**: MyBatis 3.0.3
- **Security**: Spring Security + JWT
- **Cache**: Caffeine
- **Real-time**: Server-Sent Events (SSE)
- **API Documentation**: Springdoc OpenAPI (Swagger)
- **Build Tool**: Maven 3.x

## Prerequisites

- JDK 17 or higher
- Maven 3.6 or higher

## Build

```bash
mvn clean package
```

## Run

```bash
java -jar target/table-order-backend-1.0.0.jar
```

Or with custom JVM options:

```bash
java -jar -Xmx1g -Xms512m target/table-order-backend-1.0.0.jar
```

## Configuration

Environment variables:
- `JWT_SECRET`: JWT secret key (default: default-secret-key-change-in-production)
- `SPRING_PROFILES_ACTIVE`: Active profile (dev, test, prod)

## API Documentation

Swagger UI: http://localhost:8080/swagger-ui.html

## H2 Console

H2 Console: http://localhost:8080/h2-console
- JDBC URL: jdbc:h2:mem:tableorder
- Username: sa
- Password: (empty)

## Testing

Run unit tests:
```bash
mvn test
```

## Project Structure

```
backend/
├── src/
│   ├── main/
│   │   ├── java/com/tableorder/
│   │   │   ├── common/          # Common components
│   │   │   ├── config/          # Configuration classes
│   │   │   ├── controller/      # REST controllers
│   │   │   ├── domain/          # Domain entities
│   │   │   ├── dto/             # Data Transfer Objects
│   │   │   ├── exception/       # Exception classes
│   │   │   ├── infrastructure/  # Infrastructure services
│   │   │   ├── mapper/          # MyBatis mappers
│   │   │   ├── security/        # Security components
│   │   │   ├── service/         # Business logic
│   │   │   └── util/            # Utility classes
│   │   └── resources/
│   │       ├── mybatis/mapper/  # MyBatis XML mappers
│   │       ├── application.yml
│   │       └── schema.sql
│   └── test/                    # Test classes
├── pom.xml
└── README.md
```
