" Language: Foxboro CALC Instruction List
" Maintainer: Brooks Pettit <brooks.pettit@live.com>
" Last Change: 2024 Feb 08
" Credits: Cassandra Project
"

if exists("b:current_syntax")
    finish
endif

"Any lowercase is converted before download
syn case ignore

"Inline Comment
syn region calcComment start="\;" end="$"

"Arithmetic Instructions
syn keyword calcOpcode BAS ACOS ADD ALN ALOG ASIN ATAN AVE CHS COS
syn keyword calcOpcode DEC DIV EXP IDIV IMOD INC LN LOG MAX MAXNO MIN
syn keyword calcOpcode MEDN MUL RAND RANG RND SEED SIN SQR SQRT SUB TAN TRC

"Boolean Instructions
syn keyword calcOpcode AND ANDX NAND NANX NOR NORX
syn keyword calcOpcode NOT NOTX NXOR NXOX OR ORX XOR XORX

"I/O Reference Instructions
syn keyword calcOpcode CBD CE COO IN INB INH INL INR INS OUT RBD RCL RCN
syn keyword calcOpcode RE REL RON ROO RQE RQL SAC SBD SE SEC SOO STH STL SWP

"Cascade and Propagation Instructions
syn keyword calcOpcode PRI PRO PRP 

"Memory and Stack Reference Instructions
syn keyword calcOpcode CLA CLM CST DEC DUP INC LAC LACI POP RCL STM STMI SWP TSTB

"Program Control Instructions
syn keyword calcOpcode BIF BII BIN BIP BIT BIZ END EXIT GTI GTO NOP

"Clear/Set Instructions
syn keyword calcOpcode CLR CLRB SET SETB SSF SSI SSN SSP SST SSZ

"Timing Instructions
syn keyword calcOpcode DOFF DON OSP TIM

"Logic Instructions
syn keyword calcOpcode FF MRS

"Error Control Instructions
syn keyword calcOpcode CLE RER SIEC

"I/O Registers
syn match calcRegisters "\vBI(0[1-9]|1[0-6])"
syn match calcRegisters "\vBO0[1-8]"
syn match calcRegisters "\vRI0[1-8]"
syn match calcRegisters "\vRO0[1-4]"
syn match calcRegisters "\vII0[1-2]"
syn match calcRegisters "\vIO0[1-6]"
syn match calcRegisters "\vLI0[1-2]"
syn match calcRegisters "\vLO0[1-2]"
syn match calcRegisters "\vM(0[1-9]|1[0-9]|2[0-4])"


hi def link calcOpcode Operator
hi def link calcRegisters Statement
hi def link calcComment Comment
