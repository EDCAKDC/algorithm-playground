from collections import Counter


class Solution:
    def minWindow(self, s: str, t: str) -> str:
        if len(t) > len(s):
            return ""
        # need: required character counts from t
        need = Counter(t)
        # window: current character counts inside the sliding window
        window = {}
        # valid: how many distinct characters have met their required counts
        valid = 0
        need_types = len(need)

        left = 0
        # Record the best window
        best_start = 0
        best_len = float("inf")

        for right, ch in enumerate(s):

            window[ch] = window.get(ch, 0) + 1

            if ch in need and window[ch] == need[ch]:
                valid += 1

            while valid == need_types:
                cur_len = right - left + 1
                if cur_len < best_len:
                    best_len = cur_len
                    best_start = left

                left_char = s[left]
                window[left_char] -= 1
                if left_char in need and window[left_char] < need[left_char]:
                    valid -= 1
                left += 1

        if best_len == float("inf"):
            return ""
        return s[best_start: best_start + best_len]
