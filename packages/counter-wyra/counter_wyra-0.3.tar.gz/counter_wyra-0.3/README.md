# Counter Thing
Run 
```python
pip install counter_wyra
```
to install the thing.

## For Maintainers: Setting up Trusted Publishing

To enable trusted publishing for this package on PyPI, follow these steps:

1. Log in to your PyPI account
2. Navigate to the "counter_wyra" project
3. Go to the "Settings" tab
4. Under "Publishing", select "Add a new publisher"
5. Choose "GitHub Actions"
6. Enter the following details:
   - Owner: I4LYT
   - Repository name: counter-thing
   - Workflow name: python-publish.yml
   - Environment name: pypi
7. Save the configuration

This will allow GitHub Actions to publish new versions of the package to PyPI without requiring API tokens.
