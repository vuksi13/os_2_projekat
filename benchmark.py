import os
import time
import shutil
import csv
from minio import Minio

klijent = Minio("127.0.0.1:9005", access_key="minioadmin", secret_key="minioadmin", secure=False)
bucket = "projekat-os"

izvor = "bench_source"
cilj = "bench_dest"

os.makedirs(izvor, exist_ok=True)
os.makedirs(cilj, exist_ok=True)

scenariji = [
    (100, 10, "100x10KB"),
    (500, 10, "500x10KB"),
    (1, 1024, "1x1MB"),
    (10, 1024, "10x1MB"),
    (50, 1024, "50x1MB"),
    (1, 10240, "1x10MB"),
    (5, 10240, "5x10MB"),
    (1, 51200, "1x50MB"),
    (5, 51200, "5x50MB"),
    (1, 102400, "1x100MB")
]

rezultati = []
broj_iteracija = 10

for it in range(1, broj_iteracija + 1):
    print(f"Iteracija {it}/{broj_iteracija}")
    
    for broj_fajlova, velicina_kb, naziv in scenariji:
        ukupno_mb = (broj_fajlova * velicina_kb) / 1024
        
        for i in range(broj_fajlova):
            with open(f"{izvor}/temp_{i}.bin", "wb") as f:
                f.write(os.urandom(velicina_kb * 1024))
        
        pocetak = time.time()
        for i in range(broj_fajlova):
            shutil.copy(f"{izvor}/temp_{i}.bin", f"{cilj}/temp_{i}.bin")
        vreme_lokalno = time.time() - pocetak
        rezultati.append([it, naziv, "Lokalno", broj_fajlova, ukupno_mb, vreme_lokalno])
        
        pocetak = time.time()
        for i in range(broj_fajlova):
            klijent.fput_object(bucket, f"obj_{it}_{i}.bin", f"{izvor}/temp_{i}.bin")
        vreme_minio = time.time() - pocetak
        rezultati.append([it, naziv, "MinIO", broj_fajlova, ukupno_mb, vreme_minio])
        
        for i in range(broj_fajlova):
            if os.path.exists(f"{izvor}/temp_{i}.bin"): os.remove(f"{izvor}/temp_{i}.bin")
            if os.path.exists(f"{cilj}/temp_{i}.bin"): os.remove(f"{cilj}/temp_{i}.bin")

with open("rezultati_prosiriti.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Iteracija", "Scenario", "Sistem", "Broj_fajlova", "Velicina_MB", "Vreme_s"])
    writer.writerows(rezultati)

shutil.rmtree(izvor)
shutil.rmtree(cilj)
print("Gotovo! Podaci su sačuvani u rezultati_prosiriti.csv")