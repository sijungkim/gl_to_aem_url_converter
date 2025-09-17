
---
title: "AEM URL 변환기 컴포넌트 다이어그램"
description: "AEM URL Converter의 리팩토링된 SOLID 원칙 기반 아키텍처 컴포넌트 다이어그램 - GlobalLink ZIP 파일 처리를 통한 AEM MSM 워크플로우 지원"
architect: "Sijung Kim"
authors: ["Sijung Kim", "Claude", "Gemini"]
reviewed_by: "Sijung Kim"
created_date: "2025-09-15"
last_modified: "2025-09-17"
version: "2.0.0"
document_type: "Component Diagram"
diagram_type: "Mermaid Class Diagram"
tags: ["Component Diagram", "Class Diagram", "SOLID", "Architecture", "Mermaid"]
---

# AEM URL 변환기 컴포넌트 다이어그램

리팩토링된 SOLID 원칙 기반 아키텍처

``` mermaid
classDiagram
    direction TB

    %% Core Layer
    class Config {
        <<Dataclass>>
        +aem_host: string
        +source_lang: string
        +template_file: string
        +language_mapping: Dict[str, str]
        +spac_paths: Dict[str, str]
        +get_supported_languages() list
        +get_spac_path(lang_code) string
    }

    class AEMLink {
        <<Domain Model>>
        +url: string
        +path: string
        +language: string
        +get_path_parts() List[str]
        +get_page_name() string
        +to_dict() Dict[str, str]
    }

    class LinkCollection {
        <<Domain Model>>
        +korean: List[AEMLink]
        +japanese: List[AEMLink]
        +get_total_count() int
        +get_by_language(lang_code) List[AEMLink]
        +has_links() bool
    }

    class ProcessingResult {
        <<Domain Model>>
        +links: LinkCollection
        +processed_count: int
        +error_count: int
        +warnings: List[str]
        +add_warning(message) void
        +is_successful() bool
    }

    %% Service Layer
    class LanguageDetectorService {
        <<Service>>
        +config: Config
        +detect(path) Optional[str]
        +is_supported_language(lang_code) bool
    }

    class AEMURLGenerator {
        <<Service>>
        +config: Config
        +generate(file_name, target_lang) Optional[Tuple[str, str]]
        +build_editor_url(path) string
        +create_aem_path(file_name, target_lang) string
    }

    class ZipFileProcessor {
        <<Service>>
        +language_detector: LanguageDetectorService
        +url_generator: AEMURLGenerator
        +process(uploaded_file) ProcessingResult
        +extract_language_files(zip_file) Dict[str, List[str]]
    }

    %% Presentation Layer
    class HierarchicalDataFrameBuilder {
        <<Presentation>>
        +build(links) DataFrame
        +create_hierarchical_structure(links) DataFrame
        +format_markdown_links(links) List[str]
    }

    class HTMLTableRenderer {
        <<Presentation>>
        +quick_links_generator: QuickLinksGenerator
        +template_loader: TemplateLoader
        +render(links, language_name, ...) string
        +generate_table_html(links) string
    }

    class TemplateLoader {
        <<Presentation>>
        +template_file: string
        +load_template() string
        +template_exists() bool
        +get_default_template() string
    }

    %% Application Layer
    class AEMConverterApp {
        <<Application>>
        +container: DIContainer
        +config: Config
        +run() void
        +_process_and_display(file, job_id, name) void
        +_display_results(ko_links, ja_links) void
    }

    class DIContainer {
        <<DI Container>>
        +config: Config
        +language_detector: LanguageDetectorService
        +url_generator: AEMURLGenerator
        +zip_processor: ZipFileProcessor
        +df_builder: HierarchicalDataFrameBuilder
        +html_renderer: HTMLTableRenderer
        +template_loader: TemplateLoader
        +reset() void
    }

    %% Interfaces
    class URLGenerator {
        <<Interface>>
        +generate(file_name, target_lang) Optional[Tuple[str, str]]
    }

    class FileProcessor {
        <<Protocol>>
        +process(file_path) Optional[AEMLink]
    }

    class TemplateRenderer {
        <<Interface>>
        +render(links, **kwargs) string
    }

    %% Relationships
    DIContainer --> Config : creates
    DIContainer --> LanguageDetectorService : manages
    DIContainer --> AEMURLGenerator : manages
    DIContainer --> ZipFileProcessor : manages
    DIContainer --> HierarchicalDataFrameBuilder : manages
    DIContainer --> HTMLTableRenderer : manages
    DIContainer --> TemplateLoader : manages

    AEMConverterApp --> DIContainer : uses

    ZipFileProcessor --> LanguageDetectorService : uses
    ZipFileProcessor --> AEMURLGenerator : uses
    ZipFileProcessor --> ProcessingResult : creates
    ZipFileProcessor --> LinkCollection : creates
    ZipFileProcessor --> AEMLink : creates

    LanguageDetectorService --> Config : uses
    AEMURLGenerator --> Config : uses
    TemplateLoader --> Config : uses

    HTMLTableRenderer --> TemplateLoader : uses

    ProcessingResult --> LinkCollection : contains
    LinkCollection --> AEMLink : contains

    AEMURLGenerator ..|> URLGenerator : implements
    HTMLTableRenderer ..|> TemplateRenderer : implements

    %% Notes
    note for Config "SOLID: SRP\n설정 관리만 담당"
    note for DIContainer "SOLID: DIP\n의존성 역전을 통한\n느슨한 결합"
    note for URLGenerator "SOLID: OCP\n확장 가능한 인터페이스"
    note for AEMLink "SOLID: SRP\n링크 데이터만 관리"
```