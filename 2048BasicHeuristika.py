import logic
import time
import random

# Spustenie hry
mat = logic.start_game()
move_count = 0
total_score =0
# Povolené pohyby (W len ako posledná možnosť)
moves = ["A", "S", "D"]
moves_with_w = ["A", "S", "D", "W"]


def evaluate_grid(grid):
    """
    Heuristická funkcia hodnotiaca stav mriežky:
    1. Počet voľných buniek (čím viac, tým lepšie).
    2. Najväčšia hodnota v rohu (preferujeme).
    3. Sú usporiadané veľké hodnoty vedľa seba?
    """
    empty_cells = sum(row.count(0) for row in grid)
    max_tile = max(max(row) for row in grid)

    # Bonus za držanie najväčšej dlaždice v rohu
    corner_bonus = 0
    if grid[3][0] == max_tile or grid[3][3] == max_tile:
        corner_bonus = 15  # Zväčšili sme bonus, aby solver držal číslo v rohu

    # Penalizácia za rozhádzané čísla (chceme zoradenie)
    monotonicity_score = 0
    for row in grid:
        for i in range(3):
            if row[i] > row[i + 1]:  # Ak číslo vľavo je väčšie ako vpravo, penalizácia
                monotonicity_score -= 1

    return empty_cells * 5 + corner_bonus + monotonicity_score  # Viac voľných miest = lepší pohyb


def simulate_move(grid, move):
    """Simuluje pohyb a vráti novú mriežku + či sa niečo zmenilo."""
    if move == "A":
        return logic.move_left(grid)
    elif move == "S":
        return logic.move_down(grid)
    elif move == "D":
        return logic.move_right(grid)
    elif move == "W":
        return logic.move_up(grid)
    return grid, False


def find_best_move(grid, depth=3):
    """
    Simuluje najlepšie možné ťahy niekoľko krokov dopredu
    a vyberie pohyb, ktorý má najlepší výsledok.
    """
    best_score = -float('inf')
    best_move = None

    for move in moves:
        new_grid, changed, score = simulate_move(grid, move)

        if changed:
            # Ak sa pohyb vykonal, vypočítame skóre rekurzívne
            score = score + evaluate_grid(new_grid)

            # Skúsime simulovať viacero ťahov dopredu
            if depth > 1:
                _, next_score = find_best_move(new_grid, depth - 1)
                score += next_score * 0.8  # Budúce kroky majú menší vplyv

            if score > best_score:
                best_score = score
                best_move = move

    return best_move, best_score


while True:
    # Nájdeme najlepší pohyb pomocou heuristiky a simulácie viacerých ťahov
    best_move, _ = find_best_move(mat, depth=3)

    # Ak nenájdeme dobrý pohyb, skúsime aj W ako poslednú možnosť
    if best_move is None:
        for move in moves_with_w:
            new_mat, changed,score = simulate_move(mat, move)
            if changed:
                best_move = move
                break

    # Ak už nie je možný žiadny pohyb, hra skončila
    if best_move is None:
        break

    # Vykonáme najlepší pohyb
    mat, _, score = simulate_move(mat, best_move)
    move_count += 1
    total_score=total_score+score

    # Skontrolovať stav hry
    status = logic.get_current_state(mat)
    print(f"Move {move_count}: {status}")

    # Vytlačiť aktuálnu hraciu plochu
    for row in mat:
        print(row)

    # Ak hra skončila, ukončíme cyklus
    if status != "GAME NOT OVER":
        break

    # Pridať novú 2-ku na náhodné miesto
    logic.add_new_2_or_4(mat)

    # Počkaj 0.1 sekundy, aby sme videli priebeh hry
    time.sleep(0.001)

# Výpis výsledkov
print("\nHra skončila! ")
print(f"Najvyššia dlaždica: {max(max(row) for row in mat)}")
print(f"Počet vykonaných ťahov: {move_count}")
print(f"Celkové skóre: {total_score}")
