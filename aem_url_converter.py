"""
---
title: "AEM URL Converter - Monolithic Application"
description: "Legacy monolithic Streamlit application for processing GlobalLink translated ZIP files and generating AEM editor URLs for MSM (Multi-Site Manager) content review and updates across English, target languages, and SPAC target languages."
architect: "Sijung Kim"
authors: ["Sijung Kim", "Claude", "Gemini"]
reviewed_by: "Sijung Kim"
created_date: "2025-09-15"
last_modified: "2025-09-17"
version: "1.0.0"
license: "MIT"
branch: "main (legacy production)"
architecture: "Monolithic"
file_type: "Main Application"
framework: "Streamlit"
language: "Python 3.8+"
dependencies: ["streamlit", "pandas", "zipfile", "io", "os", "datetime", "typing"]
purpose: "Process GlobalLink translation packages and provide AEM MSM editor URLs"
workflow: "ZIP upload → Language detection → URL generation → MSM report creation"
features: ["GlobalLink ZIP processing", "AEM URL generation", "MSM workflow support", "Multi-language support (Korean/Japanese)", "HTML report export", "SPAC integration"]
tags: ["AEM", "GlobalLink", "Translation", "MSM", "Streamlit", "Production", "Monolithic"]
constants:
  - "AEM_HOST: Production AEM author host URL"
  - "SOURCE_LANG_PATH: English language master path"
  - "TEMPLATE_FILE: HTML template file name"
functions:
  - "load_template(): Load HTML template with fallback"
  - "generate_aem_url(): Transform file paths to AEM editor URLs"
  - "process_zip_file(): Extract and process GlobalLink ZIP contents"
  - "build_hierarchical_df(): Create hierarchical DataFrames for display"
  - "generate_html_table(): Generate downloadable HTML reports with MSM links"
ui_components:
  - "File uploader for GlobalLink ZIP files"
  - "Optional Job ID and Submission Name inputs"
  - "Split-view results display (Korean/Japanese)"
  - "Interactive HTML report generation"
  - "Download buttons for MSM workflow reports"
msm_features:
  - "English language master links (lm-en)"
  - "Target language content links (lm-ko/ja)"
  - "SPAC target language links (spac-ko/ja)"
  - "Hierarchical content structure navigation"
---
"""

import streamlit as st
import zipfile
import io
import os
import pandas as pd
from datetime import datetime
from typing import Tuple, List, Dict, Optional

# --- 설정 ---
AEM_HOST = "https://prod-author.illumina.com"
SOURCE_LANG_PATH = "language-master#en"
TEMPLATE_FILE = "template.html"

# --- 함수들 ---

