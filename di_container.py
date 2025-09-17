"""
di_container.py - 의존성 주입 컨테이너
"""
from core.config import Config
from services.language import LanguageDetectorService, LanguagePathManager
from services.url_generator import AEMURLGenerator, URLValidator
from services.file_processor import ZipFileProcessor, FileFilter, BatchProcessor
from presentation.df_builder import HierarchicalDataFrameBuilder, SummaryDataFrameBuilder
from presentation.html_renderer import QuickLinksGenerator, HTMLTableRenderer
from presentation.template_loader import TemplateLoader, AdvancedTemplateLoader


class DIContainer:
    """의존성 주입 컨테이너 (DIP 구현)
    
    애플리케이션의 모든 의존성을 중앙에서 관리.
    객체 생성과 의존성 주입을 담당.
    """
    
    def __init__(self, config: Config = None):
        """컨테이너 초기화
        
        Args:
            config: 애플리케이션 설정 (없으면 기본값 사용)
        """
        # 설정 초기화
        self.config = config or Config()
        
        # 서비스 초기화 (지연 로딩을 위해 None으로 시작)
        self._language_detector = None
        self._language_path_manager = None
        self._url_generator = None
        self._url_validator = None
        self._zip_processor = None
        self._file_filter = None
        self._batch_processor = None
        self._df_builder = None
        self._summary_df_builder = None
        self._quick_links_generator = None
        self._html_renderer = None
        self._template_loader = None
    
    # --- Core Services ---
    
    @property
    def language_detector(self) -> LanguageDetectorService:
        """언어 감지 서비스 (싱글톤)"""
        if self._language_detector is None:
            self._language_detector = LanguageDetectorService(self.config)
        return self._language_detector
    
    @property
    def language_path_manager(self) -> LanguagePathManager:
        """언어 경로 관리자 (싱글톤)"""
        if self._language_path_manager is None:
            self._language_path_manager = LanguagePathManager(self.config)
        return self._language_path_manager
    
    @property
    def url_generator(self) -> AEMURLGenerator:
        """URL 생성기 (싱글톤)"""
        if self._url_generator is None:
            self._url_generator = AEMURLGenerator(self.config)
        return self._url_generator
    
    @property
    def url_validator(self) -> URLValidator:
        """URL 검증기 (싱글톤)"""
        if self._url_validator is None:
            self._url_validator = URLValidator(self.config)
        return self._url_validator
    
    # --- File Processing Services ---
    
    @property
    def zip_processor(self) -> ZipFileProcessor:
        """ZIP 파일 프로세서 (싱글톤)"""
        if self._zip_processor is None:
            self._zip_processor = ZipFileProcessor(
                self.language_detector,
                self.url_generator
            )
        return self._zip_processor
    
    @property
    def file_filter(self) -> FileFilter:
        """파일 필터 (싱글톤)"""
        if self._file_filter is None:
            self._file_filter = FileFilter()
        return self._file_filter
    
    @property
    def batch_processor(self) -> BatchProcessor:
        """배치 프로세서 (싱글톤)"""
        if self._batch_processor is None:
            self._batch_processor = BatchProcessor(self.zip_processor)
        return self._batch_processor
    
    # --- Presentation Services ---
    
    @property
    def df_builder(self) -> HierarchicalDataFrameBuilder:
        """DataFrame 빌더 (싱글톤)"""
        if self._df_builder is None:
            self._df_builder = HierarchicalDataFrameBuilder()
        return self._df_builder
    
    @property
    def summary_df_builder(self) -> SummaryDataFrameBuilder:
        """요약 DataFrame 빌더 (싱글톤)"""
        if self._summary_df_builder is None:
            self._summary_df_builder = SummaryDataFrameBuilder()
        return self._summary_df_builder
    
    @property
    def quick_links_generator(self) -> QuickLinksGenerator:
        """Quick Links 생성기 (싱글톤)"""
        if self._quick_links_generator is None:
            self._quick_links_generator = QuickLinksGenerator(
                self.language_path_manager
            )
        return self._quick_links_generator
    
    @property
    def html_renderer(self) -> HTMLTableRenderer:
        """HTML 렌더러 (싱글톤)"""
        if self._html_renderer is None:
            self._html_renderer = HTMLTableRenderer(
                self.quick_links_generator,
                self.template_loader
            )
        return self._html_renderer
    
    @property
    def template_loader(self) -> TemplateLoader:
        """템플릿 로더 (싱글톤)"""
        if self._template_loader is None:
            self._template_loader = TemplateLoader(self.config.template_file)
        return self._template_loader
    
    # --- Factory Methods ---
    
    def create_advanced_template_loader(self, template_dir: str = "templates") -> AdvancedTemplateLoader:
        """고급 템플릿 로더 생성 (팩토리 메서드)
        
        Args:
            template_dir: 템플릿 디렉토리
            
        Returns:
            새로운 AdvancedTemplateLoader 인스턴스
        """
        return AdvancedTemplateLoader(
            self.config.template_file,
            template_dir
        )
    
    def reset(self):
        """모든 서비스 인스턴스 초기화
        
        테스트나 설정 변경 시 사용.
        """
        self._language_detector = None
        self._language_path_manager = None
        self._url_generator = None
        self._url_validator = None
        self._zip_processor = None
        self._file_filter = None
        self._batch_processor = None
        self._df_builder = None
        self._summary_df_builder = None
        self._quick_links_generator = None
        self._html_renderer = None
        self._template_loader = None


class TestDIContainer(DIContainer):
    """테스트용 DI 컨테이너
    
    테스트 환경을 위한 설정과 모의 객체 제공.
    """
    
    def __init__(self):
        """테스트 컨테이너 초기화"""
        test_config = Config(
            aem_host="https://test.example.com",
            source_lang="en",
            template_file="test_template.html"
        )
        super().__init__(test_config)
    
    def inject_mock(self, service_name: str, mock_object):
        """모의 객체 주입
        
        Args:
            service_name: 서비스 이름
            mock_object: 주입할 모의 객체
        """
        setattr(self, f"_{service_name}", mock_object)