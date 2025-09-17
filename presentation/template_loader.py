"""
presentation/template_loader.py - 템플릿 로딩 서비스
"""
from typing import Optional
import os


class TemplateLoader:
    """템플릿 로딩 서비스 (SRP - 템플릿 로딩만 담당)
    
    HTML 템플릿 파일을 로드하고 관리.
    파일이 없을 경우 기본 템플릿 제공.
    """
    
    def __init__(self, template_file: str = "template.html"):
        """템플릿 로더 초기화
        
        Args:
            template_file: 템플릿 파일 경로
        """
        self.template_file = template_file
        self._cached_template: Optional[str] = None
    
    def load(self) -> str:
        """템플릿 로드 (캐싱 지원)
        
        Returns:
            템플릿 문자열
        """
        # 캐시된 템플릿이 있으면 반환
        if self._cached_template:
            return self._cached_template
        
        # 파일에서 템플릿 로드 시도
        template = self._load_from_file()
        if template:
            self._cached_template = template
            return template
        
        # 파일이 없으면 기본 템플릿 사용
        template = self._get_fallback_template()
        self._cached_template = template
        return template
    
    def reload(self) -> str:
        """템플릿 재로드 (캐시 무시)
        
        Returns:
            새로 로드된 템플릿 문자열
        """
        self._cached_template = None
        return self.load()
    
    def _load_from_file(self) -> Optional[str]:
        """파일에서 템플릿 로드
        
        Returns:
            템플릿 문자열 또는 None
        """
        try:
            with open(self.template_file, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            return None
        except Exception as e:
            print(f"Error loading template: {str(e)}")
            return None
    
    def _get_fallback_template(self) -> str:
        """기본 템플릿 반환
        
        Returns:
            기본 HTML 템플릿
        """
        return self.DEFAULT_TEMPLATE
    
    def template_exists(self) -> bool:
        """템플릿 파일 존재 여부 확인
        
        Returns:
            파일이 존재하면 True
        """
        return os.path.exists(self.template_file)
    
    # 기본 템플릿 (클래스 상수)
    DEFAULT_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            margin: 2em;
            line-height: 1.6;
            color: #333;
        }}
        
        h1 {{
            color: #2c3e50;
            border-bottom: 2px solid #3498db;
            padding-bottom: 10px;
        }}
        
        .source-info {{
            background-color: #f8f9fa;
            border-left: 4px solid #3498db;
            padding: 15px;
            margin: 20px 0;
            border-radius: 4px;
        }}
        
        .source-info p {{
            margin: 5px 0;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
            background: white;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        }}
        
        thead {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }}
        
        th {{
            padding: 12px;
            text-align: left;
            color: white;
            font-weight: 600;
            text-transform: uppercase;
            font-size: 12px;
            letter-spacing: 0.5px;
        }}
        
        td {{
            padding: 10px 12px;
            border-bottom: 1px solid #e9ecef;
        }}
        
        tr:hover {{
            background-color: #f8f9fa;
        }}
        
        td:first-child {{
            text-align: center;
        }}
        
        input[type="checkbox"] {{
            width: 1.2em;
            height: 1.2em;
            cursor: pointer;
        }}
        
        a {{
            color: #3498db;
            text-decoration: none;
            font-weight: 500;
        }}
        
        a:hover {{
            text-decoration: underline;
            color: #2980b9;
        }}
        
        /* Quick links styling */
        td:nth-child(2) a {{
            background: #e3f2fd;
            padding: 2px 6px;
            border-radius: 3px;
            margin: 0 2px;
            font-size: 11px;
            display: inline-block;
        }}
        
        td:nth-child(2) a:hover {{
            background: #bbdefb;
        }}
        
        @media print {{
            thead {{
                background: #f8f9fa !important;
                -webkit-print-color-adjust: exact;
            }}
            
            th {{
                color: #333 !important;
            }}
        }}
    </style>
</head>
<body>
    <h1>{title}</h1>
    <div class="source-info">
        {source_info}
    </div>
    <table>
        <thead>
            <tr>{headers}</tr>
        </thead>
        <tbody>
            {table_rows}
        </tbody>
    </table>
</body>
</html>"""


class AdvancedTemplateLoader(TemplateLoader):
    """고급 템플릿 로더 (OCP - 확장 가능)
    
    여러 템플릿 소스를 지원하는 확장된 템플릿 로더.
    """
    
    def __init__(
        self,
        template_file: str = "template.html",
        template_dir: str = "templates"
    ):
        """고급 템플릿 로더 초기화
        
        Args:
            template_file: 기본 템플릿 파일
            template_dir: 템플릿 디렉토리
        """
        super().__init__(template_file)
        self.template_dir = template_dir
        self.templates = {}
    
    def load_template(self, name: str) -> str:
        """이름으로 템플릿 로드
        
        Args:
            name: 템플릿 이름
            
        Returns:
            템플릿 문자열
        """
        if name in self.templates:
            return self.templates[name]
        
        template_path = os.path.join(self.template_dir, f"{name}.html")
        
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                template = f.read()
                self.templates[name] = template
                return template
        except FileNotFoundError:
            return self.load()  # 기본 템플릿 반환
    
    def list_available_templates(self) -> list:
        """사용 가능한 템플릿 목록
        
        Returns:
            템플릿 이름 리스트
        """
        if not os.path.exists(self.template_dir):
            return []
        
        templates = []
        for file in os.listdir(self.template_dir):
            if file.endswith('.html'):
                templates.append(file[:-5])  # .html 제거
        
        return templates