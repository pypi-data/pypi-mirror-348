# stx_security_filter

**stx_security_filter** is a lightweight and easy-to-use Python library that detects malicious input patterns such as SQL Injection, XSS, and other attack vectors. It's ideal for validating GET/POST parameters in Django, Flask, FastAPI, or any Python-based web application.

---

## 🚀 Features

- Detects common SQL injection attempts
- Flags potential XSS and JavaScript payloads
- Blocks path traversal and encoded exploits
- Can be integrated directly into views, forms, or APIs
- Lightweight and dependency-free

---

## 📦 Installation

```bash
pip install -e .


Usage

from stx_security_filter import is_safe_input

user_input = request.GET.get("search")

if not is_safe_input(user_input):
    return HttpResponseForbidden("Malicious input detected.")
