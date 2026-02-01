import re

def get_season_episode(filename):
    if not filename: return (9999, 9999, "")
    
    # Priority 1: S01E01
    match = re.search(r'(?i)s(\d+)\s*e(\d+)', filename)
    if match: return (int(match.group(1)), int(match.group(2)), filename)
    
    # Priority 2: 1x01
    match_x = re.search(r'(\d+)x(\d+)', filename)
    if match_x: return (int(match_x.group(1)), int(match_x.group(2)), filename)
    
    # Priority 3: "Episode 05" (Assume Season 1)
    num_match = re.search(r'(?i)episode\s*(\d+)', filename)
    if num_match: return (1, int(num_match.group(1)), filename)
    
    # Priority 4: Just a number
    simple = re.search(r'(\d+)', filename)
    if simple: return (1, int(simple.group(1)), filename)
    
    return (9999, 9999, filename)
