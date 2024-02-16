" Vim Syntax File
" Language: Foxboro CALCA Instruction List
" Maintainer: Brooks Pettit <brooks.pettit@live.com>
" Last Change: 2024 Feb 07
" Credits: Cassandra Project
"

if exists("b:current_syntax")
    finish
endif

"Any lowercase is converted before download
syn case ignore

"Inline Comment
syn region calcaComment start="\;" end="$"

"Arithmetic Instructions
syn keyword calcaOpcode BAS ACOS ADD ALN ALOG ASIN ATAN AVE CHS COS
syn keyword calcaOpcode DEC DIV EXP IDIV IMOD INC LN LOG MAX MAXNO MIN
syn keyword calcaOpcode MEDN MUL RAND RANG RND SEED SIN SQR SQRT SUB TAN TRC

"Boolean Instructions
syn keyword calcaOpcode AND ANDX NAN NAND NOR NORX NOT NOTX
syn keyword calcaOpcode NXO NXOR NXOX OR ORX XOR XORX

"I/O Reference Instructions
syn keyword calcaOpcode CBD CE COO IN INB INH INL INR INS OUT RBD RCL RCN
syn keyword calcaOpcode RE REL RON ROO RQE RQL SAC SBD SE SEC SOO STH STL SWP

"Cascade and Propagation Instructions
syn keyword calcaOpcode PRI PRO PRP 

"Memory and Stack Reference Instructions
syn keyword calcaOpcode CLA CLM CST DUP LAC LACI POP STM STMI TSTB

"Program Control Instructions
syn keyword calcaOpcode BIF BII BIN BIP BIT BIZ END EXIT GTI GTO NOP

"Clear/Set Instructions
syn keyword calcaOpcode CLL CLR CLRB SET SETB SSF SSI SSN SSP SST SSZ

"Timing Instructions
syn keyword calcaOpcode CHI CHN DOFF DON OSP TIM

"Logic Instructions
syn keyword calcaOpcode FF MRS

"Error Control Instructions
syn keyword calcaOpcode CLE RER SIEC

"Propagation Upstream Instruction
syn keyword calcaOpcode PMU

"I/O Registers
syn match calcaRegisters "\vBI(0[1-9]|1[0-6])"
syn match calcaRegisters "\vBO0[1-8]"
syn match calcaRegisters "\vRI0[1-8]"
syn match calcaRegisters "\vRO0[1-4]"
syn match calcaRegisters "\vII0[1-2]"
syn match calcaRegisters "\vIO0[1-6]"
syn match calcaRegisters "\vLI0[1-2]"
syn match calcaRegisters "\vLO0[1-2]"
syn match calcaRegisters "\vM(0[1-9]|1[0-9]|2[0-4])"


hi def link calcaOpcode Operator
hi def link calcaRegisters Statement
hi def link calcaComment Comment
