# 🧪 QA Automation Framework – Playwright + Pytest

This repository contains a **QA automation framework built for practice and learning purposes**, using **Playwright with Python** to automate the demo e-commerce site  
👉 **https://automationteststore.com**

The goal of this project is to simulate a **real-world QA automation framework**, applying:
- Page Object Model (POM)
- Risk-based test prioritization
- End-to-End (E2E) test coverage
- CI/CD with GitHub Actions
- Rich reporting with Allure
- Stable, maintainable automation best practices

---

## 🚀 Tech Stack

- **Language:** Python 3.12
- **Automation Tool:** Playwright
- **Test Runner:** Pytest
- **Design Pattern:** Page Object Model (POM)
- **Reporting:** Allure
- **CI/CD:** GitHub Actions
- **Target Browser:** Chromium (headless in CI)

---

## 📂 Project Structure

```text
.
├── pages/
│   ├── base/
│   │   └── base_page.py
│   ├── components/
│   │   ├── header_component.py
│   │   └── footer_component.py
│   ├── home_page.py
│   ├── login_page.py
│   ├── register_page.py
│   ├── product_page.py
│   ├── cart_page.py
│   └── checkout_page.py
│
├── tests/
│   ├── smoke/
│   ├── e2e/
│   └── regression/
│
├── test_data/
│   └── test_data.py
│
├── utils/
│   └── helpers.py
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── conftest.py
├── pytest.ini
├── requirements.txt
└── README.md

```

---

## 🧠 Test Strategy

- Smoke (P0): critical flows (login, register user, search)

- E2E (P1): full purchase flows (guest & registered user)

- Regression (P2): edge cases and validations

---

🧩 Key Features

- Stable waits using Playwright expect()

- Cart management (update, remove, multi-product)

- UI-based login/logout

- Allure reporting with screenshots

---

## ▶️ Running Tests

- Install requirements:

```
pip install -r requirements.txt
playwright install
pytest
```

- Run all tests

```
pytest
```

- Run specific suites:

```
pytest -m smoke
pytest -m e2e
pytest -m regression
```

---

## 📊 Reporting (Allure)

After running your tests you can generate and view the Allure report locally:

```
allure serve allure-results
```

These reports include:
- Test steps
- Screenshots on failure






