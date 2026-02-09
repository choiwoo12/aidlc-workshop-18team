# Build Instructions

## Prerequisites

### Required Software
- **JDK**: Java 17 or higher
- **Build Tool**: Maven 3.6 or higher
- **Operating System**: Linux (Ubuntu 20.04 LTS 권장), Windows, macOS

### Verify Prerequisites
```bash
# Java 버전 확인
java -version
# 출력 예시: openjdk version "17.0.x"

# Maven 버전 확인
mvn -version
# 출력 예시: Apache Maven 3.6.x or higher
```

---

## Build Steps

### 1. Navigate to Backend Directory
```bash
cd backend
```

### 2. Install Dependencies
```bash
mvn dependency:resolve
```

**Expected Output**:
```
[INFO] BUILD SUCCESS
[INFO] Total time: X.XXX s
```

**Troubleshooting**:
- **Error**: "Cannot resolve dependencies"
  - **Solution**: Maven Central 접속 확인, 프록시 설정 확인
  - **Command**: `mvn dependency:purge-local-repository` 후 재시도

### 3. Clean Previous Build
```bash
mvn clean
```

**Expected Output**:
```
[INFO] Deleting target directory
[INFO] BUILD SUCCESS
```

### 4. Compile Source Code
```bash
mvn compile
```

**Expected Output**:
```
[INFO] Compiling XX source files to target/classes
[INFO] BUILD SUCCESS
```

**Troubleshooting**:
- **Error**: "Compilation failure"
  - **Cause**: Java 버전 불일치, 소스 코드 오류
  - **Solution**: JDK 17 사용 확인, 소스 코드 검토

### 5. Run Tests (Optional at this stage)
```bash
mvn test
```

**Note**: 테스트 실행은 unit-test-instructions.md 참고

### 6. Package Application
```bash
mvn package
```

**Expected Output**:
```
[INFO] Building jar: target/table-order-backend-1.0.0.jar
[INFO] BUILD SUCCESS
[INFO] Total time: XX.XXX s
```

**Build Artifacts**:
- **Location**: `backend/target/`
- **Main Artifact**: `table-order-backend-1.0.0.jar` (Executable JAR)
- **Size**: ~50-60 MB (dependencies 포함)

### 7. Verify Build Success
```bash
# JAR 파일 존재 확인
ls -lh target/table-order-backend-1.0.0.jar

# JAR 파일 내용 확인 (optional)
jar tf target/table-order-backend-1.0.0.jar | head -20
```

---

## One-Command Build

전체 빌드를 한 번에 실행:
```bash
cd backend
mvn clean package
```

**Expected Output**:
```
[INFO] ------------------------------------------------------------------------
[INFO] BUILD SUCCESS
[INFO] ------------------------------------------------------------------------
[INFO] Total time: XX.XXX s
[INFO] Finished at: YYYY-MM-DDTHH:MM:SS+09:00
[INFO] ------------------------------------------------------------------------
```

---

## Build Without Tests

테스트를 건너뛰고 빌드:
```bash
mvn clean package -DskipTests
```

**Use Case**: 빠른 빌드가 필요하거나 테스트를 별도로 실행할 때

---

## Environment Configuration

### 1. Default Configuration
기본 설정은 `src/main/resources/application.yml`에 정의되어 있습니다.

### 2. Custom Configuration (Optional)
환경별 설정 파일 생성:
```bash
# 개발 환경
cp src/main/resources/application.yml src/main/resources/application-dev.yml

# 테스트 환경
cp src/main/resources/application.yml src/main/resources/application-test.yml
```

### 3. Environment Variables
빌드 시 환경 변수 설정 (optional):
```bash
export JWT_SECRET=your-secret-key-here
export SPRING_PROFILES_ACTIVE=dev
```

---

## Build Artifacts

### Generated Files
```
backend/target/
├── table-order-backend-1.0.0.jar          # Executable JAR (Main artifact)
├── classes/                                # Compiled classes
│   ├── com/tableorder/                    # Application classes
│   ├── application.yml                    # Configuration
│   ├── schema.sql                         # Database schema
│   └── data.sql                           # Sample data
├── generated-sources/                      # Generated source files
├── maven-archiver/                         # Maven metadata
├── maven-status/                           # Build status
└── test-classes/                           # Compiled test classes
```

