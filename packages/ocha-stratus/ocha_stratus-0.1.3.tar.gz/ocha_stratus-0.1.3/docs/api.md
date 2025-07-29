# API Reference

## Azure Blob Storage

The `azure_blob` module provides utilities for working with Azure Blob Storage.

### Container Operations

```{eval-rst}
.. autofunction:: ocha_stratus.get_container_client
.. autofunction:: ocha_stratus.list_container_blobs
```

### File Operations

#### CSV Files
```{eval-rst}
.. autofunction:: ocha_stratus.upload_csv_to_blob
.. autofunction:: ocha_stratus.load_csv_from_blob
```

#### Parquet Files
```{eval-rst}
.. autofunction:: ocha_stratus.upload_parquet_to_blob
.. autofunction:: ocha_stratus.load_parquet_from_blob
```

#### Shapefiles
```{eval-rst}
.. autofunction:: ocha_stratus.upload_shp_to_blob
.. autofunction:: ocha_stratus.load_shp_from_blob
```

#### Cloud Optimized GeoTIFFs
```{eval-rst}
.. autofunction:: ocha_stratus.upload_cog_to_blob
.. autofunction:: ocha_stratus.open_blob_cog
```

## Database Operations

The `database` module provides utilities for working with Azure PostgreSQL databases.

```{eval-rst}
.. autofunction:: ocha_stratus.get_engine
.. autofunction:: ocha_stratus.postgres_upsert
```
