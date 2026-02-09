# Performance Test Instructions

## Purpose

Backend 유닛의 성능 테스트 가이드입니다. NFR 요구사항을 충족하는지 검증합니다.

**Note**: 개발 환경 중심 프로젝트이므로 성능 테스트는 선택 사항입니다.

---

## Performance Requirements (NFR-1)

### Target Metrics
- **API 응답 시간**: < 1초 (95 percentile)
- **SSE 연결 시간**: < 2초
- **동시 사용자**: 50명
- **처리량**: 100 requests/second
- **에러율**: < 1%

### Test Environment
- **Server**: 전용 개발 서버 (2 Core CPU, 4GB RAM)
- **JVM**: 1GB Heap (-Xmx1g)
- **Database**: H2 In-Memory
- **Network**: Local network

---

## Performance Test Tools

### Option 1: Apache JMeter (권장)

**Installation**:
```bash
# Download JMeter
wget https://dlcdn.apache.org//jmeter/binaries/apache-jmeter-5.6.3.tgz
tar -xzf apache-jmeter-5.6.3.tgz
cd apache-jmeter-5.6.3

# Run JMeter GUI
./bin/jmeter
```

### Option 2: Gatling

**Installation**:
```bash
# Download Gatling
wget https://repo1.maven.org/maven2/io/gatling/highcharts/gatling-charts-highcharts-bundle/3.10.3/gatling-charts-highcharts-bundle-3.10.3.zip
unzip gatling-charts-highcharts-bundle-3.10.3.zip
cd gatling-charts-highcharts-bundle-3.10.3
```

### Option 3: k6 (간단한 스크립트)

**Installation**:
```bash
# Linux
sudo apt-get install k6

# macOS
brew install k6

# Windows
choco install k6
```

---

## Performance Test Scenarios

### Scenario 1: 주문 생성 부하 테스트

**Description**: 동시에 여러 고객이 주문을 생성하는 시나리오

**JMeter Test Plan**: `order-creation-load-test.jmx`

**Test Configuration**:
- **Virtual Users**: 50
- **Ramp-up Time**: 10초
- **Duration**: 60초
- **Target**: POST /api/customer/orders

**Expected Results**:
- **Average Response Time**: < 500ms
- **95th Percentile**: < 1000ms
- **Throughput**: > 50 requests/second
- **Error Rate**: < 1%

**JMeter Configuration**:
```xml
<ThreadGroup>
  <stringProp name="ThreadGroup.num_threads">50</stringProp>
  <stringProp name="ThreadGroup.ramp_time">10</stringProp>
  <stringProp name="ThreadGroup.duration">60</stringProp>
</ThreadGroup>

<HTTPSamplerProxy>
  <stringProp name="HTTPSampler.domain">localhost</stringProp>
  <stringProp name="HTTPSampler.port">8080</stringProp>
  <stringProp name="HTTPSampler.path">/api/customer/orders</stringProp>
  <stringProp name="HTTPSampler.method">POST</stringProp>
  <stringProp name="HTTPSampler.contentEncoding">UTF-8</stringProp>
  <stringProp name="HTTPSampler.postBodyRaw">
    {
      "sessionId": "${sessionId}",
      "tableId": 1,
      "items": [
        {"menuId": 1, "quantity": 2},
        {"menuId": 2, "quantity": 1}
      ]
    }
  </stringProp>
</HTTPSamplerProxy>
```

**Run Test**:
```bash
# GUI Mode (for test creation)
./bin/jmeter

# CLI Mode (for actual test)
./bin/jmeter -n -t order-creation-load-test.jmx -l results.jtl -e -o report/
```

---

### Scenario 2: 메뉴 조회 부하 테스트

**Description**: 여러 고객이 동시에 메뉴를 조회하는 시나리오 (캐싱 효과 검증)

**k6 Script**: `menu-query-load-test.js`

```javascript
import http from 'k6/http';
import { check, sleep } from 'k6';

export let options = {
  stages: [
    { duration: '10s', target: 20 },  // Ramp-up to 20 users
    { duration: '30s', target: 50 },  // Ramp-up to 50 users
    { duration: '20s', target: 50 },  // Stay at 50 users
    { duration: '10s', target: 0 },   // Ramp-down to 0 users
  ],
  thresholds: {
    http_req_duration: ['p(95)<1000'],  // 95% of requests < 1s
    http_req_failed: ['rate<0.01'],     // Error rate < 1%
  },
};

export default function () {
  let response = http.get('http://localhost:8080/api/customer/menus?storeId=1');
  
  check(response, {
    'status is 200': (r) => r.status === 200,
    'response time < 1s': (r) => r.timings.duration < 1000,
    'has menus': (r) => JSON.parse(r.body).data.length > 0,
  });
  
  sleep(1);
}
```

**Run Test**:
```bash
k6 run menu-query-load-test.js
```

**Expected Results**:
- **Average Response Time**: < 100ms (캐싱 효과)
- **95th Percentile**: < 200ms
- **Throughput**: > 100 requests/second
- **Error Rate**: < 1%

