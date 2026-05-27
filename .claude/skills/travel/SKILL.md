# Travel Loop — Skill Definition

## Identity

| Key | Value |
|-----|-------|
| Skill | travel |
| Type | sub-loop |
| Parent | scene-loop |
| Purpose | Handle overland movement between locations with random encounters, navigation, and time tracking |

## Vocabulary

| Term | Definition |
|------|-----------|
| Pace | Travel speed: fast (4 mph), normal (3 mph), slow (2 mph) |
| Random Encounter | Chance-based combat or social encounter during travel (d20, threshold varies by terrain) |
| Navigation | Survival check to stay on course in wilderness; failure = lost time |
| Foraging | Survival DC 10 to find food (1d6 + WIS modifier rations) |

## Contracts

| Contract | File |
|----------|------|
| Input | -> [[contracts/travel-action-contract.json]] |
| Output | -> [[contracts/travel-outcome-contract.json]] |

## D&D 5e Travel Pace

| Pace | Speed | Miles/Day | Effect |
|------|-------|-----------|--------|
| Fast | 4 mph | 30 | -5 passive Perception |
| Normal | 3 mph | 24 | -- |
| Slow | 2 mph | 18 | Can use Stealth |

## Resolution Flow

1. Scene loop sends travel action (origin, destination, mode, pace)
2. Calculate distance and travel time based on pace
3. Present travel options via action-prompt: set pace, set watch order, forage, forced march
4. For each travel segment (per 4 hours or per hex):
   - Roll for random encounter (d20; encounter threshold varies by terrain safety)
   - If encounter triggers: dispatch to combat-loop or social-loop, then resume travel
   - Navigation check if off-road (Survival DC based on terrain: road=auto, trail=10, wilderness=15)
   - Optional foraging (Survival DC 10; success = 1d6 + WIS mod rations found)
5. On arrival: update location in campaign state
6. Return outcome with distance covered, time elapsed, encounters triggered

## Random Encounter Thresholds

| Terrain | Encounter On | Examples |
|---------|-------------|----------|
| Road | 18+ on d20 | Triboar Trail, High Road |
| Trail | 16+ on d20 | Forest paths, mountain passes |
| Wilderness | 14+ on d20 | Neverwinter Wood, open plains |
| Dangerous | 12+ on d20 | Orc territory, underdark passages |

## Agent Execution

1. **Determine route** from act file or campaign state — origin and destination
2. **Ask pace** using action-prompt with `travel` context: fast/normal/slow
3. **Set watch** — ask party watch order for camp and travel
4. **Narrate travel** — describe terrain, weather, landmarks
5. **Roll encounters** — for each segment, "Roll d20 for random encounter"
6. **If encounter:** dispatch to appropriate loop (combat/social), then resume
7. **Navigation:** if off-road, prompt "Make a Survival check (DC 15)"
8. **Arrival:** describe destination, update campaign_state.json location

## Integration

- **Depends on:** action-prompt (user choices), combat-loop (if encounter triggers combat), campaign state (location, time)
- **Returns to:** scene-loop (outcome dict with distance, time, encounters, location_updated)
- **State updates:** campaign_state.json → location, time_elapsed, random encounters resolved
