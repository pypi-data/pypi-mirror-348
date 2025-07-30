# Integrations

LDA integrates with various tools and platforms to enhance your workflow. This guide covers built-in integrations and how to connect LDA with your existing toolchain.

## Version Control Systems

### Git Integration

LDA works seamlessly with Git for code versioning while maintaining separate data provenance tracking.

#### Automatic Git Commits

Configure automatic commits after tracking:

```yaml
# lda_config.yaml
integrations:
  git:
    auto_commit: true
    commit_message: "LDA: {message}"
    include_manifest: true
```

#### Git Hooks

Install LDA git hooks:

```bash
# Install pre-commit hook
lda git install-hooks

# Manual hook setup
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash
lda validate --strict
EOF
chmod +x .git/hooks/pre-commit
```

#### `.gitignore` Configuration

LDA automatically creates appropriate `.gitignore`:

```gitignore
# LDA generated
*.tmp
*.log
.lda_cache/
*_sandbox/

# Large data files (tracked by LDA)
data/*.csv
data/*.parquet
outputs/*.pkl

# But track manifests
!*/manifest.json
!lda_manifest.csv
```

### GitHub Integration

#### GitHub Actions

```yaml
# .github/workflows/lda-validation.yml
name: LDA Validation

on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      
      - name: Install LDA
        run: |
          pip install lda-tool
      
      - name: Validate project
        run: |
          lda validate --strict
          lda test --all
      
      - name: Check tracking
        run: |
          lda changes --check
```

#### GitHub Issues Integration

Link LDA sections to GitHub issues:

```yaml
# lda_config.yaml
integrations:
  github:
    repo: "owner/repo"
    issue_tracking:
      enabled: true
      section_prefix: "LDA:"
```

## Cloud Storage

### AWS S3

Store large files and backups in S3:

```yaml
# lda_config.yaml
integrations:
  s3:
    bucket: "my-lda-bucket"
    prefix: "projects/{project_code}"
    backup:
      enabled: true
      schedule: "daily"
    large_files:
      threshold: "100MB"
      auto_upload: true
```

#### S3 Commands

```bash
# Upload project to S3
lda s3 upload --bucket my-bucket

# Download from S3
lda s3 download --bucket my-bucket --project PROJ001

# Sync with S3
lda s3 sync
```

### Google Cloud Storage

```yaml
integrations:
  gcs:
    bucket: "my-lda-bucket"
    project: "my-gcp-project"
    credentials: "${GOOGLE_APPLICATION_CREDENTIALS}"
```

### Azure Blob Storage

```yaml
integrations:
  azure:
    container: "lda-projects"
    account: "myaccount"
    key: "${AZURE_STORAGE_KEY}"
```

## Database Integration

### PostgreSQL

Store metadata and tracking in PostgreSQL:

```yaml
integrations:
  postgres:
    host: "${DB_HOST}"
    port: 5432
    database: "lda_tracking"
    user: "${DB_USER}"
    password: "${DB_PASSWORD}"
    schema: "lda"
```

#### Database Schema

```sql
-- LDA tracking schema
CREATE SCHEMA IF NOT EXISTS lda;

CREATE TABLE lda.projects (
    id SERIAL PRIMARY KEY,
    code VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(200),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE lda.file_tracking (
    id SERIAL PRIMARY KEY,
    project_id INTEGER REFERENCES lda.projects(id),
    file_path VARCHAR(500),
    hash VARCHAR(64),
    size BIGINT,
    modified_at TIMESTAMP,
    analyst VARCHAR(100)
);
```

### MongoDB

For document-based tracking:

```yaml
integrations:
  mongodb:
    uri: "${MONGODB_URI}"
    database: "lda"
    collection: "tracking"
```

## Jupyter Integration

### Notebook Tracking

Track Jupyter notebooks with LDA:

```python
# In Jupyter notebook
import lda.jupyter

# Enable automatic tracking
lda.jupyter.enable_tracking()

# Manual checkpoint
lda.jupyter.checkpoint("Completed data preprocessing")
```

### Magic Commands

```python
# Load LDA magic commands
%load_ext lda.jupyter

# Track cell output
%%lda track
df = pd.read_csv("data.csv")
df = df.dropna()
df.to_csv("cleaned_data.csv")

# Show project status
%lda status
```

## IDE Integration

### VS Code Extension

Install the LDA VS Code extension:

```bash
code --install-extension lda-tool.vscode-lda
```

Features:
- Syntax highlighting for `lda_config.yaml`
- Command palette integration
- Status bar tracking indicator
- Inline validation

### PyCharm Plugin

Configure PyCharm for LDA:

1. Install LDA plugin from marketplace
2. Configure project interpreter
3. Set up file watchers:

```xml
<!-- .idea/watcherTasks.xml -->
<TaskOptions>
  <option name="command" value="lda" />
  <option name="arguments" value="track --auto" />
  <option name="checkSyntaxErrors" value="false" />
</TaskOptions>
```

## CI/CD Integration

### Jenkins

