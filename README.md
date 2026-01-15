# NaverMapMcp

Naver Map API를 활용한 MCP(Model Context Protocol) 서버입니다.  
LLM이 장소 검색, 좌표 변환, 경로 안내 기능을 사용할 수 있도록 도구(Tool)를 제공합니다.

---

## 🚀 주요 기능

| Tool | 설명 | API |
|------|------|-----|
| `naver_places` | 장소명으로 검색 (예: "홍대", 성수") | Naver Developers |
| `naver_geocode` | 주소 → 좌표 변환(x,y) 위도, 경도 | Naver Cloud Platform |
| `naver_directions` | 두 좌표 간 경로 안내 (거리, 소요시간) | Naver Cloud Platform |

### 사용 플로우 예시

```
"홍대에서 성수까지 얼마나 걸려?"
    ↓
1. naver_places("홍대") → 주소 획득
2. naver_places("성수") → 주소 획득
    ↓
3. naver_geocode -> 위도,경도 획득
4. naver_directions(start, goal) → 거리, 소요시간 반환
```

> 💡 **Tip**: 장소명 검색은 `naver_places`만 사용하면 됩니다!

---

## 📋 사전 요구사항

### 1. Naver Cloud Platform (Geocode, Directions용)

1. [Naver Cloud Platform](https://www.ncloud.com/) 가입
2. 콘솔 → Maps API → Application 등록
3. **Maps Geocoding**, **Maps Directions 5** API 사용 신청
4. Client ID / Client Secret 발급

### 2. Naver Developers (Places/Local Search용)

1. [Naver Developers](https://developers.naver.com/) 가입
2. 애플리케이션 등록
3. **검색 > 지역** API 사용 설정
4. Client ID / Client Secret 발급

> ⚠️ **주의**: 두 플랫폼의 API 키는 서로 다릅니다. 혼동하지 마세요!

---

## ⚙️ 설치 및 실행

### 1. 의존성 설치

```bash
uv sync
```

### 2. 환경 변수 설정

프로젝트 루트에 `.env` 파일 생성:

```env
# Naver Cloud Platform (Geocode, Directions)
NAVER_NCP_CLIENT_ID=your_ncp_client_id
NAVER_NCP_CLIENT_SECRET=your_ncp_client_secret

# Naver Developers (Places/Local Search)
NAVER_DEV_CLIENT_ID=your_dev_client_id
NAVER_DEV_CLIENT_SECRET=your_dev_client_secret
```


### 3. 서버 실행

```bash
uv run main.py
```

서버가 `http://0.0.0.0:8002`에서 실행됩니다.

---

## 🧪 테스트

### MCP Inspector로 검증

```bash
# 다른 터미널에서
npx @modelcontextprotocol/inspector
```



---

## 📁 프로젝트 구조

```
NaverMapMcp/
├── app/
│   ├── services/
│   │   └── naver_map_service.py   # Naver API 호출 서비스
│   └── tools/
│       ├── __init__.py
│       ├── directions.py          # naver_directions tool
│       ├── geocode.py             # naver_geocode tool
│       └── places.py              # naver_places tool
├── docs/                          # 문서
├── .env                           # 환경 변수 (git 제외)
├── .gitignore
├── .python-version
├── main.py                        # MCP 서버 엔트리포인트
├── pyproject.toml
├── uv.lock
└── README.md
```

---

## 🌿 Git 브랜치 전략

| 브랜치 | 설명 |
|--------|------|
| `master` | 프로덕션 배포 브랜치 |
| `develop` | 개발 통합 브랜치 |
| `feature/*` | 새로운 기능 개발 브랜치 |
| `hotfix/*` | 버그 수정 브랜치 |

### 브랜치 네이밍 예시

```bash
feature/naver-map-directions
feature/geocoding-service
hotfix/cors-middleware-error
hotfix/api-timeout-handling
```

---

## 📝 커밋 메시지 규칙

| Prefix | 설명 | 예시 |
|--------|------|------|
| `feat` | 새로운 기능 추가 | `feat: Add Naver Map directions API` |
| `fix` | 버그 수정 | `fix: Fix CORS middleware configuration` |
| `docs` | 문서 수정 | `docs: Update README with API examples` |
| `style` | 코드 포맷팅 (기능 변경 없음) | `style: Format code with Black` |
| `refactor` | 코드 리팩토링 | `refactor: Simplify routing service logic` |
| `test` | 테스트 코드 추가/수정 | `test: Add unit tests for geocoding` |
| `chore` | 빌드/설정 파일 수정 | `chore: Update dependencies in pyproject.toml` |

---

## 📚 참고 문서

- [Naver Maps Geocoding API](https://api.ncloud-docs.com/docs/application-maps-geocoding)
- [Naver Maps Directions 5 API](https://api.ncloud-docs.com/docs/application-maps-directions5)
- [Naver Developers 지역 검색 API](https://developers.naver.com/docs/serviceapi/search/local/local.md)
- [MCP (Model Context Protocol)](https://modelcontextprotocol.io/)
