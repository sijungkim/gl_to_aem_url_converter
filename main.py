"""
---
title: "Main Application Entry Point"
description: "Primary entry point for the AEM URL Converter application that processes GlobalLink translated ZIP files. Handles configuration loading, dependency injection setup, and application initialization to generate AEM MSM editor URLs for English language master, target languages, and SPAC content review. Enhanced with multi-ZIP batch processing support."
architect: "Sijung Kim"
authors: ["Sijung Kim", "Claude", "Gemini"]
reviewed_by: "Sijung Kim"
created_date: "2025-09-15"
last_modified: "2025-09-18"
version: "2.1.0"
module_type: "Application Entry Point"
dependencies: ["streamlit", "pathlib", "os", "sys"]
key_classes: ["None - functional module"]
key_functions: ["main", "load_config"]
design_patterns: ["Dependency Injection", "Factory Pattern"]
solid_principles: ["DIP - Dependency Inversion Principle"]
tags: ["entry-point", "configuration", "dependency-injection", "streamlit"]
---

main.py - Application Entry Point

This module serves as the primary entry point for the AEM URL Converter application.
It is responsible for:
- Loading application configuration from environment variables or defaults
- Setting up the dependency injection container with all required services
- Initializing and running the Streamlit application
- Handling top-level application errors and providing user feedback

The module follows the Dependency Inversion Principle by depending on abstractions
(Config, DIContainer) rather than concrete implementations, making it easy to test
and modify without affecting the core business logic.

Key Features:
- Environment-based configuration loading
- Centralized dependency injection setup
- Clean error handling with user-friendly messages
- Python path management for proper module imports
- Streamlit application lifecycle management

Architecture:
This module sits at the top of the application hierarchy and orchestrates
the initialization of all lower-level components through the DIContainer,
ensuring proper separation of concerns and adherence to SOLID principles.
"""
import sys
import os
from pathlib import Path

# 프로젝트 루트를 Python 경로에 추가
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

from core.config import Config
from di_container import DIContainer
from app import AEMConverterApp


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
        import streamlit as st
        st.error(f"Application error: {str(e)}")
        st.stop()


if __name__ == "__main__":
    main()