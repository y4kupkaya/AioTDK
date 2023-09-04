# 🔎 AioTDK

## 📝 Description

Aiotdk is an async library written to search for data in the TDK Dictionary.

### 📦 Installation

```bash
pip install aiotdk
```

## 📖 Documentation

### 📚 Usage

```python
import asyncio
from aiotdk.gts import search

async def main():
    result = await search("elma")
    print(result)

asyncio.run(main())
```

## 📜 License

This project is licensed under the NU AFFERO GENERAL PUBLIC LICENSE (v3) - see the [LICENSE](LICENSE) file for details.

## 🔖 Disclaimer

This project is not affiliated with TDK in any way. It is a project created for educational purposes.

## ✒ Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## 📌 Authors

- [**Yakup Kaya**](https://yakupkaya.net.tr)

## 🗃 Acknowledgments

- [**TDK**](https://sozluk.gov.tr/)

## 📮 Credit's

- [**TDK**](https://sozluk.gov.tr/) - For the data used in this project.
- [**TDK-PY**](https://github.com/emreozcan/tdk-py/) - For the inspiration of this project.

## 🗃 TODO

- Add more tests
- Add more documentation
- Add more examples
- Add more features
