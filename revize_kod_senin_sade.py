import pandas as pd
import matplotlib.pyplot as plt
import math

# CSV dosyasını oku
df = pd.read_csv("Football_Dataset_2015_2025.csv")
veri = df["Shots (Home)"].dropna().tolist()
n = len(veri)

# Ortalama
toplam = 0
for x in veri:
    toplam += x
ortalama = toplam / n

# Medyan
sıralı = sorted(veri)
if n % 2 == 0:
    medyan = (sıralı[n//2 - 1] + sıralı[n//2]) / 2
else:
    medyan = sıralı[n//2]

# Varyans, std sapma, hata
varyans_toplam = 0
for x in veri:
    varyans_toplam += (x - ortalama) ** 2
varyans = varyans_toplam / (n - 1)
std_sapma = varyans ** 0.5
std_hata = std_sapma / math.sqrt(n)

# %95 güven aralığı için yaklaşık t değeri
t_kritik = 1.96
ga_alt = ortalama - t_kritik * std_hata
ga_ust = ortalama + t_kritik * std_hata

# Varyans için yaklaşık güven aralığı
varyans_ga_alt = varyans * 0.80
varyans_ga_ust = varyans * 1.20

# Örneklem büyüklüğü (±0.1 hata payı, %90 güven)
z_skor = 1.645
E = 0.1
gerekli_orneklem = math.ceil((z_skor * std_sapma / E) ** 2)

# Hipotez testi: Ortalama 15 mi?
hipotez_ortalama = 15
t_istatistik = (ortalama - hipotez_ortalama) / std_hata

# Aykırı değer analizi (IQR yöntemi)
q1_index = int(n * 0.25)
q3_index = int(n * 0.75)
q1 = sıralı[q1_index]
q3 = sıralı[q3_index]
iqr = q3 - q1
alt_sinir = q1 - 1.5 * iqr
ust_sinir = q3 + 1.5 * iqr
aykiri_degerler = [x for x in veri if x < alt_sinir or x > ust_sinir]

# Sonuçlar
print("\nİSTATİSTİKSEL SONUÇLAR")
print("------------------------")
print(f"Veri Sayısı: {n}")
print(f"Ortalama: {ortalama:.2f}")
print(f"Medyan: {medyan:.2f}")
print(f"Varyans: {varyans:.2f}")
print(f"Standart Sapma: {std_sapma:.2f}")
print(f"Standart Hata: {std_hata:.4f}")
print(f"%95 Güven Aralığı (Ortalama): [{ga_alt:.2f}, {ga_ust:.2f}]")
print(f"%95 Güven Aralığı (Varyans ~yaklaşık): [{varyans_ga_alt:.2f}, {varyans_ga_ust:.2f}]")
print(f"Gerekli Örneklem (±0.1 hata ile, %90 güven): {gerekli_orneklem}")
print(f"\nHipotez Testi: Ortalama 15 mi?")
print(f"t-İstatistiği: {t_istatistik:.4f}")
print("Karar:", "H0 reddedildi. Ortalama 15'ten farklıdır." if abs(t_istatistik) > t_kritik else "H0 kabul edilir. Ortalama 15 olabilir.")
print(f"\nAykırı Değer Sayısı: {len(aykiri_degerler)}")
if aykiri_degerler:
    print(f"Aykırı Değerler: {aykiri_degerler}")

# Grafikler
plt.figure(figsize=(14, 6))

plt.subplot(1, 2, 1)
plt.hist(veri, bins=20, color='lightblue', edgecolor='black')
plt.title("Ev Sahibi Şut Sayısı (Histogram)")
plt.xlabel("Şut Sayısı")
plt.ylabel("Maç Sayısı")
plt.grid(True, axis='y', linestyle='--', alpha=0.5)

plt.subplot(1, 2, 2)
plt.boxplot(veri, vert=False, patch_artist=True, boxprops=dict(facecolor='orange'))
plt.title("Ev Sahibi Şut Sayısı (Boxplot)")
plt.xlabel("Şut Sayısı")

plt.tight_layout()
plt.show()
