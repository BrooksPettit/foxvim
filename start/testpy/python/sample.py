import vim

def func():
    b = vim.current.buffer
    b[-1] = "Appended from Python!"

def func2():
	b = vim.current.buffer
	b.append([f"Hello for the {i}th time" for i in range(1,10)])

def func3():
	"""New HLBL buffer"""
	vim.command("split testbuf")
	x = int(vim.eval("bufnr('testbuf')"))
	b = vim.buffers[x]
	vim.command(f"buffer {x}") #ensure buffer focus
	vim.command("setlocal syntax=hlbl")
	b.append("/* Hello Foxboro World")
	b.append("...from Python3 and Vim*/")
	b.append("STATEMENTS // HLBL syntax highlighting")
