func findMaxConsecutiveOnes(nums []int) int {
	ans, maxLength := 0, 0

    for _, v := range nums {
        if v == 1 {
            maxLength++
        } else if v == 0 {
            ans = max(ans, maxLength)
            maxLength = 0
        }
    }
    return max(ans, maxLength)
}
