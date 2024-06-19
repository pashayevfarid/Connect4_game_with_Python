import random as rnd

def alpha_beta_decision(board, turn, ai_level, queue, max_player):

    # We define a function to evaluate the current game position
    def evaluate_position(board, max_player):
        # If the game has been won, we return positive or negative infinity based on the winner
        if board.check_victory():
            return float('inf') if turn % 2 + 1 == max_player else float('-inf')
              
        score = 0

        # We evaluate each row on the game board
        for row in range(6):
            for horizontal_shift in range(4):
                try:
                    row_values = board.grid[horizontal_shift:horizontal_shift + 4, row]
                except IndexError:
                    # Handle index error and continue to the next iteration
                    print(f"We encountered an error: Index {horizontal_shift} is out of bounds for axis 0 with size {board.grid.shape[0]}")
                    continue
                score += evaluate_row(row_values, max_player)

        # We evaluate each column on the game board
        for column in range(7):
            for vertical_shift in range(3):
                try:
                    column_values = board.grid[column, vertical_shift:vertical_shift + 4]
                except IndexError:
                    # Handle index error and continue to the next iteration
                    print(f"We encountered an error: Index {vertical_shift} is out of bounds for axis 0 with size {board.grid.shape[0]}")
                    continue
                score += evaluate_row(column_values, max_player)

        return score
    
    # We define a function to evaluate a row of values
    def evaluate_row(row_values, max_player):
        # Count occurrences of AI and opponent pieces in the line
        ai_count = row_values.tolist().count(max_player)
        opponent_count = row_values.tolist().count(3 - max_player)

        # Evaluate the row based on piece counts
        if ai_count == 4:
            # Four AI pieces in a row is highly desirable (winning position)
            return 1000
        elif opponent_count == 4:
            # Four opponent pieces in a row is highly undesirable (losing position)
            return -1000
        elif ai_count == 3 and opponent_count == 0:
            # Three AI pieces in a row with an open spot is advantageous
            return 100
        elif ai_count == 2 and opponent_count == 0:
            # Two AI pieces in a row with an open spot is moderately advantageous
            return 10
        elif opponent_count == 3 and ai_count == 0:
            # Three opponent pieces in a row with an open spot is disadvantageous
            return -100
        elif opponent_count == 2 and ai_count == 0:
            # Two opponent pieces in a row with an open spot is moderately disadvantageous
            return -10
        elif ai_count == 3:
            # Three AI pieces in a row is moderately desirable
            return 50  
        elif ai_count == 2 and opponent_count == 1:
            # Two AI pieces and one opponent piece in a row is moderately desirable
            return 5   
        elif opponent_count == 2 and ai_count == 0:
            # Two opponent pieces in a row with an open spot is moderately disadvantageous
            return -5  

        # No significant pattern in the row
        return 0

    # We define a function for the max player's move selection
    def max_value(board, depth, alpha, beta, max_player):
        # If the depth limit is reached or the game has been won, we return the evaluation of the current position
        if depth == 0 or board.check_victory():
            return evaluate_position(board, max_player)

        value = float('-inf')
        # We iterate through possible moves and update the value using alpha-beta pruning
        for move in ordering_moves(board):
            if not board.column_filled(move):
                # Create a copy of the board with the potential move and update the value
                child_board = board.copy()
                child_board.add_disk(move, max_player, update_display=False)
                value = max(value, min_value(child_board, depth - 1, alpha, beta, max_player))
                alpha = max(alpha, value)
                # Perform alpha-beta pruning if necessary
                if beta <= alpha:
                    break
        return value

    # We define a function for the min player's move selection
    def min_value(board, depth, alpha, beta, max_player):
        # If the depth limit is reached or the game has been won, we return the evaluation of the current position
        if depth == 0 or board.check_victory():
            return evaluate_position(board, max_player)

        value = float('inf')
        # We iterate through possible moves and update the value using alpha-beta pruning
        for move in ordering_moves(board):
            if not board.column_filled(move):
                # Create a copy of the board with the potential move and update the value
                child_board = board.copy()
                child_board.add_disk(move, 3 - max_player, update_display=False)
                value = min(value, max_value(child_board, depth - 1, alpha, beta, max_player))
                beta = min(beta, value)
                # Perform alpha-beta pruning if necessary
                if beta <= alpha:
                    break
        return value
    
    # We define a function to order moves based on a specific strategy
    """Moves close to the corner and moves made in the middle columns are generally advantageous. 
       Therefore, we order the moves according to their distance from the corner and their distance from the middle columns."""
    def ordering_moves(board):
        moves = board.get_possible_moves()
        center_column = board.grid.shape[1] // 2

        # Weights for move ordering
        weight_center = 1 
        weight_corners = 2

        # We sort moves based on their distance from the center and corners
        moves.sort(key=lambda move: (
        weight_center * abs(move - center_column),
        weight_corners * (abs(move - 0) + abs(move - (board.grid.shape[1] - 1)))
        ))

        return moves

    # Initialize the best move and best value
    best_move = None
    best_value = float('-inf')
    alpha = float('-inf')
    beta = float('inf')

    # We iterate through possible moves and update the best move based on the max player's evaluation
    for move in board.get_possible_moves():
        # Create a copy of the board with the potential move
        child_board = board.copy()
        child_board.add_disk(move, max_player, update_display=False)
        # Check if the move leads to victory, return it immediately
        if child_board.check_victory():
            queue.put(move)
            return
        # Update the value and best move
        value = min_value(child_board, ai_level, alpha, beta, max_player)
        if value > best_value:
            best_value = value
            best_move = move
        alpha = max(alpha, best_value)
    
    
    queue.put(best_move)
