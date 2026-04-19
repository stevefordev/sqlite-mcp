# 🧠 SQLite MCP Server: Zero-Config AI Sidekick

**SQLite MCP Server**는 AI가 당신의 로컬 데이터에 접근하고, 분석하며, 지식을 관리할 수 있게 돕는 가장 단순하고 강력한 인터페이스입니다.

## 🚀 프로젝트 철학: "Zero-Configuration Sidekick"

1.  **Zero-Config**: API Key나 복잡한 서버 설정이 필요 없습니다. 오직 `.db` 파일 하나면 충분합니다.
2.  **Portable Brain**: 프로젝트 폴더마다 독립된 SQLite DB를 두어 AI가 해당 프로젝트의 '기억'을 로컬에 저장하고 꺼내 쓸 수 있게 합니다.
3.  **Security First**: 강력한 읽기 전용 모드와 SQL 필터링을 통해 안전한 데이터 관리를 보장합니다.

## 🛠 주요 기능

-   🔍 **Database Discovery**: 특정 경로 내의 모든 SQLite 파일(`.db`, `.sqlite`, `.sqlite3`)을 자동으로 스캔합니다.
-   🗺 **Schema Introspection**: DB의 전체 구조를 파악하여 AI가 데이터의 맥락을 완벽히 이해하게 돕습니다.
-   ⚡ **Secure Querying**: `SELECT` 쿼리만 허용하는 강력한 보안 모드로 데이터 분석을 수행합니다.
-   📝 **Note & Record Support**: AI가 아이디어나 메모를 특정 DB에 즉시 기록할 수 있는 전용 도구를 제공합니다.
-   📁 **DB Creation**: 필요한 경우 새로운 SQLite 데이터베이스 파일을 즉시 생성할 수 있습니다.

## 📦 설치 및 설정

### 1. 사전 요구 사항
- [uv](https://github.com/astral-sh/uv) 설치 권장 또는 Python 3.10 이상.

### 2. 사용 방법

#### 📦 설치 및 실행 (추천)
Windows의 보안 정책(Smart App Control 등)으로 인해 `uvx` 사용 시 실행이 차단될 수 있습니다. 이를 방지하기 위해 패키지를 로컬 도구로 설치하여 사용하는 것을 권장합니다.

```bash
# uv 사용 (권장)
uv tool install sqlite-mcp-server

# 또는 pip 사용
pip install sqlite-mcp-server
```

설치 후에는 어디서든 명령어로 실행할 수 있습니다:
```bash
sqlite-mcp-server
```

#### ⚡ uvx 사용 (선택 사항)
설치 없이 빠르게 실행해보고 싶을 때 사용합니다 (Windows에서 `os error 4551` 발생 시 위 설치 방법을 사용하세요):
```bash
uvx sqlite-mcp-server
```

### 3. MCP 클라이언트 연동

#### Gemini CLI (추천)
다음 명령어를 실행하여 서버를 추가합니다:
```bash
gemini mcp add sqlite-mcp uvx sqlite-mcp-server
```

직접 설정하려면 `.gemini/settings.json` 파일에 다음 설정을 추가하세요:
```json
{
  "mcpServers": {
    "sqlite-mcp": {
      "command": "uvx",
      "args": ["sqlite-mcp-server"]
    }
  }
}
```

#### Claude Desktop
Claude Desktop 설정 파일에 다음 내용을 추가하세요:
```json
{
  "mcpServers": {
    "sqlite-mcp": {
      "command": "uv",
      "args": [
        "tool",
        "run",
        "--from",
        "sqlite-mcp-server"
      ]
    }
  }
}
```

#### Claude Code
다음 명령어를 실행하여 서버를 추가합니다:
```bash
claude mcp add sqlite-mcp -- uvx sqlite-mcp-server
```

## 🔧 제공 도구 (Tools)

- `create_database(db_path)`: 새로운 SQLite 데이터베이스 파일을 생성합니다.
- `list_databases(path)`: 지정된 경로의 SQLite DB 목록을 반환합니다.
- `search_databases(path, query)`: 지정된 경로 내의 모든 DB를 검색하여 특정 키워드(테이블명, 컬럼명)가 포함된 위치를 찾습니다.
- `get_schema_summary(db_path)`: DB의 모든 테이블과 컬럼 구조를 요약해서 보여줍니다.
- `list_tables(db_path)`: DB 내의 모든 테이블 목록을 가져옵니다.
- `describe_table(db_path, table_name)`: 특정 테이블의 스키마와 샘플 데이터를 보여줍니다.
- `add_record(db_path, table_name, title, content)`: 데이터베이스에 새로운 레코드를 추가합니다 (테이블 자동 생성 지원).
- `execute_query(db_path, query)`: SELECT 쿼리를 실행하여 데이터를 분석합니다.

## 🌟 개발자 가이드
```bash
# 의존성 설치
uv sync

# 서버 로컬 실행
uv run sqlite-mcp
```

## 라이선스
MIT