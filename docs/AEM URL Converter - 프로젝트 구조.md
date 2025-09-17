# AEM URL Converter - 프로젝트 구조

```
aem_url_converter/
├── core/
│   ├── __init__.py
│   ├── config.py           # 설정 관리
│   ├── models.py           # 도메인 모델
│   └── interfaces.py       # 추상 인터페이스
│
├── services/
│   ├── __init__.py
│   ├── language.py         # 언어 감지 및 처리
│   ├── url_generator.py    # URL 생성 로직
│   └── file_processor.py   # ZIP 파일 처리
│
├── presentation/
│   ├── __init__.py
│   ├── html_renderer.py    # HTML 렌더링
│   ├── df_builder.py       # DataFrame 빌더
│   └── template_loader.py  # 템플릿 로더
│
├── di_container.py         # 의존성 주입 컨테이너
├── app.py                  # Streamlit 애플리케이션
├── main.py                 # 진입점
├── template.html           # HTML 템플릿
├── requirements.txt        # 의존성 패키지
└── .gitignore             # Git 제외 파일
```

## 각 디렉토리 역할

### **core/**
- 핵심 비즈니스 로직과 도메인 모델
- 외부 의존성이 없는 순수한 비즈니스 규칙

### **services/**
- 비즈니스 로직 구현
- 파일 처리, URL 생성 등의 서비스

### **presentation/**
- 사용자에게 보여지는 부분 담당
- HTML 렌더링, DataFrame 생성

### **루트 디렉토리**
- 애플리케이션 진입점과 설정 파일