package Communication;


import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;
import java.util.*;

/**
 * Created by islam on 11/1/15.
 */
public class Client {

    private static StringBuffer command = new StringBuffer();
    private static List<List<String>> permutations = new LinkedList<List<String>>();
    private static Map<Integer, Map<String, Integer>> freeNodes = new HashMap<Integer, Map<String, Integer>>();
    private static Map<Integer, Map<String, Integer>> oppOccupiedNodes = new HashMap<Integer, Map<String, Integer>>();
    private static int oppLiveNodes = 15;
    private static String oppo;

    public static void main(String[] args) {
        getDirectionPermutation(permutations, new LinkedList<String>(), new String[]{"up",
                "down", "left", "right"}, new HashSet<String>());
        try {
            Socket socket = new Socket("localhost", 1377);
            PrintWriter out = new PrintWriter(socket.getOutputStream(), true);
            BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
            String state;
            out.println("REGISTER:" + "NewJersey");
            while ((state = in.readLine()) != null) {
                if(state.equals("START")){
                    command = new StringBuffer();
                }
                else if(state.equals("END")){
                    if (!command.toString().replace("\n", "").equals("WAITING")) {
                        freeNodes = new HashMap<Integer, Map<String, Integer>>();
                        oppOccupiedNodes = new HashMap<Integer, Map<String, Integer>>();
                        parseCommand(command.toString());
                        System.out.println(oppOccupiedNodes);
                        StringBuilder commands = new StringBuilder();
                        Map<Integer, List<String>> stopNodes = muncherStopper();
                        if (stopNodes.size() > 0) {
                            for (Integer node: stopNodes.keySet()) {
                                commands.append(node);
                                for (String direction: stopNodes.get(node)) {
                                    commands.append("," + direction);
                                }
                                commands.append("|");
                            }

                            commands.append(process(command.toString()));
                            System.out.println(commands.toString());
                            out.println(commands.toString());
                        } else {
                            String cmd = process(command.toString());
                            System.out.println(cmd);
                            out.println(cmd);
                            //out.println("116,up,down,left,right");
                        }
                    }
                }else{
                    command.append(state + "\n");
                }
            }
        } catch (IOException eIO) {
            System.out.println("ERROR");
            System.out.println(eIO.getMessage());
        }
    }

    static class Move {
        public int nodeId;
        public List<String> permutation;

        public Move(int nodeId, List<String> permutation) {
            this.nodeId = nodeId;
            this.permutation = permutation;
        }
    }

    private static String process(String command){
        //System.out.println(command);

        Map<Integer, List<String>> res = new HashMap<Integer, List<String>>();
        for (int i = 4; i >= 1; i--) {
            res = getBestNodeAndPermutation(i);
            boolean find = false;
            for (Integer key: res.keySet()) {
                if (key != -1) {
                    find = true;
                    break;
                }
            }
            if (find) {
                break;
            }
        }
        System.out.println(res);
        Integer key = (Integer)res.keySet().toArray()[0];
        //Starting point for your program
        StringBuilder node = new StringBuilder();
        node.append(key);
        for (String direction: res.get(key)) {
            node.append("," + direction);
        }
        return  node.toString();
    }

    private static void parseCommand(String command) {

        String[] states = command.split("\n");
        for (int i = 0; i < states.length; i++) {
            if (states[i].length() > 0) {
                String[] cur = states[i].split(",");
                if (cur[0].equals("ONE") && !cur[1].equals("NewJersey")) {
                    oppo = "P1";
                    oppLiveNodes = Integer.parseInt(cur[2]) + Integer.parseInt(cur[4]);
                } else if (cur[0].equals("TWO") && !cur[1].equals("NewJersey")) {
                    oppo = "P2";
                    oppLiveNodes = Integer.parseInt(cur[2]) + Integer.parseInt(cur[4]);
                }
                if (isInteger(cur[0]) && cur[3].equals("FREE")) {
                    Map<String, Integer> curMap = new HashMap<String, Integer>();
                    if (!cur[4].equals("null")) {
                        curMap.put("up", Integer.parseInt(cur[4]));
                    }
                    if (!cur[5].equals("null")) {
                        curMap.put("down", Integer.parseInt(cur[5]));
                    }
                    if (!cur[6].equals("null")) {
                        curMap.put("left", Integer.parseInt(cur[6]));
                    }
                    if (!cur[7].equals("null")) {
                        curMap.put("right", Integer.parseInt(cur[7]));
                    }
                    freeNodes.put(Integer.parseInt(cur[0]), curMap);
                } else if (isInteger(cur[0]) && cur[3].equals("OCCUPIED_" + oppo)) {
                    Map<String, Integer> curMap = new HashMap<String, Integer>();
                    if (!cur[4].equals("null")) {
                        curMap.put("up", Integer.parseInt(cur[4]));
                    }
                    if (!cur[5].equals("null")) {
                        curMap.put("down", Integer.parseInt(cur[5]));
                    }
                    if (!cur[6].equals("null")) {
                        curMap.put("left", Integer.parseInt(cur[6]));
                    }
                    if (!cur[7].equals("null")) {
                        curMap.put("right", Integer.parseInt(cur[7]));
                    }
                    oppOccupiedNodes.put(Integer.parseInt(cur[0]), curMap);
                }
            }

        }
    }

