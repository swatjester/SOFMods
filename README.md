# SOF Mods - Modern U.S. Military / SOF set for Cataclysm: The Last Generation

A set of mods that add modern U.S. military and special-operations equipment, forces, and vehicles to [Cataclysm: The Last Generation](https://github.com/Cataclysm-TLG/Cataclysm-TLG). All mods depend on the core `tlg` content.

## Installation

Copy the mod folders from this repository into the `data/mods` folder inside your TLG installation:

- `Modern_SOF_Gear`
- `Modern_SOF_Forces`
- `Modern_SOF_Vehicles`

After copying, enable the mods when creating or editing a world. For example, a typical install path will look like:

```text
Cataclysm-TLG/
  data/
    mods/
      Modern_SOF_Gear/
      Modern_SOF_Forces/
      Modern_SOF_Vehicles/
```

## Mods & Load Order

Load in dependency order:

1. **Modern_SOF_Gear** (`modern_sof_gear`) - all weapons, ammunition, gunmods, armor, and carried equipment.
2. **Modern_SOF_Forces** (`modern_sof_forces`) - playable SOF professions and scenarios. Requires `modern_sof_gear`.
3. **Modern_SOF_Vehicles** (`modern_sof_vehicles`) - all SOF vehicles and custom vehicle parts.

`Modern_SOF_Vehicles` does not depend on `Modern_SOF_Gear`, but loading all three together gives the complete set.

## Content

### Modern_SOF_Gear

Adds modern SOF weapons and support equipment:

- **MRGG rifle family:** MRGG-A and MRGG-S battle rifles in 6.5mm Creedmoor, SOF-kitted variants, 6.5mm magazines and ammo, .308 conversion barrel, and .308 magazine support.
- **AR-platform upgrades:** 12.5-inch GL/SSC, 16-inch recce, and 18-inch Mk12 SPR upper receivers.
- **SOF carbines and SMGs:** LVAW carbine in .300 BLK, GL/SSC M4 build, Colt 9mm SMG, MP7, and standalone M320 smoke launcher.
- **Precision and support weapons:** M110 SASS, KAC SR-25/Mk 11, M249 Para setup, M240 short/collapsible variants, KAC LAMG, M7 rifle, M8 carbine, and M250 machine gun.
- **Launchers and ordnance:** deployable M252 81mm mortar with HE shells, Mk 153 SMAW with 83mm HEDP rockets, and FGM-148 Javelin CLU with missiles.
- **Gunmods:** short suppressor, grippod, M249 Para stock/barrel, M240 collapsible stock/short barrel, and MRGG conversion parts.
- **Load-bearing gear:** MOLLE pouches, role-configured battle belts, holsters, drone bag, breaching retention gear, and IFAK contents.

Natural gameplay integration:

- Military rifle, sniper rifle, LMG, launcher, gunmod, infantry gear, gun-store, and military cache item groups include the mod's common weapons, gunmods, battle belts, pouches, MRGG rifles, MRGG accessories, and some 6.5mm Creedmoor supplies.
- Ranger and Recon professions from `Modern_SOF_Forces` start with many of the role-specific weapons and carried equipment.

### Modern_SOF_Forces

Adds solo-start scenarios and playable professions for modern SOF characters:

- **75th Ranger Regiment scenario:** `Rangers Lead the Way`.
- **Recon Company scenario:** `Eyes Forward`.
- **Scenario balance note:** these scenarios are not yet balanced for point cost, either against each other or against vanilla scenarios.
- **75th Ranger Regiment professions:** assaulter, sniper, breacher, grenadier, drone operator, machine gunner, weapons-squad gunner, medic, fire support, and JTAC.
- **Multifunctional Reconnaissance Company professions:** scout, sniper, machine gunner, grenadier, drone operator, medic, and JTAC.
- **Bionic variants:** augmented versions of the Ranger and Recon professions with bionic loadouts.

### Modern_SOF_Vehicles

Adds modern tactical vehicles and vehicle parts:

- **M1301 ISV:** light infantry squad vehicle.
- **RSOV variants:** M240, M2, and Mk 19 turret versions.
- **Polaris MRZR:** two-seat MRZR-2 and four-seat MRZR-4.
- **Flyer light strike vehicle:** armed light strike buggy.
- **M1288 GMV HEL-AD:** endgame Ground Mobility Vehicle with Mk 19 turret, HEL-AD laser system, large battery bank, solar support, and auxiliary power hardware.
- **Custom vehicle parts:** auxiliary power unit hardware and HEL-AD laser turret.

Natural gameplay integration:

- The ISV, RSOV variants, MRZR-2, MRZR-4, and Flyer are added to the `military_vehicles` spawn group.
- The M1288 GMV HEL-AD is not in any vehicle spawn group. Spawn it from the debug menu with vehicle id `gmv_helad`.
- The HEL-AD laser turret and auxiliary power unit are vehicle parts used by the GMV HEL-AD. Outside that debug-spawned vehicle, they are not encountered through natural gameplay.

## Notes

- This is a third-party, fan-made mod set (CC BY-SA 3.0 to match TLG) and is not affiliated with the TLG project.
- All item objects use the current TLG `"type": "ITEM"` + `"subtypes": [...]` format.
