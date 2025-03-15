import pandas as pd

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

df = pd.DataFrame(data)
# Mengubah nama kolom sesuai legenda
df = df.rename(columns={
    "Nama Kecamatan": "KEC",
    "Nama Kelurahan": "KEL",
    "Konfirmasi Positif": "KP",
    "Konfirmasi Meninggal": "KM",
    "Konfirmasi Isolasi Mandiri": "KIM"
})

# Mengurutkan data berdasarkan kecamatan dan kelurahan
df = df.sort_values(by=["KEC", "KEL"]).reset_index(drop=True)

# Membuat DataFrame legenda
legend_df = pd.DataFrame({
  "LEGEND": [""],
    "KEC": ["Nama Kecamatan"],
    "KEL": ["Nama Kelurahan"],
    "KP": ["Konfirmasi Positif"],
    "KM": ["Konfirmasi Meninggal"],
    "KIM": ["Konfirmasi Isolasi Mandiri"]
})

# Mengubah index menjadi mulai dari 1
df.index = df.index + 1

# Menyimpan hasil ke dalam file Excel dengan tabel legenda di atas
with pd.ExcelWriter("grouped_covid19.xlsx", engine="xlsxwriter") as writer:
    legend_df.to_excel(writer, sheet_name="Sheet1", index=False, startrow=0)
    df.to_excel(writer, sheet_name="Sheet1", startrow=3)  # Menampilkan data berdasarkan kelurahan

# Menampilkan hasil dengan legenda
print(legend_df)
print(df)
