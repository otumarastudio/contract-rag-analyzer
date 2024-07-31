# 프로젝트 구조
root/
├──rag/
   ├── core/
   │   └──db_adapters/
   │       ├── __init__.py
   │       ├── chroma.py
   │       ├── pinecone.py
   │       └── milvus.py
   │   ├── __init__.py
   │   ├── data_ingestion.py  # data_ingestion 모듈 통합
   │   ├── data_processing.py  # data_processing 모듈 통합
   │   ├── embedding.py  # embedding 관련 기능 통합
   │   ├── retrieval.py  # retrieval 및 ranking 통합
   │   ├── query_processing.py  # query_processing 모듈 통합
   │   ├── context_bulding.py  # context_building 모듈 통합
   │   └── answer_generation.py  # answer_generation 모듈 통합
   │   └── vector_store.py 
   ├── storage/
   ├── evaluation/
   │   ├── __init__.py
   │   ├── metrics.py
   │   └── quality.py
   ├── utils/
   │   ├── __init__.py
   │   ├── config.py
   │   └── logger.py
   ├── tests/
   │   ├── __init__.py
   │   ├── test_core.py
   │   ├── test_storage.py
   │   ├── test_evaluation.py
   │   └── test_api.py
   ├── data/
   │   ├── raw/
   │   ├── processed/
   │   └── embeddings/
   └── main.py
└── app.py


# RAG 시스템 모듈화 전략 및 개발 순서
1. 사전 준비 작업 모듈
1.1 data_ingestion

역할: 데이터 수집 및 전처리
주요 기능:

PDF 파일 읽기
텍스트 추출
기본적인 텍스트 정제 (특수문자 제거, 공백 정리 등)


1.2 data_processing

역할: 청킹 및 메타데이터 확장
주요 기능:

텍스트 청킹 (섹션, 단락, 문장 단위)
메타데이터 추출 및 확장 (프로젝트명, 국가, 프로젝트 유형 등)


1.3 embedding_and_storage

역할: 텍스트 임베딩 생성 및 벡터 데이터베이스 관리
주요 기능:

텍스트 임베딩 생성
다양한 벡터 데이터베이스 지원 (예: Chroma, Pinecone, Milvus)
임베딩 저장 및 검색 인터페이스 제공


2. 쿼리 처리 및 응답 생성 모듈
2.1 retrieval

역할: 유사도 검색 및 관련 문서 검색
주요 기능:

다양한 검색 알고리즘 구현 (코사인 유사도, BM25 등)
검색 결과 랭킹


2.2 query_processing

역할: 사용자 쿼리 처리 및 확장
주요 기능:

사용자 쿼리 분석
GPT를 이용한 연계 질문 또는 분리 질문 생성
복수 질문에 대한 retrieval 요청 관리


2.3 context_building

역할: 검색 결과를 바탕으로 컨텍스트 구성
주요 기능:

검색된 문서 조각들을 조합하여 컨텍스트 생성
관련성에 따른 가중치 부여


2.4 answer_generation

역할: 최종 응답 생성
주요 기능:

GPT를 이용한 응답 생성
원문 및 메타데이터와 함께 증거 제시


3. 평가 및 최적화 모듈
3.1 evaluation

역할: 시스템 성능 평가 및 개선
주요 기능:

응답 품질 평가
검색 정확도 측정
처리 시간 모니터링


# 개발 순서 및 통합 전략

사전 준비 작업 모듈 개발 (1.1 → 1.2 → 1.3)

각 모듈 독립적으로 개발 및 단위 테스트
모듈 간 통합 테스트 (데이터 흐름 확인)


쿼리 처리 및 응답 생성 모듈 개발 (2.1 → 2.2 → 2.3 → 2.4)

각 모듈 독립적으로 개발 및 단위 테스트
점진적 통합 및 테스트 (예: 2.1과 2.2 통합 → 2.3 추가 → 2.4 추가)


Flask 백엔드 개발 및 UI 연동

