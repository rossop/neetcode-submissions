func threeSum(nums []int) [][]int {
	res := map[[3]int]struct{}{}
	sort.Ints(nums)

	fmt.Println(nums)
	// for each i < n -2
	for i := 0; i < len(nums) - 2; i++ {
		for j := i + 1; j < len(nums) -1; j++ {
			for k := j + 1; k < len(nums); k++ {
				if nums[i] + nums[j] + nums[k] == 0 {
					res[[3]int{nums[i], nums[j], nums[k]}] = struct{}{}
				}
			}
		}
	} 

	var result [][]int
	for triplet := range res {
		result = append(result, []int{triplet[0], triplet[1], triplet[2]})
	}

	return result
}