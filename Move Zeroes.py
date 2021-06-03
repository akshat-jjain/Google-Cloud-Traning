class Solution:
    def moveZeroes(self, nums: List[int]) -> None:
        a=nums.count(0)
        nums[:]=[x for x in nums if x!=0 ]+[0 for x in range(a)]
