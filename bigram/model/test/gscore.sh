#!/bin/bash

./score msr_training_words msr_testsort.txt msr_trs.txt | tee rs.txt
#./score msr_training_words gold.txt submit.txt | tee rs.txt
