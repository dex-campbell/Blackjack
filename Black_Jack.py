# -*- coding: utf-8 -*-
"""
Created on Thu Aug 15 21:37:10 2024

@author: dexte
"""

import os
import random

def menu():
    print("Menu:")
    print("1. Create user")
    print("2. View User Balance")
    print("3. Play Black Jack")
    print("4. Exit")
    return input("Please select an option (1-4): ")

def create_user():
    file_name = input("Enter the name of the file you want to create (with .txt extension): ")

    directory = r"D:\Work\Projects\Black_Jack\Users"
    full_path = os.path.join(directory, file_name)
    
    if os.path.exists(full_path):
        print(f"A user with the name '{file_name}' already exists. Please choose a different name.")
        return
    
    try:
        with open(full_path, 'w') as file:
            file.write("money=100\n")  # Add a row for money and set it to 100
            print(f"File '{file_name}' created successfully at '{directory}' with money set to 100.")
    except Exception as e:
        print(f"An error occurred while creating the file: {e}")
        
def load_user_balance(user_file):
    directory = r"D:\Work\Projects\Black_Jack\Users"
    full_path = os.path.join(directory, user_file)
    
    with open(full_path, 'r') as file:
        for line in file:
            if line.startswith("money="):
                return int(line.split('=')[1])
    return 0

def save_user_balance(user_file, balance):
    directory = r"D:\Work\Projects\Black_Jack\Users"
    full_path = os.path.join(directory, user_file)
    
    with open(full_path, 'w') as file:
        file.write(f"money={balance}\n")

def print_user_balance():
    user = pick_user()
    if not user:
        return

    balance = load_user_balance(user)
    print(f"{user}'s current balance: {balance}")

def play_black_jack():
    user = pick_user()
    if not user:
        return

    balance = load_user_balance(user)
    print(f"Your current balance: {balance}")

    while True:
        try:
            bet = int(input("Enter your bet amount: "))
            if bet > balance:
                print("You cannot bet more than your current balance.")
            else:
                break
        except ValueError:
            print("Invalid bet amount. Please enter a number.")

    deck = create_shuffled_deck()
    player_hand, dealer_hand = deal_initial_cards(deck)
    player_value = calculate_hand_value(player_hand)
    
    print(f"Your hand: {player_hand} ({player_value})")
    print(f"Dealer's hand: [{dealer_hand[0]}, Hidden]")
    
    while True:
        choice = input("Do you want to 'hit' or 'stand'? ").lower()
        
        if choice == 'hit':
            player_hand.append(deck.pop(0))
            player_value = calculate_hand_value(player_hand)
            print(f"Your hand: {player_hand} (Value: {player_value})")
            
            if player_value > 21:
                print("Bust! You exceeded 21. Dealer wins.")
                balance -= bet
                save_user_balance(user, balance)
                print(f"Your new balance: {balance}")
                return
        elif choice == 'stand':
            break
        else:
            print("Invalid choice, please enter 'hit' or 'stand'.")

    dealer_value = calculate_hand_value(dealer_hand)
    print(f"Dealer's hand: {dealer_hand} (Value: {dealer_value})")

    while dealer_value < 17:
        dealer_hand.append(deck.pop(0))
        dealer_value = calculate_hand_value(dealer_hand)
        print(f"Dealer's hand: {dealer_hand} (Value: {dealer_value})")
    
    player_value = calculate_hand_value(player_hand)
    if dealer_value > 21 or player_value > dealer_value:
        print("Congratulations! You win!")
        balance += bet
    elif player_value < dealer_value:
        print("Dealer wins!")
        balance -= bet
    else:
        print("It's a tie!")
    
    save_user_balance(user, balance)
    print(f"Your new balance: {balance}")

def create_shuffled_deck():
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
    deck = [f"{rank} of {suit}" for suit in suits for rank in ranks]
    random.shuffle(deck)
    return deck

def pick_user():
    directory = r"D:\Work\Projects\Black_Jack\Users"
    users = [file for file in os.listdir(directory) if os.path.isfile(os.path.join(directory, file))]
    
    if not users:
        print("No users found in the directory.")
        return None
    
    print("Select a user from the list below:")
    for index, user in enumerate(users, start=1):
        print(f"{index}. {user}")

    try:
        choice = int(input("Enter the number corresponding to the user you want to pick: "))
        if 1 <= choice <= len(users):
            selected_user = users[choice - 1]
            print(f"You have selected: {selected_user}")
            return selected_user
        else:
            print("Invalid choice. Please select a valid number.")
            return None
    except ValueError:
        print("Invalid input. Please enter a number.")
        return None
    
def deal_initial_cards(deck):
    player_hand = []
    dealer_hand = []

    player_hand.append(deck.pop(0))
    dealer_hand.append(deck.pop(0))
    player_hand.append(deck.pop(0))
    dealer_hand.append(deck.pop(0))

    return player_hand, dealer_hand

def calculate_hand_value(hand):
    value = 0
    aces = 0
    for card in hand:
        rank = card.split(' ')[0]
        if rank in ['Jack', 'Queen', 'King']:
            value += 10
        elif rank == 'Ace':
            aces += 1
            value += 11
        else:
            value += int(rank)
    
    while value > 21 and aces:
        value -= 10
        aces -= 1

    return value

def main():
    while True:
        choice = menu()
        if choice == '1':
            create_user()
        elif choice == '2':
            print_user_balance()
        elif choice == '3':
            play_black_jack()
        elif choice == '4':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice, please try again.")

main()

