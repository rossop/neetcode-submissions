class Solution:
    def evalRPN(self, tokens: List[str]) -> int:
        def diff(nums: list[int]) -> int:
            b, a = nums.pop(), nums.pop()
            return a - b
        
        def div(nums: list[int]) -> int:
            b, a = nums.pop(), nums.pop()
            return int(a / b)
        
        def prod(nums: list[int]) -> int:
            b, a = nums.pop(), nums.pop()
            return a * b

        def add(nums: list[int]) -> int:
            b, a = nums.pop(), nums.pop()
            return a + b

        calc = {
            "+": add,
            "-": diff,
            "*": prod,
            "/": div,
        }
        
        stack: list[int] =[]

        for t in tokens:
            if t in calc:
                stack.append(calc[t](stack))
            else:
                stack.append(int(t))
        return stack[-1]