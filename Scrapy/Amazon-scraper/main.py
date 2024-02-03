keyword = "goal"  # Replace with your keyword

# Split the keyword into words
words = keyword.split()

# Check if there are multiple words
if len(words) > 1:
    # Join the words with a '+', without any space
    keyword = '+'.join(words)

print(keyword)