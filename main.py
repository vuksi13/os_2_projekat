from minio import Minio
from minio.error import S3Error
import os

fajl = "tekst.txt"
with open (fajl,"w",encoding="utf-8") as f: f.write("aaa")
print("napravljen fajl")
with open ("fajl1.txt","w",encoding="utf-8") as f: f.write("aaa")
print("napravljen fajl1")
with open("fajl2.txt", "w") as f2: f2.write("bbb")
print("napravljen fajl2")

klijent = Minio("127.0.0.1:9005",access_key="minioadmin",secret_key="minioadmin",secure = False)
print("povezan na MinIO server.")


ime_baketa = "projekat-os"

try:
    klijent.fput_object(ime_baketa,"fajl.txt",fajl)
    klijent.fput_object(ime_baketa,"fajl_na_serveru1.txt","tekst.txt")
    klijent.fput_object(ime_baketa,"fajl_na_serveru2.txt","fajl2.txt")
    print("uspesan upload")
except S3Error as e:
    print(f"Greška prilikom uploada: {e}")

try:
    objekti = klijent.list_objects("projekat-os")
    for obj in objekti:
        print(f"nasao fajl: {obj.object_name}")
        print(f"velicine : {obj.size} bajtova")
        print("------------")
except S3Error as e:
    print(f"Greška prilikom listanja: {e}")

try:
    klijent.fget_object(ime_baketa, "fajl_na_serveru1.txt", "skinuto_fajl1.txt")
    klijent.fget_object(ime_baketa, "fajl_na_serveru2.txt", "skinuto_fajl2.txt")
    print("Skinuta oba fajla.")
except S3Error as e:
    print(f"Greška prilikom preuzimanja fajlova: {e}")

try:
    klijent.remove_object(ime_baketa, "fajl_na_serveru1.txt")
    print("Obrisan fajl_na_serveru1.txt sa servera.")
except S3Error as e:
    print(f"Greška prilikom brisanja: {e}")
print("------------")
print("\nOstalo na serveru:")

try:
    for obj in klijent.list_objects(ime_baketa):
        print(f"- {obj.object_name}")
    for obj in klijent.list_objects(ime_baketa):
        if obj.object_name != "fajl.txt":
            klijent.remove_object(ime_baketa, obj.object_name)
            print(f"Automatski obrisan: {obj.object_name}")
except S3Error as e:
    print(f"Greška prilikom finalnog čišćenja: {e}")