 #!/usr/bin/env python3
import random
import time
from pathlib import Path

# === CONSTANTS ===
HIGH_SCORE_FILE = Path("high_score.txt")
KEY_NAME = "King's Golden Key"

dungeon_rooms = 5
starting_HP = 100


# === HIGH SCORE HANDLING ===
def compute_score(player: dict, treasures: dict) -> int:
    total_value = sum(treasures.get(item, 0) for item in player["inventory"])
    return total_value + player["health"]


def load_high_score() -> int:
    try:
        return int(HIGH_SCORE_FILE.read_text().strip())
    except Exception:
        return 0


def save_high_score(score: int) -> None:
    try:
        current = load_high_score()
        if score > current:
            HIGH_SCORE_FILE.write_text(str(score))
    except Exception:
        pass  # ignore file write issues


# === GAME SETUP ===
def setup_player() -> dict:
    name = input("Player, your name: ").strip() or "Anonymous"
    return {"name": name, "health": starting_HP, "inventory": []}


def create_treasures() -> dict:
    return {
        "🪙  Gold Coin": 10,
        "💎  Diamond": 40,
        "💫  Stardust": 60,
        "⚔️  Magic Sword": 80,
        "❤️  Philosopher's Heart": 100,
    }


def create_traps() -> dict:
    return {
        "🤢  Poison Gas": 10,
        " 🐍  Snake Pit": 20,
        "🪨  Runaway Boulder": 30,
        "👻  Demon Ghost Boo": 40,
        "🧌  Elite Troll attacks": 50,
    }


def create_potions() -> dict:
    return {"🧪 Ordinary Healing Potion": 10, "⚡ Healing Elemental Thunder Potion": 50}


# ===PLAYER DISPLAY OPTIONS ===
def display_options(room_number: int) -> None:
    print(f"\n--- Room {room_number} ---")
    print("1) Search for treasure")
    print("2) Move forward to the next room")
    print("3) Check health and inventory")
    print("4) Quit the game")


# === SEARCH DUNGEON ROOM ===
def search_room(player: dict, treasures: dict, traps: dict, potions: dict) -> None:
    """Player searches the room for treasures, potions, a rare full-heal, or a trap."""

    # Rare full-health (Phoenix Tears)
    if random.random() < 0.12:  # overall 12% chance
        player["health"] = starting_HP
        print(
            f" 🐦‍🔥 💧 You found Phoenix Tears! Full recovery to {player['health']} HP!"
        )
        return

    # Rare King's Golden Key drop for BONUS ROOM (~8% chance)
    if KEY_NAME not in player["inventory"] and random.random() < 0.08:
        player["inventory"].append(KEY_NAME)
        print(
            f"🗝️  You found the {KEY_NAME}! It might open a hidden door, search if you dare..."
        )
        choice = (
            input("\nDo you wish to enter the BONUS ROOM now? (y/n): ").strip().lower()
        )
        if choice == "y":
            bonus_room(player, treasures, traps, potions)
        else:
            print("The passage fasdes back into the shadows...")
        return  # stop processing this turn once key is found

    # ---- Otherwise, random outcomes occur ----
    roll = random.random()

    # 30% treasure
    if roll < 0.30:
        item = random.choice(list(treasures.keys()))
        player["inventory"].append(item)
        print(f"💰 You found a {item}! (+{treasures.get(item, 0)} value)")

    # 20% healing potion
    elif roll < 0.50:
        potion = random.choice(list(potions.keys()))
        heal = potions[potion]
        player["health"] = min(starting_HP, player["health"] + heal)
        print(f"🏺 You obtained {potion}! (+{heal} HP, now {player['health']})")

    # Otherwise it's a trap!
    else:
        # Choose a random trap from the traps dictionary
        trap = random.choice(list(traps.keys()))
        dmg = traps[trap]

        # Apply damage
        player["health"] = max(0, player["health"] - dmg)

        # Player Results
        print(f"☠️  You triggered a {trap}! {-dmg} HP, remaining: {player['health']}")


