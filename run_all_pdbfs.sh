a=0
# -lt is less than operator
 
#Iterate the loop until a less than 10
while [ $a -lt 930 ]
do
    # Print the values
    python all_pdbfs.py -i $a 
    # increment the value
    a=`expr $a + 1`
done
