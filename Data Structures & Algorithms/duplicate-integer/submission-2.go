func hasDuplicate(nums []int) bool {
    // Create Set
    set := make(map[int]struct{}, len(nums))

    for _, item := range nums {
        set[item] = struct{}{}
    }
    // Compare set to slice
    return len(nums) != len(set)
    
}
