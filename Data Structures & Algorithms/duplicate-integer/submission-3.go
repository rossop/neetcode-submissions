func hasDuplicate(nums []int) bool {
    set := make(map[int]struct{})
    
    for _, item := range nums {
        set[item] = struct{}{}
    }

    return len(set) != len(nums)
}
