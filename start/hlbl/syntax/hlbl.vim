" Vim syntax file
" Language:	Foxboro HLBL Sequence Language
" Maintainer: Brooks Pettit <brooks.pettit@live.com>
" Last Change:	2024 Feb 09
" Credits: Cassandra Project

" Quit when a (custom) syntax file was already loaded
if exists("b:current_syntax")
  finish
endif

"Comments
syn region hlblComment start="/\*" end="\*/"
syn region hlblComment start="{" end="}"
syn region hlblRemark start="//" end="$"

"HLBL keywords
syn keyword hlblStatement EXIT GOTO
syn keyword hlblConditional IF MONITOR_CASE
syn keyword hlblRepeat EXITLOOP FOR REPEAT RETRY WAIT WHILE

syn keyword hlblControl ABORT ABS ACTCASES ACTIVATE ACTIVE AFTER ALREADY AND BAD BIT_PATTERN BLOCK_EXCEPTION 
syn keyword hlblControl BLOCK_NAME BLOCK_STMNO CALL CASES COMPOUND_NAME CONSTANTS DEPENDENT_SEQUENCE DISABLE
syn keyword hlblControl DIV DO DOWNTO E ELSE ELSEIF ENDEXCEPTION ENDFOR ENDIF ENDMONITOR ENDSEQUENCE
syn keyword hlblControl ENDSUBROUTINE ENDWHILE EXCEPTION EXCEPTION_SEQUENCE INACTIVE INDEPENDENT_SEQUENCE MOD
syn keyword hlblControl MONITOR MULT_ARRAY NOT ON OP_ERR OR ORD ROUND SBXNO SECURED SENDCONF SENDMSG SENDMSG
syn keyword hlblControl SET_ARRAY SET_SBXS SQRT START_TIMER STATEMENTS STEPNO STMNO STOP_TIMER STRING SUBR_LEVEL
syn keyword hlblControl SUBRNO SUBROUTINE SUM_ARRAY THEN TIMER TO TRUNC UNTIL USER_LABELS VARIABLES WHEN 

"Labels
syn match hlblLabel "\v(<<\w>>)"

"Preprocessor directives
"syn match hlblInclude "\v\#w" 

hi def link hlblComment Comment
hi def link hlblRemark Comment
hi def link hlblStatement Statement
hi def link hlblControl Statement
hi def link hlblConditional Conditional
hi def link hlblRepeat Repeat
hi def link hlblLabel Label
