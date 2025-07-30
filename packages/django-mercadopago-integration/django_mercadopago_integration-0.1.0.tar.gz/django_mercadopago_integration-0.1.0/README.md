# django-mercadopago-integration

**Reusable Mercado Pago integration for Django projects.**

This package provides a reusable and extensible integration with [Mercado Pago](https://www.mercadopago.com) for Django applications. It includes OAuth2 connection, split payments, webhook signature verification, and default serializers and viewsets to plug into any Django REST Framework backend.

---

## 🔧 Features

- 🔐 OAuth2 authorization flow to link accounts
- 💸 Split payments with `marketplace_fee`
- 🧾 Automatic preference creation and redirection
- 📬 Webhook handling with HMAC signature verification
- 🧩 Extensible base service to override core logic
- ✅ Default DRF serializers and viewsets ready to use

---

## 📦 Installation

### From PyPI

```bash
pip install django-mercadopago-integration
