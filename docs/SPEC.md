# Lockdown — Implementation Specification

This document defines precise game behavior for implementation.

## Core Entities
- **Card**: rank, suit, value
- **Deck**: shuffled draw pile (52 cards, no jokers)
- **Discard Pile**: face-up pile, top card visible
- **Player**:
  - List of facedown cards (initially 4)
  - One-time peek flag
  - Lockdown flag
  - AI or human

## Setup
1. Shuffle deck.
2. Deal 4 facedown cards to each player.
3. Each player may peek at exactly one card.
4. Establish turn order.

## Turn Actions
A player may choose exactly one:
- Draw → discard
- Draw → swap with own card → discard swapped
- Take discard → swap with own card
- Call lockdown

## Special Card Triggers
Triggers only occur when **drawn from deck and placed directly into discard**.

### Queen
- Look at one of your cards
- Look at one opponent’s card
- Optional swap

### Ten
- Look at one of your cards

### Red King
- Value –1 only (no action)

## Tapping
- May occur at any time unless the tapper called lockdown.
- Cannot tap two of your own cards.
- Valid targets:
  - Player card + discard top
  - Player card + another player card

### Successful Tap
- Matching cards are discarded.
- Tapping player is rewarded (cards removed).
- Other player (if involved) is penalized.

### Failed Tap or Being Tapped
- Penalized player draws 1 facedown card from the deck.

## Lockdown
- Caller ends their participation.
- Every other player gets exactly one final turn.
- No tapping allowed by the caller.

## Endgame
- Sum remaining cards.
- Lowest score wins.
- Tie-breaking: TBD.

## Open Questions
- Should special effects trigger on swapped cards?
- How ties are resolved
- Discard behavior when tapping discard + player card
