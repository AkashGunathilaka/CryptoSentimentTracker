
def is_duplicate(new_title, seen_titles):
    for title in seen_titles:
        if title.lower() in new_title.lower() or new_title.lower() in title.lower():
            return True
    return False