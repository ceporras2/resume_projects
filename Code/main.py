from art import logo
import random


def deal_card():
    # Returns a random card from the deck.
    cards = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
    return random.choice(cards)


def calculate_score(cards_):
    # Takes a list of cards and returns the score calculated from the cards.
    if len(cards_) == 2 and sum(cards_) == 21:
        return 0
    elif 11 in cards_ and sum(cards_) > 21:
        cards_.remove(11)
        cards_.append(1)
    return sum(cards_)


def compare(user_score, comp_score):
    if user_score > 21 and comp_score > 21:
        return "You went over. You lose."

    if user_score == comp_score:
        return "Draw."
    elif comp_score == 0:
        return "Lose, opponent has Blackjack!"
    elif user_score == 0:
        return "Win with a Blackjack!"
    elif user_score > 21:
        return "You went over. You lose."
    elif comp_score > 21:
        return "Opponent went over. You win!"
    elif user_score > comp_score:
        return "You win!"
    else:
        return "You lose."


def play_game():
    print(logo)

    user_cards = []
    comp_cards = []
    user_score = 0
    comp_score = 0
    is_game_over = False

    for _ in range(2):
        user_cards.append(deal_card())
        comp_cards.append(deal_card())

    while not is_game_over:
        user_score = calculate_score(user_cards)
        comp_score = calculate_score(comp_cards)

        print(f"Your cards: {user_cards}, current score: {user_score}")
        print(f"Computer's first card: {comp_cards[0]}")

        if user_score == 0 or comp_score == 0 or user_score > 21:
            is_game_over = True
        else:
            user_should_deal = input("Type 'y' to get another card, type 'n' to pass: ")
            if user_should_deal == "y":
                user_cards.append(deal_card())
            else:
                is_game_over = True

    while comp_score != 0 and comp_score < 17:
        comp_cards.append(deal_card())
        comp_score = calculate_score(comp_cards)

    print(f"Your final hand: {user_cards}, final score: {user_score}")
    print(f"Computer's final hand: {comp_cards}, final score: {comp_score}")
    print(compare(user_score, comp_score))


while input("Do you want to play a game of Blackjack? Type 'y' or 'n': ") == "y":
    play_game()
