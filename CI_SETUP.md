# CI/CD Setup Guide

## GitHub Actions CI Configuration

This project uses GitHub Actions for continuous integration and testing.

## Workflows

### 1. Quick Tests (`quick-test.yml`)
**Runs on**: Every push and PR  
**Duration**: ~2-3 minutes  
**Purpose**: Fast feedback on basic code quality

- ✅ Python syntax check
- ✅ Configuration file validation
- ✅ Code linting (critical errors only)

### 2. Full CI Tests (`ci.yml`)
**Runs on**: Every push to main/dev and PRs  
**Duration**: ~5-10 minutes  
**Purpose**: Comprehensive quality checks

- ✅ **Code Quality Check**: flake8, black, isort
- ✅ **Security Scan**: Trivy vulnerability scanning
- ✅ **Docker Build Test**: Verify Docker image builds
- ✅ **Unit Tests**: Run pytest tests
- ✅ **Configuration Validation**: Check all config files

## CI Status Badges

Add these badges to your README.md:

```markdown
![CI Tests](https://github.com/lfpaaaaa/deepfake-detector/actions/workflows/ci.yml/badge.svg)
![Quick Tests](https://github.com/lfpaaaaa/deepfake-detector/actions/workflows/quick-test.yml/badge.svg)
```

## Local Testing

Before pushing, you can run tests locally:

```bash
# Install test dependencies
pip install pytest pytest-cov pytest-asyncio flake8 black isort

# Run tests
pytest tests/ -v

# Run linting
flake8 app/ tools/
black --check app/ tools/
isort --check-only app/ tools/

# Build Docker image
docker build . --tag deepfake-detector:local-test
```

## Setting Up GitHub Actions

1. **Enable Actions**: Go to your repository → Settings → Actions → Allow all actions
2. **Secrets** (if needed): Go to Settings → Secrets and variables → Actions
3. **Branch Protection** (optional): Settings → Branches → Add rule
   - Require status checks before merging
   - Select which CI checks must pass

## What Gets Tested

### ✅ Automated Checks
- Python syntax and imports
- Code style (PEP 8)
- Security vulnerabilities
- Docker build process
- Configuration file validity
- Basic API endpoints

### ⚠️ Not Tested (Too Resource Intensive)
- Model inference (requires GPU + large model files)
- Video processing (requires substantial compute)
- Full end-to-end detection workflow

## Troubleshooting

### CI Failing on Flake8
```bash
# Fix automatically
black app/ tools/
isort app/ tools/
```

### CI Failing on Docker Build
- Check Dockerfile syntax
- Ensure requirements.txt is valid
- Verify base image is accessible

### Tests Skipped
Some tests may be skipped in CI due to:
- Missing model files (too large for CI)
- GPU requirements
- Heavy dependencies

This is expected and okay!

## Best Practices

1. ✅ **Run quick tests locally** before pushing
2. ✅ **Check CI results** before merging PRs
3. ✅ **Add tests** for new features
4. ✅ **Keep requirements.txt** up to date
5. ✅ **Don't commit** large model files

## Need Help?

- GitHub Actions docs: https://docs.github.com/en/actions
- pytest docs: https://docs.pytest.org/
- flake8 docs: https://flake8.pycqa.org/

