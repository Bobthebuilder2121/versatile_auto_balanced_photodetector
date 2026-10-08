Im bild hängen beide Dioden an einem TIA. APD: G14858-0020AA (ca. 2 pF); PIN: G14942-32 (ca. 1 pF bei 5 V). Der gezeigte Bias-Abgleich ist für die APD-Variante.

```text
modus       | S+ | S- | i_TIA   | DC-Regler
------------+----+----+---------+----------
I+          | 1  | 0  | I+      | aus
I-          | 0  | 1  | -I-     | aus
autobal.    | 1  | 1  | I+ - I- | ein
```

1 = mit TIA verbunden; 0 = vom TIA getrennt.

Kandidaten: Pickering 103GM-1-A-5/2D (Schließer), TI TMUX8612RUMR, Panasonic AQW227NS. Kritisch: C_on/off, Leckstrom, Glitches. Am offenen Schalter kann fast die volle Biasspannung liegen.

1. Inaktiven Diodenzweig offen lassen oder den Signalanschluss auf Masse umschalten?
2. Mehr Transimpedanz oder mehr Bandbreite? Sind 1 MHz minimum / 10 MHz ziel noch aktuell?
