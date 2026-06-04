# SOF Mods — Modern U.S. Military / SOF set for Cataclysm: The Last Generation

A set of mods that add modern U.S. military and special-operations equipment, forces, and vehicles to [Cataclysm: The Last Generation](https://github.com/Cataclysm-TLG/Cataclysm-TLG). All mods depend on the core `tlg` content.

## Mods & load order

Load in dependency order:

1. **MRGG_Rifles** (`mrgg_rifles`) — depends on `tlg`
   Two modular battle rifles: the MRGG-A (Assaulter) and MRGG-S (Sniper), natively 6.5mm Creedmoor with a swappable .308/7.62 NATO conversion barrel, plus the 6.5 Creedmoor cartridge.

2. **Modern_SOF_Gear** (`modern_sof_gear`) — depends on `tlg`, `mrgg_rifles`
   Core equipment module. Kitted "SOF" rifle builds, an LVAW in .300 BLK, modular AR uppers (12.5" GL/SSC, 16" recce, 18" Mk12 SPR), a K-length short suppressor, a grippod, M249/M240 collapsible/para stocks and short barrels, MOLLE battle belts, and a family of additional modern weapons: the NGSW M7/M8/M250 with the 6.8×51mm (.277 Fury) cartridge, the M110 SASS and KAC SR-25/Mk 11, the Colt 9mm SMG, the KAC LAMG, the M252 81mm mortar, the Mk 153 SMAW, and the FGM-148 Javelin.

3. **Modern_SOF_Forces** (`modern_sof_forces`) — depends on `tlg`, `mrgg_rifles`, `modern_sof_gear`
   Playable professions and solo-start scenarios for the 75th Ranger Regiment (assaulter, sniper, breacher, grenadier, drone operator, machine gunner, weapons-squad gunner) and the Multifunctional Reconnaissance Company (scout, sniper, machine gunner, grenadier, drone operator).

4. **Modern_SOF_Vehicles** (`modern_sof_vehicles`) — depends on `tlg`
   Modern tactical ground mobility: the M1301 ISV, the RSOV (M240/M2/Mk 19 turret variants), the Polaris MRZR-2/-4, the Flyer light strike vehicle, and the endgame M1288 GMV with an Mk 19 turret plus a battery/solar/APU-fed HEL-AD laser.

## Notes

- This is a third-party, fan-made mod set (CC BY-SA 3.0 to match TLG) and is not affiliated with Anthropic or the TLG project.
- All item objects use the current TLG `"type": "ITEM"` + `"subtypes": [...]` format.
Test GitHub push verification.
