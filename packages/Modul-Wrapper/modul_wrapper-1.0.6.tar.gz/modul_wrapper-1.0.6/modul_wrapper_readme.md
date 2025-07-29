# Modul Wrapper

Modul Wrapper adalah utilitas Python yang memungkinkan kita memuat banyak modul, class, atau fungsi dari file konfigurasi JSON. Tujuan utamanya adalah untuk mencegah bentrok penamaan (alias) dan menjaga kode tetap modular dan fleksibel.

Modul ini juga berguna untuk sistem dinamis dan environment besar dengan banyak dependensi agar tetap bersih dan terkontrol.

Modul ini mendukung:
- Modul lokal (buatan sendiri)
- Modul standar Python
- Library eksternal (seperti `requests`, `pandas`, dll)

---

## Contoh Penggunaan

### Struktur Folder (Contoh)
```bash
project/
│
├── cfg/
│   └── modul.min
│
├── Testing/
│   └── v1/
│       └── modul1.py
│
└── app.py
```

### Isi File: Testing/v1/modul1.py

```python
class Testing:
    def say(self):
        return "Encrypted!"
```

### Isi File: cfg/modul.min
```json
{
  "modul": [
    {
      "folder": "Testing",
      "file": ["v1", "modul1"],
      "module": "modul1",
      "function_name": "Testing",
      "alias": "test"
    },
    {
      "folder": "",
      "file": [],
      "module": "os",
      "function_name": "listdir",
      "alias": ""
    },
    {
      "folder": "",
      "file": [],
      "module": "requests",
      "function_name": "",
      "alias": ""
    },
    {
      "folder": "",
      "file": [],
      "module": "datetime",
      "function_name": "datetime",
      "alias": "jam"
    }
  ]
}
```

### Contoh Testing: app.py

```python
from Modul_Wrapper import Wrap

loader = Wrap("./cfg/modul.min", debug=False)

Test = loader.Load('test')
obj = Test()
print(obj.say())  # Encrypted!

driver = loader.Load('requests')
osmod = loader.Load("listdir")
jam = loader.Load('jam')

print(jam.now().strftime("%H:%M:%S"))  # Waktu saat ini
loader.Reload('requests')
print(osmod())  # List isi direktori

print(loader.ShowModul())  # Menampilkan semua objek modul yang sudah dimuat
print(loader.ShowAlias())  # Menampilkan alias dan asal modul
```

### Output yang Dihasilkan (Contoh)
```bash
Encrypted!
21:13:58
['cfg', 'kimin', 'modul.min', 'test.py', 'Testing', 'v1.py']
{'test': <class 'Testing.v1.app.Testing'>, 'listdir': <built-in function listdir>, 'jam': <class 'datetime.datetime'>, 'requests': <module 'requests' from '...'>}
{'test': 'Testing.v1.app', 'listdir': 'listdir', 'requests': '', 'datetime': 'datetime', 'jam': 'datetime'}
```

## Struktur Konfigurasi Modul (`modul`)

Setiap entri dalam konfigurasi harus mengikuti struktur berikut:

| Key             | Tipe Data       | Wajib | Contoh                          | Deskripsi                                                                                      |
|------------------|------------------|--------|----------------------------------|------------------------------------------------------------------------------------------------|
| `folder`         | `string`         | ❌     | `"Testing"` atau `""`            | Folder dasar tempat file modul disimpan (untuk modul lokal). Kosongkan jika modul adalah pustaka standar atau eksternal. |
| `file`           | `list[string]`   | ❌     | `["v1", "app"]` atau `[]`        | Daftar subfolder/nama file `.py` (tanpa ekstensi). Kosongkan untuk pustaka bawaan atau eksternal. |
| `module`         | `string`         | ✅     | `"app"`, `"os"`, `"requests"`    | Nama file modul atau nama pustaka. Bisa juga nama modul bawaan seperti `os`, `datetime`, dll. |
| `function_name`  | `string`         | ✅     | `"Testing"`, `"listdir"`, `"datetime"` | Nama objek (fungsi, class, dsb) yang akan diambil dari modul. Bisa kosong jika ingin mengimpor seluruh modul. |
| `alias`          | `string`         | ❌     | `"test"`, `"jam"`                | Nama alias untuk objek yang diimpor. Jika kosong, akan otomatis menggunakan nama objek atau modul. |

---

### Contoh Konfigurasi dan Artinya
| Kasus                             | Konfigurasi                                                                                                    | Import Python Yang Setara                               |
|-----------------------------------|------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------|
| Modul lokal                       | `{ "folder": "Testing", "file": ["v1", "app"], "module": "app", "function_name": "Testing", "alias": "test" }` | `from Testing.v1.app import Testing as test`            |
| Fungsi dari modul standar         | `{ "folder": "", "file": [], "module": "os", "function_name": "listdir", "alias": "" }`                        | `from os import listdir`                                |
| Seluruh modul eksternal           | `{ "folder": "", "file": [], "module": "requests", "function_name": "", "alias": "" }`                         | `import requests`                                       |
| Objek global tanpa modul eksplisit| `{ "folder": "", "file": [], "module": "", "function_name": "datetime", "alias": "" }`                         | `import datetime` (mengandalkan konteks global Python)  |
| Fungsi dalam modul eksternal      | `{ "folder": "", "file": [], "module": "datetime", "function_name": "datetime", "alias": "jam" }`             | `from datetime import datetime as jam`                  |

---

## Mekanisme Alias
- Jika `alias` **tidak diisi**, maka:
    - Jika `function_name` tersedia: `alias = function_name`
    - Jika `function_name` kosong: `alias = module`
    - Tujuan alias adalah agar kamu bisa memanggil objek yang sudah di-*load* seperti:

        ```python
            wrap = Wrap("modul.json")
            jam = wrap.Load("jam")
            print(jam.now())
        ```

## Metode Penting
- Wrap(modul_path, debug=False) → Membuat objek loader dari file JSON dan menerima parameter opsional debug. Jika debug=True, informasi debug akan ditampilkan selama proses pemuatan modul.
- .Load(alias) → Mengambil objek berdasarkan alias
- .Reload(alias) → Me-reload modul tertentu
- .ShowModul() → Menampilkan dict objek yang sudah dimuat
- .ShowAlias() → Menampilkan semua alias beserta asalnya

