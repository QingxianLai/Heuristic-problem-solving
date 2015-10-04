import java.util.*;

/**
 * Created by lyc on 10/1/15.
 */
public class MyStrategy extends NoTippingPlayer {

    private Random strategy = new Random();
    private boolean hasStarted = false;
    private int player;
    private Set<Integer> weights;
    private Set<Integer> weightsReversed;
    
    private List<Weight> weightsOnBoard;
    private int leftWight;
    private int rightWeight;
    private int[] board;
    private boolean firstRemove;

    private Set<Integer> opponentWeight;
    private Set<Integer> opponentWeightReserved;
    private int absoluteDifferent;

    public MyStrategy(int port) {
        super(port);
    }


    protected String process(String command) {
        if (!hasStarted) {
            this.player = 1;
            firstRemove = false;
            weightsOnBoard = new ArrayList<Weight>();
            // put the original 3 kg block on board
            weightsOnBoard.add(new Weight(3, -4, 1));
            board = new int[51];
            board[-4 + 25] = 3;
            weights = new TreeSet<Integer>(new Comparator<Integer>() {
                @Override
                public int compare(Integer integer, Integer t1) {
                    return integer - t1;
                }
            });
            weightsReversed = new TreeSet<Integer>(new Comparator<Integer>() {
                @Override
                public int compare(Integer integer, Integer t1) {
                    return t1 - integer;
                }
            });
            opponentWeight = new TreeSet<Integer>(new Comparator<Integer>() {
                
                @Override
                public int compare(Integer integer, Integer t1) {
                    return integer - t1;
                }
            });
            opponentWeightReserved = new TreeSet<Integer>(new Comparator<Integer>() {
                
                @Override
                public int compare(Integer integer, Integer t1) {
                    return t1 - integer;
                }
            });

            for (int i = 1; i <= 15; i ++) {
                weights.add(i);
                weightsReversed.add(i);
                opponentWeight.add(i);
                opponentWeightReserved.add(i);
            }
            hasStarted = true;
        }

        StringTokenizer tk = new StringTokenizer(command);
        // get the command, and opponent's position and weight last round.
        command = tk.nextToken();
        int position = Integer.parseInt(tk.nextToken());
        int weight = Integer.parseInt(tk.nextToken());

        // in the beginning of game, whoever gets 0, 0 for position and weight is
        // player 1
        if (position == 0 && weight == 0) {
            this.player = 0;
            firstRemove = true;
        } else {
            // execute previous player's move
            if (command.equals("ADDING")) {
                weightsOnBoard.add(new Weight(weight, position, (player + 1) % 2));
                opponentWeight.remove(weight);
                opponentWeightReserved.remove(weight);
                board[position + 25] = weight;
            } else {
                // The last user add will end up with the following message
                // REMOVING position weight
                // we must add the position and weight as player 1 before removing.
                if (weightsOnBoard.size() == 30 && firstRemove) {
                    weightsOnBoard.add(new Weight(weight, position, (player + 1) % 2));
                    firstRemove = false;
                } else {
                    removeWeight(weightsOnBoard, position, weight);
                }
            }
        }
        Weight decision;
        if (command.equals("ADDING")) {
            if (this.player == 0) {
                decision = playerOneMakeAddMove();
            } else {
                decision = playerTwoMakeAddMove(position);
            }
            // update board
            weightsOnBoard.add(decision);
            weights.remove(decision.weight);
            board[decision.position+25] = decision.weight;
        } else {
            if (this.player == 0) {
                decision = playerOneMakeRemoveMove();
            } else {
                decision = playerTwoMakeRemoveMove();
            }

            // update board
            weightsOnBoard.remove(decision);
        }
        return decision.position + " " + decision.weight;

    }

