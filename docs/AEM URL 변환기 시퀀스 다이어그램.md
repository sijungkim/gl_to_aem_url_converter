---
title: "AEM URL Converter Sequence Diagram (Legacy Monolithic Implementation)"
description: "Sequence diagram showing the monolithic workflow for processing GlobalLink translated ZIP files and generating AEM editor URLs for MSM content review across English, target languages, and SPAC target languages."
architect: "Sijung Kim"
authors: ["Sijung Kim", "Claude", "Gemini"]
reviewed_by: "Sijung Kim"
created_date: "2025-09-15"
last_modified: "2025-09-17"
version: "1.0.0"
license: "MIT"
branch: "main (legacy production)"
architecture: "Monolithic"
tags: ["AEM", "GlobalLink", "Translation", "MSM", "Streamlit", "Production", "Mermaid", "Sequence Diagram"]
dependencies: ["mermaid"]
diagram_type: "Sequence Diagram"
purpose: "Visualize monolithic execution flow and function interactions"
scope: "End-to-end workflow from ZIP upload to HTML report generation"
---

``` mermaid
sequenceDiagram
    autonumber
    
    actor User
    participant UI as Streamlit UI
    participant PZF as process_zip_file()
    participant GAU as generate_aem_url()
    participant BHD as build_hierarchical_df()
    participant GHT as generate_hierarchical_html_table()
    
    User->>UI: Input Job ID (Optional)
    User->>UI: Input Submission Name (Optional)
    User->>UI: Upload ZIP file
    activate UI
    
    UI->>UI: Show "Analyzing ZIP file..." spinner
    UI->>PZF: process_zip_file(uploaded_file)
    activate PZF
    
    PZF->>PZF: io.BytesIO(uploaded_file.getvalue())
    PZF->>PZF: Open zipfile.ZipFile()
    PZF->>PZF: Initialize links = {'ko': [], 'ja': []}
    
    rect rgb(240, 248, 255)
        note right of PZF: Process all files in ZIP
        loop for each full_path in zf.namelist()
            PZF->>PZF: Analyze path
            
            alt 'ko-KR' in full_path
                PZF->>PZF: target_lang = 'ko'
            else 'ja-JP' in full_path
                PZF->>PZF: target_lang = 'ja'
            else no language code
                PZF->>PZF: Skip to next file
            end
            
            opt target_lang is set
                PZF->>PZF: file_name = os.path.basename(full_path)
                
                alt file_name.startswith("#content")
                    PZF->>GAU: generate_aem_url(file_name, target_lang)
                    activate GAU
                    
                    GAU->>GAU: Create target_lang_path
                    GAU->>GAU: Replace SOURCE_LANG_PATH with target_lang_path
                    
                    alt filename does not start with '#'
                        GAU-->>PZF: Return None
                    else filename starts with '#'
                        GAU->>GAU: Create aem_path (remove #, .xml to .html)
                        GAU->>GAU: final_url = AEM_HOST + "/editor.html/" + aem_path
                        GAU-->>PZF: Return (final_url, aem_path)
                    end
                    
                    deactivate GAU
                    
                    opt URL is not None
                        PZF->>PZF: links[target_lang].append({"url": url, "path": path})
                    end
                end
            end
        end
    end
    
    PZF-->>UI: Return (ko_links, ja_links)
    deactivate PZF
    
    UI->>UI: Display "URL conversion complete!" success
    
    par Parallel Processing
        UI->>UI: Create 2 columns
        
        rect rgb(255, 245, 230)
            note left of UI: Display Japanese Results
            alt ja_links exists
                UI->>BHD: build_hierarchical_df(ja_links)
                activate BHD
                BHD->>BHD: Split paths by levels
                BHD->>BHD: Convert last level to Markdown links
                BHD-->>UI: Return DataFrame
                deactivate BHD
                UI->>UI: Display Japanese DataFrame
            else no ja_links
                UI->>UI: Show "Could not find Japanese files" warning
            end
        end
        
    and
        
        rect rgb(230, 245, 255)
            note right of UI: Display Korean Results
            alt ko_links exists
                UI->>BHD: build_hierarchical_df(ko_links)
                activate BHD
                BHD->>BHD: Split paths by levels
                BHD->>BHD: Convert last level to Markdown links
                BHD-->>UI: Return DataFrame
                deactivate BHD
                UI->>UI: Display Korean DataFrame
            else no ko_links
                UI->>UI: Show "Could not find Korean files" warning
            end
        end
    end
    
    opt Links exist
        UI->>UI: Show HTML download section
        User->>UI: Select language (Radio button)
        
        alt Japanese selected
            UI->>GHT: generate_hierarchical_html_table(ja_links, "Japanese", ...)
        else Korean selected
            UI->>GHT: generate_hierarchical_html_table(ko_links, "Korean", ...)
        end
        
        activate GHT
        GHT->>GHT: Create HTML headers (Check, Quick Links, Level 2+)
        GHT->>GHT: Add checkbox to each row
        GHT->>GHT: Generate lm-en, lm-ko/ja, spac links
        GHT->>GHT: Generate hierarchical table HTML
        GHT-->>UI: Return HTML string
        deactivate GHT
        
        UI->>UI: Show download button
        User->>UI: Click download button
        UI-->>User: Download HTML file
    end
    
    deactivate UI
    
    note over User, GHT: Process Complete
```