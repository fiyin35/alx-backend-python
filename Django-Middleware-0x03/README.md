# Django-Middleware-0x03

This project demonstrates how to build and configure **custom middleware in Django** to manage security, access control, logging, and rate limiting.

---

## 📌 Features Implemented

### ✅ 1. Request Logging Middleware

**File:** `chats/middleware.py`  
Logs each request made to the server with the following details:
- Timestamp
- User (or "Anonymous")
- Path accessed

**Output File:** `requests.log`

📄 Example log entry:
```
2025-07-20 22:15:32.456789 - User: admin - Path: /admin/
```

---

### ✅ 2. Access Restriction by Time

**File:** `chats/middleware.py`  
Restricts users from accessing the platform **outside the hours of 6PM and 9PM** (inclusive). Returns HTTP 403 Forbidden during restricted hours.

---

### ✅ 3. Rate Limiting by IP (OffensiveLanguageMiddleware)

**File:** `chats/middleware.py`  
Prevents abuse by limiting the number of **POST requests to /messages** per IP address:
- ⏱ Max: 5 messages per minute
- 🛑 Exceeds limit: Returns `429 Too Many Requests`

---

### ✅ 4. Role-Based Access Control (RolePermissionMiddleware)

**File:** `chats/middleware.py`  
Only allows users with roles:
- `admin`
- `moderator`

...to access protected actions. Others receive a `403 Forbidden`.

💡 Assumes your `User` model has a `.role` attribute.

---

## ⚙️ Middleware Configuration

All middleware classes are registered in `messaging_app/settings.py` under the `MIDDLEWARE` list:

```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    ...
    'chats.middleware.RequestLoggingMiddleware',
    'chats.middleware.RestrictAccessByTimeMiddleware',
    'chats.middleware.OffensiveLanguageMiddleware',
    'chats.middleware.RolePermissionMiddleware',
]
```

---

## 🧪 Testing

You can test these features using:

- ✅ **Postman** – For testing POST limits, role-based blocking, etc.
- ✅ **Browser** – To check time-based access restriction
- ✅ **Django Test Client** – For automated test cases

---

## 📁 Project Structure (Relevant Files)

```
Django-Middleware-0x03/
│
├── chats/
│   └── middleware.py          # ✅ All custom middleware classes
├── messaging_app/
│   └── settings.py            # ✅ Middleware registration
├── requests.log               # ✅ Generated request logs
```

---

## 📘 Summary of Middleware Classes

| Middleware Class                  | Purpose                                  |
|----------------------------------|------------------------------------------|
| `RequestLoggingMiddleware`       | Logs each incoming request to a file     |
| `RestrictAccessByTimeMiddleware` | Restricts access to certain hours        |
| `OffensiveLanguageMiddleware`    | Limits message sends per IP per minute   |
| `RolePermissionMiddleware`       | Blocks access for users without roles    |

---

## 🚀 Run the Server

```bash
python manage.py runserver
```