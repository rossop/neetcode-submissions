class Solution:
    def calculateTime(self, keyboard: str, word: str) -> int:
        keymap: dict[str, int] = {}
        for k, v in enumerate(keyboard):
            keymap[v] = k
        
        ans: int = 0
        start: int = 0
        for i in range(len(word)):
            end: int = keymap[word[i]]
            ans += abs(start - end)
            start: int = end
        
        return ans