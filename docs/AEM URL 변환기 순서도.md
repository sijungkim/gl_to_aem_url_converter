---
title: "AEM URL Converter Flowchart (Legacy Monolithic Implementation)"
description: "Flowchart showing the monolithic decision flow and processing logic for converting GlobalLink translated ZIP files to AEM editor URLs for MSM content review and updates."
architect: "Sijung Kim"
authors: ["Sijung Kim", "Claude", "Gemini"]
reviewed_by: "Sijung Kim"
created_date: "2025-09-15"
last_modified: "2025-09-17"
version: "1.0.0"
license: "MIT"
branch: "main (legacy production)"
architecture: "Monolithic"
tags: ["AEM", "GlobalLink", "Translation", "MSM", "Streamlit", "Production", "Mermaid", "Flowchart"]
dependencies: ["mermaid"]
diagram_type: "Flowchart"
purpose: "Visualize monolithic processing logic and decision flow"
scope: "Complete processing algorithm from file analysis to URL generation"
---

``` mermaid
graph TD
    Start[Start] --> InputFields[Display Job ID and<br/>Submission Name fields]
    InputFields --> Upload{Upload ZIP file}
    
    Upload -->|File selected| ProcessZip[Call process_zip_file]
    Upload -->|No file| Upload
    
    ProcessZip --> OpenZip[Open ZIP with BytesIO]
    OpenZip --> GetNamelist[Call zf.namelist]
    GetNamelist --> StartLoop[Start file iteration]
    
    StartLoop --> CheckPath{Path contains<br/>ko-KR or ja-JP?}
    CheckPath -->|ko-KR found| SetKorean[Set target_lang = ko]
    CheckPath -->|ja-JP found| SetJapanese[Set target_lang = ja]
    CheckPath -->|Not found| NextFile[Next file]
    
    SetKorean --> GetBasename[Call os.path.basename]
    SetJapanese --> GetBasename
    
    GetBasename --> CheckContent{Filename starts<br/>with #content?}
    CheckContent -->|No| NextFile
    CheckContent -->|Yes| GenerateURL[Call generate_aem_url]
    
    GenerateURL --> ReplaceLanguage[Replace SOURCE_LANG_PATH<br/>with target_lang_path]
    ReplaceLanguage --> CheckHash{Filename starts<br/>with hash?}
    CheckHash -->|No| ReturnNone[Return None]
    CheckHash -->|Yes| CreateAEMPath[Create AEM path<br/>Convert .xml to .html]
    
    CreateAEMPath --> BuildURL[Build URL:<br/>AEM_HOST + /editor.html/ + path]
    BuildURL --> ReturnURL[Return url and path]
    
    ReturnURL --> AddToDict[Add to links dict<br/>for target language]
    ReturnNone --> NextFile
    
    AddToDict --> NextFile
    NextFile --> MoreFiles{More files?}
    
    MoreFiles -->|Yes| CheckPath
    MoreFiles -->|No| ReturnLinks[Return ko_links, ja_links]
    
    ReturnLinks --> BuildDataFrame[Call build_hierarchical_df<br/>Create hierarchical DataFrame]
    BuildDataFrame --> DisplayColumns[Display in 2 columns:<br/>Japanese or Korean]
    
    DisplayColumns --> ShowDownload{Any links exist?}
    ShowDownload -->|Yes| GenerateHTML[Call generate_hierarchical_html_table<br/>Create HTML table]
    ShowDownload -->|No| ShowWarning[Show warning message]
    
    GenerateHTML --> DownloadButton[Provide HTML download button]
    ShowWarning --> End[End]
    DownloadButton --> End
    
    style Start fill:#e1f5e1
    style End fill:#ffe1e1
    style ProcessZip fill:#e3f2fd
    style GenerateURL fill:#e3f2fd
    style GenerateHTML fill:#e3f2fd
    style BuildDataFrame fill:#e3f2fd
    style DisplayColumns fill:#fff3e0
    style DownloadButton fill:#fff3e0
    style CheckPath fill:#fce4ec
    style CheckContent fill:#fce4ec
    style CheckHash fill:#fce4ec
    style ShowDownload fill:#fce4ec
    style MoreFiles fill:#fce4ec
```