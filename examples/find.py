import thoth as th

th.call.here()

file = 'sample.txt'
key = 'key'
key_regex = r'key\s*\d*'
number_of_matches = -2
additional_lines = -2
split_additional_lines = False
regex = False

if regex:
    keyword = key_regex
else:
    keyword = key

matches = th.text.find(keyword, file, number_of_matches, additional_lines, split_additional_lines, regex)
print(matches)
for match in matches:
    print(match)