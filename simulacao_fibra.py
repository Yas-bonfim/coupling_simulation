import numpy as np
import matplotlib.pyplot as plt

# ==========================================
# CONFIGURAÇÕES DA SIMULAÇÃO
# ==========================================
GRID_SIZE = 512        # Resolução da malha
PUPIL_RADIUS = 2.0     # Raio da pupila (mm)
W0_FIBER = 1.5         # Raio do campo modal da fibra (Mode Field Radius - w0) (mm)
WAVELENGTH = 1550e-6   # Comprimento de onda (mm) - ex: 1550 nm

# ==========================================
# CRIAÇÃO DO ESPAÇO DE COORDENADAS
# ==========================================
x = np.linspace(-3, 3, GRID_SIZE)
y = np.linspace(-3, 3, GRID_SIZE)
X, Y = np.meshgrid(x, y)
R = np.sqrt(X**2 + Y**2)

# Máscara da pupila (abertura circular)
pupil_mask = R <= PUPIL_RADIUS

# ==========================================
# DEFINIÇÃO DO PERFIL DA FRENTE DE ONDA (INCIDENTE)
# ==========================================
# Amplitude uniforme dentro da pupila, zero fora
A_inc = np.zeros_like(R)
A_inc[pupil_mask] = 1.0

# Simulando uma fase residual (ex: astigmatismo + ruído)
phase_inc = 0.5 * (X**2 - Y**2) + 0.1 * np.random.randn(*R.shape)
phase_inc[~pupil_mask] = 0.0

# Campo elétrico complexo incidente: E = A * exp(i * phi)
E_inc = A_inc * np.exp(1j * phase_inc)

# ==========================================
# DEFINIÇÃO DO PERFIL DA FIBRA MONOMODO (SMF)
# ==========================================
# O modo fundamental da fibra é aproximado por uma Gaussiana
# E_fib = exp(-r^2 / w0^2)
E_fib = np.exp(-(R**2) / (W0_FIBER**2))

# ==========================================
# 4. CÁLCULO DA EFICIÊNCIA DE ACOPLAMENTO
# ==========================================
# A eficiência é a integral de sobreposição ao quadrado
numerador = np.abs(np.sum(E_inc * np.conj(E_fib)))**2
denominador = np.sum(np.abs(E_inc)**2) * np.sum(np.abs(E_fib)**2)

eta = numerador / denominador
eta_db = 10 * np.log10(eta)

print(f"Eficiência de Acoplamento: {eta * 100:.2f}%")
print(f"Perda de Inserção: {eta_db:.2f} dB")

# ==========================================
# DIVISÃO DO PERFIL DA FRENTE DE ONDA PELO DA FIBRA
# ==========================================
# Para evitar divisão por zero ou números ínfimos longe do centro,
# aplicamos um limite de tolerância (epsilon) no denominador.
epsilon = 1e-6
E_fib_safe = np.where(E_fib < epsilon, epsilon, E_fib)

# Divisão complexa: (Amplitude_inc / Amplitude_fib) * exp(i * (Fase_inc - Fase_fib))
# Como a fase da fibra fundamental ideal é plana (0), isso afeta mais a amplitude.
E_div = E_inc / E_fib_safe

# Extraindo amplitude e fase resultantes da divisão
A_div = np.abs(E_div)
Phase_div = np.angle(E_div)

# Mascarando para visualização apenas dentro da pupila
A_div[~pupil_mask] = 0
Phase_div[~pupil_mask] = 0

# ==========================================
# VISUALIZAÇÃO DOS RESULTADOS
# ==========================================
fig, axes = plt.subplots(2, 3, figsize=(16, 10))

# Linha 1: Campos originais
im0 = axes[0, 0].imshow(np.abs(E_inc), extent=[-3, 3, -3, 3], cmap='gray')
axes[0, 0].set_title("Amplitude Incidente (Pupila)")
plt.colorbar(im0, ax=axes[0, 0])

im1 = axes[0, 1].imshow(phase_inc, extent=[-3, 3, -3, 3], cmap='turbo')
axes[0, 1].set_title("Fase Incidente (rad)")
plt.colorbar(im1, ax=axes[0, 1])

im2 = axes[0, 2].imshow(np.abs(E_fib), extent=[-3, 3, -3, 3], cmap='hot')
axes[0, 2].set_title("Modo da Fibra (Gaussiana)")
plt.colorbar(im2, ax=axes[0, 2])

# Linha 2: Resultados da divisão
im3 = axes[1, 0].imshow(A_div, extent=[-3, 3, -3, 3], cmap='viridis', vmax=3)
axes[1, 0].set_title("Divisão: Amplitude (Incidente / Fibra)")
plt.colorbar(im3, ax=axes[1, 0])

im4 = axes[1, 1].imshow(Phase_div, extent=[-3, 3, -3, 3], cmap='turbo')
axes[1, 1].set_title("Divisão: Fase Resultante")
plt.colorbar(im4, ax=axes[1, 1])

# Texto com eficiência
axes[1, 2].axis('off')
texto = (f"Resultados do Acoplamento:\n\n"
         f"Eficiência ($\eta$): {eta*100:.1f}%\n"
         f"Perda: {eta_db:.2f} dB\n\n"
         f"Raio Pupila: {PUPIL_RADIUS} mm\n"
         f"Raio Fibra ($w_0$): {W0_FIBER} mm")
axes[1, 2].text(0.1, 0.5, texto, fontsize=14, va='center', bbox=dict(facecolor='white', alpha=0.8))

for ax in axes.flat:
    if ax != axes[1, 2]:
        ax.set_xlabel("x (mm)")
        ax.set_ylabel("y (mm)")

plt.tight_layout()
plt.show()