    private static Map<Integer, List<String>> muncherStopper() {
        Map<Integer, List<String>> stopNodes = new HashMap<Integer, List<String>>();
        String[] dirs = {"up", "down", "left", "right"};

        // iterate every opponent's muncher
        for (int node: oppOccupiedNodes.keySet()) {

            // each opponent muncher record the max stop score and number of availble ways.
            int numWays = 0;
            int maxScore = 0;
            int maxNextM = 0;
            List<String> maxNextMoves = null;

            // iterate through every possible directions.
            for (String dir: dirs) {

                // if the positin is free
                if (oppOccupiedNodes.get(node).containsKey(dir)
                        && freeNodes.containsKey(oppOccupiedNodes.get(node).get(dir))) {

                    numWays++;
                    int stopNode = oppOccupiedNodes.get(node).get(dir);

                    // if the stopNode has two way to go and we will choose its next node(opposite to the opponent) as stopNode (replace the old one)
                    stopNode = checkStopNode(node, stopNode);
                    if (stopNode == -1) {
                        continue;
                    }

                    // calculate the local maximum score among all the possible moves.
                    int maxMoveScore = 0;
                    List<String> maxMoves = null;
                    for (List<String> moves: permutations) {
                        int score = getScore(stopNode, moves);
                        if (score > maxMoveScore) {
                            maxMoveScore = score;
                            maxMoves = moves;
                        }
                    }

                    // update the max of the opponent's muncher
                    if (maxMoveScore > maxScore) {
                        maxScore = maxMoveScore;
                        maxNextM = stopNode;
                        maxNextMoves = maxMoves;
                    }

                }
            }

            // if less equal than 2 available way out and the max Score greater then 2, add it to the stopNodes
            if (numWays <= 4 && maxScore >= 2) {
                stopNodes.put(maxNextM, maxNextMoves);
            }
        }

        //System.out.println("find Stop Nodes: " + stopNodes.toString());
        return stopNodes;
    }

    // find if the current stop node has a next node opposite to oppponent, then return the nodeId, otherwise return -1.
    private static int checkStopNode(int oppoNode, int prevNode){
        // only choose the node has two way to go.
        if (freeNodes.get(prevNode).keySet().size()!=2) {
            return -1;
        }

        int nextNode = -1;

        for (String dir: freeNodes.get(prevNode).keySet()) {

            //choose the direction opposite to the oppponent's muncher
            if (freeNodes.get(prevNode).get(dir) != oppoNode) {
                nextNode = freeNodes.get(prevNode).get(dir);
                break;
            }
        }

        // this node should be exist and free to go.
        if (nextNode == -1 || !freeNodes.containsKey(nextNode)) {
            return -1;
        }

        return nextNode;
    }


    private static Map<Integer, List<String>> getBestNodeAndPermutation(int openDirections) {
        int node = -1;
        int max = 0;
        List<String> bestPermutation = new LinkedList<String>();
        for (Integer nodeId: freeNodes.keySet()) {
            if (freeNodes.get(nodeId).size() != openDirections) {
                continue;
            }
            for (List<String> permutation : permutations) {
                int score = getScore(nodeId, permutation);
                if (score > max) {
                max = score;
                node = nodeId;
                bestPermutation = permutation;
                }
            }
        }

        Map<Integer, List<String>> res = new HashMap<Integer, List<String>>();
        res.put(node, bestPermutation);

        //System.out.println("res: " + res + " max: " + max);
        return res;
    }

    private static int getScore(int nodeId, List<String> permutation) {
        int count = 1;
        int direction = 0;
        Set<Integer> set = new HashSet<Integer>();
        set.add(nodeId);
        //System.out.println("permutation: " + permutation);
        while (true) {
            boolean findNext = false;
            for (int j = direction; j < 4; j++) {
                if (freeNodes.containsKey(nodeId) && freeNodes.get(nodeId).containsKey(permutation
                        .get(j))) {

                    int newNodeId = freeNodes.get(nodeId).get(permutation.get(j));
                    if (set.contains(newNodeId)) {
                        continue;
                    }
                    set.add(newNodeId);
                    nodeId = newNodeId;
                    //System.out.println("cur node id: " + nodeId);
                    //System.out.println(set);
                    count += 1;
                    direction = (j + 1) % 4;
                    findNext = true;
                    break;
                }
            }
            if (!findNext) {
                for (int j = 0; j < direction; j++) {
                    if (freeNodes.containsKey(nodeId) && freeNodes.get(nodeId).containsKey(permutation
                                    .get(j)
                    )) {
                        int newNodeId = freeNodes.get(nodeId).get(permutation.get(j));
                        if (set.contains(newNodeId)) {
                            continue;
                        }
                        set.add(newNodeId);
                        nodeId = newNodeId;
                        count += 1;
                        direction = (j + 1) % 4;
                        findNext = true;
                        break;
                    }
                }
            }
            if (!findNext) {
                break;
            }
        }
        return count;
    }

    public static boolean isInteger(String s) {
        try {
            Integer.parseInt(s);
        } catch(Exception e) {
            return false;
        }
        return true;
    }

    public static void getDirectionPermutation(List<List<String>> permutations, List<String> cur,
                                         String[] directions, Set<String> set) {
        if (cur.size() == 4) {
            permutations.add(new LinkedList<String>(cur));
            return;
        }
        for (int i = 0; i < 4; i++) {
            if (set.contains(directions[i])) {
                continue;
            }
            cur.add(directions[i]);
            set.add(directions[i]);
            getDirectionPermutation(permutations, cur, directions, set);
            cur.remove(directions[i]);
            set.remove(directions[i]);
        }
    }
}
