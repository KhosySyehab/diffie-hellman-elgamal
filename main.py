import tkinter as tk
from math_utils import mod_exp, is_primitive_root

BG = "#1c202c"      # latar utama
FACE = "#232939"    # permukaan kartu
SUNK = "#1a1e29"    # permukaan input (cekung)
LIGHT = "#2f3750"   # sisi terang
SHADE = "#11141c"   # sisi gelap
TXT, DIM = "#e8ecf5", "#7f89a3"
ACC, PINK, GREEN, RED = "#8b7cf6", "#f08ac0", "#5fd6a4", "#f27a7a"
FONT, MONO = "Segoe UI", "Consolas"
D, R = 6, 18        # kedalaman bayangan dan radius sudut


def rrect(c, x1, y1, x2, y2, r, fill):
    pts = [x1+r, y1, x2-r, y1, x2, y1, x2, y1+r, x2, y2-r, x2, y2,
           x2-r, y2, x1+r, y2, x1, y2, x1, y2-r, x1, y1+r, x1, y1]
    c.create_polygon(pts, smooth=True, fill=fill, outline="", tags="bg")


class Neu(tk.Canvas):
    def __init__(self, parent, pressed=False, pad=18, face=FACE):
        super().__init__(parent, bg=BG, highlightthickness=0, bd=0)
        self.pressed, self.face, self.p = pressed, face, pad + D
        self.inner = tk.Frame(self, bg=face)
        self.win = self.create_window(self.p, self.p, window=self.inner, anchor="nw")
        self.inner.bind("<Configure>", self._fit)
        self.bind("<Configure>", self._draw)

    def _fit(self, e=None):
        self.config(width=self.inner.winfo_reqwidth() + 2*self.p,
                    height=self.inner.winfo_reqheight() + 2*self.p)

    def _draw(self, e=None):
        w, h = self.winfo_width(), self.winfo_height()
        self.delete("bg")
        tl, br = (SHADE, LIGHT) if self.pressed else (LIGHT, SHADE)
        r = min(R, h // 2 - 2)
        rrect(self, D, D, w, h, r, br)
        rrect(self, 0, 0, w - D, h - D, r, tl)
        rrect(self, D//2, D//2, w - D//2, h - D//2, r, self.face)
        self.tag_lower("bg")


def btn(parent, text, cmd):
    n = Neu(parent, pad=12)
    lbl = tk.Label(n.inner, text=text, bg=FACE, fg=ACC, font=(FONT, 11, "bold"),
                   padx=26, pady=8, cursor="hand2")
    lbl.pack(fill="x")

    def click(e=None):
        n.pressed = True
        n._draw()
        n.after(110, lambda: (setattr(n, "pressed", False), n._draw()))
        cmd()

    n.bind("<Button-1>", click)
    lbl.bind("<Button-1>", click)
    return n


def field(parent, label, default):
    tk.Label(parent, text=label, bg=FACE, fg=DIM, font=(FONT, 9)).pack(anchor="w", pady=(12, 4))
    n = Neu(parent, pressed=True, pad=8, face=SUNK)
    n.pack(fill="x")
    e = tk.Entry(n.inner, width=22, bg=SUNK, fg=TXT, insertbackground=TXT,
                 relief="flat", bd=0, font=(MONO, 12))
    e.insert(0, str(default))
    e.pack(padx=8, pady=6, ipady=4)
    return e


def head(parent, title, sub):
    tk.Label(parent, text=title, bg=BG, fg=TXT, font=(FONT, 20, "bold")).pack(anchor="w")
    tk.Label(parent, text=sub, bg=BG, fg=DIM, font=(FONT, 10)).pack(anchor="w", pady=(2, 0))


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Operasi Strix")
        self.geometry("1080x720")
        self.minsize(960, 640)
        self.configure(bg=BG)

        side = tk.Frame(self, bg=BG, width=250)
        side.pack(side="left", fill="y", padx=(28, 0), pady=28)
        side.pack_propagate(False)
        tk.Label(side, text="OPERASI", bg=BG, fg=TXT, font=(FONT, 18, "bold")).pack(anchor="w", padx=8)
        tk.Label(side, text="STRIX", bg=BG, fg=ACC, font=(FONT, 18, "bold")).pack(anchor="w", padx=8)
        tk.Label(side, text="Misi Lloyd & Anya", bg=BG, fg=DIM, font=(FONT, 9)).pack(anchor="w", padx=8, pady=(2, 30))

        self.nav = {}
        for name in ("Diffie-Hellman", "ElGamal"):
            n = Neu(side, pad=10)
            n.pack(fill="x", pady=6)
            lbl = tk.Label(n.inner, text=name, bg=FACE, fg=DIM, font=(FONT, 11),
                           width=18, anchor="w", padx=20, pady=10, cursor="hand2")
            lbl.pack()
            for w in (n, lbl):
                w.bind("<Button-1>", lambda e, nm=name: self.show(nm))
            self.nav[name] = (n, lbl)

        self.content = tk.Frame(self, bg=BG)
        self.content.pack(side="left", fill="both", expand=True, padx=40, pady=28)
        self.show("Diffie-Hellman")

    def show(self, name):
        for nm, (n, lbl) in self.nav.items():
            on = nm == name
            n.pressed = on
            n._draw()
            lbl.config(fg=TXT if on else DIM)
        for w in self.content.winfo_children():
            w.destroy()
        if name == "Diffie-Hellman":
            self.page_dh()
        else:
            head(self.content, "ElGamal", "Halaman ini menunggu elgamal.py dari Orang 2.")

    def page_dh(self):
        head(self.content, "Diffie-Hellman", "Lloyd dan Anya menyepakati kunci rahasia lewat saluran publik.")
        row = tk.Frame(self.content, bg=BG)
        row.pack(fill="both", expand=True, pady=(26, 0))

        left = Neu(row, pad=22)
        left.pack(side="left", anchor="n")
        f = left.inner
        tk.Label(f, text="PARAMETER", bg=FACE, fg=DIM, font=(FONT, 9, "bold")).pack(anchor="w")
        self.e = [field(f, l, d) for l, d in [
            ("p   bilangan prima", 251),
            ("g   akar primitif", 6),
            ("x   rahasia Lloyd", 124),
            ("y   rahasia Anya", 158),
        ]]
        btn(f, "Jalankan misi", self.run_dh).pack(fill="x", pady=(22, 0))
        self.status = tk.Label(f, text="", bg=FACE, fg=RED, font=(FONT, 9), wraplength=260, justify="left")
        self.status.pack(anchor="w", pady=(12, 0))

        right = tk.Frame(row, bg=BG)
        right.pack(side="left", fill="both", expand=True, padx=(26, 0))

        tiles = tk.Frame(right, bg=BG)
        tiles.pack(fill="x")
        self.tiles = {}
        for i, (k, t, c) in enumerate([("X", "X  ·  Lloyd → Anya", PINK),
                                       ("Y", "Y  ·  Anya → Lloyd", PINK),
                                       ("K", "K  ·  kunci bersama", GREEN)]):
            n = Neu(tiles, pad=18)
            n.pack(side="left", fill="x", expand=True, padx=(0 if i == 0 else 14, 0))
            tk.Label(n.inner, text=t, bg=FACE, fg=DIM, font=(FONT, 9)).pack(anchor="w")
            v = tk.Label(n.inner, text="—", bg=FACE, fg=c, font=(FONT, 24, "bold"))
            v.pack(anchor="w", pady=(6, 0))
            self.tiles[k] = v

        self.verdict = tk.Label(right, text="Penyadap hanya melihat p, g, X, dan Y.",
                                bg=BG, fg=DIM, font=(FONT, 10))
        self.verdict.pack(anchor="w", pady=(22, 10))

        log = Neu(right, pressed=True, pad=16, face=SUNK)
        log.pack(fill="both", expand=True)
        self.log = tk.Text(log.inner, bg=SUNK, fg=TXT, relief="flat", bd=0, highlightthickness=0,
                           font=(MONO, 10), width=60, height=9, padx=12, pady=10)
        self.log.pack()
        self.log.config(state="disabled")

    def write(self, lines):
        self.log.config(state="normal")
        self.log.delete("1.0", "end")
        for text, color in lines:
            self.log.tag_config(color, foreground=color)
            self.log.insert("end", text + "\n", color)
        self.log.config(state="disabled")

    def run_dh(self):
        try:
            p, g, x, y = (int(e.get()) for e in self.e)
        except ValueError:
            self.status.config(text="Isi semua kolom dengan angka bulat.")
            return
        if not is_primitive_root(g, p):
            self.status.config(text=f"{g} bukan akar primitif dari {p}.")
            return
        self.status.config(text="")

        X, Y = mod_exp(g, x, p), mod_exp(g, y, p)
        K, K2 = mod_exp(Y, x, p), mod_exp(X, y, p)
        ok = K == K2

        self.tiles["X"].config(text=str(X))
        self.tiles["Y"].config(text=str(Y))
        self.tiles["K"].config(text=str(K) if ok else "✗", fg=GREEN if ok else RED)
        self.verdict.config(
            text="K = K′, kunci disepakati tanpa pernah dikirim." if ok else "K ≠ K′, ada yang salah.",
            fg=GREEN if ok else RED)

        self.write([
            (f"[1] Lloyd   X = {g}^{x} mod {p} = {X}", TXT),
            (f"[2] Anya    Y = {g}^{y} mod {p} = {Y}", TXT),
            ("    X dan Y dikirim lewat saluran publik", DIM),
            (f"[3] Lloyd   K  = Y^x mod {p} = {K}", ACC),
            (f"[4] Anya    K′ = X^y mod {p} = {K2}", ACC),
        ])


if __name__ == "__main__":
    App().mainloop()