# === STATUS ===
def check_status(player: dict, treasures: dict) -> None:
    print("\n--- Status ---")
    print(f"🌡️ Health: {player['health']}")
    if player["inventory"]:
        print("Inventory:", ", ".join(player["inventory"]))
    else:
        print("Inventory: (empty)")

    # Calculate current treasure value and live score
    total_value = sum(treasures.get(item, 0) for item in player["inventory"])
    score = total_value + player["health"]
    print(f"Treasure Value: {total_value}")
    print(f"🏆 Current Score: {score:,}")


# === BONUS ROOM ===
def bonus_room(player: dict, treasures: dict, traps: dict, potions: dict) -> None:
    print("\n ✨ A hidden gateway is revealed...welcome to the BONUS ROOM!")
    roll = random.random()

    if roll < 0.45:  # 45% chance of finding treasure
        item = random.choice(list(treasures.keys()))
        player["inventory"].append(item)
        print(f"BONUS FIND! You found a {item}! (+{treasures.get(item, 0)} value)")
    elif roll < 0.70:
        potion = random.choice(list(potions.keys()))
        heal = potions[potion]
        player["health"] = min(starting_HP, player["health"] + heal)
        print(f"Excellent! {potion} heals you (+{heal} HP, now {player['health']})")
    else:  # 30% trap
        trap = random.choice(list(traps.keys()))
        dmg = traps[trap]
        player["health"] = max(0, player["health"] - dmg)
        print(f"💣 You triggered a {trap}! (-{dmg} HP, remaining {player['health']})")


# === END GAME ===
def end_game(player: dict, treasures: dict) -> None:
    total_value = sum(treasures.get(item, 0) for item in player["inventory"])
    print("\n=== GAME OVER ===")
    print(f"Final Health: {player['health']}")
    if player["inventory"]:
        print("Final Inventory:", ", ".join(player["inventory"]))
    else:
        print("Inventory: (empty)")
    print(f"Total Treasure Value: {total_value}")


# === MAIN GAME LOOP ===
def run_game_loop(player: dict, treasures: dict, traps: dict, potions: dict) -> None:
    room = 1
    while room <= dungeon_rooms and player["health"] > 0:
        display_options(room)
        choice = input("> ").strip()

        if choice == "1":
            search_room(player, treasures, traps, potions)
        elif choice == "2":
            room += 1
            print("⏭️  Passing onto the next room...")
        elif choice == "3":
            check_status(player, treasures)
        elif choice == "4":
            print("👣 You are leaving the dungeon...")
            break
        else:
            print("{Please select 1, 2, 3, or 4.")

        # small pause between turns
        time.sleep(1.5)

    # Bonus room offered if the player finds the key and survives
    if player["health"] > 0 and KEY_NAME in player["inventory"]:
        choice = (
            input(
                "A hidden passage way opens, do you wish to enter the BONUS ROOM? (y/n: "
            )
            .strip()
            .lower()
        )
        if choice == "y":
            bonus_room(player, treasures, traps, potions)
        else:
            print(" the passage closes.")

    end_game(player, treasures)


# === MAIN ===
def main() -> None:
    print(
        "Welcome treasure hunters and adventurers 💀 🗡️, enter the Dungeon of Death and collect treasure if you dare!"
    )

    while True:
        # Blank slate, fresh game each round
        player = setup_player()
        treasures = create_treasures()
        traps = create_traps()
        potions = create_potions()

        # Play one full game run
        run_game_loop(player, treasures, traps, potions)

        # --- Scoring and high-scoare game tracking ---
        score = compute_score(player, treasures)
        high = load_high_score()
        if score > high:
            save_high_score(score)
            print(f"\n 🎉 New High Score: {high}  (Previous: {high})")

        # ---replay options ---
        again = input("\nPlay again? (y/n): ").strip().lower()
        if again != "y":
            print("Until we meet again adventurer!")
            break


if __name__ == "__main__":
    main()
