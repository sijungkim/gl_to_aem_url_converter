"""
---
title: "ZIP File Processing Services"
description: "Service layer components for processing GlobalLink translated ZIP archives downloaded from translation management system. Implements batch file processing, filtering, and AEM MSM editor link extraction for English language master, target languages, and SPAC content review workflow with comprehensive error handling. Enhanced with multi-ZIP support for batch processing with deduplication."
architect: "Sijung Kim"
authors: ["Sijung Kim", "Claude", "Gemini"]
reviewed_by: "Sijung Kim"
created_date: "2025-09-15"
last_modified: "2025-09-18"
version: "2.1.0"
module_type: "Service Layer"
dependencies: ["zipfile", "io", "os", "typing", "core.models", "services.language", "services.url_generator"]
key_classes: ["ZipFileProcessor", "FileFilter", "BatchProcessor"]
key_functions: ["process", "extract_language_files", "filter_content_files", "process_batch"]
design_patterns: ["Strategy Pattern", "Chain of Responsibility", "Observer Pattern"]
solid_principles: ["SRP - Single Responsibility Principle", "DIP - Dependency Inversion Principle"]
features: ["ZIP Processing", "File Filtering", "Batch Operations", "Error Handling", "Progress Tracking", "Multi-ZIP Support", "Deduplication"]
tags: ["file-processing", "zip-extraction", "batch-processing", "services", "multi-zip"]
---

services/file_processor.py - ZIP File Processing Services

This module provides comprehensive ZIP file processing capabilities for
GlobalLink translation archives. It implements the core business logic for
extracting, filtering, and processing files to generate AEM links with
robust error handling and progress tracking.

Key Responsibilities:
- Process GlobalLink ZIP archives and extract relevant files
- Filter files based on content type and language criteria
- Generate AEM links from processed files using language detection and URL generation
- Handle processing errors and provide detailed feedback
- Track processing progress and statistics
- Manage batch operations for multiple files

Service Classes:

1. ZipFileProcessor:
   Main processing service that orchestrates the entire ZIP file processing
   workflow from extraction to AEM link generation.

2. FileFilter:
   Specialized service for filtering relevant files from ZIP archives
   based on content criteria and file patterns.

3. BatchProcessor:
   Service for handling batch processing operations with progress tracking
   and error accumulation across multiple files.

Processing Workflow:
1. Extract ZIP archive to memory buffer
2. Enumerate all files in archive
3. Filter files based on content criteria (#content prefix)
4. Detect language for each relevant file
5. Generate AEM URLs using URL generation service
6. Collect results into ProcessingResult with error tracking
7. Provide comprehensive processing statistics and warnings

The module demonstrates dependency inversion by depending on language
detection and URL generation abstractions rather than concrete implementations.
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
    
    def process(self, uploaded_file, source_name: str = None) -> ProcessingResult:
        """ZIP 파일 처리 및 링크 추출

        Args:
            uploaded_file: Streamlit UploadedFile 객체
            source_name: 소스 ZIP 파일명 (optional)

        Returns:
            처리 결과 객체
        """
        links = {'ko': [], 'ja': []}
        processed_count = 0
        error_count = 0
        warnings = []
        zip_name = source_name or getattr(uploaded_file, 'name', 'unknown.zip')
        
        try:
            with zipfile.ZipFile(io.BytesIO(uploaded_file.getvalue())) as zf:
                file_list = zf.namelist()
                
                for full_path in file_list:
                    processed_count += 1
                    
                    try:
                        link = self._process_single_file(full_path, zip_name)
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
    
    def _process_single_file(self, full_path: str, source_zip: str = None) -> Optional[AEMLink]:
        """단일 파일 처리 (SRP)

        Args:
            full_path: ZIP 내 파일 경로
            source_zip: 소스 ZIP 파일명

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
            return AEMLink(url=url, path=path, language=target_lang, source_zip=source_zip)
        
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
    
    def process_multiple_zips(self, zip_files: List) -> ProcessingResult:
        """여러 ZIP 파일 일괄 처리 및 병합

        Args:
            zip_files: ZIP 파일 리스트

        Returns:
            병합된 처리 결과
        """
        results = []

        for zip_file in zip_files:
            source_name = getattr(zip_file, 'name', f'file_{len(results)+1}.zip')
            result = self.file_processor.process(zip_file, source_name)
            results.append(result)

        # 결과 병합 및 중복 제거
        return self.merge_and_deduplicate_results(results)
    
    def merge_and_deduplicate_results(self, results: List[ProcessingResult]) -> ProcessingResult:
        """여러 처리 결과 병합 및 중복 제거

        Args:
            results: 처리 결과 리스트

        Returns:
            병합된 및 중복 제거된 처리 결과
        """
        all_korean = []
        all_japanese = []
        total_processed = 0
        total_errors = 0
        all_warnings = []

        # 모든 결과 수집
        for result in results:
            all_korean.extend(result.links.korean)
            all_japanese.extend(result.links.japanese)
            total_processed += result.processed_count
            total_errors += result.error_count
            all_warnings.extend(result.warnings)

        # 경로 기준 중복 제거 (나중 파일 우선)
        korean_dedup = self._deduplicate_links(all_korean)
        japanese_dedup = self._deduplicate_links(all_japanese)

        # 경로 기준 정렬
        korean_dedup.sort(key=lambda x: x.path)
        japanese_dedup.sort(key=lambda x: x.path)

        merged_links = LinkCollection(
            korean=korean_dedup,
            japanese=japanese_dedup
        )

        # 중복 제거 경고 추가
        ko_removed = len(all_korean) - len(korean_dedup)
        ja_removed = len(all_japanese) - len(japanese_dedup)
        if ko_removed > 0 or ja_removed > 0:
            all_warnings.append(
                f"Removed {ko_removed + ja_removed} duplicate links "
                f"(Korean: {ko_removed}, Japanese: {ja_removed})"
            )

        return ProcessingResult(
            links=merged_links,
            processed_count=total_processed,
            error_count=total_errors,
            warnings=all_warnings
        )

    def _deduplicate_links(self, links: List[AEMLink]) -> List[AEMLink]:
        """링크 중복 제거 (경로 기준, 나중 파일 우선)

        Args:
            links: AEMLink 리스트

        Returns:
            중복 제거된 링크 리스트
        """
        seen_paths = {}
        for link in links:
            seen_paths[link.path] = link  # 나중 파일이 이전 파일을 덮어쓰기
        return list(seen_paths.values())