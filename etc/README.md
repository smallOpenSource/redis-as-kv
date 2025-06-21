# Documentation and Development Files

This folder contains additional documentation and development-related files for Redis KeyVault.

## 📁 Files Description

### 🚀 Release Documentation
- **`GITHUB_RELEASE.md`** - GitHub release description template
- **`RELEASE_NOTES.md`** - Detailed release notes for v1.0.0
- **`RELEASE_CHECKLIST.md`** - Release preparation checklist

### 🛠️ Development Documentation  
- **`DEPLOYMENT.md`** - Complete deployment and build guide

### 🔧 Build Scripts (Windows)
- **`build-whl.cmd`** - Build wheel package with cleanup and validation
- **`test-package.cmd`** - Test the built package installation and functionality  
- **`clean-build.cmd`** - Clean all build artifacts and cache files

## 📋 Usage

### For Building Packages
```cmd
# Clean previous builds
etc\clean-build.cmd

# Build new wheel package  
etc\build-whl.cmd

# Test the built package
etc\test-package.cmd
```

### For Maintainers
These files are used by project maintainers for:
- Creating GitHub releases
- Building and deploying packages
- Following release procedures
- Maintaining documentation standards

### For Contributors
Contributors can reference these files to understand:
- Release process and standards
- Deployment procedures
- Documentation formatting

## 🔗 Quick Links

- **Main Documentation**: [README.md](../README.md)
- **Korean Documentation**: [README-ko.md](../README-ko.md)
- **Application Examples**: [app/README.md](../app/README.md)
- **Sample Configurations**: [samples/README.md](../samples/README.md)

---

*These files are maintained separately to keep the main project directory clean and focused on user-facing documentation.*
