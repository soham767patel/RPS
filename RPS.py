import random

def player(prev_play, opponent_history=[], player_history=[], model_opponent={}, model_player={}, x=14, min_occurrence=3, decay_factor=0.995, confidence_threshold=0.60):
    valid_moves = {"R", "P", "S"}

    # Append opponent's move to history
    if prev_play in valid_moves:
        opponent_history.append(prev_play)

    # --- Update opponent-based model with decay ---
    for length in range(1, x + 1):
        if len(opponent_history) > length:
            pattern = ''.join(opponent_history[-length-1:-1])
            next_move = opponent_history[-1]
            
            if pattern not in model_opponent:
                model_opponent[pattern] = {"R": 0, "P": 0, "S": 0}
            
            # Apply decay to the occurrence of patterns (older patterns are decayed more)
            decay_weight = decay_factor ** length
            model_opponent[pattern][next_move] += 1 * decay_weight

    # --- Update player-based model with decay ---
    for length in range(1, x + 1):
        if len(player_history) > length and len(opponent_history) > 0:
            pattern = ''.join(player_history[-length-1:-1])
            next_move = opponent_history[-1]
            
            if pattern not in model_player:
                model_player[pattern] = {"R": 0, "P": 0, "S": 0}
            
            # Apply decay to the occurrence of patterns (older patterns are decayed more)
            decay_weight = decay_factor ** length
            model_player[pattern][next_move] += 1 * decay_weight

    # --- Prediction phase ---
    predicted = None
    highest_prob = 0.0
    best_pattern_length = 0  # To track the longest pattern for tie-breaking

    # Check opponent model for the most probable prediction
    for length in range(1, x + 1):
        if len(opponent_history) >= length:
            pattern = ''.join(opponent_history[-length:])
            if pattern in model_opponent:
                counts = model_opponent[pattern]
                total = sum(counts.values())
                if total >= min_occurrence:
                    move = max(counts, key=counts.get)
                    prob = counts[move] / total
                    if prob > highest_prob or (prob == highest_prob and length > best_pattern_length):
                        predicted = move
                        highest_prob = prob
                        best_pattern_length = length

    # Check player model for the most probable prediction
    for length in range(1, x + 1):
        if len(player_history) >= length:
            pattern = ''.join(player_history[-length:])
            if pattern in model_player:
                counts = model_player[pattern]
                total = sum(counts.values())
                if total >= min_occurrence:
                    move = max(counts, key=counts.get)
                    prob = counts[move] / total
                    if prob > highest_prob or (prob == highest_prob and length > best_pattern_length):
                        predicted = move
                        highest_prob = prob
                        best_pattern_length = length

    # --- Confidence check ---
    # If the highest probability is above the confidence threshold, use that move
    if highest_prob >= confidence_threshold:
        pass  # Use predicted move
    else:
        # If no prediction has high enough confidence, pick random
        predicted = "R"

    # Counter the predicted move (the counter move to beat the prediction)
    counter_moves = {"R": "P", "P": "S", "S": "R"}
    move = counter_moves[predicted]

    # Append the player's move to history
    player_history.append(move)

    return move
