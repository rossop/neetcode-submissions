func getConcatenation(nums []int) []int {
    n := len(nums)
	ans := make([]int, 2*n)
	// for i:=0; i < n; i++ {
	for i, val := range nums {
		ans[i] = val
		ans[n + i] = val
	}
	return ans
}
