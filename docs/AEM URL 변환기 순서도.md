---
title: "AEM URL 변환기 순서도"
description: "AEM URL Converter의 리팩토링된 SOLID 원칙 기반 아키텍처의 처리 흐름 순서도 - GlobalLink 번역 파일에서 AEM MSM 에디터 링크 생성 프로세스"
architect: "Sijung Kim"
authors: ["Sijung Kim", "Claude", "Gemini"]
reviewed_by: "Sijung Kim"
created_date: "2025-09-15"
last_modified: "2025-09-17"
version: "2.0.0"
document_type: "Flowchart"
diagram_type: "Mermaid Flowchart"
tags: ["Flowchart", "Process Flow", "SOLID", "Architecture", "Mermaid"]
---

# AEM URL 변환기 순서도

리팩토링된 SOLID 원칙 기반 아키텍처의 처리 흐름

``` mermaid
graph TD
    Start[Start: main.py 실행] --> LoadConfig[Config 로드<br/>환경변수 또는 기본값]
    LoadConfig --> CreateDI[DIContainer 생성<br/>의존성 주입 컨테이너]
    CreateDI --> InitApp[AEMConverterApp 초기화]

    InitApp --> ShowUI[Streamlit UI 표시]
    ShowUI --> InputFields[Job ID & Submission Name<br/>입력 필드 렌더링]
    InputFields --> FileUpload{ZIP 파일 업로드}

    FileUpload -->|파일 선택됨| ProcessStart[처리 시작: "Processing ZIP file..."]
    FileUpload -->|파일 없음| FileUpload

    ProcessStart --> GetZipProcessor[DIContainer에서<br/>ZipFileProcessor 획득]
    GetZipProcessor --> ProcessZip[ZipFileProcessor.process 호출]

    ProcessZip --> OpenZip[BytesIO로 ZIP 열기]
    OpenZip --> InitResult[ProcessingResult 초기화<br/>LinkCollection 생성]
    InitResult --> StartLoop[파일 목록 순회 시작]

    StartLoop --> CheckFile{다음 파일 존재?}
    CheckFile -->|예| DetectLang[LanguageDetectorService로<br/>언어 감지]
    CheckFile -->|아니오| ProcessComplete[처리 완료]

    DetectLang --> LangFound{언어 감지됨?}
    LangFound -->|ko-KR 발견| SetKorean[target_lang = 'ko']
    LangFound -->|ja-JP 발견| SetJapanese[target_lang = 'ja']
    LangFound -->|언어 없음| NextFile[다음 파일로]

    SetKorean --> CheckContent
    SetJapanese --> CheckContent
    CheckContent{파일명이 #content로<br/>시작하는가?}

    CheckContent -->|아니오| NextFile
    CheckContent -->|예| GenerateURL[AEMURLGenerator로<br/>URL 생성]

    GenerateURL --> ValidateFile{파일명이 #으로<br/>시작하는가?}
    ValidateFile -->|아니오| NextFile
    ValidateFile -->|예| CreateAEMPath[AEM 경로 생성<br/>.xml을 .html로 변환]

    CreateAEMPath --> BuildURL[에디터 URL 구성<br/>AEM_HOST + /editor.html/ + path]
    BuildURL --> CreateLink[AEMLink 객체 생성<br/>url, path, language]
    CreateLink --> AddToCollection[LinkCollection에 추가]

    AddToCollection --> NextFile
    NextFile --> CheckFile

    ProcessComplete --> ValidateResult{ProcessingResult<br/>유효성 검사}
    ValidateResult -->|실패| ShowError[오류 메시지 표시<br/>경고 표시]
    ValidateResult -->|성공| ShowSuccess[성공 메시지 표시<br/>처리된 파일 수]

    ShowError --> End[종료]
    ShowSuccess --> CreateTabs[탭 생성<br/>Summary, Japanese, Korean]

    CreateTabs --> BuildSummary[SummaryDataFrameBuilder로<br/>요약 정보 생성]
    BuildSummary --> ParallelDisplay[병렬 결과 표시]

    ParallelDisplay --> JapaneseTab[일본어 탭]
    ParallelDisplay --> KoreanTab[한국어 탭]

    JapaneseTab --> CheckJapanese{일본어 링크<br/>존재?}
    CheckJapanese -->|예| BuildJADF[HierarchicalDataFrameBuilder로<br/>일본어 DataFrame 생성]
    CheckJapanese -->|아니오| ShowJAWarning[일본어 파일 없음 경고]

    KoreanTab --> CheckKorean{한국어 링크<br/>존재?}
    CheckKorean -->|예| BuildKODF[HierarchicalDataFrameBuilder로<br/>한국어 DataFrame 생성]
    CheckKorean -->|아니오| ShowKOWarning[한국어 파일 없음 경고]

    BuildJADF --> DisplayJATable[일본어 계층 테이블 표시]
    BuildKODF --> DisplayKOTable[한국어 계층 테이블 표시]
    ShowJAWarning --> CheckDownload
    ShowKOWarning --> CheckDownload
    DisplayJATable --> CheckDownload
    DisplayKOTable --> CheckDownload

    CheckDownload{링크가 존재하는가?}
    CheckDownload -->|아니오| End
    CheckDownload -->|예| ShowDownloadSection[HTML 다운로드 섹션 표시]

    ShowDownloadSection --> SelectLanguage[언어 선택 드롭다운<br/>Japanese/Korean]
    SelectLanguage --> UserSelect{사용자 언어 선택}

    UserSelect -->|일본어| GetHTMLRenderer[DIContainer에서<br/>HTMLTableRenderer 획득]
    UserSelect -->|한국어| GetHTMLRenderer

    GetHTMLRenderer --> LoadTemplate[TemplateLoader로<br/>HTML 템플릿 로드]
    LoadTemplate --> TemplateExists{사용자 정의<br/>템플릿 존재?}

    TemplateExists -->|예| UseCustom[사용자 템플릿 사용]
    TemplateExists -->|아니오| UseDefault[기본 템플릿 사용]

    UseCustom --> RenderHTML
    UseDefault --> RenderHTML[HTMLTableRenderer로<br/>HTML 렌더링]

    RenderHTML --> GenerateQuickLinks[QuickLinksGenerator로<br/>lm-en, lm-ko/ja, spac 링크 생성]
    GenerateQuickLinks --> CreateHTMLTable[계층적 HTML 테이블 생성<br/>체크박스, Quick Links 포함]

    CreateHTMLTable --> ShowDownloadBtn[다운로드 버튼 표시]
    ShowDownloadBtn --> UserDownload{사용자 다운로드<br/>클릭?}

    UserDownload -->|예| DownloadFile[HTML 파일 다운로드]
    UserDownload -->|아니오| ShowDownloadBtn

    DownloadFile --> End

    %% 스타일 정의
    style Start fill:#e1f5e1
    style End fill:#ffe1e1
    style CreateDI fill:#e3f2fd
    style GetZipProcessor fill:#e3f2fd
    style GetHTMLRenderer fill:#e3f2fd
    style ProcessZip fill:#e8f5e8
    style GenerateURL fill:#e8f5e8
    style RenderHTML fill:#e8f5e8
    style CreateTabs fill:#fff3e0
    style ShowDownloadSection fill:#fff3e0
    style ParallelDisplay fill:#f3e5f5
    style CheckFile fill:#fce4ec
    style LangFound fill:#fce4ec
    style CheckContent fill:#fce4ec
    style ValidateFile fill:#fce4ec
    style ValidateResult fill:#fce4ec
    style CheckDownload fill:#fce4ec
    style UserSelect fill:#fce4ec
```

