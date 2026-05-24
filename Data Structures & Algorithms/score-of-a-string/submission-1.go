func scoreOfString(s string) int {
    lenS := len(s)
    ans := 0
    for i := 0; i < lenS - 1; i++ {
        score := int(s[i]) - int(s[i+1])
        if score > 0 {
            ans += score
        } else {
            ans -= score
        }
    }
    return ans
}
