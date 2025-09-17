"""
services/file_processor.py - ZIP 파일 처리 서비스
"""
import zipfile
import io
import os
from typing import Optional, List
from core.models import AEMLink, LinkCollection, ProcessingResult
from core.interfaces import URLGenerator
from services.language import LanguageDetectorService


class ZipFileProcessor:
    """ZIP 파일 처리 서비스 (SRP - ZIP 처리만 담당)
    
    ZIP 파일을 열고 내용을 처리하는 역할만 수행.
    """
    
    def __init__(
        self,
        language_detector: LanguageDetectorService,
        url_generator: URLGenerator
    ):
        """ZIP 프로세서 초기화
        
        Args:
            language_detector: 언어 감지 서비스
            url_generator: URL 생성기
        """
        self.language_detector = language_detector
        self.url_generator = url_generator
    
    def process(self, uploaded_file) -> ProcessingResult:
        """ZIP 파일 처리 및 링크 추출
        
        Args:
            uploaded_file: Streamlit UploadedFile 객체
            
        Returns:
            처리 결과 객체
        """
        links = {'ko': [], 'ja': []}
        processed_count = 0
        error_count = 0
        warnings = []
        
        try:
            with zipfile.ZipFile(io.BytesIO(uploaded_file.getvalue())) as zf:
                file_list = zf.namelist()
                
                for full_path in file_list:
                    processed_count += 1
                    
                    try:
                        link = self._process_single_file(full_path)
                        if link:
                            links[link.language].append(link)
                    except Exception as e:
                        error_count += 1
                        warnings.append(f"Error processing {full_path}: {str(e)}")
        
        except zipfile.BadZipFile:
            error_count += 1
            warnings.append("Invalid ZIP file format")
        except Exception as e:
            error_count += 1
            warnings.append(f"Unexpected error: {str(e)}")
        
        # LinkCollection 생성
        link_collection = LinkCollection(
            korean=links['ko'],
            japanese=links['ja']
        )
        
        # ProcessingResult 생성
        result = ProcessingResult(
            links=link_collection,
            processed_count=processed_count,
            error_count=error_count,
            warnings=warnings
        )
        
        return result
    
    def _process_single_file(self, full_path: str) -> Optional[AEMLink]:
        """단일 파일 처리 (SRP)
        
        Args:
            full_path: ZIP 내 파일 경로
            
        Returns:
            AEMLink 객체 또는 None
        """
        # 언어 감지
        target_lang = self.language_detector.detect(full_path)
        if not target_lang:
            return None
        
        # 파일명 확인
        file_name = os.path.basename(full_path)
        if not self._is_content_file(file_name):
            return None
        
        # URL 생성
        result = self.url_generator.generate(file_name, target_lang)
        if result:
            url, path = result
            return AEMLink(url=url, path=path, language=target_lang)
        
        return None
    
    def _is_content_file(self, file_name: str) -> bool:
        """콘텐츠 파일인지 확인
        
        Args:
            file_name: 파일명
            
        Returns:
            #content로 시작하면 True
        """
        return file_name.startswith("#content")


class FileFilter:
    """파일 필터링 서비스 (SRP)
    
    처리할 파일을 필터링하는 역할만 수행.
    """
    
    def __init__(self):
        """필터 초기화"""
        self.content_prefix = "#content"
        self.excluded_patterns = [
            '__MACOSX',
            '.DS_Store',
            'Thumbs.db'
        ]
    
    def should_process(self, file_path: str) -> bool:
        """파일 처리 여부 결정
        
        Args:
            file_path: 파일 경로
            
        Returns:
            처리해야 할 파일이면 True
        """
        # 제외 패턴 확인
        for pattern in self.excluded_patterns:
            if pattern in file_path:
                return False
        
        # 파일명 추출
        file_name = os.path.basename(file_path)
        
        # 콘텐츠 파일인지 확인
        if not file_name.startswith(self.content_prefix):
            return False
        
        # XML 파일인지 확인
        if not file_name.endswith('.xml'):
            return False
        
        return True
    
    def filter_file_list(self, file_list: List[str]) -> List[str]:
        """파일 리스트 필터링
        
        Args:
            file_list: 전체 파일 리스트
            
        Returns:
            처리할 파일 리스트
        """
        return [f for f in file_list if self.should_process(f)]


class BatchProcessor:
    """배치 처리 서비스 (OCP)
    
    여러 파일을 일괄 처리하는 서비스.
    새로운 처리 방식 추가 시 확장 가능.
    """
    
    def __init__(self, file_processor: ZipFileProcessor):
        """배치 프로세서 초기화
        
        Args:
            file_processor: 파일 처리 서비스
        """
        self.file_processor = file_processor
    
    def process_multiple_zips(self, zip_files: List) -> List[ProcessingResult]:
        """여러 ZIP 파일 일괄 처리
        
        Args:
            zip_files: ZIP 파일 리스트
            
        Returns:
            처리 결과 리스트
        """
        results = []
        
        for zip_file in zip_files:
            result = self.file_processor.process(zip_file)
            results.append(result)
        
        return results
    
    def merge_results(self, results: List[ProcessingResult]) -> ProcessingResult:
        """여러 처리 결과 병합
        
        Args:
            results: 처리 결과 리스트
            
        Returns:
            병합된 처리 결과
        """
        all_korean = []
        all_japanese = []
        total_processed = 0
        total_errors = 0
        all_warnings = []
        
        for result in results:
            all_korean.extend(result.links.korean)
            all_japanese.extend(result.links.japanese)
            total_processed += result.processed_count
            total_errors += result.error_count
            all_warnings.extend(result.warnings)
        
        merged_links = LinkCollection(
            korean=all_korean,
            japanese=all_japanese
        )
        
        return ProcessingResult(
            links=merged_links,
            processed_count=total_processed,
            error_count=total_errors,
            warnings=all_warnings
        )