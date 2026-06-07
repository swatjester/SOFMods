# CLAUDE.md — SOF Mods development guide

Context for working on this mod set for **Cataclysm: The Last Generation (TLG)** — a fork of Cataclysm: DDA at https://github.com/Cataclysm-TLG/Cataclysm-TLG. Repo: https://github.com/swatjester/SOFMods

Overarching goal: a comprehensive set of mods simulating modern-day U.S. military and SOF structure and equipment, even where it doesn't fit the game's time period or slightly overlaps existing content.

## Mods & load order (dependency order)

1. **Modern_SOF_Gear** (`modern_sof_gear`) — deps `["tlg"]`. The big equipment + weapons module (see below), including MRGG-A/-S modular battle rifles, 6.5 Creedmoor + .308 swap barrel, and the 6.5 Creedmoor cartridge.
2. **Modern_SOF_Forces** (`modern_sof_forces`) — deps `["tlg", "modern_sof_gear"]`. Professions + solo-start scenarios (75th Rangers, Multifunctional Reconnaissance Company).
3. **Modern_SOF_Vehicles** (`modern_sof_vehicles`) — deps `["tlg"]`. ISV, RSOV (M240/M2/Mk19 variants), MRZR-2/-4, Flyer, GMV (endgame).

## CRITICAL TLG gotchas (these cause hard load/character-creation errors)

- **Base content mod id is `tlg`, NOT `dda`.** There is no `dda` mod in TLG. All `dependencies` must use `tlg`. (Early files wrongly used `dda`; all fixed.)
- **All item objects must use `"type": "ITEM"` + `"subtypes": [...]`.** TLG folded every standalone item type into ITEM. Legacy `"type": "AMMO"` / `"GUN"` / `"MAGAZINE"` / `"GUNMOD"` / `"ARMOR"` / `"TOOL"` etc. throw **"unrecognized JSON object"** at the `type` line and bounce the player to the main menu during new-character creation (worldgen may still appear to work). Conversions: `"type":"AMMO"` → `"type":"ITEM","subtypes":["AMMO"]`, etc.
  - NOT items (leave as-is): `ammunition_type`, `ammo_effect`, `effect_type`, `item_group`, `profession`, `scenario`, `vehicle`, `vehicle_part`, `furniture`, `effect_on_condition`, `recipe`, `MOD_INFO`, `migration`.
- After ANY change, validate JSON parse + cross-references before considering it done. A standard validation script lives in the chat history; it builds an id universe from `data/json` + all mods and checks copy-from / ammo / magazine `item_restriction` / `ammo_restriction` / ammo_effects / deploy-furniture / spawn-group refs.

## Key implementation patterns

- **Modular guns** (M4 family): a frame item (`modular_m4_carbine`, ammo NULL) + `retool_ar15_*` upper-receiver GUNMODs (location `bore`, with `ammo_modifier`, `magazine_adaptor`, `barrel_length`, `add_mod`). Pre-made configs are item_groups that spawn the frame with a cosmetic `variant` + `contents-item` parts (see `m4_cqbr` / our `m4_glssc`).
- **`default_mods`** = removable pre-installed mods (used for the "SOF" kitted builds and the para/shorty MG configs — all share the base weapon name, no rename, since a swapped part would make a fixed name wrong). **`built_in_mods`** = permanent.
- **Gunmod `barrel_length`** on a `barrel`-location mod OVERRIDES the host gun's barrel length (affects damage/dispersion). Used for the M249-para/M240-short barrels.
- **Cartridges**: `ammunition_type` (with `default` pointing to an AMMO item) + AMMO items + MAGAZINE items (`ammo_restriction: {<ammotype>: N}`) + the gun's `pocket_data` `MAGAZINE_WELL` `item_restriction` listing accepted magazine ids. See `Modern_SOF_Gear/ammo/277fury.json` for the full pattern.
- **Vehicle weapon turrets**: `turret_mount` + an auto-generated `turret_<gunid>` part (e.g. `turret_m240`, `turret_mark19`, `turret_m2browning`, `turret_atgm_launcher`), loaded via `{"part":..,"ammo":N,"ammo_types":[...],"ammo_qty":[lo,hi]}`. For a gun with no auto-turret (the RMES/HEL-AD laser) define a part explicitly: `copy-from: turret` + `item: <gun_id>` (see `Modern_SOF_Vehicles/vehicleparts/rmes_laser_turret.json`).
- **Vehicles**: +x = front (engine/headlights high x), 5-wide grid (wheels on outer columns y=-1/3, seats interior y=0/1/2). One entry per tile with a combined `parts` list is valid. Omit `blueprint` (auto-generated). `vehicle_group` does NOT support `copy-from`/`extend` in TLG — to add spawns you must REDEFINE the base group (e.g. `military_vehicles`) with the full list + your vehicles; re-sync if upstream changes.
- **Vehicle power/REACTOR**: TLG's appliance generators use `REACTOR`, but spawned vehicle prototypes initialize every reactor with `plut_cell` regardless of `fuel_type`. Do not put `REACTOR` on normal GMV parts backed by diesel/generator items; it causes `item::ammo_set` debug errors. The GMV uses batteries, solar, and the engine alternator; `hel_apu` is non-reactor generator hardware. Solar panels in TLG all output **50 W regardless of tier** (advanced/reinforced only differ in durability). Battery capacity: `large_storage_battery` = 100,000 kJ, `storage_battery` = 50,000 kJ, 1 unit ≈ 1 kJ.
- **Mortars** = a deploy-furniture item (`use_action: deploy_furn`) + a `furniture` with `examine_action: {type:"mortar", ammo:[<ammotype>], ...}` driving range/aim via an inline EOC + an `aimed_<cal>` effect_type + an AMMO shell whose lethality comes from an `EXPLOSIVE_*` ammo_effect. See `Modern_SOF_Gear/{guns,ammo,furniture}` for the M252 81mm set (modeled on the base M224 60mm).
- **MOLLE**: platforms (battle belts) have `BELT_CLIP`/holster pockets + `use_action [holster, attach_molle (size N), detach_molle]`; pouches are ARMOR flagged `PALS_SMALL`(1)/`MEDIUM`(2)/`LARGE`(3) slot cost. Presets assembled at item-group level: `{ "item": "<belt>", "contents-group": "<contents>" }`.
- **Professions/scenarios**: professions use `items.both/male/female.entries` (item/group, `ammo-item`, `charges`, `container-item`, `contents-item`, `contents-group`); flag `SCEN_ONLY` ties them to scenarios that list them. Scenarios list `professions`, `allowed_locs` (sloc_*), `flags` (LONE_START, CITY_START...). Role professions reference our gear groups (battle belts, m4_glssc group) and guns. Drone operators field FPV strike drones = `bot_grenade_hack` + `bot_c4_hack` (NOT manhacks).

