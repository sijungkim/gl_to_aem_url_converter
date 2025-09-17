"""
presentation/html_renderer.py - HTML 렌더링 서비스
"""
from typing import List, Dict, Optional
from datetime import datetime
from core.interfaces import TemplateRenderer
from services.language import LanguagePathManager
from presentation.template_loader import TemplateLoader


class QuickLinksGenerator:
    """Quick Links 생성 서비스 (SRP - Quick Links 생성만 담당)
    
    각 링크에 대한 Quick Links (lm-en, lm-ko/ja, spac) 생성.
    """
    
    def __init__(self, path_manager: LanguagePathManager):
        """Quick Links 생성기 초기화
        
        Args:
            path_manager: 언어 경로 관리자
        """
        self.path_manager = path_manager
    
    def generate(self, url: str, lang_code: str) -> str:
        """Quick Links HTML 생성
        
        Args:
            url: 원본 URL
            lang_code: 언어 코드
            
        Returns:
            Quick Links HTML 문자열
        """
        # 각 버전의 URL 생성
        en_url = self.path_manager.convert_to_english_url(url, lang_code)
        spac_url = self.path_manager.convert_to_spac_url(url, lang_code)
        
        # HTML 링크 생성
        links = [
            self._create_link(en_url, 'lm-en'),
            self._create_link(url, f'lm-{lang_code}'),
            self._create_link(spac_url, f'spac-{lang_code}')
        ]
        
        return ' | '.join(links)
    
    def _create_link(self, url: str, label: str) -> str:
        """단일 링크 HTML 생성
        
        Args:
            url: 링크 URL
            label: 링크 레이블
            
        Returns:
            HTML 링크 문자열
        """
        return f'<a href="{url}" target="_blank">{label}</a>'


