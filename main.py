"""
---
title: "AEM URL Converter - Docker Application"
description: "Single-file Docker application for processing GlobalLink translated ZIP files and generating AEM MSM editor URLs. Combines configuration loading, dependency injection, and Streamlit UI in one streamlined entry point for containerized deployment."
architect: "Sijung Kim"
authors: ["Sijung Kim", "Claude", "Gemini"]
reviewed_by: "Sijung Kim"
created_date: "2025-09-15"
last_modified: "2025-09-18"
version: "2.1.0"
module_type: "Docker Application Entry Point"
dependencies: ["streamlit", "typing", "pathlib", "os", "sys"]
key_classes: ["AEMConverterApp"]
key_functions: ["main", "load_config", "run", "_process_and_display_multiple"]
design_patterns: ["MVC Pattern", "Dependency Injection", "Factory Pattern"]
solid_principles: ["SRP - Single Responsibility Principle", "DIP - Dependency Inversion Principle"]
ui_components: ["file_uploader", "tabs", "dataframe", "download_button", "metrics"]
tags: ["docker", "streamlit", "entry-point", "ui", "multi-zip", "container"]
---

main.py - Docker Application Entry Point

This module serves as the complete Docker application entry point, combining
configuration management, dependency injection, and Streamlit UI in a single
file optimized for containerized deployment.

Key Responsibilities:
- Application configuration from environment variables
- Dependency injection container setup
- Complete Streamlit web interface
- File upload processing and validation
- Multi-ZIP batch processing with deduplication
- Results presentation and HTML report generation
- Error handling and user feedback

Docker Optimization:
This consolidated approach reduces the container footprint and simplifies
deployment by combining the minimal entry point logic with the UI layer,
perfect for the Docker-only deployment strategy.

Architecture Benefits:
- Single entry point for Docker containers
- Streamlined file structure for minimal image size
- Combined configuration and UI logic
- Maintains SOLID principles through dependency injection
- Clean separation of business logic via service layer
"""
import sys
import os
import streamlit as st
from pathlib import Path
from typing import List, Dict, Optional

# 프로젝트 루트를 Python 경로에 추가
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

from core.config import Config
from core.models import ProcessingResult, AEMLink
from di_container import DIContainer


