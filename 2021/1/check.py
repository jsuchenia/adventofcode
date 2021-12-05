#!/usr/local/bin/python3

def ex2(data):
	datalen = len(data)
	print("  > datalen = ", datalen)
	sums=[data[i] + data[i+1] + data[i+2] for i in range(datalen-2)]

	prev = sums[0]
	counter = 0

	for entry in sums[1:]:
		if entry > prev:
			counter+=1
		prev = entry

	print("[Excercise 2] ", counter)

def ex1(data):
	prev = data[0]
	counter = 0
	for entry in data[1:]:
		if entry > prev:
			counter+=1
		prev = entry

	print("[Excercise 1] ", counter)


if __name__ == "__main__":
	strdata = open('data', 'r').readlines()
	data = [int(x) for x in strdata]

	ex1(data)
	ex2(data)