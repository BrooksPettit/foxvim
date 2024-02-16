if exists('g:loaded_iccvim')
    finish
endif
let g:loaded_iccvim = 1

"command! Iccvim call popup_menu(['The quick fox...', '...jumped over...', '...the lazy dogs'],
"    \ #{title: "Well? Pick one!", callback: 'MenuCB', line: 25, col: 40, 
"    \ border: [], close: 'click', padding: [1,1,0,1]})

" attempt 01
"


func IccInputEntered(text) 
    let text = a:text->toupper()
    call ch_sendraw(g:iccJob, a:text .. "\n")
endfunc

func GotStdErr(channel, msg)
    call append(line("$") - 1, "- " .. a:msg)
endfunc

func IccExit(job, status)
    quit!
endfunc 

func NewICCVim()
    let iccdrvrtsk = 'D:\opt\fox\ciocfg\api\iccdrvr.tsk.exe'
    let g:iccJob = job_start(iccdrvrtsk, #{
                \ out_io: "buffer",
                \ out_name: "std_out",
                \ err_io: "buffer",
                \ err_name: "std_out",
                \ })
    let res = job_status(g:iccJob)
    call popup_notification("ICCDrvrTsk job status: " .. res, #{})
    vnew std_in
    setlocal buftype=prompt
    let inbuf = bufnr('std_in')
    call prompt_setcallback(inbuf, function("IccInputEntered"))
    eval prompt_setprompt(inbuf, "ICC Command >>> ")
    startinsert
    sbuffer std_out
endfunc

command! ICCVimInteractive call NewICCVim()

command! -nargs=1 -complete=command IccCall call IccInputEntered(<q-args>)
