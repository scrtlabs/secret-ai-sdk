#!/bin/bash
# Secret AI SDK - PyPI Publishing Script
# =====================================

set -e  # Exit on any error

echo "🚀 Secret AI SDK PyPI Publishing Script"
echo "======================================="

# Check if we're in the right directory
if [[ ! -f "pyproject.toml" ]] || [[ ! -d "secret_ai_sdk" ]]; then
    echo "❌ Error: Please run this script from the secret-ai-sdk root directory"
    exit 1
fi

# Step 1: Clean previous builds
echo "🧹 Cleaning previous builds..."
rm -rf dist/ build/ *.egg-info/

# Step 2: Build the package
echo "🔨 Building package..."
python -m build

# Step 3: Validate the package
echo "🔍 Validating package..."
python -m twine check dist/*

# Step 4: Show current version
echo "📦 Package version:"
python -c "import secret_ai_sdk; print(f'Version: {secret_ai_sdk.__version__}')"

# Step 5: Ask user what to do
echo ""
echo "Choose publishing option:"
echo "1) Test PyPI (recommended first)"
echo "2) Production PyPI"
echo "3) Exit"
read -p "Enter choice (1-3): " choice

case $choice in
    1)
        echo "📤 Uploading to Test PyPI..."
        echo "Make sure you have configured your .pypirc file or have TWINE_PASSWORD set"
        twine upload --repository testpypi dist/*
        echo ""
        echo "✅ Uploaded to Test PyPI!"
        echo "Test install with: pip install --index-url https://test.pypi.org/simple/ secret-ai-sdk"
        ;;
    2)
        echo "📤 Uploading to Production PyPI..."
        echo "⚠️  This is PRODUCTION - make sure you've tested on Test PyPI first!"
        read -p "Are you sure? (y/N): " confirm
        if [[ $confirm =~ ^[Yy]$ ]]; then
            twine upload dist/*
            echo ""
            echo "🎉 Successfully published to PyPI!"
            echo "Your package is now available at: https://pypi.org/project/secret-ai-sdk/"
            echo "Install with: pip install secret-ai-sdk"
        else
            echo "Publishing cancelled."
        fi
        ;;
    3)
        echo "Exiting..."
        exit 0
        ;;
    *)
        echo "Invalid choice. Exiting..."
        exit 1
        ;;
esac

echo ""
echo "📋 Next steps:"
echo "• Test the published package: pip install secret-ai-sdk"
echo "• Create a git tag: git tag v$(python -c 'import secret_ai_sdk; print(secret_ai_sdk.__version__)')"
echo "• Push the tag: git push origin --tags"
echo "• Update version numbers for next release"