    public Weight playerOneMakeAddMove() {
        for (Integer weight : weightsReversed) {
            for (int pos = 24; pos >= 0; pos--) {
                //System.out.println("1: " + "weight = " + weight + " postion = " + pos);
                if (board[pos + 25] == 0) {
                    if (validAddMove(weight, pos, weightsOnBoard)) {
                        weightsReversed.remove(weight);
                        weights.remove(weight);
                        board[pos + 25] = weight;
                        List<Weight> myBlocks = getMyBlocks(weightsOnBoard, player);
                        leftWight = 0;
                        rightWeight = 0;
                        for (Weight myWeight: myBlocks) {
                            if (myWeight.position < -3) {
                                leftWight += myWeight.weight * (-3 - myWeight.position);
                            } else if (myWeight.position > -1) {
                                rightWeight += myWeight.weight * (myWeight.position + 1);
                            }
                        }
                        return new Weight(weight, pos, player);
                    }
                }
            }
        }
        for (Integer weight : weights) {
            for (int pos = -1; pos >= -25; pos--) {
                if (board[pos + 25] == 0) {
                    if (validAddMove(weight, pos, weightsOnBoard)) {
                        weightsReversed.remove(weight);
                        weights.remove(weight);
                        board[pos + 25] = weight;
                        List<Weight> myBlocks = getMyBlocks(weightsOnBoard, player);
                        leftWight = 0;
                        rightWeight = 0;
                        for (Weight myWeight: myBlocks) {
                            if (myWeight.position < -3) {
                                leftWight += myWeight.weight;
                            } else if (myWeight.position > -1) {
                                rightWeight += myWeight.weight;
                            }
                        }
                        return new Weight(weight, pos, player);
                    }
                }
            }
        }
        // basically we lost
        // below is a dummy.
        int candidate = (Integer)weights.toArray()[0];
        Weight returnLosingMove = new Weight(candidate, 1, player);
        for (int pos = -25; pos <= 25; pos ++) {
            if (board[pos + 25] == 0) {
                board[pos + 25] = candidate;
                returnLosingMove = new Weight(candidate, pos, player);
                break;
            }
        }
        return returnLosingMove;
    }

    private class OptPair {
        private Weight w;
        private int opt;

        public OptPair(Weight weight, int opti) {
            this.w = weight;
            this.opt = opti;
        }

        public Weight getWeight() {
            return w;
        }

        public int getOpt() {
            return opt;
        }
    }

    public Weight playerTwoMakeAddMove(int playerOneLastMovePos) {

        OptPair opt = optimizedMove(false, 3, player);

        return opt.getWeight();
    }

    private OptPair optimizedMove(boolean isMax, int maxDepth, int player) {
//        System.out.println("opt: isMax = " + isMax + ", maxDepth = " + maxDepth + ", player = " + player);
        Set<Integer> currentWeights = new HashSet<Integer>(player == this.player ? weights : opponentWeight);
        Set<Integer> weightsAvailable = player == this.player ? weights : opponentWeight;
        int nextPlayer = (player + 1) % 2;

        OptPair res;

        if (isMax) {
            isMax = !isMax;
            int maxValue = -1;
            Weight maxWeight = null;
            for (int w : currentWeights) {
                weightsAvailable.remove(w);
                for (int i = 0; i < board.length; i++) {

                    if (!validAddMove(w, i - 25, weightsOnBoard)) {
                        continue;
                    }
                    Weight weight = new Weight(w, i - 25, player);
                    board[i] = w;
                    weightsOnBoard.add(weight);

                    if (maxDepth > 1) {
                        OptPair pair = optimizedMove(isMax, maxDepth - 1, nextPlayer);
                        if (pair.getOpt() > maxValue) {
                            maxValue = pair.getOpt();
                            maxWeight = weight;
                        } else if(pair.getOpt() == maxValue) {
                            boolean val = new Random().nextInt(2)==0;
                            if (val) {
                                maxValue = pair.getOpt();
                                maxWeight = weight;
                            }
                        }
//                        System.out.println("maxValue:" + maxValue + "; maxWeight" + maxWeight);
                    } else {
                        int diff = getPlayer2AbsoluteDifferent();
                        if (diff > maxValue) {
                            maxValue = diff;
                            maxWeight = weight;
                        } else if(diff == maxValue) {
                            boolean val = new Random().nextInt(2)==0;
                            if (val) {
                                maxValue = diff;
                                maxWeight = weight;
                            }
                        }
                    }

                    board[i] = 0;
                    weightsOnBoard.remove(weight);
                }
                weightsAvailable.add(w);
            }

            res = new OptPair(maxWeight, maxValue);
        } else {
            isMax = !isMax;
            int minValue = Integer.MAX_VALUE;
            Weight minWeight = null;
            for (int w : currentWeights) {
                weightsAvailable.remove(w);
                for (int i = 0; i < board.length; i++) {
//                    System.out.println("weight: " + w + ", position:" + (i-25));
//                    System.out.println(validAddMove(w, i - 25, weightsOnBoard));
                    boolean verify = !validAddMove(w, i-25, weightsOnBoard);
                    if (!validAddMove(w, i - 25, weightsOnBoard)) {
                        continue;
                    }
                    Weight weight = new Weight(w, i - 25, player);
                    board[i] = w;
                    weightsOnBoard.add(weight);

                    if (maxDepth > 1) {
                        OptPair pair = optimizedMove(isMax, maxDepth - 1, nextPlayer);
                        if (pair.getOpt() < minValue) {
//                            System.out.println("weight: " + weight + " verify:" + verify);
                            minValue = pair.getOpt();
                            minWeight = weight;
                        } else if(pair.getOpt() == minValue) {
                            boolean val = new Random().nextInt(2)==0;
                            if (val) {
                                minValue = pair.getOpt();
                                minWeight = weight;
                            }
                        }
//                        System.out.println("minValue:" + minValue + "; minWeight" + minWeight);
//                        System.out.println(validAddMove(minWeight.weight, minWeight.position, weightsOnBoard));

                    } else {
                        int diff = getPlayer2AbsoluteDifferent();
                        if (diff < minValue) {

                            minValue = diff;
                            minWeight = weight;
                        } else if(diff == minValue) {
                            boolean val = new Random().nextInt(2)==0;
                            if (val) {
                                minValue = diff;
                                minWeight = weight;
                            }
                        }
                    }
                    board[i] = 0;
                    weightsOnBoard.remove(weight);
//                    System.out.println("minValue:" + minValue + "; minWeight" + minWeight);
//                    System.out.println(validAddMove(minWeight.weight, minWeight.position, weightsOnBoard));
                }
                weightsAvailable.add(w);
            }
            res = new OptPair(minWeight, minValue);
        }
//        System.out.println(validAddMove(res.getWeight().weight, res.getWeight().position, weightsOnBoard));
        return res;
    }

