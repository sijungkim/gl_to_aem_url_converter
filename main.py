"""
main.py - 애플리케이션 진입점
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