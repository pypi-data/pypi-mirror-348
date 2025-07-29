![easyssp-logo-light](https://raw.githubusercontent.com/exxcellent/easyssp-auth-client-python/refs/heads/master/images/logo-light.png#gh-light-mode-only)

# easySSP Import-Export Python Client

This is the official Python client for the **Import/Export API** of the easySSP. This client simplifies the process of
importing and exporting `.ssp` and `.ssd` model files through the API, enabling easy programmatic access for integration
into your workflows.

---

## ✨ Features

- 📤 Import `.ssp` and `.ssd` files into the easySSP platform
- 🔎 View imported models directly in easySSP
- 📥 Export `.ssp` files from easySSP for use in other tools or storage

---

## 📦 Installation

```bash
pip install easyssp-import-export-client
```

Or clone and install from source:

```bash
git clone https://github.com/exxcellent/easyssp-import-export-client-python.git
cd easyssp-import-export-client-python
pip install -e .
```

## Tests

Execute `pytest` or `python -m pytest` to run the tests.

## 📁 Project Structure

```bash
easyssp_import_export/
├── __init__.py
├── client/
│   ├── __init__.py
│   └── import_export_client.py      # Importing and exporting .ssp/.ssd files
│
├── models/
│   ├── __init__.py
│   └── upload_response.py           # Info about the uploaded .ssp/.ssd file
```

## 📖 API Reference

This client is built against the official **Import/Export API** specification, available as an OpenAPI (Swagger)
document.

You can explore the full API documentation here:  
👉 [**Import/Export API**](https://apps.exxcellent.de/easy-ssp/docs/integration-api/v1/import-export/index.html)

## 📚 Examples Repository & Extended Documentation

Looking for working demos? Check out the Import/Export Client Examples Repository here:  
👉 [**Import/Export Client Examples Repository**](https://github.com/exxcellent/easyssp-import-export-examples-python)

It includes:

- Real-world examples for importing and exporting .ssp/.ssd files
- Usage patterns for authentication and error handling

It's the best place to explore how the client works in action and how to integrate it into your own workflows.

## 🛠️ Requirements

- Python 3.11+
- easyssp Pro Edition Account

Install dependencies using uv:

```bash
pip install uv
uv sync
```

## 🤝 Contributing

This module is maintained as part of the easySSP ecosystem. If you find issues or want to suggest improvements, please
open an issue or submit a pull request.

## 📄 License

This project is licensed under the MIT License.
