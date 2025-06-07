import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, RadioButtons

# Początkowe wartości
procentPaliwa = 95
masaPoczatkowa = 334.5
predkoscWylotu = 3053
mi = 1253.5
g = 9.81

# Obliczenia wstępne
masaKoncowa = masaPoczatkowa * (1 - procentPaliwa / 100)
deltaM = masaPoczatkowa - masaKoncowa

# Tworzenie wykresu
figura, os = plt.subplots()
plt.subplots_adjust(left=0.25, bottom=0.5, right=0.75)

masa = np.linspace(masaKoncowa, masaPoczatkowa, 1000)
predkosc = (predkoscWylotu * np.log(masaPoczatkowa / masa)) - (g * (deltaM / mi))
[linia] = os.plot(masa, predkosc, lw=2, color='maroon')

os.set_title("Zależność prędkości rakiety od pozostałej masy w polu grawitacyjnym")
os.set_xlabel("Masa rakiety [t]")
os.set_ylabel("Prędkość [m/s]")
os.grid(True, linestyle="--", alpha=0.5)

# Suwaki
ax_masa = plt.axes([0.25, 0.4, 0.5, 0.03])
ax_predkosc = plt.axes([0.25, 0.3, 0.5, 0.03])
ax_paliwo = plt.axes([0.25, 0.2, 0.5, 0.03])
ax_mi = plt.axes([0.25, 0.1, 0.5, 0.03])

ax_tabela = plt.axes([0.8, 0.2, 0.18, 0.15])
ax_tabela.axis('off')
tekst_info = ax_tabela.text(0, 1, "", verticalalignment='top', fontsize=10, family="monospace")

suwakMasaPoczatkowa = Slider(ax_masa, 'Masa początkowa [t]', 1, 500, valinit=masaPoczatkowa, color="maroon")
suwakPredkoscWylotu = Slider(ax_predkosc, 'Prędkość wylotu [m/s]', 1000, 4000, valinit=predkoscWylotu, color="maroon")
suwakProcentPaliwa = Slider(ax_paliwo, 'Paliwo [%]', 80, 99, valinit=procentPaliwa, color="maroon")
suwakMi = Slider(ax_mi, "Spalanie [kg/s]", 250, 2000, valinit=mi, color="maroon")

# Funkcja aktualizacji wykresu
def aktualizujDane(_):
    masaPoczatkowa = suwakMasaPoczatkowa.val
    procentPaliwa = suwakProcentPaliwa.val / 100
    masaKoncowa = masaPoczatkowa * (1 - procentPaliwa)
    predkoscWylotu = suwakPredkoscWylotu.val
    deltaM = masaPoczatkowa - masaKoncowa
    mi = suwakMi.val
    masa = np.linspace(masaKoncowa, masaPoczatkowa, 1000)
    predkosc = (predkoscWylotu * np.log(masaPoczatkowa / masa)) - (g * (deltaM / mi))
    linia.set_xdata(masa)
    linia.set_ydata(predkosc)
    os.relim()
    os.autoscale_view()
    figura.canvas.draw_idle()

    v_biezaca = predkosc[0]
    masaCelowa = 250
    if masaCelowa >= masaKoncowa and masaCelowa <= masaPoczatkowa:
        predkoscDla250 =(predkoscWylotu * np.log(masaPoczatkowa / masaCelowa)) - (g * (deltaM / mi))
        tekst_info.set_text(
            f"Prędkość końcowa:\n{v_biezaca:.2f} m/s\n"
            f"Prędkość dla 250 t:\n{predkoscDla250:.2f} m/s"
        )
    else:
        tekst_info.set_text(
            f"Prędkość końcowa:\n{v_biezaca:.2f} m/s\n"
            f"Brak danych dla 250 t"
        )

# Podłączenie funkcji do suwaków i przycisków
suwakMasaPoczatkowa.on_changed(aktualizujDane)
suwakPredkoscWylotu.on_changed(aktualizujDane)
suwakProcentPaliwa.on_changed(aktualizujDane)
suwakMi.on_changed(aktualizujDane)

os.invert_xaxis()
aktualizujDane(None)
plt.show()
