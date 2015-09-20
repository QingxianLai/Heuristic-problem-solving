public class Problem1 {
    int[] targetDenominations = new int[7];
    public void go(final int N) {
        Runnable runnable = new Runnable() {
            public void run() {
                int min = Integer.MAX_VALUE;
                for (int i = 2; i <= 9; i += 1) {
                    for (int j = 10; j <= 236; j += 5) {
                        for (int k = j + 5; k <= 237; k += 5) {
                            for (int m = k + 5; m <= 238; m += 5) {
                                for (int n = m + 5; n <= 239; n += 5) {
                                    for (int z = n + 5; z <= 240; z += 5) {
                                        int[] score = getScore(new int[]{1, i, j, k, m, n, z}, N);
                                        if (score[2] <= min) {
                                            min = score[2];
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
        int[] dp = new int[240];
        dp[0] = 0;
        for (int i = 1; i < 240; i++) {
            int localMin = 250;
            for (int denomination: denominations) {
                if (i - denomination >= 0) {
                    if (dp[i - denomination] < localMin) {
                        localMin = dp[i - denomination];
                    }
                }
            }
            dp[i] = localMin + 1;
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
        /* Problem1 solution = new Problem1(); */
        /* solution.go(1); */
        double N = Double.parseDouble(args[0])
        if (N <= 1.974358) {
            System.out.println(1 + " " + 5 + " " + 11 + " " + 24 + " " + 60 + " " + 67 + " " + 88);
        } else if (N <=18.888888) {
            System.out.println(1 + " " + 4 + " " + 15 + " " + 20 + " " + 65 + " " + 75 + " " + 105);
        } else {
            System.out.println(1 + " " + 5 + " " + 20 + " " + 30 + " " + 70 + " " + 80 + " " + 115);
        }
    }
}
