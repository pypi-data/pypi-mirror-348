# anyeval

Universal Evaluation for Gen AI

## Design

#### Data Schema (Parquet)

| id  | dataset | meta | media | label | created_at | updated_at |
| --- | ------- | ---- | ----- | ----- | ---------- | ---------- |

#### CLI Commands

- `anyeval run [parquet_file]` open parquet file and get the UI for evaluation
- `anyeval merge [parquet_files|dir] [output_parquet_file]` merge parquet files into one

## Installation

### For Users

Install directly from PyPI:
```bash
pip install anyeval
```

This will install the complete package with the pre-built web UI.

### Development Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/anyeval.git
cd anyeval
```

2. Set up the Python environment:
```bash
# Using uv for package management (recommended)
uv venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
uv pip install -e .
```

3. For development of the frontend (optional, requires Node.js):
```bash
cd anyeval/frontend
npm install
npm start
```

4. To build the frontend for distribution:
```bash
python build_frontend.py
```

## Usage

### Running the Evaluation UI

To start the evaluation UI with a parquet file:

```bash
anyeval run path/to/your/data.parquet
```

This will:
1. Start a web server at http://localhost:8000
2. Automatically open your browser to the evaluation UI
3. Allow you to browse and evaluate your data

### Merging Parquet Files

To merge multiple parquet files into a single output file:

```bash
anyeval merge path/to/file1.parquet path/to/file2.parquet output.parquet
```

Or to merge all parquet files in a directory:

```bash
anyeval merge path/to/directory output.parquet
```