```groovy
// Jenkinsfile
pipeline {
    agent any
    
    stages {
        stage('Setup') {
            steps {
                sh 'pip install lda-tool'
            }
        }
        
        stage('Validate') {
            steps {
                sh 'lda validate --strict'
            }
        }
        
        stage('Track') {
            steps {
                sh 'lda track --all'
            }
        }
        
        stage('Export') {
            steps {
                sh 'lda export manifest --output manifest.json'
                archiveArtifacts artifacts: 'manifest.json'
            }
        }
    }
}
```

### GitLab CI

```yaml
# .gitlab-ci.yml
stages:
  - validate
  - track
  - report

lda-validate:
  stage: validate
  script:
    - pip install lda-tool
    - lda validate --strict
  
lda-track:
  stage: track
  script:
    - lda track --all
    - lda changes --check
  
lda-report:
  stage: report
  script:
    - lda export report --format html --output report.html
  artifacts:
    paths:
      - report.html
```

## Workflow Automation

### Apache Airflow

Create LDA DAGs:

```python
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'lda',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
}

dag = DAG(
    'lda_workflow',
    default_args=default_args,
    schedule_interval='@daily',
)

validate = BashOperator(
    task_id='validate',
    bash_command='lda validate --strict',
    dag=dag,
)

track = BashOperator(
    task_id='track',
    bash_command='lda track --all',
    dag=dag,
)

export = BashOperator(
    task_id='export',
    bash_command='lda export manifest --output /data/manifest.json',
    dag=dag,
)

validate >> track >> export
```

### Make Integration

```makefile
# Makefile
.PHONY: init validate track report clean

init:
	lda init --template research

validate:
	lda validate --strict

track:
	lda track --all --message "$(MSG)"

report:
	lda export report --format html --output report.html

clean:
	rm -rf lda_sandbox/
	rm -f *.log

workflow: validate track report
```

## Notification Systems

### Slack Integration

```yaml
integrations:
  slack:
    webhook_url: "${SLACK_WEBHOOK}"
    notifications:
      on_track: true
      on_error: true
      on_validate: false
    channel: "#lda-updates"
```

### Email Notifications

```yaml
integrations:
  email:
    smtp_server: "smtp.gmail.com"
    smtp_port: 587
    username: "${EMAIL_USER}"
    password: "${EMAIL_PASS}"
    recipients:
      - "team@example.com"
    notifications:
      daily_summary: true
      error_alerts: true
```

## Data Science Tools

### Pandas Integration

```python
import pandas as pd
import lda.pandas

# Enable LDA tracking for pandas
lda.pandas.enable_tracking()

# Read with tracking
df = pd.read_csv("data.csv")  # Automatically tracked

# Save with tracking
df.to_csv("output.csv")  # Automatically tracked

# Manual tracking
with lda.pandas.track_operation("data_cleaning"):
    df = df.dropna()
    df = df[df['value'] > 0]
```

### MLflow Integration

```python
import mlflow
import lda.mlflow

# Configure MLflow with LDA
lda.mlflow.configure()

with mlflow.start_run():
    # Log parameters
    mlflow.log_param("alpha", 0.01)
    
    # Train model
    model = train_model()
    
    # Log with LDA tracking
    mlflow.log_model(model, "model")
    lda.track("models/model.pkl", "Trained model v1")
```

### DVC Integration

```yaml
# dvc.yaml
stages:
  preprocess:
    cmd: python preprocess.py
    deps:
      - data/raw.csv
    outs:
      - data/processed.csv
    meta:
      lda_track: true
      lda_section: "sec01_preprocessing"
```

## Custom Integrations

### Creating Integration Plugins

```python
# my_integration.py
from lda.integrations import Integration

class MyServiceIntegration(Integration):
    """Custom service integration."""
    
    def __init__(self, config):
        super().__init__(config)
        self.api_key = config.get("api_key")
        self.endpoint = config.get("endpoint")
    
    def connect(self):
        """Establish connection."""
        self.client = MyServiceClient(
            self.api_key,
            self.endpoint
        )
    
    def on_track(self, files):
        """Handle file tracking."""
        for file in files:
            self.client.upload(file)
    
    def on_validate(self, results):
        """Handle validation results."""
        if results.errors:
            self.client.alert(results.errors)
```

### Integration Configuration

```yaml
integrations:
  custom:
    my_service:
      class: "my_integration.MyServiceIntegration"
      api_key: "${MY_SERVICE_KEY}"
      endpoint: "https://api.myservice.com"
      events:
        - track
        - validate
```

## Best Practices

### 1. Security

- Never commit credentials to version control
- Use environment variables for sensitive data
- Encrypt data in transit and at rest
- Implement proper access controls

### 2. Performance

- Use async operations for external services
- Implement caching for frequently accessed data
- Batch operations when possible
- Set appropriate timeouts

### 3. Reliability

- Implement retry logic with backoff
- Handle service outages gracefully
- Provide fallback mechanisms
- Log integration events

### 4. Monitoring

```yaml
integrations:
  monitoring:
    prometheus:
      enabled: true
      port: 9090
    metrics:
      - tracking_operations
      - validation_errors
      - integration_failures
```

## See Also

- [Plugins](plugins.md) - Creating custom plugins
- [Configuration](../user-guide/configuration.md) - Integration configuration
- [API Reference](../api-reference/core.md) - Integration APIs