---

### Scenario 3: SSE 연결 부하 테스트

**Description**: 여러 고객이 동시에 SSE 연결을 유지하는 시나리오

**Gatling Script**: `SSELoadTest.scala`

```scala
import io.gatling.core.Predef._
import io.gatling.http.Predef._
import scala.concurrent.duration._

class SSELoadTest extends Simulation {
  
  val httpProtocol = http
    .baseUrl("http://localhost:8080")
    .acceptHeader("text/event-stream")
  
  val scn = scenario("SSE Connection Load Test")
    .exec(
      http("Connect SSE")
        .get("/api/customer/sse/connect?sessionId=${sessionId}")
        .check(status.is(200))
    )
    .pause(30.seconds)  // Keep connection for 30 seconds
  
  setUp(
    scn.inject(
      rampUsers(50) during (10.seconds)
    )
  ).protocols(httpProtocol)
}
```

**Run Test**:
```bash
./bin/gatling.sh -s SSELoadTest
```

**Expected Results**:
- **Connection Time**: < 2초
- **Concurrent Connections**: 50
- **Connection Stability**: > 99%
- **Memory Usage**: < 1GB JVM Heap

---

### Scenario 4: 주문 상태 변경 스트레스 테스트

**Description**: 관리자가 빠르게 여러 주문의 상태를 변경하는 시나리오

**JMeter Test Plan**: `order-status-stress-test.jmx`

**Test Configuration**:
- **Virtual Users**: 10 (관리자)
- **Ramp-up Time**: 5초
- **Duration**: 60초
- **Target**: PUT /api/admin/orders/{orderId}/status

**Expected Results**:
- **Average Response Time**: < 300ms
- **95th Percentile**: < 800ms
- **Throughput**: > 20 requests/second
- **Error Rate**: < 1%
- **Optimistic Lock Conflicts**: < 5%

---

### Scenario 5: 파일 업로드 부하 테스트

**Description**: 관리자가 여러 메뉴 이미지를 업로드하는 시나리오

**k6 Script**: `file-upload-load-test.js`

```javascript
import http from 'k6/http';
import { check } from 'k6';

export let options = {
  vus: 5,
  duration: '30s',
  thresholds: {
    http_req_duration: ['p(95)<3000'],  // 95% of requests < 3s
  },
};

const binFile = open('./test-image.jpg', 'b');

export default function () {
  const data = {
    file: http.file(binFile, 'test-image.jpg', 'image/jpeg'),
  };
  
  let response = http.post('http://localhost:8080/api/admin/menus/1/image', data, {
    headers: {
      'Authorization': 'Bearer ${token}',
    },
  });
  
  check(response, {
    'status is 200': (r) => r.status === 200,
    'response time < 3s': (r) => r.timings.duration < 3000,
  });
}
```

**Run Test**:
```bash
k6 run file-upload-load-test.js
```

**Expected Results**:
- **Average Response Time**: < 1초
- **95th Percentile**: < 3초
- **Throughput**: > 5 uploads/second
- **Error Rate**: < 1%

---

## Performance Test Execution

### Step 1: Prepare Test Environment

```bash
# 1. Start Backend Application
cd backend
java -jar -Xmx1g -Xms512m target/table-order-backend-1.0.0.jar

# 2. Verify Application is Running
curl http://localhost:8080/actuator/health

# 3. Prepare Test Data
# - Create test stores, tables, menus
# - Generate test sessions
```

### Step 2: Run Performance Tests

```bash
# JMeter Tests
./bin/jmeter -n -t order-creation-load-test.jmx -l results/order-creation.jtl -e -o report/order-creation/

# k6 Tests
k6 run menu-query-load-test.js --out json=results/menu-query.json

# Gatling Tests
./bin/gatling.sh -s SSELoadTest
```

### Step 3: Analyze Results

**JMeter Report**:
```bash
# Open HTML report
open report/order-creation/index.html
```

**k6 Report**:
```bash
# View console output
k6 run menu-query-load-test.js

# Example output:
#   http_req_duration..........: avg=150ms  min=50ms  med=120ms  max=800ms  p(95)=400ms
#   http_req_failed............: 0.50%
#   http_reqs..................: 3000
#   iteration_duration.........: avg=1.15s
```

**Gatling Report**:
```bash
# Open HTML report
open results/sseloadtest-*/index.html
```

---

## Performance Monitoring

### 1. JVM Monitoring

**Enable JMX**:
```bash
java -jar \
  -Xmx1g -Xms512m \
  -Dcom.sun.management.jmxremote \
  -Dcom.sun.management.jmxremote.port=9010 \
  -Dcom.sun.management.jmxremote.authenticate=false \
  -Dcom.sun.management.jmxremote.ssl=false \
  target/table-order-backend-1.0.0.jar
```

**Monitor with JConsole**:
```bash
jconsole localhost:9010
```

**Key Metrics**:
- **Heap Memory Usage**: < 800MB (80% of 1GB)
- **GC Frequency**: < 10 times/minute
- **Thread Count**: < 100
- **CPU Usage**: < 80%

