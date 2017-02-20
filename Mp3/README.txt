To run this program, use terminal to navigate to the folder where all required files are stored.
python ./goverdh2.py
To run on the sample data. Enter 'b'  (Make sure sample.txt is in same folder and has 25 nodes)
To run on the default data. Enter 'a' (*Long Running Time*)
Output will be saved to multiple files in the same directory. 

Algorithm/Flow of Program:

1) Loads data from given source.
2) Stores data in an Igraph where the nodes have different attributes.
3) We then run the exact/approximate betweeness algorigthm for each graph for 1-5 number of communities and store the edged removed and modularity.
4)This data is then written to file. Times are printed out.

 - Modularity is calculated using the expression given to us in class. 
 - Exact Betweeness is calculated using the algorithm given to us.
 