### Main Artifact Details
- **Name**: `table-order-backend-1.0.0.jar`
- **Type**: Executable JAR (Spring Boot Fat JAR)
- **Size**: ~50-60 MB
- **Contents**: Application code + All dependencies + Embedded Tomcat
- **Execution**: `java -jar table-order-backend-1.0.0.jar`

---

## Common Build Warnings

### Acceptable Warnings
다음 경고는 무시해도 됩니다:
```
[WARNING] Using platform encoding (UTF-8 actually) to copy filtered resources
[WARNING] Parameter 'xxx' is deprecated
```

### Warnings to Address
다음 경고는 확인이 필요합니다:
```
[WARNING] Compilation failure
[WARNING] Tests run: X, Failures: X, Errors: X
```

---

## Build Profiles

### Development Profile
```bash
mvn clean package -Pdev
```

### Production Profile (향후)
```bash
mvn clean package -Pprod
```

---

## Troubleshooting

### Issue 1: Maven Dependency Download Failure
**Symptoms**:
```
[ERROR] Failed to execute goal on project: Could not resolve dependencies
```

**Solutions**:
1. 인터넷 연결 확인
2. Maven Central 접속 확인
3. 로컬 저장소 정리: `rm -rf ~/.m2/repository`
4. 재시도: `mvn clean package`

### Issue 2: Java Version Mismatch
**Symptoms**:
```
[ERROR] Source option 17 is no longer supported. Use 17 or later.
```

**Solutions**:
1. JDK 17 설치 확인: `java -version`
2. JAVA_HOME 환경 변수 설정:
   ```bash
   export JAVA_HOME=/path/to/jdk-17
   export PATH=$JAVA_HOME/bin:$PATH
   ```

### Issue 3: Out of Memory Error
**Symptoms**:
```
[ERROR] Java heap space
```

**Solutions**:
1. Maven 메모리 증가:
   ```bash
   export MAVEN_OPTS="-Xmx2g -Xms512m"
   mvn clean package
   ```

### Issue 4: Compilation Errors
**Symptoms**:
```
[ERROR] Compilation failure: cannot find symbol
```

**Solutions**:
1. 소스 코드 검토 (implementation-guide.md 참고)
2. 누락된 클래스 구현
3. Import 문 확인

---

## Build Performance

### Typical Build Times
- **Clean Build**: 30-60초 (dependencies 다운로드 포함)
- **Incremental Build**: 10-20초
- **With Tests**: +20-40초

### Optimization Tips
1. **Parallel Build**: `mvn -T 4 clean package` (4 threads)
2. **Offline Mode**: `mvn -o package` (dependencies 이미 다운로드된 경우)
3. **Skip Tests**: `mvn package -DskipTests` (빠른 빌드)

---

## Next Steps

빌드 성공 후:
1. ✅ **Run Application**: `java -jar target/table-order-backend-1.0.0.jar`
2. ✅ **Run Tests**: `unit-test-instructions.md` 참고
3. ✅ **Integration Tests**: `integration-test-instructions.md` 참고
4. ✅ **Deployment**: `deployment-architecture.md` 참고

---

## Build Verification Checklist

- [ ] JDK 17 설치 확인
- [ ] Maven 3.6+ 설치 확인
- [ ] Dependencies 다운로드 성공
- [ ] Compilation 성공
- [ ] JAR 파일 생성 확인 (`target/table-order-backend-1.0.0.jar`)
- [ ] JAR 파일 크기 확인 (~50-60 MB)
- [ ] BUILD SUCCESS 메시지 확인

---

## References

- **Maven Documentation**: https://maven.apache.org/guides/
- **Spring Boot Maven Plugin**: https://docs.spring.io/spring-boot/docs/current/maven-plugin/reference/htmlsingle/
- **Project README**: `backend/README.md`
- **Deployment Guide**: `aidlc-docs/construction/backend/infrastructure-design/deployment-architecture.md`