### 2. Application Metrics

**Spring Boot Actuator**:
```bash
# Health Check
curl http://localhost:8080/actuator/health

# Metrics
curl http://localhost:8080/actuator/metrics

# HTTP Trace
curl http://localhost:8080/actuator/httptrace
```

### 3. Database Monitoring

**H2 Console**:
```bash
# Access H2 Console
http://localhost:8080/h2-console

# Check active connections
SELECT COUNT(*) FROM INFORMATION_SCHEMA.SESSIONS;
```

---

## Performance Optimization

### If Response Time > 1s

**Possible Causes**:
1. Database query performance
2. N+1 query problem
3. Missing indexes
4. Cache not working

**Solutions**:
1. Add database indexes (see `schema.sql`)
2. Use `@BatchSize` for collections
3. Enable query logging: `spring.jpa.show-sql=true`
4. Verify cache configuration

### If Memory Usage > 800MB

**Possible Causes**:
1. Memory leak
2. Too many SSE connections
3. Large objects in cache

**Solutions**:
1. Analyze heap dump: `jmap -dump:live,format=b,file=heap.bin <pid>`
2. Limit SSE connections per session
3. Configure cache eviction policy

### If Error Rate > 1%

**Possible Causes**:
1. Optimistic lock conflicts
2. Connection pool exhausted
3. Timeout errors

**Solutions**:
1. Increase retry attempts
2. Increase connection pool size
3. Increase timeout values

---

## Performance Test Report Template

### Test Summary
```markdown
## Performance Test Results

### Test Environment
- **Date**: YYYY-MM-DD
- **Server**: 2 Core CPU, 4GB RAM
- **JVM**: 1GB Heap
- **Database**: H2 In-Memory

### Test Scenarios

#### 1. Order Creation Load Test
- **Virtual Users**: 50
- **Duration**: 60s
- **Total Requests**: 3000
- **Average Response Time**: 450ms
- **95th Percentile**: 850ms
- **Throughput**: 50 req/s
- **Error Rate**: 0.5%
- **Status**: ✅ PASS

#### 2. Menu Query Load Test
- **Virtual Users**: 50
- **Duration**: 70s
- **Total Requests**: 5000
- **Average Response Time**: 80ms
- **95th Percentile**: 150ms
- **Throughput**: 120 req/s
- **Error Rate**: 0.2%
- **Status**: ✅ PASS

#### 3. SSE Connection Load Test
- **Concurrent Connections**: 50
- **Duration**: 30s
- **Connection Time**: 1.2s
- **Connection Stability**: 99.5%
- **Memory Usage**: 750MB
- **Status**: ✅ PASS

### Overall Assessment
- ✅ All NFR requirements met
- ✅ Response times within target
- ✅ Error rates acceptable
- ✅ System stable under load

### Recommendations
1. Monitor memory usage in production
2. Consider horizontal scaling for > 100 users
3. Optimize database queries for complex reports
```

---

## Troubleshooting

### Issue 1: High Response Time
**Symptoms**: Response time > 2s

**Solutions**:
1. Check database query performance
2. Enable query logging
3. Add missing indexes
4. Verify cache is working

### Issue 2: Out of Memory
**Symptoms**: `java.lang.OutOfMemoryError`

**Solutions**:
1. Increase JVM heap: `-Xmx2g`
2. Analyze heap dump
3. Fix memory leaks
4. Reduce cache size

### Issue 3: Connection Pool Exhausted
**Symptoms**: `Cannot get connection from pool`

**Solutions**:
1. Increase pool size in `application.yml`:
   ```yaml
   spring:
     datasource:
       hikari:
         maximum-pool-size: 20
   ```
2. Check for connection leaks
3. Reduce connection timeout

---

## Performance Test Checklist

- [ ] 주문 생성 부하 테스트 (50 users, 60s)
- [ ] 메뉴 조회 부하 테스트 (50 users, 70s)
- [ ] SSE 연결 부하 테스트 (50 connections, 30s)
- [ ] 주문 상태 변경 스트레스 테스트 (10 users, 60s)
- [ ] 파일 업로드 부하 테스트 (5 users, 30s)
- [ ] JVM 메모리 모니터링 (< 800MB)
- [ ] CPU 사용률 모니터링 (< 80%)
- [ ] 에러율 검증 (< 1%)
- [ ] 응답 시간 검증 (95th < 1s)

---

## Next Steps

Performance 테스트 완료 후:
1. ✅ **Test Summary**: `build-and-test-summary.md` 참고
2. ✅ **Deployment**: `deployment-architecture.md` 참고

---

## References

- **JMeter Documentation**: https://jmeter.apache.org/usermanual/index.html
- **k6 Documentation**: https://k6.io/docs/
- **Gatling Documentation**: https://gatling.io/docs/current/
- **Spring Boot Actuator**: https://docs.spring.io/spring-boot/docs/current/reference/html/actuator.html
- **NFR Requirements**: `aidlc-docs/construction/backend/nfr-requirements/nfr-requirements.md`
