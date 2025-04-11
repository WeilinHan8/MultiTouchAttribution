from collections import defaultdict
def get_unique_channels(list_of_paths):
    """Create a set of unique channels from list of paths.
    
    Args:
        list_of_paths: List of customer paths
    
    Returns:
        Set of unique channels
    """
    return {channel for path in list_of_paths for channel in path}

def transition_states_from_path(unique_channels,list_of_paths):
    """Get all possible transitions between marketing channels and number of occurance from the list of paths.
    
    Args:
        unique_channels: Set of marketing channels.
        list_of_paths: List of customer paths
    
    Returns:
        Dictionary of transition counts (e.g., {'Email>Social': 5})
    """
    all_transition={x + '>' + y: 0 for x in unique_channels for y in unique_channels}

    for path in list_of_paths:
        for i in range(len(path) - 1):
            current, next_ = path[i], path[i + 1]
            if current not in {'Conversion', 'Null'}:
                all_transition[f"{current}>{next_}"] += 1

    return all_transition


def transition_prob_optimized(unique_channels, trans_states, list_of_paths):
    """Calculate transition probabilities between marketing channels.
    
    Args:
        trans_states: Dictionary of transition counts (e.g., {'Email>Social': 5})
        list_of_paths: List of customer paths
        unique_channels: Set of marketing channels.
    
    Returns:
        Dictionary of transition probabilities (e.g., {'Email>Social': 0.5})
    """    
    transition_groups = defaultdict(list)
    for transition, count in trans_states.items():
        from_state, _ = transition.split('>', 1)
        transition_groups[from_state].append((transition, count))
    
    trans_prob = {}
    for state in unique_channels:
        if state in ['Conversion', 'Null']:
            continue
            
        if state not in transition_groups:
            continue
            
        total = sum(count for _, count in transition_groups[state])
        
        for transition, count in transition_groups[state]:
            trans_prob[transition] = count / total
    
    return trans_prob