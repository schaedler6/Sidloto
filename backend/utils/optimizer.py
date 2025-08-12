import random

def parity_count(nums):
    even = sum(1 for n in nums if n % 2 == 0)
    return even, 15 - even

def sum_ok(nums, min_sum=None, max_sum=None):
    s = sum(nums)
    if min_sum is not None and s < min_sum: return False
    if max_sum is not None and s > max_sum: return False
    return True

def repeat_ok(nums, last_result, min_rep=None, max_rep=None):
    if not last_result: return True
    rep = len(set(nums) & set(last_result))
    if min_rep is not None and rep < min_rep: return False
    if max_rep is not None and rep > max_rep: return False
    return True

def parity_ok(nums, even_target=None):
    if even_target is None: return True
    even, _ = parity_count(nums)
    return even == even_target

def generate_one(
    rng,
    last_result,
    hot=set(),
    cold=set(),
    repeat_target=9,
    even_target=None,
    min_sum=None, max_sum=None,
    avoid=set(), must=set()
):
    last_sorted = sorted(set(last_result))
    base_rep = min(max(repeat_target, 0), min(15, len(last_sorted)))
    picked = set(rng.sample(last_sorted, base_rep)) if base_rep > 0 else set()
    picked |= (must - avoid)

    all_nums = [n for n in range(1, 26) if n not in picked and n not in avoid]
    def score(n):
        if n in cold: return 0
        if n in hot:  return 2
        return 1
    all_nums.sort(key=score, reverse=True)

    for n in all_nums:
        if len(picked) >= 15: break
        picked.add(n)

    nums = sorted(list(picked))[:15]
    ATTEMPTS = 500
    pool = [n for n in range(1, 26) if n not in nums and n not in avoid]
    for _ in range(ATTEMPTS):
        if parity_ok(nums, even_target) and sum_ok(nums, min_sum, max_sum) and repeat_ok(nums, last_result, repeat_target, repeat_target):
            return nums
        if not pool: break
        i = rng.randrange(0, 15)
        add = rng.choice(pool)
        new = sorted(list((set(nums) - {nums[i]}) | {add}))
        score_old = (
            (1 if parity_ok(nums, even_target) else 0) +
            (1 if sum_ok(nums, min_sum, max_sum) else 0) +
            (1 if repeat_ok(nums, last_result, repeat_target, repeat_target) else 0)
        )
        score_new = (
            (1 if parity_ok(new, even_target) else 0) +
            (1 if sum_ok(new, min_sum, max_sum) else 0) +
            (1 if repeat_ok(new, last_result, repeat_target, repeat_target) else 0)
        )
        if score_new >= score_old:
            pool.append(nums[i]); pool.remove(add); nums = new
    return nums

def generate_batch(
    quantity,
    last_result,
    hot=set(), cold=set(),
    repeat_target=9,
    even_target=None,
    min_sum=None, max_sum=None,
    avoid=set(), must=set(),
    seed=None
):
    rng = random.Random(seed)
    out = []
    seen = set()
    CAP = 4000; tries = 0
    while len(out) < quantity and tries < CAP:
        g = tuple(generate_one(
            rng, last_result, hot, cold, repeat_target,
            even_target, min_sum, max_sum, avoid, must
        ))
        tries += 1
        if len(g) != 15: continue
        if g in seen: continue
        seen.add(g); out.append(list(g))
    return out
