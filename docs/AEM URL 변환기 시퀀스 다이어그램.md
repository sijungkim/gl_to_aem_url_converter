---
title: "AEM URL 변환기 시퀀스 다이어그램"
description: "AEM URL Converter의 리팩토링된 SOLID 원칙 기반 아키텍처의 실행 흐름 시퀀스 다이어그램 - GlobalLink ZIP 처리부터 AEM MSM 링크 생성까지"
architect: "Sijung Kim"
authors: ["Sijung Kim", "Claude", "Gemini"]
reviewed_by: "Sijung Kim"
created_date: "2025-09-15"
last_modified: "2025-09-17"
version: "2.0.0"
document_type: "Sequence Diagram"
diagram_type: "Mermaid Sequence Diagram"
tags: ["Sequence Diagram", "Process Flow", "SOLID", "Architecture", "Mermaid"]
---

# AEM URL 변환기 시퀀스 다이어그램

리팩토링된 SOLID 원칙 기반 아키텍처의 실행 흐름

``` mermaid
sequenceDiagram
    autonumber

    actor User
    participant App as AEMConverterApp
    participant DI as DIContainer
    participant ZipProc as ZipFileProcessor
    participant LangDetector as LanguageDetectorService
    participant URLGen as AEMURLGenerator
    participant DFBuilder as HierarchicalDataFrameBuilder
    participant HTMLRenderer as HTMLTableRenderer
    participant TempLoader as TemplateLoader

    User->>App: main.py 실행
    App->>DI: DIContainer(config) 생성
    activate DI
    DI->>DI: 모든 서비스 인스턴스 준비 (지연 로딩)

    User->>App: Job ID 입력 (선택사항)
    User->>App: Submission Name 입력 (선택사항)
    User->>App: ZIP 파일 업로드
    activate App

    App->>App: "Processing ZIP file..." 스피너 표시
    App->>DI: zip_processor 요청
    DI->>ZipProc: 인스턴스 반환 (싱글톤)
    activate ZipProc

    App->>ZipProc: process(uploaded_file)
    ZipProc->>ZipProc: io.BytesIO(uploaded_file.getvalue())
    ZipProc->>ZipProc: zipfile.ZipFile() 열기
    ZipProc->>ZipProc: ProcessingResult 초기화

    rect rgb(240, 248, 255)
        note right of ZipProc: ZIP 파일 내 모든 파일 처리
        loop 각 full_path in zf.namelist()
            ZipProc->>LangDetector: detect(full_path)
            activate LangDetector
            LangDetector->>LangDetector: 경로에서 언어 코드 추출

            alt 'ko-KR' 발견
                LangDetector-->>ZipProc: 'ko' 반환
            else 'ja-JP' 발견
                LangDetector-->>ZipProc: 'ja' 반환
            else 언어 코드 없음
                LangDetector-->>ZipProc: None 반환
            end
            deactivate LangDetector

            opt 언어가 감지된 경우
                ZipProc->>ZipProc: file_name = os.path.basename(full_path)

                alt file_name이 "#content"로 시작
                    ZipProc->>URLGen: generate(file_name, target_lang)
                    activate URLGen

                    URLGen->>URLGen: create_aem_path(file_name, target_lang)
                    URLGen->>URLGen: 언어 경로 생성 및 변환

                    alt 파일명이 '#'로 시작하지 않음
                        URLGen-->>ZipProc: None 반환
                    else 파일명이 '#'로 시작
                        URLGen->>URLGen: AEM 경로 생성 (.xml을 .html로 변환)
                        URLGen->>URLGen: build_editor_url(path)
                        URLGen-->>ZipProc: (url, path) 튜플 반환
                    end
                    deactivate URLGen

                    opt URL이 None이 아닌 경우
                        ZipProc->>ZipProc: AEMLink 객체 생성
                        ZipProc->>ZipProc: LinkCollection에 추가
                    end
                end
            end
        end
    end

    ZipProc->>ZipProc: ProcessingResult 완료
    ZipProc-->>App: ProcessingResult 반환
    deactivate ZipProc

    App->>App: 결과 검증 (is_successful())
    App->>App: 성공 메시지 표시

    par 병렬 처리
        App->>App: 탭 생성 (Summary, Japanese, Korean)

        rect rgb(255, 245, 230)
            note left of App: 일본어 결과 표시
            opt 일본어 링크 존재
                App->>DI: df_builder 요청
                DI->>DFBuilder: 인스턴스 반환
                activate DFBuilder
                App->>DFBuilder: build(ja_links.to_dict())
                DFBuilder->>DFBuilder: 경로를 레벨별로 분할
                DFBuilder->>DFBuilder: 마지막 레벨을 마크다운 링크로 변환
                DFBuilder-->>App: DataFrame 반환
                deactivate DFBuilder
                App->>App: 일본어 DataFrame 표시
            else 일본어 링크 없음
                App->>App: "일본어 파일을 찾을 수 없습니다" 경고 표시
            end
        end

    and

        rect rgb(230, 245, 255)
            note right of App: 한국어 결과 표시
            opt 한국어 링크 존재
                App->>DFBuilder: build(ko_links.to_dict())
                activate DFBuilder
                DFBuilder->>DFBuilder: 경로를 레벨별로 분할
                DFBuilder->>DFBuilder: 마지막 레벨을 마크다운 링크로 변환
                DFBuilder-->>App: DataFrame 반환
                deactivate DFBuilder
                App->>App: 한국어 DataFrame 표시
            else 한국어 링크 없음
                App->>App: "한국어 파일을 찾을 수 없습니다" 경고 표시
            end
        end
    end

    opt 링크가 존재하는 경우
        App->>App: HTML 다운로드 섹션 표시
        User->>App: 언어 선택 (selectbox)

        alt 일본어 선택
            App->>DI: html_renderer 요청
            DI->>HTMLRenderer: 인스턴스 반환 (의존성과 함께)
            App->>HTMLRenderer: render(ja_links.to_dict(), "Japanese", ...)
        else 한국어 선택
            App->>HTMLRenderer: render(ko_links.to_dict(), "Korean", ...)
        end

        activate HTMLRenderer
        HTMLRenderer->>TempLoader: load_template()
        activate TempLoader
        TempLoader->>TempLoader: 템플릿 파일 존재 확인

        alt 사용자 정의 템플릿 존재
            TempLoader-->>HTMLRenderer: 사용자 템플릿 반환
        else 기본 템플릿 사용
            TempLoader-->>HTMLRenderer: 기본 템플릿 반환
        end
        deactivate TempLoader

        HTMLRenderer->>HTMLRenderer: HTML 헤더 생성 (체크박스, Quick Links, 레벨별 컬럼)
        HTMLRenderer->>HTMLRenderer: 각 행에 체크박스 추가
        HTMLRenderer->>HTMLRenderer: lm-en, lm-ko/ja, spac 링크 생성
        HTMLRenderer->>HTMLRenderer: 계층적 테이블 HTML 생성
        HTMLRenderer-->>App: HTML 문자열 반환
        deactivate HTMLRenderer

        App->>App: 다운로드 버튼 표시
        User->>App: 다운로드 버튼 클릭
        App-->>User: HTML 파일 다운로드
    end

    deactivate App
    deactivate DI

    note over User, TempLoader: 처리 완료 - SOLID 원칙 적용된 클린 아키텍처
```

## 주요 개선사항

### SOLID 원칙 적용
1. **SRP (Single Responsibility)**: 각 클래스가 단일 책임을 가짐
2. **OCP (Open/Closed)**: 인터페이스를 통한 확장 가능한 구조
3. **LSP (Liskov Substitution)**: 구현체들이 상호 교체 가능
4. **ISP (Interface Segregation)**: 클라이언트가 필요한 인터페이스만 의존
5. **DIP (Dependency Inversion)**: DIContainer를 통한 의존성 역전

### 아키텍처 개선
- **의존성 주입**: 중앙화된 의존성 관리
- **계층 분리**: Core, Services, Presentation 계층으로 분리
- **타입 안정성**: 강타입 도메인 모델 사용
- **오류 처리**: ProcessingResult를 통한 체계적 오류 관리