from core.bloom_filter import BloomFilter


bf = BloomFilter(size=1000, hash_count=4)

bf.add("apple")
bf.add("banana")
bf.add("grape")

print("apple:", bf.contains("apple"))    # True
print("banana:", bf.contains("banana"))  # True
print("grape:", bf.contains("grape"))    # True
print("orange:", bf.contains("orange"))  # False (probably)