    private int getPlayer2AbsoluteDifferent() {
        int left = 1;
        int right = 0;
        for (Weight wat : weightsOnBoard) {
            if (wat.player == 1) {
                if (wat.position <= -3) {
                    left++;
                }
                if (wat.position >= -1) {
                    right++;
                }
            }
        }
        int diff = Math.abs(right - left);
        return diff;
    }

    public Weight playerOneMakeRemoveMove() {
        List<Weight> removeCandidate = new ArrayList<Weight>(weightsOnBoard);
        if (leftWight < rightWeight) {
            int max = 0;
            Weight target = null;
            for (Weight weight: removeCandidate) {
                //System.out.println(weight);
                if (weight.position != -4 && (-1 - weight.position) * weight.weight > max &&
                        canRemove(weight, removeCandidate)) {
                    max = (-1 - weight.position) * weight.weight;
                    target = weight;
                }
            }
            if (target != null) {
                removeCandidate.remove(target);
                weightsOnBoard.remove(target);
                return target;
            } else {
                int min = Integer.MAX_VALUE;
                for (Weight weight: removeCandidate) {
                    if (weight.position > -1 && (weight.position + 1) * weight.weight < min &&
                            canRemove(weight, removeCandidate)) {
                        min = (weight.position + 1) * weight.weight;
                        target = weight;
                    }
                }
                if (target != null) {
                    removeCandidate.remove(target);
                    weightsOnBoard.remove(target);
                    return target;
                }
            }

        }
        return null;
    }

    public Weight playerTwoMakeRemoveMove() {
        return null; 
    }

    private boolean canRemove(Weight weight, List<Weight> weights_on_board) {
        List<Weight> temp = new ArrayList<Weight>();
        for (Weight w: weights_on_board) {
            temp.add(w);
        }
        temp.remove(weight);
        return verifyGameNotOver(temp);
    }

    private boolean validAddMove(int weight, int position, List<Weight> weights_on_board) {
        if (board[position+25]!=0) {
            return false;
        }
        List<Weight> temp = new ArrayList<Weight>();
        for (Weight w: weights_on_board) {
            temp.add(w);
        }
        temp.add(new Weight(weight, position, player));
        //System.out.println(temp);
        return verifyGameNotOver(temp);
    }

    private void removeWeight(List<Weight> weights_on_board, int pos, int weight) {
        Weight retW = new Weight(0, 0, 0);
        for (Weight w : weights_on_board) {
            if (w.position == pos && w.weight == weight) {
                retW = w;
            }
        }
        weights_on_board.remove(retW);
    }

    private List<Weight> getMyBlocks(List<Weight> weights_on_board, int player) {
        List<Weight> returnBlock = new ArrayList<Weight>();
        for (Weight w: weights_on_board) {
            if (w.player == player) {
                returnBlock.add(w);
            }
        }
        return returnBlock;
    }

    private boolean verifyGameNotOver(List<Weight> weights_on_board) {
        int left_torque = -9;
        int right_torque = -3;
        for (Weight weight: weights_on_board) {
            left_torque += ((-3) - weight.position) * weight.weight;

            right_torque += ((-1) - weight.position) * weight.weight;
        }
        return !(left_torque > 0 || right_torque < 0);
    }

    public static void main(String[] args) throws Exception {
        new MyStrategy(Integer.parseInt(args[0]));
    }

    public class Weight {
        public int weight;
        public int position;
        public int player;
        public Weight(int weight, int position, int player) {
            this.weight = weight;
            this.position = position;
            this.player = player;
        }

        @Override
        public String toString() {
            return "Weight = " + weight + " position = " + position;
        }
    }
}
