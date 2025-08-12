def passes_parity(nums, target_even=None):
    if target_even is None: return True
    even = sum(1 for n in nums if n % 2 == 0)
    return even == target_even

def passes_sum(nums, min_sum=None, max_sum=None):
    s = sum(nums)
    if min_sum is not None and s < min_sum: return False
    if max_sum is not None and s > max_sum: return False
    return True

def passes_repeat(nums, reference=None, min_repeat=None, max_repeat=None):
    if not reference or (min_repeat is None and max_repeat is None): return True
    rep = len(set(nums) & set(reference))
    if min_repeat is not None and rep < min_repeat: return False
    if max_repeat is not None and rep > max_repeat: return False
    return True
