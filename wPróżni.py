import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# początkowe
procentPaliwa = 95 # [%]
masaPoczatkowa = 334.5  # [t] #Atlas V w tonach
masaKoncowa = masaPoczatkowa * ((100 - procentPaliwa)/100) # [t]
predkoscWylotu = 3053 # [m/s]

figura, os = plt.subplots()
plt.subplots_adjust(left=0.25, bottom=0.4)

masa = np.linspace(masaKoncowa,masaPoczatkowa, 1000)
predkosc = (predkoscWylotu * np.log(masaPoczatkowa / masa))
[linia] = os.plot(masa, predkosc, lw=2)

os.set_title("Zależność prędkości rakiety od pozostałej masy [w próżni]")
os.set_xlabel("Masa rakiety [t]")
os.set_ylabel("Prędkość [m/s]")
os.grid(True, linestyle="--", alpha=0.5)

# suwaki
poleMasaPoczatkowa = plt.axes([0.25, 0.25, 0.65, 0.03])
polePredkoscWylotu = plt.axes([0.25, 0.15, 0.65, 0.03])
poleProcentPaliwa = plt.axes([0.25,0.20,0.65,0.03])

ax_tabela = plt.axes([0.8, 0.2, 0.18, 0.15])
ax_tabela.axis('off')
tekst_info = ax_tabela.text(0, 1, "", verticalalignment='top', fontsize=10, family="monospace")

suwakMasaPoczatkowa = Slider(poleMasaPoczatkowa, 'Masa początkowa [t]', 100, 1000, valinit=masaPoczatkowa)
suwakPredkoscWylotu = Slider(polePredkoscWylotu, 'Prędkość wylotu spalanego paliwa [m/s]', 1000, 5000, valinit=predkoscWylotu)
suwakProcentPaliwa= Slider(poleProcentPaliwa, '% paliwa w masie rakiety ', 80,99, valinit=procentPaliwa)

# funkcja do wykresu
def aktualizujDane(_):
    masaPoczatkowa = suwakMasaPoczatkowa.val
    procentPaliwa = suwakProcentPaliwa.val / 100
    masaKoncowa = masaPoczatkowa * (1-procentPaliwa)
    predkoscWylotu = suwakPredkoscWylotu.val

    masa = np.linspace(masaKoncowa, masaPoczatkowa, 1000)
    predkosc = 11200 + (predkoscWylotu * np.log(masaPoczatkowa / masa))
    linia.set_xdata(masa)
    linia.set_ydata(predkosc)
    os.relim()
    os.autoscale_view()
    figura.canvas.draw_idle()

    v_biezaca = predkosc[0]
    masaCelowa = 250
    if masaCelowa >= masaKoncowa and masaCelowa <= masaPoczatkowa:
        predkoscDla250 = 11200 + (predkoscWylotu * np.log(masaPoczatkowa / masaCelowa))
        tekst_info.set_text(
            f"Prędkość końcowa:\n{v_biezaca:.2f} m/s\n"
            f"Prędkość dla 250 t:\n{predkoscDla250:.2f} m/s"
        )
    else:
        tekst_info.set_text(
            f"Prędkość końcowa:\n{v_biezaca:.2f} m/s\n"
            f"Brak danych dla 250 t"
        )

suwakMasaPoczatkowa.on_changed(aktualizujDane)
suwakPredkoscWylotu.on_changed(aktualizujDane)
suwakProcentPaliwa.on_changed(aktualizujDane)
os.invert_xaxis()
aktualizujDane(None)
plt.show()