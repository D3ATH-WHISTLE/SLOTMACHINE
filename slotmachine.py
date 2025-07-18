import random
from dataclasses import dataclass
from typing import List, Dict, Tuple

@dataclass
class SlotSymbol:
    name: str
    value: int
    weight: int

class SlotMachine:
    def __init__(self):
        self.symbols = [
            SlotSymbol("Cherry", 2, 20),
            SlotSymbol("Lemon", 5, 15),
            SlotSymbol("Orange", 10, 10),
            SlotSymbol("Plum", 15, 8),
            SlotSymbol("Bell", 20, 5),
            SlotSymbol("Bar", 50, 2),
            SlotSymbol("Seven", 100, 1)
        ]
        self.balance = 100  # Starting balance
        self.current_bet = 5  # Default bet amount
    
    def spin(self) -> Tuple[List[SlotSymbol], int]:
        """Simulate a spin and return the result and winnings"""
        if self.balance < self.current_bet:
            raise ValueError("Insufficient balance for bet")
        
        self.balance -= self.current_bet
        
        # Weighted random selection of symbols
        result = [
            random.choices(
                self.symbols,
                weights=[s.weight for s in self.symbols],
                k=1
            )[0] for _ in range(3)
        ]
        
        # Calculate winnings
        first_symbol = result[0].name
        if all(s.name == first_symbol for s in result):
            # All three match
            winnings = 10 * result[0].value * self.current_bet
        elif result[0].name == result[1].name or \
             result[1].name == result[2].name or \
             result[0].name == result[2].name:
            # Two match
            if result[0].name == result[1].name:
                winnings = 2 * result[0].value * self.current_bet
            else:
                winnings = 2 * result[1].value * self.current_bet
        else:
            winnings = 0
            
        self.balance += winnings
        return (result, winnings)
    
    def change_bet(self, amount: int):
        """Set the bet amount"""
        if amount <= 0:
            raise ValueError("Bet amount must be positive")
        self.current_bet = amount

if __name__ == "__main__":
    slot = SlotMachine()
    print("Welcome to Python Slot Machine!")
    print(f"Starting balance: ${slot.balance}")
    
    while True:
        print(f"\nCurrent bet: ${slot.current_bet}")
        print(f"Balance: ${slot.balance}")
        
        cmd = input("Enter 'spin', 'bet X', or 'quit': ").lower().strip()
        
        if cmd.startswith("bet "):
            try:
                amount = int(cmd.split()[1])
                slot.change_bet(amount)
                print(f"Bet amount set to ${amount}")
            except (ValueError, IndexError):
                print("Invalid bet command. Usage: 'bet X'")
        elif cmd == "spin":
            try:
                result, winnings = slot.spin()
                symbols = [s.name for s in result]
                print(f"{' | '.join(symbols)}")
                if winnings > 0:
                    print(f"You won ${winnings}!")
                else:
                    print("No win this time.")
            except ValueError as e:
                print(str(e))
        elif cmd == "quit":
            print(f"Game over. Final balance: ${slot.balance}")
            break
        else:
            print("Invalid command")