## 주요 개선사항

### SOLID 원칙 적용된 처리 흐름

#### 1. Single Responsibility Principle (SRP)
- **Config**: 설정 관리만 담당
- **LanguageDetectorService**: 언어 감지만 담당
- **AEMURLGenerator**: URL 생성만 담당
- **ZipFileProcessor**: ZIP 파일 처리만 담당

#### 2. Open/Closed Principle (OCP)
- **URLGenerator 인터페이스**: 새로운 URL 생성 방식 추가 가능
- **TemplateRenderer 인터페이스**: 새로운 렌더링 방식 추가 가능
- **FileProcessor 프로토콜**: 새로운 파일 처리 방식 추가 가능

#### 3. Liskov Substitution Principle (LSP)
- 모든 구현체가 인터페이스를 통해 상호 교체 가능
- AEMURLGenerator ↔ 다른 URLGenerator 구현체

#### 4. Interface Segregation Principle (ISP)
- 클라이언트가 필요한 인터페이스만 의존
- LanguageDetector, DataFrameBuilder 등 특화된 프로토콜

#### 5. Dependency Inversion Principle (DIP)
- **DIContainer**를 통한 의존성 역전
- 고수준 모듈이 저수준 모듈에 직접 의존하지 않음
- 추상화(인터페이스)에 의존하는 구조

### 아키텍처 장점

#### 확장성
- 새로운 언어 지원: Config에 매핑만 추가
- 새로운 템플릿 엔진: TemplateRenderer 구현체 추가
- 새로운 파일 포맷: FileProcessor 구현체 추가

#### 테스트 용이성
- **TestDIContainer**를 통한 모의 객체 주입
- 각 서비스의 독립적 단위 테스트 가능
- 인터페이스 기반의 모의 객체 생성

#### 유지보수성
- 계층별 분리로 변경 영향 최소화
- 의존성 주입으로 느슨한 결합
- 타입 안전성으로 런타임 오류 감소