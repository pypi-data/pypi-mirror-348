# FinDrum

**FinDrum** is a modular Python package for collecting, processing, and storing financial data from sources like the SEC and Yahoo Finance. It is designed with extensibility, testability, and backend independence in mind — ideal for building robust local or cloud-based data pipelines.

---

## 🚀 Features

- 🧾 Fetch structured financial data from **SEC EDGAR company facts**
- 📊 Historical market data via **Yahoo Finance**
- 💾 Read/write Parquet files through an abstracted `DataClient`
- 📦 Built-in clients for **local storage** and **MinIO (S3-compatible)** object storage
- 🧪 Fully typed and tested with `pytest` and `pytest-cov`

---

## 📦 Installation

```bash
pip install .  # for regular use
pip install .[dev]  # for development with tests and coverage
```

---

## 📂 Project Structure

```
findrum/
├── clients/         # Abstract DataClient + Local and MinIO implementations
├── crawlers/        # Abstract Crawler + SEC and Yahoo Finance crawlers
├── readers/         # ParquetReader
├── writers/         # ParquetWriter
```

---

## 🔍 Example: Full Workflow — SEC Crawler + Local Parquet Writer

```python
from findrum.crawlers.sec_crawler import SecCrawler
from findrum.clients.local_client import LocalDataClient
from findrum.writers.parquet_writer import ParquetWriter

client = LocalDataClient()
writer = ParquetWriter(client)

crawler = SecCrawler(email="oscar.rico101@alu.ulpgc.es")

for raw_data in crawler.fetch():
    if raw_data.empty:
        continue

    cik = raw_data.iloc[0]["cik"]
    object_path = f"./datalake/{cik}/company_facts.parquet"
    writer.write(object_path, raw_data)
```

---

## ✨ Other Examples

### Yahoo Finance Crawler

```python
from findrum import YahooCrawler

crawler = YahooCrawler(period="1mo")
for df in crawler.fetch(["AAPL", "GOOGL"]):
    print(df.head())
```

### Parquet Reader

```python
from findrum.clients.local_client import LocalDataClient
from findrum.readers.parquet_reader import ParquetWriter

client = LocalDataClient()
reader = ParquetReader(client)
df = reader.read("./datalake/0000320193/company_facts.parquet")
print(df.head())
```

---

## 🧪 Running Tests

```bash
python -m pytest --cov=findrum --cov-report=term-missing
```

---

## 📄 License and Attribution

This project includes components licensed under the [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0) and other permissive open source licenses.

Portions of this software incorporate third-party libraries, including:

- [`minio`](https://github.com/minio/minio-py)
- [`yfinance`](https://github.com/ranaroussi/yfinance)
- [`pyarrow`](https://github.com/apache/arrow)
- [`fastparquet`](https://github.com/dask/fastparquet)
- [`requests`](https://github.com/psf/requests)

These libraries are licensed under the Apache License, Version 2.0.

See the LICENSE file for full license texts and additional legal information.
