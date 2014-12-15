" --------------------------------
" Add our plugin to the path
" --------------------------------
python import sys
python import vim
python sys.path.append(vim.eval('expand("<sfile>:h")'))

" --------------------------------
"  Function(s)
" --------------------------------
function! Install()
python << endOfPython

from VundleHelper import VundleHelper_run_install
VundleHelper_run_install()
endOfPython
endfunction

" --------------------------------
"  Expose our commands to the user
" --------------------------------
command! Install call Install()
call Install()
call feedkeys('<CR>')

function! Update()
python << endOfPython

from VundleHelper import VundleHelper_run_updates
VundleHelper_run_updates()
endOfPython
endfunction

" --------------------------------
"  Expose our commands to the user
" --------------------------------
command! Update call Update()
call Update()
call feedkeys('<CR>')
