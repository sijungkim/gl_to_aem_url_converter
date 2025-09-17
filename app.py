"""
---
title: "Streamlit Application Layer"
description: "Main Streamlit application interface for processing GlobalLink translated ZIP files and generating AEM MSM editor URLs. Implements the presentation layer handling GlobalLink file uploads, content analysis, and AEM editor link generation for English language master, target languages, and SPAC content review workflow. Enhanced with multi-ZIP batch processing support."
architect: "Sijung Kim"
authors: ["Sijung Kim", "Claude", "Gemini"]
reviewed_by: "Sijung Kim"
created_date: "2025-09-15"
last_modified: "2025-09-18"
version: "2.1.0"
module_type: "Presentation Layer"
dependencies: ["streamlit", "typing", "core.models", "di_container"]
key_classes: ["AEMConverterApp"]
key_functions: ["run", "_process_and_display", "_display_results", "_display_download_section"]
design_patterns: ["MVC Pattern", "Observer Pattern", "Strategy Pattern"]
solid_principles: ["SRP - Single Responsibility Principle", "DIP - Dependency Inversion Principle"]
ui_components: ["file_uploader", "tabs", "dataframe", "download_button", "metrics"]
tags: ["streamlit", "ui", "presentation", "user-interface", "web-app", "multi-zip"]
---

app.py - Streamlit Application Layer

This module implements the presentation layer of the AEM URL Converter application
using Streamlit. It provides a clean, user-friendly web interface for uploading
GlobalLink translation files and viewing/downloading processed results.

Key Responsibilities:
- User interface rendering and interaction handling
- File upload processing and validation
- Results presentation in multiple formats (tables, summaries, tabs)
- HTML report generation and download functionality
- Error handling and user feedback display
- Progress indication during processing

Architecture:
The AEMConverterApp class follows the Single Responsibility Principle by focusing
solely on presentation concerns. It depends on the DIContainer for all business
logic services, implementing the Dependency Inversion Principle. The UI is
organized into logical sections with clear separation of concerns.

Key Features:
- Responsive multi-tab interface (Summary, Japanese, Korean)
- Interactive data tables with hierarchical organization
- Real-time processing feedback with spinners
- Downloadable HTML reports with custom templates
- Comprehensive error handling and validation
- Configurable settings display
- Language-specific result organization
- Multi-ZIP batch processing with deduplication
- Source file tracking for merged results

UI Components:
- File uploader for ZIP files
- Input fields for Job ID and Submission Name
- Multi-tab result display
- Interactive data tables
- Download buttons for HTML reports
- Status messages and progress indicators
- Metric cards for summary statistics

The module maintains clean separation between presentation logic and business
logic, making it easy to test and modify the UI without affecting core
functionality.
"""
import streamlit as st
from typing import List, Dict, Optional
from core.models import ProcessingResult, AEMLink
from di_container import DIContainer


