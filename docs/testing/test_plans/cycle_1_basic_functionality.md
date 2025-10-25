# Test Plan - Cycle 1: Basic Functionality

**Project**: Deepfake Detector  
**Test Cycle**: Cycle 1  
**Focus**: Basic Functionality and Core Features  
**Start Date**: October 25, 2025  
**End Date**: October 27, 2025  
**Tester(s)**: Xiyu Guan  
**Environment**: Docker + Local Development

---

## 1. Test Cycle Overview

### 1.1 Objectives
- ✅ Verify core system setup and configuration
- ✅ Test user authentication flow (register/login)
- ✅ Validate API endpoints accessibility
- ✅ Confirm basic integration between components
- ✅ Ensure CI/CD pipeline runs successfully

### 1.2 Scope

#### In Scope:
- Module imports and configuration validation
- User registration and login functionality
- JWT token generation and validation
- Protected endpoint authentication
- Health check and web page accessibility
- Basic error handling (401/403 responses)

#### Out of Scope:
- Model inference functionality (Cycle 2)
- File upload and detection (Cycle 2)
- Performance testing (Cycle 3)
- Security testing (Cycle 3)
- Edge cases with special characters (Cycle 2)

### 1.3 Test Environment

**Hardware**:
- CPU: Intel/AMD x64
- RAM: 8GB minimum
- Disk: 10GB free space

**Software**:
- OS: Windows 10/11 or Linux
- Docker Desktop: Latest
- Python: 3.11
- Browser: Chrome/Firefox (latest)

**Test Data**:
- Test user credentials (to be generated)
- No model weights required for Cycle 1

---

## 2. Selected Test Cases

### 2.1 Unit Tests (5 test cases)

| Test ID | Test Name | Priority | Source |
|---------|-----------|----------|--------|
| TC-U-001 | Module Import Test | High | TEST_CASES.md |
| TC-U-002 | Configuration File Validation | High | TEST_CASES.md |
| TC-U-003 | Config YAML Structure Validation | Medium | TEST_CASES.md |

**Rationale**: These tests ensure basic system setup is correct before proceeding with integration tests.

---

### 2.2 Integration Tests (8 test cases)

| Test ID | Test Name | Priority | Source |
|---------|-----------|----------|--------|
| TC-I-001 | Health Check Endpoint | High | TEST_CASES.md |
| TC-I-002 | Web Pages Accessibility | High | TEST_CASES.md |

**Rationale**: Verify system is accessible and basic endpoints respond correctly.

---

### 2.3 Authentication Tests (7 test cases)

| Test ID | Test Name | Priority | Automated | Source |
|---------|-----------|----------|-----------|--------|
| TC-A-001 | User Registration - Success | High | Yes | TEST_CASES.md |
| TC-A-003 | User Login - Valid Credentials | High | Yes | TEST_CASES.md |
| TC-A-004 | User Login - Invalid Credentials | High | Yes | TEST_CASES.md |
| TC-A-005 | Token Validation - Valid Token | High | Yes | TEST_CASES.md |
| TC-A-006 | Token Validation - Invalid Token | High | Yes | TEST_CASES.md |
| TC-A-007 | Protected Endpoint - No Token | High | Yes | TEST_CASES.md |

**Rationale**: Authentication is critical for system security. All high-priority auth tests included.

---

### 2.4 API Endpoint Tests (2 test cases)

| Test ID | Test Name | Priority | Automated | Source |
|---------|-----------|----------|-----------|--------|
| TC-E-001 | Model Status Endpoint Structure | High | Yes | TEST_CASES.md |
| TC-E-002 | History Endpoint - Empty History | Medium | Yes | TEST_CASES.md |

**Rationale**: Verify API endpoints return correct structure even without models loaded.

---

## 3. Test Execution Strategy

### 3.1 Automated Tests
**Tool**: pytest  
**Command**: `python scripts/run_tests.py --unit --integration`

**Steps**:
1. Start Docker container: `docker compose up -d --build`
2. Wait for server startup (~30s)
3. Run automated tests: `pytest tests/ -v -m "unit or integration"`
4. Generate coverage report: `pytest tests/ --cov=app --cov-report=html`
5. Review test results and coverage

**Expected Outcome**:
- All automated tests should pass
- Code coverage > 60%

---

### 3.2 Manual Tests
**No manual tests required for Cycle 1** - all selected tests are automated.

---

## 4. Entry and Exit Criteria

### 4.1 Entry Criteria
- ✅ Code is committed to `main` branch
- ✅ Docker image builds successfully
- ✅ CI pipeline passes (GitHub Actions)
- ✅ Test environment is set up

### 4.2 Exit Criteria
- ✅ All high-priority test cases pass
- ✅ At least 90% of selected tests pass
- ✅ All critical bugs are fixed
- ✅ Test report is completed and reviewed
- ✅ Code coverage ≥ 60%

---

## 5. Test Schedule

| Date | Activity | Owner | Status |
|------|----------|-------|--------|
| Oct 25 | Setup test environment | Xiyu Guan | ✅ Complete |
| Oct 25 | Run automated unit tests | Xiyu Guan | 🟡 In Progress |
| Oct 25 | Run automated integration tests | Xiyu Guan | 🟡 Pending |
| Oct 26 | Review results and fix bugs | Xiyu Guan | 🟡 Pending |
| Oct 27 | Complete test report | Xiyu Guan | 🟡 Pending |
| Oct 27 | Cycle 1 review meeting | Team | 🟡 Pending |

---

## 6. Risks and Mitigation

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Docker environment issues | High | Low | Have local Python environment as backup |
| CI pipeline failures | Medium | Medium | Run tests locally first, check GitHub Actions logs |
| Test flakiness | Low | Medium | Implement retry logic, use fixtures properly |
| Missing dependencies | High | Low | Verify requirements.txt is complete |

---

## 7. Test Deliverables

1. ✅ Test execution logs (pytest output)
2. ✅ Code coverage report (HTML format)
3. ✅ Test report document (test_reports/cycle_1_report.md)
4. ✅ Bug reports (if any critical issues found)
5. ✅ CI/CD pipeline evidence (GitHub Actions results)

---

## 8. Test Case Summary

**Total Selected**: 22 test cases

**By Priority**:
- High: 18 test cases (82%)
- Medium: 4 test cases (18%)
- Low: 0 test cases (0%)

**By Automation**:
- Automated: 22 test cases (100%)
- Manual: 0 test cases (0%)

**By Type**:
- Unit: 5 test cases (23%)
- Integration: 17 test cases (77%)

---

## 9. Approvals

| Role | Name | Date | Signature |
|------|------|------|-----------|
| Test Lead | Xiyu Guan | Oct 25, 2025 | _Approved_ |
| Developer | Xiyu Guan | Oct 25, 2025 | _Approved_ |
| Project Owner | Xiyu Guan | Oct 25, 2025 | _Approved_ |

---

## 10. Notes and Comments

- This is the first test cycle focusing on foundational functionality
- No model weights are required for these tests
- All tests are automated using pytest
- Coverage target is conservative (60%) for first cycle
- Subsequent cycles will add model inference and performance tests

---

**Document Version**: 1.0  
**Last Updated**: October 25, 2025  
**Next Review**: October 27, 2025

