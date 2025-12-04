from collections import Counter


def sliding_window(s, t):
    # need: required character counts from t
    need = Counter(t)
    window = {}

    left = 0
    valid = 0

    for right, ch in enumerate(s):
        # Expand the window by including s[right]
        window[ch] = window.get(ch, 0) + 1

        if ch in need and window[ch] == need[ch]:
            valid += 1

        while valid == len(need):

            # Prepare to shrink: remove s[left] from the window
            left_char = s[left]
            window[left_char] -= 1

            if left_char in need and window[left_char] < need[left_char]:
                valid -= 1

            left += 1
