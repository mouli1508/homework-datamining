import itertools
from collections import defaultdict

def read_transactions(filename):
    with open(filename, 'r') as file:
        transactions = [line.strip().split() for line in file]
    return transactions

def get_support(itemset, transactions):
    count = sum(1 for transaction in transactions if set(itemset).issubset(transaction))
    return count

def generate_candidates(itemsets, length):
    return list(itertools.combinations(set(itertools.chain(*itemsets)), length))

def apriori(filename, min_support_percentage):
    transactions = read_transactions(filename)
    num_transactions = len(transactions)
    min_support = num_transactions * (min_support_percentage / 100)

    #Generate 1-itemsets and calculate support
    one_itemsets = [{item} for transaction in transactions for item in transaction]
    one_itemsets = [list(itemset) for itemset in set(frozenset(item) for item in one_itemsets)]
    
    freq_itemsets = defaultdict(int)
    for itemset in one_itemsets:
        support = get_support(itemset, transactions)
        if support >= min_support:
            freq_itemsets[frozenset(itemset)] = support

    #Iteratively generate k-itemsets until no more frequent itemsets can be found
    k = 2
    prev_freq_itemsets = list(freq_itemsets.keys())
    while prev_freq_itemsets:
        candidates = generate_candidates(prev_freq_itemsets, k)
        candidate_freqs = defaultdict(int)
        
        for candidate in candidates:
            support = get_support(candidate, transactions)
            if support >= min_support:
                candidate_freqs[frozenset(candidate)] = support
        
        if candidate_freqs:
            freq_itemsets.update(candidate_freqs)
            prev_freq_itemsets = list(candidate_freqs.keys())
        else:
            break
        
        k += 1

    # Output the frequent itemsets and their support
    for itemset, support in freq_itemsets.items():
        print(f"Itemset: {set(itemset)}, Support: {support} ({(support / num_transactions) * 100:.2f}%)")

if __name__ == '__main__':
    filename = input("Enter the filename: ")
    min_support_percentage = float(input("Enter minimum support percentage: "))
    apriori(filename, min_support_percentage)
