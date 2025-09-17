---
title: "AEM URL Converter - 프로젝트 구조"
description: "AEM URL Converter의 리팩토링된 SOLID 원칙 기반 프로젝트 구조 문서 - GlobalLink 번역 ZIP 파일을 처리하여 AEM MSM 콘텐츠 검토 및 업데이트를 위한 에디터 URL 생성"
architect: "Sijung Kim"
authors: ["Sijung Kim", "Claude", "Gemini"]
reviewed_by: "Sijung Kim"
created_date: "2025-09-15"
last_modified: "2025-09-17"
version: "2.0.0"
document_type: "Architecture Documentation"
tags: ["Project Structure", "SOLID", "Clean Architecture", "Documentation"]
---

# AEM URL Converter - 프로젝트 구조

```
gl_to_aem_url_converter/
├── core/                    # 핵심 비즈니스 로직 레이어
│   ├── __init__.py
│   ├── config.py           # 애플리케이션 설정 관리 (Config 클래스)
│   ├── models.py           # 도메인 모델 (AEMLink, LinkCollection, ProcessingResult)
│   └── interfaces.py       # 추상 인터페이스 및 프로토콜 정의
│
├── services/               # 비즈니스 서비스 레이어
│   ├── __init__.py
│   ├── language.py         # 언어 감지 및 경로 관리 (LanguageDetectorService, LanguagePathManager)
│   ├── url_generator.py    # AEM URL 생성 및 검증 (AEMURLGenerator, URLValidator)
│   └── file_processor.py   # ZIP 파일 처리 (ZipFileProcessor, FileFilter, BatchProcessor)
│
├── presentation/           # 프레젠테이션 레이어
│   ├── __init__.py
│   ├── html_renderer.py    # HTML 렌더링 (QuickLinksGenerator, HTMLTableRenderer)
│   ├── df_builder.py       # DataFrame 구성 (HierarchicalDataFrameBuilder, SummaryDataFrameBuilder)
│   └── template_loader.py  # 템플릿 관리 (TemplateLoader, AdvancedTemplateLoader)
│
├── docs/                   # 프로젝트 문서
│   ├── AEM URL Converter - 프로젝트 구조.md
│   ├── AEM URL 변환기 컴포넌트 다이어그램.md
│   ├── AEM URL 변환기 시퀀스 다이어그램.md
│   └── AEM URL 변환기 순서도.md
│
├── di_container.py         # 의존성 주입 컨테이너 (DIContainer, TestDIContainer)
├── app.py                  # Streamlit 애플리케이션 레이어 (AEMConverterApp)
├── main.py                 # 애플리케이션 진입점
├── template.html           # HTML 템플릿 (선택사항)
├── requirements.txt        # Python 의존성 패키지
├── README.md              # 프로젝트 개요 및 사용법
└── .gitignore             # Git 제외 파일
```

## 각 디렉토리 역할

### **core/** - 핵심 비즈니스 로직
- **config.py**: 애플리케이션 전역 설정 관리 (AEM 호스트, 언어 매핑 등)
- **models.py**: 도메인 모델 정의 (AEMLink, LinkCollection, ProcessingResult)
- **interfaces.py**: 추상 인터페이스와 프로토콜 (URLGenerator, FileProcessor, TemplateRenderer)
- 외부 의존성이 없는 순수한 비즈니스 규칙과 데이터 구조

### **services/** - 비즈니스 서비스
- **language.py**: 언어 감지 및 경로 관리 서비스
- **url_generator.py**: AEM URL 생성 및 유효성 검증
- **file_processor.py**: ZIP 파일 처리 및 배치 작업
- 핵심 비즈니스 로직의 구체적인 구현

### **presentation/** - 프레젠테이션 계층
- **df_builder.py**: DataFrame 구성 (계층적 구조, 요약 정보)
- **html_renderer.py**: HTML 렌더링 및 Quick Links 생성
- **template_loader.py**: HTML 템플릿 로드 및 관리
- 사용자 인터페이스와 데이터 표현 담당

### **docs/** - 프로젝트 문서
- 프로젝트 구조, 컴포넌트 다이어그램, 시퀀스 다이어그램, 순서도
- Mermaid 다이어그램을 통한 시각적 문서화

### **루트 디렉토리**
- **di_container.py**: 의존성 주입 컨테이너 (싱글톤 패턴)
- **app.py**: Streamlit 웹 애플리케이션 인터페이스
- **main.py**: 애플리케이션 진입점 및 설정 로드
- **requirements.txt**: Python 패키지 의존성 관리

## SOLID 원칙 적용

### Single Responsibility Principle (SRP)
- 각 클래스와 모듈이 하나의 책임만 가짐
- Config는 설정만, AEMLink는 링크 데이터만 담당

### Open/Closed Principle (OCP)
- 인터페이스를 통한 확장 가능한 구조
- 새로운 URL 생성기나 템플릿 렌더러 추가 가능

### Liskov Substitution Principle (LSP)
- 추상 인터페이스의 구현체들이 상호 교체 가능
- URLGenerator 인터페이스의 모든 구현체가 동일하게 동작

### Interface Segregation Principle (ISP)
- 클라이언트가 필요한 인터페이스만 의존
- FileProcessor, TemplateRenderer 등 특화된 인터페이스

### Dependency Inversion Principle (DIP)
- 고수준 모듈이 저수준 모듈에 의존하지 않음
- DIContainer를 통한 의존성 주입으로 구현