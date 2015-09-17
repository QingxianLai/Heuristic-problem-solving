/**
 * Created by LaiQX on 09/17/15.
 */
public class Problem2 {
    private static final int UPPER = 240;
    public static void main(String[] args) {
        int[] dp = new int[UPPER+1];
        dp[0] = 0;
        int[] denominations = {1,3,7,15,30,60,120};

        for (int i = 1; i< UPPER; i++) {
            int min = 10;
            for (int coin: denominations) {
                if (i-coin>=0) {
                    min = Math.min(min, dp[i-coin] + 1);
                }
            }
            dp[i] = min;
        }


        for (int i = UPPER-1; i>0; i--) {
            if (i == 30) {
                int aaa = i;
            }
            int min = 10;
            for (int coin: denominations) {
                if (i+coin <= UPPER) {
                    min = Math.min(min, dp[i+coin]+1);
                }
            }

            dp[i] = Math.min(dp[i], min);
            System.out.println(i + "=> " + dp[i]);
        }

    }
}
