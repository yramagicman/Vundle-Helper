" --------------------------------
" Add our plugin to the path
" --------------------------------
python import sys
python import vim
python sys.path.append(vim.eval('expand("<sfile>:h")'))

" --------------------------------
"  Function(s)
" --------------------------------
function! VundleHelper#Install()
python << endOfPython

from VundleHelper import VundleHelper_run_install
VundleHelper_run_install()
endOfPython
endfunction

" --------------------------------
"  Expose our commands to the user
" --------------------------------
command! VHInstall call VundleHelper#Install()
call VundleHelper#Install()
call feedkeys('<CR>')

function! VundleHelper#Update()
python << endOfPython

from VundleHelper import VundleHelper_run_updates
VundleHelper_run_updates()
endOfPython
endfunction

" --------------------------------
"  Expose our commands to the user
" --------------------------------
command! VHUpdate call VundleHelper#Update()
call VundleHelper#Update()
call feedkeys('<CR>')

function! VundleHelper#SelfUpdate()
python << endOfPython
import Self_update
from VundleHelper import VundleHelper_self_update
VundleHelper_self_update()
endOfPython
endfunction
autocmd! VimLeave call VundleHelper#SelfUpdate()
