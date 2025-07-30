# PYAWS_S3

## Description

`S3Client` is a Python class that simplifies interaction with AWS S3 for uploading, managing, and deleting files. It supports uploading images, DataFrames, PDFs, and generating pre-signed URLs.

## Installation

Make sure you have installed:

```bash
pip install pyaws_s3
```

### Env Variabiles

Make sure to add this environment variable:

```bash
AWS_ACCESS_KEY_ID=<Your Access Key Id>
AWS_SECRET_ACCESS_KEY=<Your Secrect Access Key>
AWS_REGION=<Your Region>
AWS_BUCKET_NAME=<Your Bucket Name>
```bash

## Usage

### Initialization

You can initialize the class by passing AWS credentials as parameters or via environment variables:

```python
from s3_client import S3Client

s3 = S3Client(
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION"),
    bucket_name=os.getenv("AWS_BUCKET_NAME")
)
```

### Main Methods

#### 1. `upload_image(fig, object_name, format_file=Literal["png", "jpeg", "svg", "html"])`

Uploads a figure (e.g., Matplotlib or Plotly) to S3 as an image (svg, png, jpeg, html).

```python
url = s3.upload_image(fig, "folder/image.svg", format_file="svg")
```

#### 2. `upload_from_dataframe(df, object_name, format_file=Literal["xlsx", "csv", "pdf"])`

Uploads a DataFrame to S3 as an Excel, CSV, or PDF file.

```python
url = s3.upload_from_dataframe(df, "folder/data", format_file="csv")
```

#### 3. `upload_to_pdf(text, object_name)`

Exports text to PDF and uploads it to S3.

```python
url = s3.upload_to_pdf("Text to export", "folder/file.pdf")
```

#### 4. `await delete_all(filter=None)`

Deletes all files from the bucket, optionally filtering by name.

```python
import asyncio
await s3.delete_all(filter="your_filter")
```

## Notes

- All upload methods return a pre-signed URL for downloading the file.
- Integrated error handling with logging.
- For uploading images and DataFrames, utility functions are required (`bytes_from_figure`, `html_from_figure`).

## Complete Example

```python
import matplotlib.pyplot as plt
import pandas as pd

fig, ax = plt.subplots()
ax.plot([1, 2, 3], [4, 5, 6])

df = pd.DataFrame({"a": [1, 2], "b": [3, 4]})

s3 = S3Client(bucket_name="my-bucket")
img_url = s3.upload_image(fig, "test.svg")
df_url = s3.upload_from_dataframe(df, "mydata")
pdf_url = s3.upload_to_pdf("Hello PDF", "hello.pdf")
```
