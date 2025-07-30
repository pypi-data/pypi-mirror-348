# Performance Optimization

This guide covers performance optimization techniques for LDA projects, especially when dealing with large datasets, many files, or complex tracking requirements.

## File Tracking Performance

### Hash Calculation Optimization

Choose the right hash algorithm for your needs:

```yaml
# lda_config.yaml
tracking:
  hash_algorithm: "xxhash"  # Fastest
  # hash_algorithm: "md5"    # Fast, less secure
  # hash_algorithm: "sha256" # Default, balanced
  # hash_algorithm: "sha512" # Most secure, slower
```

Performance comparison (1GB file):
- xxhash: ~0.3s
- md5: ~2.1s
- sha256: ~5.8s (default)
- sha512: ~4.2s

### Parallel Processing

Enable parallel file processing:

```yaml
performance:
  parallel_tracking: true
  max_workers: 8  # CPU cores
  chunk_size: 100  # Files per batch
```

### Selective Tracking

Track only what you need:

```yaml
tracking:
  patterns:
    include:
      - "*.csv"
      - "*.parquet"
    exclude:
      - "*.tmp"
      - "*.log"
      - "__pycache__/"
  
  # Skip large files
  size_limit: "1GB"
  
  # Track by modification time
  track_if_modified: true
```

### Incremental Tracking

Use incremental tracking for large projects:

```python
# Python API
from lda.core.tracking import IncrementalTracker

tracker = IncrementalTracker(manifest)
changes = tracker.scan_changes()
tracker.update_changed_only(changes)
```

## Memory Management

### Large File Handling

Process large files in chunks:

```python
# lda_config.yaml
performance:
  large_file_threshold: "100MB"
  chunk_size: "10MB"
  
  # Memory mapping for huge files
  use_mmap: true
  mmap_threshold: "1GB"
```

### Manifest Optimization

For projects with many files:

```yaml
performance:
  manifest:
    format: "binary"  # vs "json"
    compression: "gzip"
    index_type: "btree"  # Fast lookups
    cache_size: "100MB"
```

### Memory Profiling

Profile memory usage:

```bash
# Profile memory usage
lda track --profile-memory

# Generate memory report
lda debug memory-report
```

```python
# Python API
from lda.profiling import memory_profile

@memory_profile
def process_large_dataset():
    # Your code here
    pass
```

## Database Performance

### PostgreSQL Optimization

```sql
-- Optimized schema
CREATE TABLE lda.file_tracking (
    id BIGSERIAL PRIMARY KEY,
    project_id INTEGER NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    hash VARCHAR(64) NOT NULL,
    size BIGINT,
    modified_at TIMESTAMP,
    analyst VARCHAR(100),
    -- Indexes for common queries
    CONSTRAINT uk_project_file UNIQUE (project_id, file_path)
);

CREATE INDEX idx_modified ON lda.file_tracking(modified_at);
CREATE INDEX idx_hash ON lda.file_tracking(hash);
CREATE INDEX idx_analyst ON lda.file_tracking(analyst);

-- Partitioning for large projects
CREATE TABLE lda.file_tracking_2024 PARTITION OF lda.file_tracking
FOR VALUES FROM ('2024-01-01') TO ('2025-01-01');
```

### Connection Pooling

```yaml
database:
  postgres:
    pool_size: 20
    max_overflow: 10
    pool_timeout: 30
    pool_recycle: 3600
```

### Query Optimization

```python
# Batch operations
from lda.db import batch_insert

# Instead of individual inserts
for file in files:
    db.insert(file)  # Slow

# Use batch insert
batch_insert(files, batch_size=1000)  # Fast
```

## Caching Strategies

### File System Cache

```yaml
performance:
  cache:
    enabled: true
    type: "filesystem"
    path: ".lda_cache"
    size_limit: "1GB"
    ttl: 3600  # seconds
```

### Redis Cache

```yaml
performance:
  cache:
    type: "redis"
    host: "localhost"
    port: 6379
    db: 0
    ttl: 86400
```

### Memory Cache

```python
from lda.cache import MemoryCache

cache = MemoryCache(max_size="500MB")

@cache.memoize
def expensive_operation(file_path):
    # Cached computation
    return process_file(file_path)
```