## What's been built

- **Modern_SOF_Gear**: MRGG-A, MRGG-S, SOF kitted builds, 6.5 Creedmoor ammo/mags, .308 conversion; SOF rifle builds; LVAW (.300 BLK) + SOF; modular AR uppers (GL/SSC 12.5", recce 16", Mk12 SPR 18"); short suppressor; grippod; M249-para/M240-collapsible stocks + short barrels; MOLLE battle belts (assaulter/breacher/grenadier/drone) + pouches incl. breaching tool hooks; **added weapons**: NGSW M7/M8/M250 + `277fury` (.277 Fury) cartridge; M110 SASS; KAC SR-25 (with Mk 11 variant); Colt 9mm SMG (Uzi mags); KAC LAMG; M252 81mm mortar + shell; Mk 153 SMAW + rocket; FGM-148 Javelin + missile. All wired into military spawn groups.
- **Modern_SOF_Forces**: 75th Ranger professions (assaulter, sniper, breacher, grenadier, drone operator, machine gunner [M249-para], weapons-squad gunner [M240]) + bionic mirrors with role-specific CBMs + "Rangers Lead the Way" scenario; MFRC professions (scout, sniper, machine gunner [M249-para], grenadier, drone operator [M4A1]) + bionic mirrors with role-specific CBMs + "Eyes Forward" scenario. Solo-start only so far.
- **Modern_SOF_Vehicles**: `isv` (9-seat, unarmed), `rsov_m240`/`rsov_m2`/`rsov_mk19` (M249 pintle on all), `mrzr2`/`mrzr4` (M249 pintle, diesel_engine_inline4), `flyer` (ATGM turret + M240 pintle), `gmv_helad` (M1288: Mk19 + HEL-AD laser + 6 batteries + 6 solar + JP8 APU; NOT in spawn groups - debug-spawn only). Custom parts: `turret_rmes_laser` (HEL-AD), `hel_apu`.

## Remaining backlog (not yet built)

- **NPC companions + the solo→duo→fireteam→section→squad progression** wired onto the existing solo scenarios.
- **Additional SOF professions**:
  - Medic for Rangers and MFRC Recon, normal + bionic. Ranger medic gets a Mk18/CQBR; Recon medic gets an M4A1. Both should be combat-capable, but their distinctiveness comes from medical skills and expanded trauma/field-care gear.
  - Ranger Fire Support for Rangers only, normal + bionic. Primary specialty weapon is the Carl Gustaf; start with a small load, roughly 2 HEAT/HEDP and 1 smoke/illum if supported. Personal weapon should be an MP7.
  - JTAC for Rangers and MFRC Recon, normal + bionic. Intent is a lighter assaulter/scout with excellent optics and situational-awareness tools for laser designation, not a drone operator and not a sniper competitor. Ranger JTAC gets an MRGG-A; Recon JTAC gets an SPR. Rifle/marksmanship skills should be one step below the relevant assaulter baseline. Give an e-reader rather than a laptop, no robOS, a military map, extra smoke grenades, a flare gun with a small number of flares, and a standalone M320 with smoke rounds. Bionic package should emphasize radio/comms, targeting, enhanced vision/optics, and light survivability.
- **Starting vehicles for SOF scenarios** after profession testing: decide which starts should receive ISV/RSOV/MRZR/Flyer support and wire them into scenarios only after the non-vehicle starts are verified.
- **Additional map features**: FOB, COP, Patrol Base, Black Site, Urban Black Site, National Guard Armory, and Recruiter's Office.
- **Additional units and scenario families**: RRC, Special Activities Center, SEALs, DEVGRU, CAG, Infantry, Marines, Force Recon, MARSOC, AFSOC, TFO, Special Forces, and a PMC faction (Greywater or Double Canopy). Group the JSOC units together and label their scenarios by color, e.g. Task Force Red, Task Force Blue, etc.
- **SP10-M rifle**: add the Seekins SP10-M as a new rifle similar to the MRGG-S, but longer/heavier with slightly better range and slightly worse recoil. When a CAG sniper profession is added, make the SP10-M their default rifle.
- **Zombified preset versions** of the SOF forces (enemy spawns reusing the role loadouts).
- **Low-visibility / undercover operator scenario** — the LVAW (.300 BLK) is reserved for this; keep it out of the standard Ranger/MFRC kits.

## Style / policy

- Third-party fan mod, CC BY-SA 3.0 to match TLG; not affiliated with the TLG project or upstream.
- Realism matters to the author — match real-world platforms/calibers/magazines where the game supports it; substitute the closest in-game analogue and note it when it doesn't.
