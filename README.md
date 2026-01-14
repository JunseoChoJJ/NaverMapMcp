# NaverMapMcp









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