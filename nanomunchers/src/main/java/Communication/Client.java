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
    public static void main(String[] args) {
        getDirectionPermutation(permutations, new LinkedList<String>(), new String[]{"up",
                "down", "left", "right"}, new HashSet<String>());
        try {
            Socket socket = new Socket("localhost", 1377);
            PrintWriter out = new PrintWriter(socket.getOutputStream(), true);
            BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
            String state;
            out.println("REGISTER:" + args[0]);
            while ((state = in.readLine()) != null) {
                if(state.equals("START")){
                    command = new StringBuffer();
                }
                else if(state.equals("END")){
                    if (!command.toString().replace("\n", "").equals("WAITING")) {
                        out.println(process(command.toString()));
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

    private static String process(String command){
        Map<Integer, Map<String, Integer>> map = parseCommand(command);
        Map<Integer, List<String>> res = new HashMap<Integer, List<String>>();
        for (int i = 4; i >= 1; i--) {
            res = getBestNodeAndPermutation(map, i);
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
        Integer key = (Integer)res.keySet().toArray()[0];
        StringBuilder node = new StringBuilder();
        node.append(key);
        for (String direction: res.get(key)) {
            node.append("," + direction);
        }
        return  node.toString();
    }

    private static Map<Integer, Map<String, Integer>> parseCommand(String command) {
        Map<Integer, Map<String, Integer>> relation = new HashMap<Integer, Map<String, Integer>>();
        String[] states = command.split("\n");
        for (int i = 0; i < states.length; i++) {
            if (states[i].length() > 0) {
                String[] cur = states[i].split(",");
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
                    relation.put(Integer.parseInt(cur[0]), curMap);
                }
            }

        }
        return relation;
    }

    private static Map<Integer, List<String>> getBestNodeAndPermutation(Map<Integer, Map<String,
            Integer>> relation, int openDirections) {
        int node = -1;
        int max = 0;
        List<String> bestPermutation = new LinkedList<String>();
        for (Integer nodeId: relation.keySet()) {
            if (relation.get(nodeId).size() != openDirections) {
                continue;
            }
            for (List<String> permutation : permutations) {
                int score = getScore(relation, nodeId, permutation);
                if (score > max) {
                    max = score;
                    node = nodeId;
                    bestPermutation = permutation;
                }
            }
        }
        Map<Integer, List<String>> res = new HashMap<Integer, List<String>>();
        res.put(node, bestPermutation);
        return res;
    }

    private static int getScore(Map<Integer, Map<String, Integer>> relation, int nodeId,
                                List<String> permutation) {
        Map<Integer, Map<String, Integer>> copy = new HashMap<Integer, Map<String, Integer>>
                (relation);

        int count = 1;
        int direction = 0;
        Set<Integer> set = new HashSet<Integer>();
        set.add(nodeId);
        while (true) {
            boolean findNext = false;
            for (int j = direction; j < 4; j++) {
                if (copy.get(nodeId) != null && copy.get(nodeId).containsKey(permutation
                        .get(j))) {
                    nodeId = copy.get(nodeId).get(permutation.get(j));
                    if (set.contains(nodeId)) {
                        continue;
                    }
                    set.add(nodeId);
                    count += 1;
                    direction = (j + 1) % 4;
                    findNext = true;
                    break;
                }
            }
            if (!findNext) {
                for (int j = 0; j < direction; j++) {
                    if (copy.get(nodeId) != null && copy.get(nodeId).containsKey(permutation.get(j)
                    )) {
                        nodeId = copy.get(nodeId).get(permutation.get(j));
                        if (set.contains(nodeId)) {
                            continue;
                        }
                        set.add(nodeId);
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
