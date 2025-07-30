# 코딩 에이전트 툴킷 (Coding Agent Toolkit)

파이썬 개발을 위한 코딩 에이전트 툴킷 라이브러리입니다. 이 라이브러리는 코드 컨텍스트 관리, 코드 분석, 코드 생성 등의 기능을 제공합니다.

## 주요 기능

- 코드 컨텍스트 관리
- AST(추상 구문 트리) 기반 코드 분석
- 코드 생성 및 변환
- 프로젝트 구조 분석

## 설치 방법

```bash
pip install coding-agent-toolkit
```

## 사용 예시

```python
from coding_agent_toolkit import CodeContext, CodeAnalyzer

# 코드 컨텍스트 로드
context = CodeContext("my_project/")

# 코드 분석
analyzer = CodeAnalyzer(context)
functions = analyzer.find_functions("module_name")
```
