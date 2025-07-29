# Modul-Wrapper

Modul Wrapper Adalah Modul Untuk Menyimpan Semua Library Yang Akan Digunakan Dalam Bentuk Dictionary Guna Menghindari Crash Karena Penamaan Class atau Function Yang Sama Antar Library. 

## Example

Tanpa Menggunakan Deklarasi Khusus
```python
from Modul_Wrapper import Wrap

modul = Wrap(modul_path="modul.json")
datetime = modul.modul['datetime'].datetime.now().strftime("%H:%M")
print(datetime)
```

Menggunakan Deklarasi Khusus
```python
from Modul_Wrapper import Wrap

modul = Wrap(modul_path="modul.json")
datetime = modul.modul['modul_jam'].datetime.now().strftime("%H:%M")
print(datetime)
```
## Konfigurasi Modul


| Field | Description                |
| :-------- | :------------------------- |
| `folder` | Nama Library / Lokasi File Dimana Class / Function Disimpan |
| `file` |  Nama File Library / Class / Function |
| `class` |  Nama Class / Function Yang Akan Dipanggil |
| `defined` |  Akan Disimpan Menggunakan Deklarasi Khusus |

**NB: Jika Field "defined" di isi "" atau di isi Kosong, Maka Yang Untuk Memanggil Library Yang Kita Set Bisa Menggunakan "class"**

## Load / Import Library

Tanpa Menggunakan Deklarasi Khusus
```python
modul = Wrap(modul_path="modul.json")
# modul_path adalah lokasi Dimana Konfigurasi Modul Disimpan

datetime = modul.modul['datetime'].datetime.now().strftime("%H:%M")
# Memanggil Modul Dengan class "datetime" kemudian Panggil Fungsi datetime.now()
print(datetime)

datetime = modul.modul['modul_jam'].datetime.now().strftime("%H:%M")
# Memanggil Modul Dengan defined "datetime" kemudian Panggil Fungsi datetime.now()
print(datetime)
```
