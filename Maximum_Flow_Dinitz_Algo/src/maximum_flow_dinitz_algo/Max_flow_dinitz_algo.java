/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package maximum_flow_dinitz_algo;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import static java.lang.Integer.min;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Iterator;
import java.util.LinkedList;
import java.util.ListIterator;
import java.util.Random;
import java.util.Scanner;
import java.util.logging.Level;
import java.util.logging.Logger;

/**
 * Reference for the implementation on the Dinitz's algorithm:
 * Dinitz, Y., 1974. Dinitz'algorithm: The Original Version And Even's Version. [ebook] Israel: Ben-Gurion University of the Negev. Available at: <https://www.cs.bgu.ac.il/~dinitz/Papers/Dinitz_alg.pdf> [Accessed 30 March 2020].
 * Rougharden, T., 2016. CS261: A Second Course In Algorithms Lecture #2: Augmenting Path Algorithms For Maximum Flow∗. [ebook] Available at: <http://timroughgarden.org/w16/l/l2.pdf> [Accessed 30 March 2020].
 * GeeksforGeeks. 2020. Dinic's Algorithm For Maximum Flow - Geeksforgeeks. [online] Available at: <https://www.geeksforgeeks.org/dinics-algorithm-maximum-flow/> [Accessed 30 March 2020].
 * @author Issam
 */
public class Max_flow_dinitz_algo {
    static class Edge {
        int destination, currentFlow, maxCapacity, source;

        public Edge(int destination, int currentFlow, int maxCapacity, int source) {
            this.destination=destination;
            this.currentFlow=currentFlow;
            this.maxCapacity=maxCapacity;
            this.source=source;
        }
    }
    

    static class Graph {
        int vertexNum;
        int[] level;
        LinkedList<Edge> adjacentList[];
        LinkedList<Edge> adjacentListResidualGraph[];
         
         
         
        public Graph(int vertexNum) {
            adjacentList = new LinkedList[vertexNum];
            adjacentListResidualGraph = new LinkedList[vertexNum];
            
            this.vertexNum=vertexNum;
            level=new int[vertexNum];
            
            for (int l = 0; l < vertexNum; l++) adjacentList[l] = new LinkedList<>();
            for (int g = 0; g < vertexNum; g++) adjacentListResidualGraph[g] = new LinkedList<>();
        }
        
        public void addEdge(int source, int destination, int maxCapacity) {
            Edge front = new Edge(destination, 0, maxCapacity, adjacentListResidualGraph[destination].size());
            Edge back = new Edge(source, 0, 0, adjacentList[source].size());
            
            adjacentList[source].add(front);
            adjacentListResidualGraph[destination].add(back);
        }
        
        public boolean bfs(int source, int destination) {
            for (int k = 0; k < vertexNum; k++) level[k] = -1;
            
            LinkedList<Integer> queue = new LinkedList<>();
            
            level[source] = 0;
            queue.push(source);
            
            while(!queue.isEmpty()) {
                int u = queue.poll();
                ListIterator<Edge> i = adjacentList[u].listIterator();
                
                while(i.hasNext()) {
                    Edge edge = i.next();
                    if((level[edge.destination]<0) && (edge.currentFlow < edge.maxCapacity)) {
                        level[edge.destination] = level[u]+1;
                        queue.add(edge.destination);
                        //counter++; Used to count the number of iteration in the residual graph
                    }
                    
                }
            }
            return level[destination] > 0;
        }
        
        public int sendFlow(int source, int stream, int destination, int start[]) {
            if (source==destination) return stream;
            
            Edge edge;
            int curr_flow;
            int temp_flow;
            
            for(;start[source] < adjacentList[source].size(); start[source]++) {
                edge = adjacentList[source].get(start[source]); 
                if ((level[edge.destination] == (level[source]+1)) && (edge.currentFlow < edge.maxCapacity)) {
                    curr_flow = min(stream, edge.maxCapacity - edge.currentFlow);
                    temp_flow = sendFlow(edge.destination, curr_flow, destination, start);
                    if(temp_flow > 0) {
                        edge.currentFlow += temp_flow;
                        adjacentListResidualGraph[edge.destination].get(edge.source).currentFlow-=temp_flow;
                        return temp_flow;
                    }
                } 
            }
            return 0;
        }
        
        public int dinicMaxFlow(int source, int sink) {
            if (source==sink) return -1;
           
            int total=0;
            int[] start;
            int flow;

            while(bfs(source, sink) == true) {
               start = new int[vertexNum+1];
               while((flow = sendFlow(source, Integer.MAX_VALUE, sink, start))!=0) {
                   total += flow;
               }    
            }   
           return total;
        }
                
        private void resetFlow() {
            for (int j = 0; j < vertexNum; j++) for (Edge e : adjacentList[j]) e.currentFlow=0;
        }
        
        public void clearGraph() {
            for (int k = 0; k < vertexNum; k++) adjacentList[k].clear();
        }
        
