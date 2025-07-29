import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="apple-style-ui",  # パッケージ名（pip でインストールする際に使用）
    version="0.1.1",  # バージョン
    author="Yamamoto Atsushi",  # あなたの名前
    author_email="nasebanaru1975@gmail.com",  # あなたのメールアドレス
    description="A library of Apple-style UI components for PyQt6.",  # 簡単な説明
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yamamoto-atsushi/AppleUI.git",  # プロジェクトの GitHub リポジトリの URL (もしあれば)
    packages=setuptools.find_packages(where="."),  # パッケージを自動検出
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # 例: MIT License
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",  # 必要な Python のバージョン
    install_requires=[
        "PyQt6 >= 6.0",  # 依存関係（PyQt6）とそのバージョン
    ],
)
