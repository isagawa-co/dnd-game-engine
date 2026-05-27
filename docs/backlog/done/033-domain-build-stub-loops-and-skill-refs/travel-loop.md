# Travel Loop

## Status
NEW

## Location
`.claude/skills/travel/SKILL.md` + `.claude/skills/travel/contracts/`

## What
Travel loop for overland movement between locations. Handles distance/time calculation, random encounter checks, navigation (Survival checks to avoid getting lost), foraging, and weather. Dispatched by state evaluation when `travel.active == true` or by scene loop when `encounter_type == "travel"`.

## Resolution Flow
1. Receive travel action (origin, destination, mode, pace)
2. Calculate distance and travel time based on pace (fast/normal/slow)
3. For each travel segment (per 4 hours or per hex):
   - Roll for random encounter (d20, encounter on 17+ in wilderness)
   - If encounter: dispatch to combat or social loop, then resume travel
   - Navigation check if off-road (Survival DC based on terrain)
   - Optional foraging (Survival DC 10 for 1d6+WIS food)
4. Update location in campaign state
5. Return outcome with distance covered, time elapsed, encounters triggered

## Contracts Needed
- `travel-action-contract.json` — input: origin, destination, pace (fast/normal/slow), mode (foot/mount/vehicle)
- `travel-outcome-contract.json` — output: distance_covered, time_elapsed, encounters, location_updated, navigation_result

## D&D 5e Travel Pace
| Pace | Speed | Effect |
|------|-------|--------|
| Fast | 4 mph / 30 miles/day | -5 passive Perception |
| Normal | 3 mph / 24 miles/day | — |
| Slow | 2 mph / 18 miles/day | Can stealth |

## Dependencies
- action-prompt skill (user choices)
- combat loop (if random encounter triggers combat)
- campaign state (location, time tracking)
- adventure act files (encounter tables)
