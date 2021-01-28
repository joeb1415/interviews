# https://leetcode.com/problems/continuous-subarray-sum
from typing import List


class Solution:
    def checkSubarraySum(self, nums: List[int], k: int) -> bool:
        """
        Keep track of the mod(k) running sum all numbers from the start through each index.
        If we ever see a repeat modulo, then the subset from the index of when we first saw that modulo
        through the second time we saw it, must be 0.
        Include 0 as a first seed modulo in case the full set sums to mod 0, we can use the same test.
        If we ever have [0,0] in the list of nums, then we have a multiple of 0*k.
        """
        if len(nums) < 2:
            return False
        for start in range(len(nums) - 1):
            if nums[start:start+2] == [0, 0]:
                return True
        if k == 0:
            return False
        sums = {0: -1}
        if nums[0] not in sums:
            sums[nums[0]] = 0
        sum_so_far = nums[0] % k
        for end in range(1, len(nums)):
            sum_so_far += nums[end]
            sum_so_far %= k
            if sum_so_far in sums and end > sums[sum_so_far] + 1:
                return True
            else:
                sums[sum_so_far] = end
        return False


if __name__ == "__main__":
    s = Solution()
    s.checkSubarraySum([1, 2, 3], 5)
