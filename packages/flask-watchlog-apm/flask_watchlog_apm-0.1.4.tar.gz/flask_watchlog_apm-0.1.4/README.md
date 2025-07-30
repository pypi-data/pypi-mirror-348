# APM for Flask – Watchlog Integration

🎯 Lightweight and production-safe Application Performance Monitoring (APM) middleware for Flask apps, made for [Watchlog](https://watchlog.io).

Track route execution time, status codes, memory usage, and errors — and send them periodically to your Watchlog agent.

---

## 🚀 Features

- 🔧 Automatic tracking of all Flask routes
- 📊 Aggregation of metrics by path and method
- ⚠️ Error tracking support (optional)
- 🌐 Sends metrics to Watchlog agent over HTTP
- 🧠 Captures memory usage (`rss`, `vms`)
- 💡 Safe-by-default (never crashes your app)

---

## 📦 Installation

```bash
pip install flask_watchlog_apm
