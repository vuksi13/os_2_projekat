from minio import Minio
import os

fajl = "tekst.txt"
with open (fajl,"w",encoding="utf-8") as f: f.write("aaa")
print("napravljen fajl")
with open ("fajl1.txt","w",encoding="utf-8") as f: f.write("aaa")
print("napravljen fajl1")
with open("fajl2.txt", "w") as f2: f2.write("bbb")
print("napravljen fajl2")

klijent = Minio("127.0.0.1:9005",access_key="minioadmin",secret_key="minioadmin",secure = False)
print("Povezan na MinIO server.")


ime_baketa = "projekat-os"
klijent.fput_object(ime_baketa,"fajl.txt",fajl)
klijent.fput_object(ime_baketa,"fajl_na_serveru1.txt","tekst.txt")
klijent.fput_object(ime_baketa,"fajl_na_serveru2.txt","fajl2.txt")

objekti = klijent.list_objects("projekat-os")
for obj in objekti:
    print(f"nasao fajl: {obj.object_name}")
    print(f"velicine : {obj.size} bajtova")
    print("------------")

klijent.fget_object(ime_baketa, "fajl_na_serveru1.txt", "skinuto_fajl1.txt")
klijent.fget_object(ime_baketa, "fajl_na_serveru2.txt", "skinuto_fajl2.txt")
print("Skinuta oba fajla.")
print("------------")

klijent.remove_object(ime_baketa, "cloud_fajl1.txt")
print("Obrisan cloud_fajl1.txt sa servera.")
print("\nOstalo na serveru:")

for obj in klijent.list_objects(ime_baketa):
    print(f"- {obj.object_name}")


for obj in klijent.list_objects(ime_baketa):
    if obj.object_name != "fajl.txt":
        klijent.remove_object(ime_baketa, obj.object_name)
        print(f"Obrisan: {obj.object_name}")