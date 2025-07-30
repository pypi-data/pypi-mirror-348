# Syncing Projects with Configuration

The `sync` command allows you to update your project structure based on changes to the configuration file. This is useful when you want to add sections, change settings, or update the project structure without reinitializing.

## Basic Usage

Sync your project with the configuration:

```bash
uvx ldanalysis sync
```

This command will:
1. Read your project's configuration file
2. Compare it with the existing project structure
3. Add any missing sections
4. Create playground directory if needed
5. Report any discrepancies

## Configuration Discovery

The sync command looks for configuration files in this order:
1. File specified with `--config` flag
2. Files matching `*_config.yaml` in current directory
3. Default `lda_config.yaml`

If multiple config files exist, you must specify which one to use.

## Dry Run Mode

Preview changes without making them:

```bash
uvx ldanalysis sync --dry-run
```

This shows:
- Sections that would be created
- Playground creation status
- Sections that exist but aren't in config

## Common Use Cases

### Adding New Sections

1. Edit your config file to add sections:
   ```yaml
   sections:
   - name: intro
     inputs: []
     outputs: []
   - name: methods  # New section
     inputs: []
     outputs: []
   ```

2. Run sync:
   ```bash
   uvx ldanalysis sync
   ```

3. The new section will be created with all standard directories and scripts.

### Creating Playground Later

If you initialized with `--no-playground`, you can add it later:

1. Edit config:
   ```yaml
   project:
     create_playground: true
   ```

2. Run sync:
   ```bash
   uvx ldanalysis sync
   ```

### Handling Removed Sections

If you remove sections from your config, sync will warn you but won't delete them:

```
WARNING: Sections exist but not in config: old_section
INFO: These sections were NOT removed. Remove manually if needed.
```

This prevents accidental data loss. To remove sections, delete them manually.

## Options

- `--config, -c`: Specify configuration file path
- `--dry-run`: Preview changes without making them

## Examples

### Sync with specific config
```bash
uvx ldanalysis sync --config project_2024_config.yaml
```

### Preview changes
```bash
uvx ldanalysis sync --dry-run
```

### Typical workflow
```bash
# Edit your config file
vi climate_analysis_config.yaml

# Preview changes
uvx ldanalysis sync --dry-run

# Apply changes
uvx ldanalysis sync
```

## Best Practices

1. **Always preview with dry-run** before actual sync
2. **Back up your work** before major structure changes
3. **Keep configs in version control** to track changes
4. **Document section purposes** in the config file
5. **Don't rely on sync to remove sections** - do it manually

## Safety Features

- Sync never deletes existing sections
- Sync never removes files
- Sync preserves all existing data
- Dry-run mode for safe preview
- Clear warnings about discrepancies

The sync command is designed to be safe and additive, helping you grow your project structure as needed while protecting existing work.