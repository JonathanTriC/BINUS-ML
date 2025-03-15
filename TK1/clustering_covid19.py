import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Membuat DataFrame berdasarkan data dalam tabel
data = {
    "Nama Kecamatan": ["Cengkareng", "Cengkareng", "Cengkareng", "Cengkareng", "Cengkareng", "Cengkareng",
                        "Grogol Petamburan", "Grogol Petamburan", "Grogol Petamburan", "Grogol Petamburan", "Grogol Petamburan", "Grogol Petamburan", "Grogol Petamburan",
                         "Kali Deres", "Kali Deres", "Kali Deres", "Kali Deres", "Kali Deres",
                         "Kebon Jeruk", "Kebon Jeruk", "Kebon Jeruk", "Kebon Jeruk", "Kebon Jeruk", "Kebon Jeruk", "Kebon Jeruk",
                         "Palmerah", "Palmerah", "Palmerah", "Palmerah", "Palmerah", "Palmerah"],
    "Nama Kelurahan": ["Cengkareng Barat", "Cengkareng Timur", "Duri Kosambi", "Kapuk", "Kedaung Kali Angke", "Rawa Buaya",
                        "Grogol", "Jelambar", "Jelambar Baru", "Tanjung Duren Selatan", "Tanjung Duren Utara", "Tomang", "Wijaya Kusuma",
                        "Kalideres", "Kamal", "Pegadungan", "Semanan", "Tegal Alur",
                        "Duri Kepa", "Kebon Jeruk", "Kedoya Selatan", "Kedoya Utara", "Kelapa Dua", "Sukabumi Selatan", "Sukabumi Utara",
                        "Jati Pulo", "Kemanggisan", "Kota Bambu Selatan", "Kota Bambu Utara", "Palmerah", "Slipi"],
    "Konfirmasi Positif": [8676, 8926, 7437, 9480, 3146, 5648,
                           3704, 5557, 5377, 5138, 3869, 4304, 4642,
                           7467, 2538, 8462, 3939, 6774,
                           8347, 8410, 4402, 5618, 3483, 3377, 4362,
                           2603, 5113, 2378, 2252, 8175, 3107],
    "Konfirmasi Meninggal": [120, 119, 88, 189, 39, 71,
                              44, 63, 50, 50, 38, 39, 56,
                              99, 41, 65, 56, 85,
                              87, 94, 59, 61, 44, 37, 51,
                              51, 65, 40, 39, 139, 33],
    "Konfirmasi Isolasi Mandiri": [104, 89, 81, 62, 32, 72,
                                    53, 89, 84, 123, 74, 93, 72,
                                    86, 28, 169, 57, 66,
                                    173, 136, 87, 76, 62, 55, 53,
                                    34, 85, 13, 13, 91, 24]
}

# Konversi ke DataFrame
df = pd.DataFrame(data)

# Menggunakan hanya fitur numerik untuk clustering
X = df[["Konfirmasi Positif", "Konfirmasi Meninggal", "Konfirmasi Isolasi Mandiri"]]

# Normalisasi data agar lebih seimbang
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# K-Means Clustering dengan 3 Cluster
kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
df["Cluster"] = kmeans.fit_predict(X_scaled)

# Menentukan zona berdasarkan nilai centroid
cluster_centers = kmeans.cluster_centers_
sorted_clusters = sorted(range(len(cluster_centers)), key=lambda k: np.sum(cluster_centers[k]))

# Mapping cluster ke Zona
zone_mapping = {sorted_clusters[2]: "Zona Merah", sorted_clusters[1]: "Zona Kuning", sorted_clusters[0]: "Zona Hijau"}
df["Zona"] = df["Cluster"].map(zone_mapping)

# Warna untuk setiap zona
colors = {"Zona Merah": "red", "Zona Kuning": "orange", "Zona Hijau": "green"}

# Menyusun tabel daftar kelurahan berdasarkan zona
zona_merah = df[df["Zona"] == "Zona Merah"]["Nama Kelurahan"].tolist()
zona_kuning = df[df["Zona"] == "Zona Kuning"]["Nama Kelurahan"].tolist()
zona_hijau = df[df["Zona"] == "Zona Hijau"]["Nama Kelurahan"].tolist()

# Menentukan panjang maksimum dari daftar zona
max_length = max(len(zona_merah), len(zona_kuning), len(zona_hijau))

# Menyesuaikan panjang daftar dengan menambahkan string kosong jika perlu
zona_merah += [""] * (max_length - len(zona_merah))
zona_kuning += [""] * (max_length - len(zona_kuning))
zona_hijau += [""] * (max_length - len(zona_hijau))

# Membuat tabel daftar kelurahan berdasarkan zona
zona_df = pd.DataFrame({
    "Zona Merah": zona_merah,
    "Zona Kuning": zona_kuning,
    "Zona Hijau": zona_hijau
})
zona_df.index = zona_df.index + 1

# Menampilkan tabel zona tanpa NaN
print(zona_df)

# Visualisasi hasil clustering
plt.figure(figsize=(12, 6))

for zona, color in colors.items():
    subset = df[df["Zona"] == zona]
    plt.scatter(subset["Konfirmasi Positif"], subset["Konfirmasi Meninggal"], label=zona, color=color)

plt.xlabel("Konfirmasi Positif")
plt.ylabel("Konfirmasi Meninggal")
plt.title("Clustering Zona COVID-19 di Jakarta Barat")
plt.legend()
plt.grid(True)
plt.show()
