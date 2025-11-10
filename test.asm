add $t0, $t1, $t2
addi $t0, $zero, 42
sub $t1, $t2, $t3
and $t2, $t3, $t4
or $t3, $t4, $t5
xor $t4, $t5, $t6
slt $t5, $t6, $t7
slti $t6, $t7, 100
sll $t7, $t0, 3
srl $t8, $t1, 1
lui $t9, 1000
lw $s0, 16($sp)
sw $s1, 20($sp)
beq $t0, $t1, 5
bne $t2, $t3, 8
j 500
jal 600
jr $ra
nop
