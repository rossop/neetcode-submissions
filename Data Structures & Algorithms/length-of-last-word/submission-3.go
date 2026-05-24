func lengthOfLastWord(s string) int {
    ans := 0
    for idx := len(s) - 1; idx > -1; idx-- {
        if s[idx] != ' ' {
            ans++
        } else {
            if ans > 0 { return ans }
        }
    }
    return ans
}