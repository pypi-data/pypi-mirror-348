from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ai-zap",
    version="1.0.4",  # Увеличиваем версию
    packages=find_packages(),
    package_data={
        'ai_zap': ['*.txt', '*.py'],
    },
    include_package_data=True,
    install_requires=[
        "openai>=1.0.0",
    ],
    author="Danila",
    author_email="your.email@example.com",  # Замените на ваш email
    description="Библиотека для работы с ИИ и практическими заданиями",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/ai-zap",  # Замените на URL вашего репозитория
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
) 