class AEMConverterApp:
    """AEM URL Converter 애플리케이션
    
    Streamlit을 사용한 웹 애플리케이션 인터페이스.
    비즈니스 로직과 UI를 분리하여 관리.
    """
    
    def __init__(self, container: DIContainer):
        """애플리케이션 초기화
        
        Args:
            container: 의존성 주입 컨테이너
        """
        self.container = container
        self.config = container.config
    
    def run(self):
        """애플리케이션 메인 실행"""
        self._setup_page_config()
        self._render_header()
        
        # 입력 필드 렌더링
        job_id, submission_name = self._render_input_fields()
        
        # 파일 업로드
        uploaded_files = self._render_file_uploader()

        if uploaded_files:
            self._process_and_display_multiple(uploaded_files, job_id, submission_name)
    
    def _setup_page_config(self):
        """Streamlit 페이지 설정"""
        st.set_page_config(
            page_title="AEM URL Converter - Multi-ZIP",
            page_icon="🚀",
            layout="wide",
            initial_sidebar_state="collapsed"
        )
    
    def _render_header(self):
        """헤더 렌더링"""
        st.title("🚀 TPT GlobalLink AEM URL Converter")
        st.markdown(f"**AEM Host:** `{self.config.aem_host}`")
        st.markdown("📦 **Now supports multiple ZIP files!** Upload one or more GlobalLink ZIP files to process them together.")
        
        # 템플릿 파일 상태 표시
        if not self.container.template_loader.template_exists():
            st.info(
                "ℹ️ Using default HTML template. "
                "Create `template.html` for custom styling."
            )
    
    def _render_input_fields(self) -> tuple:
        """입력 필드 렌더링
        
        Returns:
            (job_id, submission_name) 튜플
        """
        col1, col2 = st.columns(2)
        
        with col1:
            job_id = st.text_input(
                "Job ID (Optional)",
                help="Enter the GlobalLink job ID for tracking"
            )
        
        with col2:
            submission_name = st.text_input(
                "Submission Name (Optional)",
                help="Enter the submission name for reference"
            )
        
        return job_id, submission_name
    
    def _render_file_uploader(self):
        """파일 업로더 렌더링

        Returns:
            업로드된 파일 리스트 또는 None
        """
        uploaded_files = st.file_uploader(
            "Upload GlobalLink ZIP file(s)",
            type="zip",
            accept_multiple_files=True,
            help="You can select multiple ZIP files to process them all at once"
        )

        if not uploaded_files:
            with st.expander("ℹ️ How to use"):
                st.markdown("""
                1. Download the translated ZIP file(s) from GlobalLink
                2. Upload one or more ZIP files using the file uploader above
                3. View the extracted and merged AEM URLs in the table
                4. Download the comprehensive HTML report for reference

                **Multi-ZIP Processing:**
                - Select multiple files at once for batch processing
                - Duplicate URLs are automatically removed (latest file wins)
                - Source file tracking shows which ZIP each URL came from
                """)

        return uploaded_files
    
    def _process_and_display_multiple(
        self,
        uploaded_files,
        job_id: str,
        submission_name: str
    ):
        """여러 파일 처리 및 결과 표시

        Args:
            uploaded_files: 업로드된 ZIP 파일 리스트
            job_id: Job ID
            submission_name: Submission 이름
        """
        # 파일 처리
        file_count = len(uploaded_files)
        with st.spinner(f"Processing {file_count} ZIP file{'s' if file_count > 1 else ''}..."):
            if hasattr(self.container, 'batch_processor'):
                # BatchProcessor가 있으면 사용
                result = self.container.batch_processor.process_multiple_zips(uploaded_files)
            else:
                # 단일 파일 처리 (하위 호환성)
                if file_count == 1:
                    result = self.container.zip_processor.process(uploaded_files[0])
                else:
                    st.error("❌ Multiple file processing requires BatchProcessor. Please update your configuration.")
                    return
        
        # 결과 검증
        if not result.is_successful():
            self._display_errors(result)
            return
        
        # 성공 메시지
        self._display_success_message(result, uploaded_files)
        
        # 경고 표시 (있는 경우)
        if result.warnings:
            self._display_warnings(result.warnings)
        
        # 결과 테이블 표시
        self._display_results(result.links.korean, result.links.japanese)
        
        # 다운로드 섹션
        if result.links.has_links():
            file_names = [f.name for f in uploaded_files]
            self._display_download_section(
                result.links.korean,
                result.links.japanese,
                file_names,
                job_id,
                submission_name
            )
    
    def _display_errors(self, result: ProcessingResult):
        """오류 표시
        
        Args:
            result: 처리 결과
        """
        st.error(f"❌ Processing failed with {result.error_count} errors")
        
        if result.warnings:
            for warning in result.warnings:
                st.warning(warning)
    
    def _display_success_message(self, result: ProcessingResult, uploaded_files):
        """성공 메시지 표시

        Args:
            result: 처리 결과
            uploaded_files: 업로드된 파일 리스트
        """
        total_links = result.links.get_total_count()
        ko_count = len(result.links.korean)
        ja_count = len(result.links.japanese)
        file_count = len(uploaded_files)

        st.success(
            f"✅ Processed {file_count} ZIP file{'s' if file_count > 1 else ''}."
        )
        st.info(
            f"📊 Found {ko_count} unique Korean and {ja_count} unique Japanese pages "
            f"(Total: {total_links} pages)"
        )

        # 처리된 파일 목록 표시
        if file_count > 1:
            with st.expander("📁 Processed Files", expanded=False):
                for i, file in enumerate(uploaded_files, 1):
                    st.write(f"{i}. {file.name}")
    
    def _display_warnings(self, warnings: List[str]):
        """경고 메시지 표시
        
        Args:
            warnings: 경고 메시지 리스트
        """
        with st.expander("⚠️ Warnings", expanded=False):
            for warning in warnings:
                st.warning(warning)
    
    def _display_results(
        self,
        ko_links: List[AEMLink],
        ja_links: List[AEMLink]
    ):
        """결과 테이블 표시
        
        Args:
            ko_links: 한국어 링크 리스트
            ja_links: 일본어 링크 리스트
        """
        # 탭으로 분리
        tab1, tab2, tab3 = st.tabs(["📊 Summary", "🇯🇵 Japanese", "🇰🇷 Korean"])
        
        with tab1:
            self._display_summary(ko_links, ja_links)
        
        with tab2:
            self._display_language_results("Japanese", ja_links)
        
        with tab3:
            self._display_language_results("Korean", ko_links)
    
    def _display_summary(
        self,
        ko_links: List[AEMLink],
        ja_links: List[AEMLink]
    ):
        """요약 정보 표시
        
        Args:
            ko_links: 한국어 링크 리스트
            ja_links: 일본어 링크 리스트
        """
        st.header("📊 Processing Summary")
        
        # 통계 카드
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Pages", len(ko_links) + len(ja_links))
        
        with col2:
            st.metric("Korean Pages", len(ko_links))
        
        with col3:
            st.metric("Japanese Pages", len(ja_links))
        
        # 요약 DataFrame
        summary_df = self.container.summary_df_builder.build_summary(
            ko_links, ja_links
        )
        st.dataframe(summary_df, hide_index=True, use_container_width=True)
    
    def _display_language_results(
        self,
        language_name: str,
        links: List[AEMLink]
    ):
        """언어별 결과 표시

        Args:
            language_name: 언어 이름
            links: AEMLink 리스트
        """
        st.header(f"{language_name} Pages ({len(links)})")

        if links:
            # AEMLink를 딕셔너리로 변환
            dict_links = [link.to_dict() for link in links]
            # source_zip 필드가 있는지 확인
            show_source = any('source_zip' in link for link in dict_links)
            df = self.container.df_builder.build(dict_links, show_source=show_source)

            st.dataframe(
                df,
                hide_index=True,
                use_container_width=True,
                height=400
            )
        else:
            st.warning(f"No {language_name} files found in the ZIP archive(s).")
    
    def _display_download_section(
        self,
        ko_links: List[AEMLink],
        ja_links: List[AEMLink],
        file_names: List[str],
        job_id: str,
        submission_name: str
    ):
        """다운로드 섹션 표시

        Args:
            ko_links: 한국어 링크 리스트
            ja_links: 일본어 링크 리스트
            file_names: 원본 파일명 리스트
            job_id: Job ID
            submission_name: Submission 이름
        """
        st.markdown("---")
        st.header("📥 Download HTML Report")
        
        # 다운로드 옵션
        options = []
        if ja_links:
            options.append(("Japanese", ja_links, 'ja'))
        if ko_links:
            options.append(("Korean", ko_links, 'ko'))
        
        if not options:
            return
        
        # 언어 선택
        col1, col2 = st.columns([1, 3])
        
        with col1:
            selected_idx = st.selectbox(
                "Select language:",
                range(len(options)),
                format_func=lambda x: options[x][0]
            )
        
        with col2:
            if selected_idx is not None:
                lang_name, links, lang_code = options[selected_idx]
                
                # 딕셔너리로 변환
                dict_links = [link.to_dict() for link in links]

                # HTML 생성
                html_data = self.container.html_renderer.render(
                    dict_links,
                    lang_name,
                    file_names,
                    job_id,
                    submission_name,
                    lang_code
                )

                # 파일명 생성
                file_suffix = 'jp' if lang_code == 'ja' else 'ko'
                if len(file_names) > 1:
                    from datetime import datetime
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M')
                    output_name = f"aem_links_combined_{len(file_names)}files_{file_suffix}_{timestamp}.html"
                else:
                    output_name = f"aem_links_{file_names[0].replace('.zip', '')}_{file_suffix}.html"
                
                # 다운로드 버튼
                st.download_button(
                    label=f"⬇️ Download {lang_name} Report",
                    data=html_data,
                    file_name=output_name,
                    mime="text/html",
                    use_container_width=True
                )