# Testing-playwright

1. Клонируйте репозиторий:
```bash
git clone https://github.com/st-b2/Testing-playwright.git
cd Testing-playwright
```
2. Создайте виртуальное окружение:
```bash
conda create -n test_env python=3.11
conda activate test_env
```
3. Установка зависимостей
```bash
pip install -r requirements.txt
playwright install
```
4. Структура репозитория
```text
tests/
├── conftest.py
├── playwright + pytest/
│   ├── api/
│   ├── authentication/
│   │   ├── docstring.py
│   │   ├── test_auth_neg.py
│   │   └── test_auth_pos.py
│   └── registration/
│       ├── docstring.py
│       ├── test_reg_neg.py
│       └── test_reg_pos.py
└── (abandoned) selenium + p.../ (игнорируется)
```

5. Требования
```bash
- Python 3.11+
- Playwright
- Pytest
- Miniconda / Anaconda (environment)

[!] Подробнее - environment.yml
```
