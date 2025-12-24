# Lockdown

A multiplayer digital version of the card game **Lockdown**, playable with **4–8 players**, with an optional **AI practice mode**.

## Objective
Finish the round with the **lowest total card sum**.

## Rules

### The Deal
- Each player is dealt **4 cards** from a standard 52-card deck (**no jokers**).
- Cards are placed **face down** in a **2×2 grid**.
- At the start of the game, each player may look at **exactly one** of their cards **one time**.
- Players must keep their cards hidden from others for the entire game.

### The Play
Players take turns. On your turn, you may do **one** of the following:
1. Draw a card from the deck and place it in the discard pile.
2. Draw a card from the deck, swap it with one of your cards, then discard the swapped card.
3. Take the top card from the discard pile and swap it with one of your cards.
4. **Call lockdown** (every other player gets one final turn, then the game ends).

### Special Cards
- **Queens (any suit)**  
  If drawn from the deck and discarded, you may:
  - Look at one of your cards
  - Look at one card from another player
  - Optionally swap those two cards

- **10s (any suit)**  
  If drawn from the deck and discarded, you may look at one of your cards.

- **Red Kings (♦ ♥)**  
  Worth **–1 point**.

### Tapping
If a player knows the identity of **two cards with the same value**, they may tap them:
- A tap may occur **at any time**, even when it is not your turn.
- Players **cannot** tap two of their own cards together.
- Players who have called lockdown **cannot tap** afterward.

#### Successful Tap
- Matching cards are discarded **without replacement**.
- The tapping player is **rewarded** (reduces card count).
- If another player’s card was tapped, that player is **penalized**.

#### Failed Tap or Being Tapped
- The penalized player must **increase their card count by one**.

### Scoring
After lockdown and final turns:
- Remaining cards are totaled.
- **Lowest score wins**.

Card values:
- Red King: –1
- A–10: face value
- Jack: 11
- Queen: 12
- Black King: 13

## Planned Features
- Online multiplayer (4–8 players)
- AI practice opponents
- Game state validation & logging
- Clean UI with hidden information support

See `docs/SPEC.md` for the full implementation specification.

