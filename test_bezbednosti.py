from minio import Minio
from minio.error import S3Error

client = Minio("127.0.0.1:9005", access_key="student", secret_key="student123", secure=False)
ime_baketa = "projekat-os"

with open("hak.txt", "w") as f: f.write("Pokusaj uploada")
print("pokusavam upload")
try:
    client.fput_object(ime_baketa, "hak_na_serveru.txt", "hak.txt")
    print("Proslo!")
except S3Error as e:
    print(f"Blokirano! Server kaze: {e.code}")