def load_template() -> str:
    """HTML 템플릿을 파일에서 로드하거나 기본 템플릿 사용.
    
    Returns:
        str: HTML 템플릿 문자열
    """
    try:
        with open(TEMPLATE_FILE, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        # 파일이 없을 때 사용할 간단한 기본 템플릿
        return """<!DOCTYPE html>
<html><head><meta charset="UTF-8"><title>{title}</title>
<style>
    body {{ font-family: Arial, sans-serif; margin: 2em; }}
    table {{ width: 100%; border-collapse: collapse; }}
    th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
    th {{ background: #f2f2f2; }}
    a {{ color: #d63324; text-decoration: none; }}
</style></head><body>
<h1>{title}</h1>
<div>{source_info}</div>
<table><thead><tr>{headers}</tr></thead><tbody>{table_rows}</tbody></table>
</body></html>"""

def generate_aem_url(file_name: str, target_lang: str) -> Optional[Tuple[str, str]]:
    """파일명과 대상 언어로 AEM URL 생성.
    
    Args:
        file_name: 원본 파일명 (#content로 시작)
        target_lang: 대상 언어 코드 ('ko' 또는 'ja')
    
    Returns:
        튜플 (URL, 경로) 또는 None
    """
    target_lang_path = f"language-master#{target_lang}"
    
    # 소스 언어 경로가 없으면 처리 불가
    if SOURCE_LANG_PATH not in file_name: 
        return None
    
    # 언어 경로 교체
    target_file_name = file_name.replace(SOURCE_LANG_PATH, target_lang_path)
    
    # #으로 시작하지 않으면 유효하지 않음
    if not target_file_name.startswith('#'): 
        return None
    
    # AEM 경로로 변환 (# 제거, # -> /)
    aem_path = target_file_name[1:].replace('#', '/')
    
    # XML을 HTML로 변환
    if aem_path.endswith('.xml'):
        aem_path = aem_path[:-4] + '.html'
    else:
        return None
    
    final_url = f"{AEM_HOST}/editor.html/{aem_path}"
    return final_url, aem_path

def process_zip_file(uploaded_file) -> Tuple[List[Dict[str, str]], List[Dict[str, str]]]:
    """ZIP 파일을 처리하고 언어별 AEM URL 추출.
    
    Args:
        uploaded_file: Streamlit의 UploadedFile 객체
    
    Returns:
        튜플 (한국어 링크 리스트, 일본어 링크 리스트)
    """
    links = {'ko': [], 'ja': []}
    
    with zipfile.ZipFile(io.BytesIO(uploaded_file.getvalue())) as zf:
        for full_path in zf.namelist():
            # 언어 감지
            target_lang = None
            if 'ko-KR' in full_path: 
                target_lang = 'ko'
            elif 'ja-JP' in full_path: 
                target_lang = 'ja'
            
            if target_lang:
                file_name = os.path.basename(full_path)
                # #content로 시작하는 파일만 처리
                if file_name.startswith("#content"):
                    result = generate_aem_url(file_name, target_lang)
                    if result:
                        url, path = result
                        links[target_lang].append({"url": url, "path": path})
    
    return links['ko'], links['ja']

def build_hierarchical_df(links: List[Dict[str, str]]) -> pd.DataFrame:
    """링크 리스트를 계층적 데이터프레임으로 변환.
    
    Args:
        links: URL과 경로를 포함한 딕셔너리 리스트
    
    Returns:
        계층적 구조의 DataFrame
    """
    if not links:
        return pd.DataFrame()
    
    # 경로를 레벨별로 분할 (content 레벨 제외)
    paths = []
    for link in links:
        path_parts = link['path'].strip('/').replace('.html', '').split('/')[1:]
        paths.append(path_parts)
    
    max_depth = max(len(p) for p in paths) if paths else 0
    
    # 테이블 데이터 구성
    table_data = []
    for i, path_parts in enumerate(paths):
        row = {}
        for j in range(max_depth):
            col_name = f"Level {j+2}"
            if j < len(path_parts) - 1:
                # 중간 레벨들
                row[col_name] = path_parts[j]
            elif j == len(path_parts) - 1:
                # 마지막 레벨: 마크다운 링크로 생성
                page_name = path_parts[j]
                url = links[i]['url']
                row[col_name] = f"[{page_name}]({url})"
            else:
                # 빈 셀
                row[col_name] = ""
        table_data.append(row)
    
    return pd.DataFrame(table_data)

def generate_html_table(
    links: List[Dict[str, str]], 
    language_name: str, 
    source_name: str, 
    job_id: str, 
    submission_name: str, 
    lang_code: str
) -> str:
    """링크 리스트를 HTML 테이블로 변환.
    
    Args:
        links: URL과 경로를 포함한 딕셔너리 리스트
        language_name: 언어 이름 ('Korean' 또는 'Japanese')
        source_name: 소스 ZIP 파일명
        job_id: Job ID (선택사항)
        submission_name: Submission 이름 (선택사항)
        lang_code: 언어 코드 ('ko' 또는 'ja')
    
    Returns:
        완성된 HTML 문자열
    """
    if not links:
        return f"<h1>AEM {language_name} Links (0)</h1><p>No links to display.</p>"
    
    # 경로 처리
    paths = []
    for link in links:
        path_parts = link['path'].strip('/').replace('.html', '').split('/')[1:]
        paths.append(path_parts)
    
    max_depth = max(len(p) for p in paths) if paths else 0
    
    # 헤더 생성
    headers = "<th>Check</th><th>Quick Links</th>"
    headers += "".join([f"<th>Level {i+2}</th>" for i in range(max_depth)])
    
    # 테이블 행 생성
    table_rows = ""
    for i, path_parts in enumerate(paths):
        # 체크박스 컬럼
        row = '<tr><td><input type="checkbox"></td>'
        
        # Quick Links 컬럼
        url = links[i]['url']
        lm_path = f'/language-master/{lang_code}/'
        en_url = url.replace(lm_path, '/language-master/en/')
        spac_path = '/spac/ko_KR/' if lang_code == 'ko' else '/spac/ja_JP/'
        spac_url = url.replace(lm_path, spac_path)
        
        row += f'<td><a href="{en_url}">lm-en</a> | '
        row += f'<a href="{url}">lm-{lang_code}</a> | '
        row += f'<a href="{spac_url}">spac-{lang_code}</a></td>'
        
        # 경로 레벨들
        for j in range(max_depth):
            if j < len(path_parts) - 1:
                row += f"<td>{path_parts[j]}</td>"
            elif j == len(path_parts) - 1:
                row += f'<td><a href="{url}">{path_parts[j]}</a></td>'
            else:
                row += "<td></td>"
        row += "</tr>"
        table_rows += row
    
    # 소스 정보 생성
    if job_id and submission_name:
        source_info = f"<p>Job ID: {job_id} | Submission: {submission_name}</p>"
        title = f"AEM {language_name} Links - {submission_name}"
    else:
        source_info = f"<p>Source: {source_name}</p>"
        title = f"AEM {language_name} Links - {source_name}"
    
    # 템플릿 렌더링
    template = load_template()
    
    # 고급 템플릿 사용 가능 여부 확인
    if 'language_name' in template:
        # 고급 템플릿 변수들
        return template.format(
            language_name=language_name,
            title_source=source_name,
            source_info=source_info,
            total_links=len(links),
            level_headers="".join([f"<th>Level {i+2}</th>" for i in range(max_depth)]),
            table_rows=table_rows,
            headers=headers,
            generation_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )
    else:
        # 기본 템플릿 변수들
        return template.format(
            title=title,
            source_info=source_info,
            headers=headers,
            table_rows=table_rows
        )

# --- Streamlit UI ---
st.set_page_config(page_title="AEM URL Converter", layout="wide")
st.title("🚀 TPT GlobalLink AEM URL Converter")
st.markdown(f"**AEM Host:** `{AEM_HOST}`")

# 입력 필드
col1, col2 = st.columns(2)
with col1:
    job_id = st.text_input("Job ID (Optional)")
with col2:
    submission_name = st.text_input("Submission Name (Optional)")

# 파일 업로드
uploaded_file = st.file_uploader("Upload GlobalLink ZIP file", type="zip")

if uploaded_file:
    # 파일 처리
    with st.spinner("Processing..."):
        ko_links, ja_links = process_zip_file(uploaded_file)
    
    st.success(f"✅ Found {len(ko_links)} Korean and {len(ja_links)} Japanese pages")
    
    # 결과 표시
    col1, col2 = st.columns(2)
    with col1:
        st.header(f"🇯🇵 Japanese ({len(ja_links)})")
        if ja_links:
            df_ja = build_hierarchical_df(ja_links)
            st.dataframe(df_ja, hide_index=True, use_container_width=True)
        else:
            st.warning("No Japanese files found")
    
    with col2:
        st.header(f"🇰🇷 Korean ({len(ko_links)})")
        if ko_links:
            df_ko = build_hierarchical_df(ko_links)
            st.dataframe(df_ko, hide_index=True, use_container_width=True)
        else:
            st.warning("No Korean files found")
    
    # 다운로드 섹션
    if ko_links or ja_links:
        st.markdown("---")
        st.header("📥 Download HTML Report")
        
        # 다운로드 옵션 구성
        options = []
        if ja_links: 
            options.append(("Japanese", ja_links, 'ja'))
        if ko_links: 
            options.append(("Korean", ko_links, 'ko'))
        
        if options:
            # 언어 선택
            selected = st.radio(
                "Select language:", 
                [opt[0] for opt in options], 
                horizontal=True
            )
            
            # 선택된 언어에 대한 HTML 생성 및 다운로드
            for lang_name, links, lang_code in options:
                if lang_name == selected:
                    html_data = generate_html_table(
                        links, lang_name, uploaded_file.name,
                        job_id, submission_name, lang_code
                    )
                    
                    # 파일명 생성
                    file_suffix = 'jp' if lang_code == 'ja' else 'ko'
                    file_name = f"aem_links_{uploaded_file.name.replace('.zip','')}_{file_suffix}.html"
                    
                    st.download_button(
                        f"Download {lang_name} Report",
                        html_data, 
                        file_name, 
                        "text/html"
                    )