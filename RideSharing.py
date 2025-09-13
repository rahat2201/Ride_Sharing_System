from typing import List, Dict
from collections import defaultdict

class Person:
    def __init__(self, name: str):
        self.name = name
        self.id = id(self)

    def __repr__(self):
        return self.name

class Expense:
    def __init__(self, description: str, amount: float, payer: Person, participants: List[Person]):
        self.description = description
        self.amount = amount
        self.payer = payer
        self.participants = participants

    def split_amount(self) -> Dict[Person, float]:
        share = self.amount / len(self.participants)
        return {p: share for p in self.participants}

class FairShareApp:
    def __init__(self):
        self.people: List[Person] = []
        self.expenses: List[Expense] = []

    def add_person(self, name: str):
        person = Person(name)
        self.people.append(person)
        print(f"Added person: {person.name}")

    def add_expense(self, desc: str, amount: float, payer_name: str, participant_names: List[str]):
        payer = next((p for p in self.people if p.name == payer_name), None)
        participants = [p for p in self.people if p.name in participant_names]
        if payer and participants:
            expense = Expense(desc, amount, payer, participants)
            self.expenses.append(expense)
            print(f"Added expense: {desc}, Amount: {amount}, Payer: {payer}, Participants: {participants}")
        else:
            print("Invalid payer or participants.")

    def calculate_shares(self):
        balances = defaultdict(float)
        for expense in self.expenses:
            shares = expense.split_amount()
            for person, share in shares.items():
                balances[person] -= share
            balances[expense.payer] += expense.amount
        return balances

    def get_report(self):
        balances = self.calculate_shares()
        print("\n--- Fair Share Report ---")
        for person, balance in balances.items():
            print(f"{person.name}: {'owes' if balance < 0 else 'is owed'} {abs(balance):.2f}")
        print("------------------------\n")

# Demo usage
if __name__ == "__main__":
    app = FairShareApp()
    app.add_person("Alice")
    app.add_person("Bob")
    app.add_person("Charlie")
    app.add_expense("Dinner", 90, "Alice", ["Alice", "Bob", "Charlie"])
    app.add_expense("Movie", 60, "Bob", ["Alice", "Bob"])
    app.add_expense("Drinks", 30, "Charlie", ["Alice", "Charlie"])
    app.get_report()