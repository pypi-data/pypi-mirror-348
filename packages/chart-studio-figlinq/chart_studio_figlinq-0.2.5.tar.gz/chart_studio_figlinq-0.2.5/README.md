# Chart Studio Figlinq python library

This package contains utilities for interfacing with Plotly's Chart Studio and Figlinq services. The project has been cloned from [chart-studio 1.1.0](https://pypi.org/project/chart-studio/). The original package has been modified so that credentials and configuration can be set from environment variables (see chart_studio.tools.get_credentials() and chart_studio.tools.get_config()).

# Release

```bash
rm -r dist/* && python3 setup.py sdist bdist_wheel && twine upload --repository pypi dist/*
```