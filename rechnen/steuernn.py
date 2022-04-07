def berechnen(betrag, prozent=10):
    ergebnis = betrag * (prozent / 100)
    return ergebnis


def abgaben(betrag):
    ergebnis = betrag * 0.1
    return ergebnis


steuer_betrag = berechnen(100)
print(steuer_betrag)


buch_steuer = berechnen(100, prozent=5)
print(buch_steuer)
