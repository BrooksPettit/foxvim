"test python vim plugin
if !has('python3')
	echo "Error: Require vim compiled with +python3"
	finish
endif

let s:pluginRootDir = fnamemodify(resolve(expand('<sfile>:p')), ':h')

py3 << EOF
import sys
from os.path import normpath, join
import vim
pluginRootDir = vim.eval('s:pluginRootDir')
pythonRootDir = normpath(join(pluginRootDir, '..', 'python'))
sys.path.append(pythonRootDir)
import sample

EOF


function! AppendStuff()
	py3 import sample
	py3 sample.func()
endfunction

function! AppendMore()
	py3 import sample
	py3 sample.func2()
endfunction

function! HlblBuffer()
	py3 import sample
	py3 sample.func3()
endfunction

command! -nargs=0 AppendStuff call AppendStuff()
command! -nargs=0 AppendMore call AppendMore()
command! -nargs=0 HlblBuffer call HlblBuffer()
