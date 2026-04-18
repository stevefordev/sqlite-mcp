# 🧠 SQLite MCP: Zero-Config AI Sidekick

**SQLite MCP**는 AI가 당신의 로컬 데이터에 접근하고, 분석하며, 지식을 관리할 수 있게 돕는 가장 단순하고 강력한 인터페이스입니다.

## 🚀 프로젝트 철학: "Zero-Configuration Sidekick"

현대적인 AI 도구들은 종종 복잡한 API 설정, 클라우드 연동, 데이터 프라이버시 문제를 동반합니다. 이 MCP는 다음 세 가지 원칙을 따릅니다.

1.  **Zero-Config**: API Key나 복잡한 서버 설정이 필요 없습니다. 오직 `.db` 파일 하나면 충분합니다.
2.  **Portable Brain**: 프로젝트 폴더마다 독립된 SQLite DB를 두어 AI가 해당 프로젝트의 '기억'을 로컬에 저장하고 꺼내 쓸 수 있게 합니다.
3.  **Security First**: 물리적(`mode=ro`) 및 논리적(SQL 필터링) 이중 보안을 통해 AI가 실수로 데이터를 수정하거나 삭제하는 것을 원천 차단합니다.

## 🛠 주요 기능

-   🔍 **Database Discovery**: 특정 경로 내의 모든 SQLite 파일(`.db`, `.sqlite`, `.sqlite3`)을 자동으로 스캔합니다.
-   🗺 **Schema Introspection**: DB의 전체 구조(테이블, 컬럼 타입)를 한눈에 파악하여 AI가 데이터의 맥락을 완벽히 이해하게 돕습니다.
-   ⚡ **Secure Querying**: 오직 `SELECT` 쿼리만 허용하는 강력한 읽기 전용 모드로 안전한 데이터 분석을 수행합니다.
-   📝 **AI-Ready Schema**: 샘플 데이터를 미리 보기하여 AI가 쿼리를 작성하기 전 데이터의 실제 형태를 학습합니다.

## 📦 설치 및 설정

### 1. 사전 요구 사항
-   Python 3.10 이상
-   [uv](https://github.com/astral-sh/uv) (추천)

### 2. 설치
```bash
cd sqlite-mcp
uv pip install .
```

### 3. Claude Desktop 설정
`claude_desktop_config.json` 파일에 아래 설정을 추가하세요. (경로는 실제 프로젝트 경로로 수정 필요)

```json
{
  "mcpServers": {
    "sqlite-browser": {
      "command": "uv",
      "args": [
        "--directory",
        "D:/work/git/test/sqlite-mcp",
        "run",
        "sqlite-mcp"
      ]
    }
  }
}
```

## 🔧 제공 도구 (Tools)

-   `create_database(db_path)`: 새로운 SQLite 데이터베이스 파일을 생성합니다.
-   `list_databases(path)`: 지정된 경로의 SQLite DB 목록을 반환합니다.
-   `get_schema_summary(db_path)`: DB의 모든 테이블과 컬럼 구조를 요약해서 보여줍니다.
-   `list_tables(db_path)`: DB 내의 모든 테이블 목록을 가져옵니다.
-   `describe_table(db_path, table_name)`: 특정 테이블의 스키마와 5개의 샘플 데이터를 보여줍니다.
- `add_note(db_path, title, content)`: AI가 아이디어나 메모를 특정 DB의 `notes` 테이블에 즉시 기록합니다.

## 🌟 실제 활용 예시 (Use Cases)

### 1. 프로젝트 브레인 (Project Knowledge Base)
- **상황**: 프로젝트 아키텍처 설계나 중요한 의사결정 과정을 기록하고 싶을 때.
- **활용**: AI에게 대화 요약을 시키고 이를 로컬 DB에 저장하여, 나중에 프로젝트의 역사나 결정 이유를 즉시 검색할 수 있습니다.
- **프롬프트**: *"지금까지 논의한 서비스 구조의 장단점을 요약해서 `architecture_notes.db`에 저장해줘."*

### 2. 로컬 데이터 분석가 (Local Data Analyst)
- **상황**: 대용량 로그 파일이나 서비스 데이터를 SQL로 빠르게 분석해야 할 때.
- **활용**: AI가 전체 스키마를 파악하고 복잡한 SQL 쿼리를 대신 작성하여 데이터 인사이트를 도출합니다.
- **프롬프트**: *"이 폴더에 있는 `sales_data.db` 분석해줘. 지난달 매출이 가장 높았던 제품 TOP 3를 찾아줘."*

### 3. 코드 스니펫 및 템플릿 관리 (Code Snippet Manager)
- **상황**: 자주 사용하는 설정 파일이나 복잡한 정규식 등을 프로젝트별로 관리하고 싶을 때.
- **활용**: 클라우드 서비스 대신 프로젝트 루트의 `.snippets.db`에 저장하여 프로젝트 소스코드와 함께 관리합니다.
- **프롬프트**: *"방금 작성한 API 응답 처리 로직을 'Response Utility'라는 제목으로 내 아이디어 DB에 기록해줘."*

---
*이 프로젝트는 AI와 인간이 함께 아이디어를 빌드하고, 그 지식을 가장 안전하고 효율적으로 관리하기 위해 만들어졌습니다.*