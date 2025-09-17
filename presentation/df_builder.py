"""
presentation/df_builder.py - DataFrame 생성 서비스
"""
import pandas as pd
from typing import List, Dict, Optional
from core.models import AEMLink


class HierarchicalDataFrameBuilder:
    """계층적 DataFrame 생성 서비스 (SRP - DataFrame 생성만 담당)
    
    링크 리스트를 계층적 구조의 DataFrame으로 변환.
    """
    
    def __init__(self):
        """DataFrame 빌더 초기화"""
        self.level_prefix = "Level"
        self.start_level = 2  # Level 2부터 시작
    
    def build(self, links: List[Dict[str, str]]) -> pd.DataFrame:
        """링크 리스트를 계층적 DataFrame으로 변환
        
        Args:
            links: URL과 경로를 포함한 딕셔너리 리스트
            
        Returns:
            계층적 구조의 pandas DataFrame
        """
        if not links:
            return pd.DataFrame()
        
        # 경로 추출 및 처리
        paths = self._extract_paths(links)
        max_depth = self._get_max_depth(paths)
        
        # 테이블 데이터 구성
        table_data = self._build_table_data(links, paths, max_depth)
        
        return pd.DataFrame(table_data)
    
    def build_from_aem_links(self, aem_links: List[AEMLink]) -> pd.DataFrame:
        """AEMLink 객체 리스트를 DataFrame으로 변환
        
        Args:
            aem_links: AEMLink 객체 리스트
            
        Returns:
            계층적 구조의 pandas DataFrame
        """
        # AEMLink를 딕셔너리로 변환
        links = [link.to_dict() for link in aem_links]
        return self.build(links)
    
    def _extract_paths(self, links: List[Dict[str, str]]) -> List[List[str]]:
        """링크에서 경로 추출 및 분할
        
        Args:
            links: 링크 딕셔너리 리스트
            
        Returns:
            분할된 경로 리스트
        """
        paths = []
        for link in links:
            # /content/... 에서 content 제외하고 분할
            path_parts = link['path'].strip('/').replace('.html', '').split('/')[1:]
            paths.append(path_parts)
        return paths
    
    def _get_max_depth(self, paths: List[List[str]]) -> int:
        """최대 경로 깊이 계산
        
        Args:
            paths: 분할된 경로 리스트
            
        Returns:
            최대 깊이
        """
        return max(len(p) for p in paths) if paths else 0
    
    def _build_table_data(
        self,
        links: List[Dict[str, str]],
        paths: List[List[str]],
        max_depth: int
    ) -> List[Dict[str, str]]:
        """테이블 데이터 구성
        
        Args:
            links: 링크 딕셔너리 리스트
            paths: 분할된 경로 리스트
            max_depth: 최대 깊이
            
        Returns:
            테이블 행 데이터 리스트
        """
        table_data = []
        
        for i, path_parts in enumerate(paths):
            row = self._build_row(path_parts, links[i]['url'], max_depth)
            table_data.append(row)
        
        return table_data
    
    def _build_row(
        self,
        path_parts: List[str],
        url: str,
        max_depth: int
    ) -> Dict[str, str]:
        """단일 행 데이터 구성
        
        Args:
            path_parts: 경로 구성 요소
            url: 링크 URL
            max_depth: 최대 깊이
            
        Returns:
            행 데이터 딕셔너리
        """
        row = {}
        
        for j in range(max_depth):
            col_name = f"{self.level_prefix} {j + self.start_level}"
            
            if j < len(path_parts) - 1:
                # 중간 레벨: 경로 구성 요소
                row[col_name] = path_parts[j]
            elif j == len(path_parts) - 1:
                # 마지막 레벨: 마크다운 링크
                page_name = path_parts[j]
                row[col_name] = f"[{page_name}]({url})"
            else:
                # 빈 셀
                row[col_name] = ""
        
        return row


class SummaryDataFrameBuilder:
    """요약 DataFrame 생성 서비스 (OCP - 확장 가능)
    
    링크 컬렉션의 요약 정보를 DataFrame으로 생성.
    """
    
    def build_summary(self, korean_links: List, japanese_links: List) -> pd.DataFrame:
        """요약 정보 DataFrame 생성
        
        Args:
            korean_links: 한국어 링크 리스트
            japanese_links: 일본어 링크 리스트
            
        Returns:
            요약 정보 DataFrame
        """
        summary_data = {
            'Language': ['Korean', 'Japanese', 'Total'],
            'Page Count': [
                len(korean_links),
                len(japanese_links),
                len(korean_links) + len(japanese_links)
            ]
        }
        
        return pd.DataFrame(summary_data)
    
    def build_detailed_summary(
        self,
        korean_links: List[AEMLink],
        japanese_links: List[AEMLink]
    ) -> pd.DataFrame:
        """상세 요약 정보 DataFrame 생성
        
        Args:
            korean_links: 한국어 AEMLink 리스트
            japanese_links: 일본어 AEMLink 리스트
            
        Returns:
            상세 요약 정보 DataFrame
        """
        # 경로별 통계 수집
        ko_paths = self._collect_path_stats(korean_links)
        ja_paths = self._collect_path_stats(japanese_links)
        
        summary_data = []
        
        # 한국어 통계
        for path, count in ko_paths.items():
            summary_data.append({
                'Language': 'Korean',
                'Section': path,
                'Count': count
            })
        
        # 일본어 통계
        for path, count in ja_paths.items():
            summary_data.append({
                'Language': 'Japanese',
                'Section': path,
                'Count': count
            })
        
        return pd.DataFrame(summary_data)
    
    def _collect_path_stats(self, links: List[AEMLink]) -> Dict[str, int]:
        """경로별 통계 수집
        
        Args:
            links: AEMLink 리스트
            
        Returns:
            경로별 카운트 딕셔너리
        """
        path_stats = {}
        
        for link in links:
            parts = link.get_path_parts()
            if parts:
                section = parts[0] if len(parts) > 0 else 'root'
                path_stats[section] = path_stats.get(section, 0) + 1
        
        return path_stats