import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
from math import sqrt

# Mendefinisikan data
kelurahan = [
    "Cengkareng Barat", "Cengkareng Timur", "Duri Kosambi", "Kapuk", 
    "Kedaung Kali Angke", "Rawa Buaya", "Grogol", "Jelambar", 
    "Jelambar Baru", "Tanjung Duren Selatan", "Tanjung Duren Utara", 
    "Tomang", "Wijaya Kusuma", "Kalideres", "Kamal", "Pegadungan", 
    "Semanan", "Tegal Alur", "Kebon Jeruk", "Kedoya Selatan", 
    "Kedoya Utara", "Duri Kepa", "Kelapa Dua", "Sukabumi Selatan", 
    "Sukabumi Utara", "Jati Pulo", "Kemanggisan", "Kota Bambu Selatan", 
    "Kota Bambu Utara", "Palmerah", "Slipi"
]

konfirmasi_positif = [
    8676, 8926, 7437, 9480, 3146, 5648, 3704, 5557, 5377, 5138, 
    3869, 4304, 4642, 7467, 2538, 8462, 3939, 6774, 8410, 4402, 
    5618, 8347, 3483, 3377, 4362, 2603, 5113, 2378, 2252, 8175, 3107
]

konfirmasi_sembuh = [
    8556, 8807, 7349, 9291, 3107, 5577, 3660, 5494, 5327, 5088, 
    3831, 4265, 4586, 7368, 2497, 8397, 3883, 6689, 8316, 4343, 
    5557, 8260, 3439, 3340, 4311, 2552, 5048, 2338, 2213, 8036, 3074
]

# Langkah 1: Implementasi manual regresi linear
# Mengubah list menjadi array numpy untuk perhitungan yang lebih mudah
X = np.array(konfirmasi_positif)
y = np.array(konfirmasi_sembuh)

# Menghitung parameter yang dibutuhkan untuk rumus regresi linear
n = len(X)
sum_X = np.sum(X)
sum_y = np.sum(y)
sum_X_squared = np.sum(X**2)
sum_XY = np.sum(X * y)

# Menghitung koefisien (a) dan konstanta (b) menggunakan rumus
a = (n * sum_XY - sum_X * sum_y) / (n * sum_X_squared - sum_X**2)
b = (sum_y - a * sum_X) / n

print("Hasil Regresi Linear:")
print(f"Model: y = {b:.5f} + {a:.5f}X")
print(f"Koefisien (a): {a:.5f}")
print(f"Konstanta (b): {b:.5f}")

# Langkah 2: Membuat prediksi
y_pred = b + a * X

# Membuat dataframe untuk membandingkan nilai aktual vs prediksi
results_df = pd.DataFrame({
    'Kelurahan': kelurahan,
    'Konfirmasi Positif': X,
    'Konfirmasi Sembuh (Aktual)': y,
    'Konfirmasi Sembuh (Prediksi)': y_pred.round(2),
    'Error': (y - y_pred).round(2),
    'Error^2': ((y - y_pred)**2).round(2)
})

# Langkah 3: Menghitung RMSE
errors = y - y_pred
squared_errors = errors**2
mse = np.mean(squared_errors)
rmse = np.sqrt(mse)

print(f"\nMetrik Error:")
print(f"Mean Squared Error (MSE): {mse:.5f}")
print(f"Root Mean Squared Error (RMSE): {rmse:.5f}")

# Langkah 4: Menghitung R-squared (akurasi)
y_mean = np.mean(y)
ss_total = np.sum((y - y_mean)**2)
ss_residual = np.sum(squared_errors)
r_squared = 1 - (ss_residual / ss_total)

print(f"\nMetrik Akurasi:")
print(f"R-squared: {r_squared:.5f}")
print(f"Akurasi: {r_squared * 100:.3f}%")

# Langkah 5: Visualisasi data dan garis regresi
plt.figure(figsize=(12, 8))
plt.scatter(X, y, color='blue', label='Data Aktual')
plt.plot([min(X), max(X)], [b + a*min(X), b + a*max(X)], color='red', label='Garis Regresi')
plt.xlabel('Konfirmasi Positif')
plt.ylabel('Konfirmasi Sembuh')
plt.title('Regresi Linear: Kasus COVID-19 vs Kesembuhan')
plt.legend()
plt.grid(True)

# Menambahkan teks pada plot yang menunjukkan persamaan dan akurasi
equation_text = f"y = {b:.2f} + {a:.2f}X\nR² = {r_squared:.5f}\nRMSE = {rmse:.2f}"
plt.text(0.05, 0.95, equation_text, transform=plt.gca().transAxes, 
         bbox=dict(facecolor='white', alpha=0.7))

# Menyimpan plot ke file
plt.savefig('covid_regression.png')
plt.show()

# Menampilkan tabel hasil
print("\nDetail untuk Setiap Kelurahan:")
print(results_df.to_string())