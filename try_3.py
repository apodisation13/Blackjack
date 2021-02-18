from random import choice
from calc_card import calc_cards


def starting_draw_dealer(cards: list):
    """начальный дро дилера"""
    starting_dealer_hand = []
    for _ in range(2):
        dealer_choice = choice(cards)
        cards.remove(dealer_choice)
        starting_dealer_hand.append(dealer_choice)
    print(f"Карты в руке дилера: ['{starting_dealer_hand[0]}', ??]")
    print(starting_dealer_hand)
    return starting_dealer_hand


def starting_draw_player(cards: list):
    """начальный дро игрока"""
    starting_player_hand = []
    for _ in range(2):
        player_choice = choice(cards)
        cards.remove(player_choice)
        starting_player_hand.append(player_choice)
    print(f'Карты в руке игрока: {starting_player_hand}')
    return starting_player_hand


def hit(cards: list, hand: list):
    """кто-то берет 1 карту"""
    player_choice = choice(cards)
    cards.remove(player_choice)
    hand.append(player_choice)
    print(f'hit {player_choice}')
    return hand


def check_score(result: tuple):
    if result[1]:
        if result[1] == 21:
            print("BLACKJACK!!!")
            return result[1]
        print(f'Результат игрока {result[0]}/{result[1]}')
    else:
        print(f'Результат игрока {result[0]}')
        if result[0] > 21:
            print("\033[31m{}\033[0m".format("BUSTED! You lose the game!"))
        elif result[0] == 21:
            print("BLACKJACK!!!")
    return result[0]


def check_starting_hand_blackjack(player, dealer, hand):
    if dealer == 21 and player != 21:
        print("\033[31m{}\033[0m".format(f'{hand} - BLACKJACK!!! Dealer wins, you lose!'))
    elif player == 21 and dealer != 21:
        print("\033[32m{}\033[0m".format('BLACKJACK!!! You win the game!'))
    elif player == 21 and dealer == 21:
        print("НИЧЬЯ! НУ НИЧЕГО СЕБЕ...")
    else:
        return


def dealer_AI(dealer_score, player_score, dealer_hand, player_hand):
    """логика дилера - взять карту пока у него не столько же сколько у игрока"""
    while dealer_score <= player_score:
        hit(cards, dealer_hand)
        d_result = calc_cards(dealer_hand, first_draw=False)
        dealer_score = d_result[0]
        print(f'Карты в руке дилера: {dealer_hand} - {dealer_score}')
    print(f'Игрок: {player_hand} - {player_score}, Дилер: {dealer_hand} - {dealer_score}')
    return dealer_score


def check_win(player_score, dealer_score):
    if dealer_score > 21:
        print("\033[32m{}\033[0m".format("DEALER BUSTED! You win the game!"))
        return
    if dealer_score == 21 and player_score == 21:
        print("НИЧЬЯ! НУ НИЧЕГО СЕБЕ...")
        return
    if dealer_score == player_score:
        print('НИЧЬЯ')
    if dealer_score > player_score:
        print("\033[31m{}\033[0m".format("Dealer wins the game! You lose!"))
    if dealer_score < player_score:
        print("\033[32m{}\033[0m".format("You win the game!"))



cards = [2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5,
         6, 6, 6, 6, 7, 7, 7, 7, 8, 8, 8, 8, 9, 9, 9, 9, 10, 10, 10, 10,
         "J", "J", "J", "J", "Q", "Q", "Q", "Q", "K", "K", "K", "K",
         "A", "A", "A", "A"]

dealer_hand = starting_draw_dealer(cards)
player_hand = starting_draw_player(cards)
player_result = calc_cards(player_hand, first_draw=True)
dealer_result = calc_cards(dealer_hand, first_draw=True)

if player_result[1]:
    print(f'Результат игрока {player_result[0]}/{player_result[1]}')
else:
    print(f'Результат игрока {player_result[0]}')

check_starting_hand_blackjack(player_result[0], dealer_result[0], dealer_hand)

print("\nВы можете ввести: hit/h чтобы взять ещё карту, "
      "stand/s чтобы остановиться, double/d чтобы удвоить ставку и взять одну карту")

hit_status = False

while True:
    command = input("\nВведите команду: ")

    if command.lower() in ["hit", 'h']:
        hit_status = True
        hit(cards, player_hand)
        # player_hand = ["A", 3, "A"]
        player_result = calc_cards(player_hand, first_draw=False)
        print(f'Карты в руке игрока: {player_hand}')
        player_score = check_score(player_result)

        if player_score >= 21:
            break

    elif command.lower() in ["stand", "s"]:
        print(f'\nКарты дилера: {dealer_hand} - {dealer_result[0]}')
        dealer_score = dealer_AI(dealer_result[0], player_result[0], dealer_hand, player_hand)
        if hit_status:
            check_win(player_score, dealer_score)
        else:
            check_win(player_result[0], dealer_score)
        break
