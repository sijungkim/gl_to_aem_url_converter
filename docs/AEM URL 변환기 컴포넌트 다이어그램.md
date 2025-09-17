
``` mermaid
classDiagram
    direction TB
    
    class StreamlitApp {
        <<Main>>
        -AEM_HOST: string = "https://prod-author.illumina.com"
        -SOURCE_LANG_PATH: string = "language-master#en"
        +file_uploader() UploadedFile
        +text_input(label) string
        +columns(num) list
        +dataframe(df) void
        +download_button(label, data, filename) void
        +success(message) void
        +warning(message) void
    }
    
    class process_zip_file {
        <<Function>>
        +uploaded_file: BytesIO
        +returns: tuple[list, list]
        -extracts ko-KR and ja-JP files
        -filters #content files
    }
    
    class generate_aem_url {
        <<Function>>
        +file_name: string
        +target_lang: string  
        +returns: tuple[url, path]
        -replaces language codes
        -converts xml to html
        -builds editor URL
    }
    
    class build_hierarchical_df {
        <<Function>>
        +links: list[dict]
        +returns: DataFrame
        -splits paths into levels
        -creates markdown links
        -builds column structure
    }
    
    class generate_hierarchical_html_table {
        <<Function>>
        +links: list[dict]
        +language_name: string
        +source_zip_name: string
        +job_id: string
        +submission_name: string
        +lang_code: string
        +returns: string
        -creates HTML with checkboxes
        -adds Quick Links column
        -generates lm-en, lm-ko/ja, spac links
    }
    
    class Link {
        <<Dictionary>>
        +url: string
        +path: string
    }
    
    class DataFrame {
        <<pandas.DataFrame>>
        +Level 2: string
        +Level 3: string
        +Level N: string
        +contains markdown links
    }
    
    StreamlitApp --> process_zip_file : calls on upload
    process_zip_file --> generate_aem_url : iteratively calls
    generate_aem_url --> Link : creates
    process_zip_file --> Link : aggregates by language
    StreamlitApp --> build_hierarchical_df : calls for display
    build_hierarchical_df --> DataFrame : creates
    StreamlitApp --> generate_hierarchical_html_table : calls for download
    StreamlitApp --> DataFrame : displays in columns
    
    note for StreamlitApp "주요 설정값:\n- AEM 호스트 URL\n- 소스 언어 경로\n- Job ID/Submission Name 입력"
    note for generate_hierarchical_html_table "HTML 특징:\n- 체크박스 컬럼\n- Quick Links (lm-en, lm-ko/ja, spac)\n- 계층적 테이블 구조"
```