class HTMLTableRenderer(TemplateRenderer):
    """HTML 테이블 렌더링 서비스 (DIP - 인터페이스 구현)
    
    링크 리스트를 HTML 테이블로 렌더링.
    TemplateRenderer 인터페이스를 구현하여 의존성 역전.
    """
    
    def __init__(
        self,
        quick_links_generator: QuickLinksGenerator,
        template_loader: TemplateLoader
    ):
        """HTML 렌더러 초기화
        
        Args:
            quick_links_generator: Quick Links 생성기
            template_loader: 템플릿 로더
        """
        self.quick_links_generator = quick_links_generator
        self.template_loader = template_loader
    
    def render(
        self,
        links: List[Dict[str, str]],
        language_name: str,
        source_name: str,
        job_id: str,
        submission_name: str,
        lang_code: str
    ) -> str:
        """링크 리스트를 HTML로 렌더링
        
        Args:
            links: 렌더링할 링크 리스트
            language_name: 언어 이름 ('Korean', 'Japanese')
            source_name: 소스 파일명
            job_id: Job ID (선택사항)
            submission_name: Submission 이름 (선택사항)
            lang_code: 언어 코드 ('ko', 'ja')
            
        Returns:
            렌더링된 HTML 문자열
        """
        if not links:
            return self._render_empty_result(language_name)
        
        # 데이터 준비
        paths = self._extract_paths(links)
        max_depth = max(len(p) for p in paths) if paths else 0
        
        # HTML 구성 요소 생성
        headers = self._build_headers(max_depth)
        table_rows = self._build_rows(links, paths, max_depth, lang_code)
        source_info = self._build_source_info(job_id, submission_name, source_name)
        
        # 템플릿 렌더링
        return self._render_template(
            language_name, source_name, source_info,
            headers, table_rows, len(links), max_depth
        )
    
    def _render_empty_result(self, language_name: str) -> str:
        """빈 결과 HTML 렌더링
        
        Args:
            language_name: 언어 이름
            
        Returns:
            빈 결과 HTML
        """
        return f"""
        <h1>AEM {language_name} Links (0)</h1>
        <p>No links to display.</p>
        """
    
    def _extract_paths(self, links: List[Dict[str, str]]) -> List[List[str]]:
        """링크에서 경로 추출
        
        Args:
            links: 링크 리스트
            
        Returns:
            분할된 경로 리스트
        """
        paths = []
        for link in links:
            path_parts = link['path'].strip('/').replace('.html', '').split('/')[1:]
            paths.append(path_parts)
        return paths
    
    def _build_headers(self, max_depth: int) -> str:
        """테이블 헤더 생성
        
        Args:
            max_depth: 최대 경로 깊이
            
        Returns:
            헤더 HTML 문자열
        """
        headers = "<th>Check</th><th>Quick Links</th>"
        headers += "".join([f"<th>Level {i+2}</th>" for i in range(max_depth)])
        return headers
    
    def _build_rows(
        self,
        links: List[Dict[str, str]],
        paths: List[List[str]],
        max_depth: int,
        lang_code: str
    ) -> str:
        """테이블 행 생성
        
        Args:
            links: 링크 리스트
            paths: 분할된 경로 리스트
            max_depth: 최대 깊이
            lang_code: 언어 코드
            
        Returns:
            테이블 행 HTML 문자열
        """
        rows = []
        for i, path_parts in enumerate(paths):
            row = self._build_single_row(
                links[i]['url'],
                path_parts,
                max_depth,
                lang_code
            )
            rows.append(row)
        return "".join(rows)
    
    def _build_single_row(
        self,
        url: str,
        path_parts: List[str],
        max_depth: int,
        lang_code: str
    ) -> str:
        """단일 테이블 행 생성
        
        Args:
            url: 링크 URL
            path_parts: 경로 구성 요소
            max_depth: 최대 깊이
            lang_code: 언어 코드
            
        Returns:
            행 HTML 문자열
        """
        # 체크박스 컬럼
        row = '<tr><td><input type="checkbox"></td>'
        
        # Quick Links 컬럼
        quick_links = self.quick_links_generator.generate(url, lang_code)
        row += f'<td>{quick_links}</td>'
        
        # 경로 레벨 컬럼들
        for j in range(max_depth):
            if j < len(path_parts) - 1:
                row += f"<td>{path_parts[j]}</td>"
            elif j == len(path_parts) - 1:
                row += f'<td><a href="{url}" target="_blank">{path_parts[j]}</a></td>'
            else:
                row += "<td></td>"
        
        row += "</tr>"
        return row
    
    def _build_source_info(
        self,
        job_id: str,
        submission_name: str,
        source_name: str
    ) -> str:
        """소스 정보 HTML 생성
        
        Args:
            job_id: Job ID
            submission_name: Submission 이름
            source_name: 소스 파일명
            
        Returns:
            소스 정보 HTML
        """
        if job_id and submission_name:
            return f"""
            <p><strong>Job ID:</strong> {job_id}</p>
            <p><strong>Submission Name:</strong> {submission_name}</p>
            """
        return f"<p><strong>Source File:</strong> {source_name}</p>"
    
    def _render_template(
        self,
        language_name: str,
        source_name: str,
        source_info: str,
        headers: str,
        table_rows: str,
        total_links: int,
        max_depth: int
    ) -> str:
        """템플릿 렌더링
        
        Args:
            language_name: 언어 이름
            source_name: 소스 이름
            source_info: 소스 정보 HTML
            headers: 헤더 HTML
            table_rows: 테이블 행 HTML
            total_links: 전체 링크 수
            max_depth: 최대 깊이
            
        Returns:
            최종 HTML 문자열
        """
        template = self.template_loader.load()
        
        # 템플릿 변수 준비
        template_vars = {
            'language_name': language_name,
            'title_source': source_name,
            'source_info': source_info,
            'total_links': total_links,
            'headers': headers,
            'table_rows': table_rows,
            'generation_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # 고급 템플릿이 있는지 확인
        if 'language_name' in template:
            template_vars['level_headers'] = "".join(
                [f"<th>Level {i+2}</th>" for i in range(max_depth)]
            )
            return template.format(**template_vars)
        else:
            # 기본 템플릿 사용
            title = f"AEM {language_name} Links - {source_name}"
            return template.format(
                title=title,
                source_info=source_info,
                headers=headers,
                table_rows=table_rows
            )