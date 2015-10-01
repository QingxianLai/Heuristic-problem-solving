/**
 * Created by LaiQX on 10/01/15.
 */
public class FirstPlayerStrategy extends NoTippingPlayer {
    /**
     * Pass the port with which you registered yourselves
     *
     * @param port
     */
    FirstPlayerStrategy(int port) {
        super(port);
    }

    @Override
    protected String process(String command) {
        // TODO: fill this methods with our First Player strategy,
        // Its input and output format should be a string of "<Position> <Weight>",
        // We can use this player to against AI at first.
        return null;
    }
}