        public void delEdge(int source, int sink, Graph graph) {
            for (int j = 0; j < graph.vertexNum; j++) {
                for(Iterator<Edge> i = adjacentList[j].iterator(); i.hasNext();) {
                    Edge edge = i.next();
                    if ( (j==source && edge.destination==sink)) i.remove();
                    if ((j==sink && edge.destination==source)) adjacentListResidualGraph[j].remove();
                }
            }
        }           
            
        public void modifyMaxFlow(int source, int destination, int maxCapacity) {
            for (int j = 0; j < vertexNum; j++) {
                for (Edge e : adjacentList[j]) {
                    if (j==source && e.destination==destination) {
                        System.out.println("Source: "+j+" | Destination: "+e.destination);
                        e.maxCapacity=maxCapacity;
                       
                    }
                }
            }
        }
       
        public void printGraph(){
            for (int j = 0; j < vertexNum; j++) {
                System.out.print("Adjacency list of vertex " + j);
                System.out.println(" | head");
                for (Edge i : adjacentList[j]) {
                    System.out.println(j + " - (" + i.currentFlow + "/"+ i.maxCapacity+ ") -> " + i.destination);
                    //System.out.print(" - " + "(" + i.currentFlow + "/"+ i.maxCapacity+") |"+i.name+"|-> " + i.destination);
                }
                System.out.println("");
            }
        }
        
    }  
    
    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        // TODO code application logic here
        Graph graphDS1 = new Graph(6);
        datasetReader("Dataset1.txt", graphDS1);
        menu(graphDS1);
    }
    
    private static void datasetReader(String path, Graph graph) {
        File file = new File(path);
        try {
            BufferedReader reader = new BufferedReader(new FileReader(file));
            String str;
            while ((str = reader.readLine()) != null) {
                Random rand = new Random();
                graph.addEdge(Integer.valueOf(str.split(",")[0]), 
                        Integer.valueOf(str.split(",")[1]), 
                        Integer.valueOf(str.split(",")[2]) /*1+rand.nextInt(100)*/);
            }
            
        } catch (FileNotFoundException ex) {
            Logger.getLogger(Max_flow_dinitz_algo.class.getName()).log(Level.SEVERE, null, ex);
        } catch (IOException ex) {
            Logger.getLogger(Max_flow_dinitz_algo.class.getName()).log(Level.SEVERE, null, ex);
        }
    } 
    
    public static void comparativeAnalysis(Graph graph) {
        String[] datasetArr = {"Dataset1.txt", 
                                "Dataset2.txt", 
                                "Dataset3.txt", 
                                "Dataset4.txt", 
                                "Dataset5.txt"};
        int[] sizeDataset = {6, 6, 10, 16, 48};
        
        long startClock, stopClock;
        
        double[] results = new double[datasetArr.length];
        
        System.out.println("|-----------------------------------------------------------|");
        for (int i = 0; i < datasetArr.length; i++) {
            graph.clearGraph();
            graph = new Graph(sizeDataset[i]);
            graph.resetFlow();
            datasetReader(datasetArr[i], graph);

            double elapsedTime, minResult, maxResult, resultAverage = 0.0;
            
            ArrayList<Double> values = new ArrayList<>();
            int f = 0;
            for (int k = 0; k < 1000; k++) {
                f = 0;
                startClock = System.nanoTime();
                f = graph.dinicMaxFlow(0, sizeDataset[i]-1);
                stopClock = System.nanoTime();
                graph.resetFlow();
                elapsedTime = (stopClock - startClock);
                
                values.add(elapsedTime);
            }
            elapsedTime = values.get((values.size()+1)/2);

            values.clear();
            System.out.println("FLOW: " + f);
            System.out.println("| " + (i+1) + " | AVERAGE:  " + elapsedTime);
            System.out.println("|-----------------------------------------------------------|");
        }
    }
    
    public static Graph loadDataset() {
        Scanner scanner = new Scanner(System.in);
        System.out.println("|-----------------------------------------------------------|");
        System.out.println("| To select Dataset 1 enter 1_________________________: '1' |");
        System.out.println("| To select Dataset 2 enter 2_________________________: '2' |");
        System.out.println("| To select Dataset 3 enter 3_________________________: '3' |");
        System.out.println("| To select Dataset 4 enter 4_________________________: '4' |");
        System.out.println("| To select Dataset 5 enter 5_________________________: '5' |");
        System.out.println("|-----------------------------------------------------------|");
        System.out.print("| Please enter your dataset choice: ");

        switch (scanner.nextInt()) {
            case 1:
                System.out.println("|-----------------------------------------------------------|");
                Graph graphDS1 = new Graph(6);
                datasetReader("Dataset1.txt", graphDS1);
                System.out.println("|                   DATASET N°1 LOADED                      |");
                return graphDS1;
            case 2:
                System.out.println("|-----------------------------------------------------------|");
                Graph graphDS2 = new Graph(6);
                datasetReader("Dataset2.txt", graphDS2);
                System.out.println("|                   DATASET N°2 LOADED                      |");
                return graphDS2;
            case 3:
                System.out.println("|-----------------------------------------------------------|");
                Graph graphDS3 = new Graph(10);
                datasetReader("Dataset3.txt", graphDS3);
                System.out.println("|                   DATASET N°3 LOADED                      |");
                return graphDS3;
            case 4:
                System.out.println("|-----------------------------------------------------------|");
                Graph graphDS4 = new Graph(16);
                datasetReader("Dataset4.txt", graphDS4);
                System.out.println("|                   DATASET N°4 LOADED                      |");
                return graphDS4;
            case 5:
                System.out.println("|-----------------------------------------------------------|");
                Graph graphDS5 = new Graph(20);
                datasetReader("Dataset5.txt", graphDS5);
                System.out.println("|                   DATASET N°5 LOADED                      |");
                return graphDS5;
            default:
                System.out.println("Please enter a valid option");
                break;
        }
        return null;
    }
    
    public static void menu(Graph g) {
        System.out.println("|-----------------------------------------------------------|");
        System.out.println("| To delete a node enter______________________________: 'd' |"); 
        System.out.println("| To add a node enter_________________________________: 'a' |");
        System.out.println("| To modify the maximum flow of a node enter__________: 'm' |");
        System.out.println("| To print the graph enter____________________________: 'p' |");
        System.out.println("| To run the maximum flow algorithm enter_____________: 'r' |");
        System.out.println("| To load a different dataset enter___________________: 'l' |");
        System.out.println("| To run a comparative analysis of the algorithm enter: 'c' |");
        System.out.println("| To exit the program enter___________________________: 'e' |");
        System.out.println("|-----------------------------------------------------------|");
        Scanner scanner = new Scanner(System.in);
        System.out.print("| Please enter your option: ");
        
        switch (scanner.next()) {
            
            case "d":
                {
                    int source, destination;
                    System.out.println("|-----------------------------------------------------------|");
                    System.out.print("| Enter the source of the node to delete: ");
                    source = Integer.valueOf(scanner.next());
                    System.out.print("| Enter the destination of the node to delete: ");
                    destination = Integer.valueOf(scanner.next());
                    System.out.println("|-----------------------------------------------------------|");
                    System.out.println("| " + source + " | " + destination);
                    
                    g.delEdge(source, destination, g);
                    
                    menu(g);
                    break;
                }
            case "a":
                {
                    int source, destination, maxCapacity;
                    System.out.println("|-----------------------------------------------------------|");
                   
                    System.out.print("| Please enter the source of the new node: ");
                    source = Integer.valueOf(scanner.next());
                    System.out.print("| Please enter the destination of the new node: ");
                    destination = Integer.valueOf(scanner.next());
                    System.out.print("| Please enter the maximum capacity of the new node: ");
                    maxCapacity = Integer.valueOf(scanner.next());
                    System.out.println("| New node added | Source: " + source +
                            " | Desintation: " + destination +
                            " | Maximum capacity: " + maxCapacity);
                    
                    g.addEdge(source, destination, maxCapacity);
                    
                    menu(g);
                    break;
                }
            case "m":
                {
                    System.out.println("|-----------------------------------------------------------|");
                    int source, destination, newCapacity;
                    System.out.print("| Please enter the source of the node to modify: ");
                    source = Integer.valueOf(scanner.next());
                    System.out.print("| Please enter the destination of the node to modify: ");
                    destination = Integer.valueOf(scanner.next());
                    System.out.print("| Please enter the new capacity of the node to modify: ");
                    newCapacity = Integer.valueOf(scanner.next());
                    System.out.println("| Node modification | Source: " + source + 
                            " | Destination: " + destination +
                            " | New maximum capacity: " + newCapacity);
                    
                    g.modifyMaxFlow(source, destination, newCapacity);
                    
                    menu(g);
                    break;
                }
            case "p": 
                {
                    System.out.println("|-----------------------------------------------------------|");
                    System.out.println("|                        GRAPH PRINTING                     |");
                    g.printGraph();
                    
                    menu(g);
                    break;
                }
            case "r":
                {
                    System.out.println("|-----------------------------------------------------------|");
                    System.out.println("|                    MAXIMUM FLOW ALGORITHM                 |");
                    int result = g.dinicMaxFlow(0, g.vertexNum-1);
                    System.out.println("|-----------------------------------------------------------|");
                    System.out.println("| - Maximum flow: " + result + " -                          |");
                    
                    menu(g);
                    break;
                }
            case "l":
                {
                    g = loadDataset();
                    menu(g);
                    break;
                }
            case "c":
                {
                    comparativeAnalysis(g);
                    menu(g);
                    break;
                }
            case "e":
                {
                    System.exit(0);
                }
            default:
                System.out.println("| Please enter a correct option");
                menu(g);
                break;
        }
    
    
    }
    
}
