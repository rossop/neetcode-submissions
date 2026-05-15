class Solution:
    def isValid(self, s: str) -> bool:
        pairs: dict[str, str] = {
            '(': ')',
            '[': ']',
            '{': '}',
        }
        stack: list[str|None] = []
        for c in s:
            if c in pairs.keys():
                stack.append(c)
            else:
                if len(stack) > 0:
                    p: str = stack.pop()
                    if c != pairs[p]:
                        return False
                else:
                    return False
        if len(stack) == 0:
            return True
        return False
        