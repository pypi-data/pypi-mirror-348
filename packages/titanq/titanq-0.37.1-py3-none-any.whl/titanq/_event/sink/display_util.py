# Copyright (c) 2025, InfinityQ Technology, Inc.

def generate_word_animation(word: str):
    """Generates a cool TITANQ ASCII animation, returned in a list by frames"""
    word_len = len(word)
    frame = "." * word_len
    frames = [frame]

    for (target_position, letter) in enumerate(word):
        current_index = word_len - 1
        frame = frame[:-1] + letter
        frames.append(frame)

        while current_index != target_position-1:
            frame = (frame[:current_index] + letter).ljust(word_len, ".")
            frames.append(frame)
            current_index -= 1

    frames.append("TITANQ")
    frames.append("TITAN•")
    frames.append("TITA•Q")
    frames.append("TIT•NQ")
    frames.append("TI•ANQ")
    frames.append("T•TANQ")
    frames.append("•ITANQ")
    frames.append("••••••")
    frames.append("TITANQ")
    frames.append("••••••")
    frames.append("TITANQ")
    return frames