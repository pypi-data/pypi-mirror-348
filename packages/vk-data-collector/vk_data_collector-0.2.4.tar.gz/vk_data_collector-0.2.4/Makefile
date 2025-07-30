.PHONY: install test pypi clean clean-cmd

install:
	uv sync

test:
	pytest

pypi:
	python -m build
	python -m twine upload dist/*

clean:
	rm -rf dist
	rm -rf .pytest_cache
	rm -rf **/__pycache__ **/**/__pycache__

clean-cmd:
	cmd /c "if exist dist rmdir /s /q dist"
	cmd /c "if exist .pytest_cache rmdir /s /q .pytest_cache"
	cmd /c "for /d /r . %%d in (__pycache__) do @if exist "%%d" rmdir /s /q "%%d""
