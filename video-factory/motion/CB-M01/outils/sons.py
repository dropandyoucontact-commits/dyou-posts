#!/usr/bin/env python3
"""Synthétise les bruitages de CB-M01 dans ../sons/*.wav (48 kHz, mono, crête -1 dBFS).

Rien n'est téléchargé : pas de licence à vérifier, et relancer le script refait
exactement les mêmes sons (graine fixe). Les niveaux relatifs se règlent dans
edit.js (troisième argument de son()), pas ici.

    python3 outils/sons.py
"""
import pathlib
import numpy as np
from scipy.signal import butter, sosfilt, lfilter
import wave

SR = 48000
ICI = pathlib.Path(__file__).resolve().parent.parent
SONS = ICI / "sons"
rng = np.random.default_rng(20261005)


def t_(d):
    return np.arange(int(d * SR)) / SR


def env(n, att, dec_tau, sustain=0.0):
    """attaque linéaire puis décroissance exponentielle"""
    t = np.arange(n) / SR
    a = np.clip(t / max(att, 1e-4), 0, 1)
    return a * np.exp(-np.maximum(t - att, 0) / dec_tau) * (1 - sustain) + sustain * a


def bande(x, lo, hi, ordre=2):
    sos = butter(ordre, [lo / (SR / 2), min(hi / (SR / 2), 0.99)], btype="band", output="sos")
    return sosfilt(sos, x)


def passe_bas(x, f, ordre=2):
    return sosfilt(butter(ordre, f / (SR / 2), output="sos"), x)


def passe_haut(x, f, ordre=2):
    return sosfilt(butter(ordre, f / (SR / 2), btype="high", output="sos"), x)


def balayage(x, f0, f1, q=1.2, bloc=256):
    """filtre passe-bande dont la fréquence centrale glisse de f0 à f1 (souffle)"""
    out = np.zeros_like(x)
    n = len(x)
    zi = None
    for i in range(0, n, bloc):
        u = i / max(n - 1, 1)
        fc = f0 * (f1 / f0) ** u
        bw = fc / q
        lo, hi = max(30, fc - bw / 2), min(SR / 2 * 0.98, fc + bw / 2)
        b, a = butter(2, [lo / (SR / 2), hi / (SR / 2)], btype="band")
        if zi is None or len(zi) != max(len(a), len(b)) - 1:
            zi = np.zeros(max(len(a), len(b)) - 1)
        seg, zi = lfilter(b, a, x[i:i + bloc], zi=zi)
        out[i:i + bloc] = seg
    return out


def normal(x, crete=0.89):
    m = np.max(np.abs(x)) or 1
    return x / m * crete


def fondu(x, ms=4):
    n = int(SR * ms / 1000)
    x[:n] *= np.linspace(0, 1, n)
    x[-n:] *= np.linspace(1, 0, n)
    return x


def souffle(d, f0, f1, att_frac=0.55, q=1.3):
    n = int(d * SR)
    x = rng.standard_normal(n)
    x = balayage(x, f0, f1, q)
    t = np.linspace(0, 1, n)
    e = np.where(t < att_frac, (t / att_frac) ** 2, ((1 - t) / (1 - att_frac)) ** 1.6)
    return fondu(normal(x * e))


def impact(d=0.6, f0=62, f1=36, tau=0.22, clic=0.35):
    t = t_(d)
    f = f1 + (f0 - f1) * np.exp(-t / 0.06)
    ph = 2 * np.pi * np.cumsum(f) / SR
    corps = np.sin(ph) * env(len(t), 0.002, tau)
    n = rng.standard_normal(len(t)) * env(len(t), 0.0005, 0.012)
    attaque = passe_bas(n, 2500) * clic
    return fondu(normal(corps + attaque))


def note(freqs, d, tau, att=0.002, poids=None):
    t = t_(d)
    poids = poids or [1] * len(freqs)
    x = sum(w * np.sin(2 * np.pi * f * t + rng.uniform(0, 6.28)) for f, w in zip(freqs, poids))
    return fondu(normal(x * env(len(t), att, tau)))


def chirp(f0, f1, d, tau):
    t = t_(d)
    f = f0 * (f1 / f0) ** (t / d)
    return fondu(normal(np.sin(2 * np.pi * np.cumsum(f) / SR) * env(len(t), 0.002, tau)))


def ecrire(nom, x):
    SONS.mkdir(exist_ok=True)
    y = (np.clip(x, -1, 1) * 32767).astype(np.int16)
    with wave.open(str(SONS / f"{nom}.wav"), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(y.tobytes())


def tous():
    s = {}
    s["whoosh"] = souffle(0.46, 280, 3200)
    s["whoosh_court"] = souffle(0.26, 600, 4200, 0.5)
    s["whoosh_long"] = souffle(0.85, 180, 2400, 0.62, 1.1)
    s["whoosh_bas"] = souffle(0.5, 1800, 140, 0.35, 1.0)
    s["swipe"] = souffle(0.22, 1500, 6000, 0.4, 1.6)
    s["impact"] = impact()
    s["impact_doux"] = normal(impact(0.5, 74, 46, 0.16, 0.15) * 0.8)
    # tampon : petit impact + claque de papier
    claque = bande(rng.standard_normal(int(0.12 * SR)), 700, 3200) * env(int(0.12 * SR), 0.001, 0.025)
    tam = impact(0.35, 90, 50, 0.08, 0.5)
    tam[: len(claque)] += normal(claque) * 0.9
    s["tampon"] = fondu(normal(tam))
    s["pop"] = chirp(520, 980, 0.11, 0.035)
    s["clic"] = fondu(normal(note([2100], 0.035, 0.006) + passe_haut(rng.standard_normal(int(0.035 * SR)), 3000) * env(int(0.035 * SR), 0.0003, 0.003) * 0.6))
    s["tick"] = note([3300], 0.03, 0.005)
    s["blip"] = chirp(1100, 1500, 0.09, 0.03)
    s["check"] = fondu(normal(np.concatenate([note([1318.5, 2637], 0.09, 0.05, poids=[1, 0.3]), note([1975.5, 3951], 0.5, 0.16, poids=[1, 0.25])])))
    s["verre"] = note([2093, 3140.5, 4186, 5281.3, 6620], 1.1, 0.34, 0.003, [1, 0.6, 0.45, 0.3, 0.15])
    s["message"] = fondu(normal(np.concatenate([souffle(0.08, 900, 5000, 0.3, 1.5) * 0.5, chirp(880, 1320, 0.12, 0.04)])))
    s["message_in"] = fondu(normal(np.concatenate([note([1046.5, 2093], 0.09, 0.05, poids=[1, 0.2]), note([1568, 3136], 0.24, 0.08, poids=[1, 0.2])])))
    fr = bande(rng.standard_normal(int(0.05 * SR)), 1200, 5200) * env(int(0.05 * SR), 0.0005, 0.008)
    s["frappe"] = fondu(normal(fr + note([180], 0.05, 0.01) * 0.3))
    n = int(0.85 * SR)
    mont = balayage(rng.standard_normal(n), 300, 4500, 1.4)
    tt = np.linspace(0, 1, n)
    mont = mont * tt ** 2.2 + 0.25 * np.sin(2 * np.pi * np.cumsum(220 * 4 ** tt) / SR) * tt ** 2
    s["montee"] = fondu(normal(mont))
    for k, v in s.items():
        ecrire(k, v)
    return s


if __name__ == "__main__":
    s = tous()
    print(len(s), "sons :", ", ".join(f"{k} {len(v)/SR:.2f}s" for k, v in s.items()))