def load_config() -> Config:
    """설정 로드

    환경 변수나 설정 파일에서 설정을 로드.

    Returns:
        Config 객체
    """
    # 환경 변수에서 설정 로드 (있는 경우)
    aem_host = os.getenv("AEM_HOST", "https://prod-author.illumina.com")
    source_lang = os.getenv("SOURCE_LANG", "en")
    template_file = os.getenv("TEMPLATE_FILE", "template.html")

    # Config 객체 생성
    config = Config(
        aem_host=aem_host,
        source_lang=source_lang,
        template_file=template_file
    )

    return config


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

        if uploaded_files:
            # 파일 정보 표시
            if len(uploaded_files) == 1:
                st.success(f"📁 Uploaded: {uploaded_files[0].name}")
            else:
                st.success(f"📁 Uploaded {len(uploaded_files)} files:")
                for i, file in enumerate(uploaded_files, 1):
                    st.write(f"   {i}. {file.name}")

        return uploaded_files

    def _process_and_display_multiple(self, uploaded_files: List, job_id: str, submission_name: str):
        """다중 파일 처리 및 결과 표시

        Args:
            uploaded_files: 업로드된 파일 리스트
            job_id: Job ID (선택사항)
            submission_name: Submission 이름 (선택사항)
        """
        # 처리 시작 메시지
        processing_message = f"Processing {len(uploaded_files)} file(s)..."

        with st.spinner(processing_message):
            # 배치 처리 실행
            if len(uploaded_files) == 1:
                # 단일 파일 처리
                source_name = uploaded_files[0].name
                result = self.container.zip_processor.process(uploaded_files[0], source_name)
                source_names = source_name
            else:
                # 다중 파일 처리
                result = self.container.batch_processor.process_multiple_zips(uploaded_files)
                source_names = [f.name for f in uploaded_files]

        # 결과 표시
        self._display_results(result, source_names, job_id, submission_name)

    def _display_results(self, result: ProcessingResult, source_names, job_id: str, submission_name: str):
        """처리 결과 표시

        Args:
            result: 처리 결과 객체
            source_names: 소스 파일명 (리스트 또는 문자열)
            job_id: Job ID
            submission_name: Submission 이름
        """
        # 결과 요약 표시
        self._display_summary(result, source_names)

        # 경고 메시지 표시
        if result.warnings:
            with st.expander("⚠️ Processing Warnings", expanded=False):
                for warning in result.warnings:
                    st.warning(warning)

        # 결과가 있는 경우에만 탭 표시
        if result.links.korean or result.links.japanese:
            self._display_tabs(result, source_names, job_id, submission_name)
        else:
            st.error("No valid content files found in the uploaded ZIP(s).")

    def _display_summary(self, result: ProcessingResult, source_names):
        """요약 정보 표시

        Args:
            result: 처리 결과
            source_names: 소스 파일명들
        """
        # 파일 정보 표시
        if isinstance(source_names, list) and len(source_names) > 1:
            st.subheader(f"📊 Processing Summary ({len(source_names)} files)")
        else:
            source_display = source_names[0] if isinstance(source_names, list) else source_names
            st.subheader(f"📊 Processing Summary: {source_display}")

        # 메트릭 표시
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Total Processed", result.processed_count)

        with col2:
            st.metric("Korean Pages", len(result.links.korean))

        with col3:
            st.metric("Japanese Pages", len(result.links.japanese))

        with col4:
            st.metric("Errors", result.error_count)

    def _display_tabs(self, result: ProcessingResult, source_names, job_id: str, submission_name: str):
        """결과 탭 표시

        Args:
            result: 처리 결과
            source_names: 소스 파일명들
            job_id: Job ID
            submission_name: Submission 이름
        """
        # 요약 DataFrame 생성
        summary_df = self.container.summary_df_builder.build_summary(
            result.links.korean,
            result.links.japanese
        )

        # 탭 생성
        tab1, tab2, tab3 = st.tabs(["📊 Summary", "🇯🇵 Japanese", "🇰🇷 Korean"])

        with tab1:
            st.subheader("📊 Summary")
            st.dataframe(summary_df, use_container_width=True)

            # 소스 파일 정보 표시
            if isinstance(source_names, list) and len(source_names) > 1:
                st.subheader("📁 Source Files")
                for i, name in enumerate(source_names, 1):
                    st.write(f"{i}. {name}")

        with tab2:
            self._display_language_results(
                result.links.japanese,
                "Japanese",
                "ja",
                source_names,
                job_id,
                submission_name
            )

        with tab3:
            self._display_language_results(
                result.links.korean,
                "Korean",
                "ko",
                source_names,
                job_id,
                submission_name
            )

    def _display_language_results(self, links: List[AEMLink], language_name: str, lang_code: str,
                                  source_names, job_id: str, submission_name: str):
        """언어별 결과 표시

        Args:
            links: AEM 링크 리스트
            language_name: 언어 이름
            lang_code: 언어 코드
            source_names: 소스 파일명들
            job_id: Job ID
            submission_name: Submission 이름
        """
        if not links:
            st.info(f"No {language_name} content found.")
            return

        st.subheader(f"🔗 {language_name} AEM Links ({len(links)} pages)")

        # DataFrame 생성
        link_dicts = [link.to_dict() for link in links]
        show_source = isinstance(source_names, list) and len(source_names) > 1
        df = self.container.df_builder.build(link_dicts, show_source=show_source)

        if not df.empty:
            st.dataframe(df, use_container_width=True)

            # 다운로드 섹션
            self._display_download_section(
                link_dicts, language_name, lang_code,
                source_names, job_id, submission_name
            )
        else:
            st.warning(f"No {language_name} links to display.")

    def _display_download_section(self, links: List[Dict], language_name: str, lang_code: str,
                                  source_names, job_id: str, submission_name: str):
        """다운로드 섹션 표시

        Args:
            links: 링크 딕셔너리 리스트
            language_name: 언어 이름
            lang_code: 언어 코드
            source_names: 소스 파일명들
            job_id: Job ID
            submission_name: Submission 이름
        """
        if not links:
            return

        st.subheader(f"📥 Download {language_name} Report")

        # HTML 생성
        html_content = self.container.html_renderer.render(
            links, language_name, source_names,
            job_id, submission_name, lang_code
        )

        # 파일명 생성
        if isinstance(source_names, list) and len(source_names) > 1:
            filename = f"aem_links_{lang_code}_multi_files.html"
        else:
            source_name = source_names[0] if isinstance(source_names, list) else source_names
            clean_name = source_name.replace('.zip', '').replace(' ', '_')
            filename = f"aem_links_{lang_code}_{clean_name}.html"

        # 다운로드 버튼
        st.download_button(
            label=f"📥 Download {language_name} HTML Report",
            data=html_content,
            file_name=filename,
            mime="text/html",
            help=f"Download an HTML report with {len(links)} {language_name} AEM links"
        )


def main():
    """메인 실행 함수"""
    try:
        # 설정 로드
        config = load_config()

        # DI 컨테이너 생성
        container = DIContainer(config)

        # 애플리케이션 생성 및 실행
        app = AEMConverterApp(container)
        app.run()

    except Exception as e:
        st.error(f"Application error: {str(e)}")
        st.stop()


if __name__ == "__main__":
    main()