## Network Performance

### S3 Upload Optimization

```yaml
integrations:
  s3:
    multipart_threshold: "100MB"
    multipart_chunksize: "10MB"
    max_concurrency: 10
    use_threads: true
    
    # Transfer acceleration
    use_accelerate_endpoint: true
```

### Compression

```yaml
performance:
  compression:
    enabled: true
    algorithm: "zstd"  # Best ratio/speed
    level: 3  # 1-9
    threshold: "1MB"
```

## Monitoring and Profiling

### Performance Monitoring

```yaml
monitoring:
  enabled: true
  metrics:
    - operation_duration
    - memory_usage
    - disk_io
    - network_bandwidth
  
  export:
    prometheus:
      port: 9090
    grafana:
      dashboard: "lda-performance"
```

### Built-in Profiler

```bash
# Profile specific operation
lda track --profile

# Generate performance report
lda debug performance-report --output perf.html

# Continuous monitoring
lda monitor --interval 60
```

### Custom Metrics

```python
from lda.metrics import Timer, gauge

# Time operations
with Timer("data_processing"):
    process_large_dataset()

# Track metrics
gauge("memory_usage", get_memory_usage())
gauge("active_files", len(tracked_files))
```

## Best Practices

### 1. Optimize Configuration

```yaml
# Optimized production config
performance:
  parallel_tracking: true
  max_workers: 16
  chunk_size: 1000
  
  cache:
    enabled: true
    type: "redis"
    
  compression:
    enabled: true
    algorithm: "zstd"
    
  database:
    pool_size: 50
    batch_size: 1000
```

### 2. Lazy Loading

```python
from lda.core import LazyManifest

# Load manifest on demand
manifest = LazyManifest("manifest.json")

# Only loads required sections
section_files = manifest.get_section("sec01")
```

### 3. Async Operations

```python
import asyncio
from lda.async import AsyncTracker

async def track_files_async():
    tracker = AsyncTracker()
    
    tasks = []
    for file in files:
        task = tracker.track_file_async(file)
        tasks.append(task)
    
    results = await asyncio.gather(*tasks)
    return results
```

### 4. Resource Limits

```yaml
performance:
  limits:
    max_memory: "4GB"
    max_cpu_percent: 80
    max_disk_io: "100MB/s"
    
  throttling:
    enabled: true
    rate_limit: 1000  # ops/sec
```

## Benchmarking

### Built-in Benchmarks

```bash
# Run performance benchmarks
lda benchmark --all

# Specific benchmarks
lda benchmark --hash-algorithms
lda benchmark --file-operations
lda benchmark --database
```

### Custom Benchmarks

```python
from lda.benchmark import Benchmark

bench = Benchmark("custom_operation")

# Warm up
bench.warmup(iterations=10)

# Run benchmark
results = bench.run(
    function=my_operation,
    iterations=1000,
    parallel=True
)

print(results.summary())
```

## Troubleshooting Performance

### Slow File Tracking

1. Check hash algorithm
2. Enable parallel processing
3. Exclude unnecessary files
4. Use incremental tracking

```bash
# Diagnose slow tracking
lda debug trace-tracking
```

### High Memory Usage

1. Enable chunked processing
2. Reduce cache size
3. Use memory mapping
4. Implement pagination

```bash
# Memory analysis
lda debug memory-analysis
```

### Database Bottlenecks

1. Add appropriate indexes
2. Enable connection pooling
3. Use batch operations
4. Consider partitioning

```bash
# Database performance
lda debug db-performance
```

## Performance Tuning Checklist

- [ ] Choose appropriate hash algorithm
- [ ] Enable parallel processing
- [ ] Configure caching strategy
- [ ] Optimize database queries
- [ ] Set up monitoring
- [ ] Implement resource limits
- [ ] Use compression where appropriate
- [ ] Profile before optimizing
- [ ] Test with production-size data
- [ ] Document performance settings

## See Also

- [Configuration](../user-guide/configuration.md) - Performance configuration
- [Monitoring](monitoring.md) - Performance monitoring
- [Troubleshooting](../troubleshooting.md) - Common issues