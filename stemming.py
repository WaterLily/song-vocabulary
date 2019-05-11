# pattern for decoding escaped unicode blocks
test = r"\u00e2"
decoded = bytes(test, "utf-8").decode("unicode-escape")