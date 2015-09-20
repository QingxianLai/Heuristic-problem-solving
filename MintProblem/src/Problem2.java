/**
 * Created by LaiQX on 09/17/15.
 */
public class Problem2 {
    private static final int UPPER = 240;
    int[] targetDenominations = new int[7];
    public void go(final int N) {
        Runnable runnable = new Runnable() {
            public void run() {
                int min = Integer.MAX_VALUE;
                for (int i = 2; i <= 11; i += 1) {
                    for (int j = i + 1; j <= 236; j += 1) {
                        if (j > 10 * i) {
                            break;
                        }
                        for (int k = j + 1; k <= 237; k += 1) {
                            if (k > 2 * j) {
                                break;
                            }
                            for (int m = k + 5; m <= 238; m += 1) {
                                if (m > 2 * k) {
                                    break;
                                }
                                for (int n = m + 5; n <= 239; n += 1) {
                                    if (n > 120) {
                                        break;
                                    }
                                    for (int z = n + 5; z <= 240; z += 1) {
                                        if (z > 200) {
                                            break;
                                        }
                                        int[] score = getScore(new int[]{1, i, j, k, m, n, z}, N);
                                        if (score[0] <= min) {
                                            min = score[0];
                                            targetDenominations = new int[]{1, i, j, k, m, n, z};
                                            System.out.println(1 + " " + i + " " + j + " " + k + " " + m + " " + n + " " + z + " score1 = " + score[1] + " score2 = " + score[2]);   
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        };
        Thread thread = new Thread(runnable);
        thread.start();
    }
    public int[] getScore(int[] denominations, int N) {
        int score = 0;
        int score1 = 0;
        int score2 = 0;
        int[] dp = new int[UPPER + 1];
        dp[0] = 0;

        for (int i = 1; i < UPPER; i++) {
            int min = 10;
            for (int coin: denominations) {
                if (i - coin >= 0) {
                    min = Math.min(min, dp[i - coin] + 1);
                }
            }
            dp[i] = min;
        }

        for (int i = UPPER - 1; i > 0; i--) {
            int min = 10;
            for (int coin: denominations) {
                if (i + coin <= UPPER) {
                    min = Math.min(min, dp[i + coin] + 1);
                }
            }
            dp[i] = Math.min(dp[i], min);
            if (i % 5 == 0) {
                score += dp[i] * N;
                score2 += dp[i] * N;
            } else {
                score += dp[i];
                score1 += dp[i];
            }
        }
        return new int[]{score, score1, score2};
    }
    public static void main (String[] args) {
        /* Problem2 solution = new Problem2(); */
        /* solution.go(1); */
        Double N = Double.parseInt(args[0]);
        /**
         * Potential solution:
         * (1) 1 5 30 45 50 55 170 (652 82) Minimum score2
         * (2) 1 3 10 20 25 85 140 (567 89)
         *     1 4 20 40 50 55 175 (598 88) Minimum score2 when minizing score1
         * (3) 1 4 16 23 34 82 113 (497 128) Minimum total score(keep searching)
         */ 
    }
}