RESTful API 설계 및 구현
쿼리 처리 및 응답 생성 모듈과 백엔드 통합
프론트엔드 UI 개발 및 백엔드 연동


평가 및 최적화 모듈 개발

시스템 전체 성능 평가 지표 정의
평가 결과를 바탕으로 각 모듈 최적화


지속적인 개선 및 확장

사용자 피드백 수집 및 분석
새로운 기능 추가 (예: 다국어 지원, 문서 버전 관리 등)



=== 인수인계 ===

# RAG 시스템 요약 및 인수인계 사항


## 주요 파일 및 역할

### config.py
- 환경 변수 및 시스템 설정 관리
- API 키, 데이터베이스 경로, 모델 설정 등 중앙 관리

### main.py
- RAG 시스템의 진입점
- `RAGSystem` 클래스를 통해 전체 프로세스 조율
- 문서 수집, 처리, 쿼리 처리 등 고수준 작업 수행

### core/data_ingestion.py
- 문서 로딩 담당 (예: PDF 파일 읽기)

### core/data_processing.py
- 로드된 문서의 전처리 및 청크 분할

### core/embedding.py
- 텍스트 임베딩 생성

### core/vector_store.py
- 벡터 데이터베이스 생성 및 관리
- Chroma 벡터 저장소 사용

### core/retrieval.py
- 관련 문서 검색 로직
- 기본 검색 및 압축 검색(ContextualCompressionRetriever) 제공

### core/query_processing.py
- 사용자 쿼리 처리 및 프롬프트 템플릿 관리

### core/answer_generation.py
- LLM을 사용한 최종 응답 생성

## 2. 주요 클래스 및 함수

### RAGSystem (in main.py)
- 초기화: `__init__()` - 시스템 구성요소 초기화
- 문서 처리: `ingest_and_process(file_path)` - 문서 수집 및 처리
- 쿼리 처리: `process_query(question, use_compression=False)` - 사용자 쿼리에 대한 응답 생성

### VectorStore (in core/vector_store.py)
- 벡터 저장소 생성: `create_vectorstore(documents, embeddings)`
- 벡터 저장소 로드: `load_vectorstore(embeddings)`

### Retriever (in core/retrieval.py)
- 기본 검색기 생성: `get_basic_retriever()`
- 압축 검색기 생성: `get_compressed_retriever()`
- 문서 검색: `retrieve(query, use_compression=False)`

## 3. 인수인계 주요 사항

1. **환경 설정**
   - `config.py`에서 모든 설정 관리
   - `.env` 파일을 통한 환경 변수 관리 (API 키 등)

2. **데이터 처리 흐름**
   - 문서 수집 (PyMuPDFLoader) → 청크 분할 (RecursiveCharacterTextSplitter) → 임베딩 생성 (OpenAIEmbeddings) → 벡터 저장소 저장 (Chroma)

3. **쿼리 처리 흐름**
   - 사용자 쿼리 입력 → 관련 문서 검색 → 컨텍스트 구성 → LLM을 통한 응답 생성

4. **확장 및 커스터마이징**
   - 새로운 문서 타입 지원: `data_ingestion.py` 수정
   - 다른 벡터 저장소 사용: `vector_store.py` 수정
   - 검색 로직 변경: `retrieval.py` 수정
   - 프롬프트 템플릿 수정: `query_processing.py` 수정

5. **성능 최적화**
   - `retrieval.py`의 `use_compression` 파라미터로 검색 정확도 vs 속도 조절 가능

6. **주의사항**
   - API 키 보안 관리 철저
   - 대용량 문서 처리 시 메모리 사용량 모니터링 필요
   - LLM 사용량 및 비용 관리 필요

7. **향후 개선 사항**
   - 다중 문서 타입 지원 확장
   - 사용자 인터페이스 개발 (웹 애플리케이션 등)
   - 비동기 처리를 통한 성능 개선
   - 캐싱 메커니즘 도입으로 반복 쿼리 최적화

