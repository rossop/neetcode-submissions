func maxArea(heights []int) int {
    l, r := 0, len(heights) -1
    maxArea := 0 

    for l < r {
        height := min(heights[l], heights[r])
        length := r - l 
        maxArea = max(maxArea, height * length)

        if heights[l] < heights[r]{
            l++
        } else {
            r--
        }
    }
    return maxArea
}
