
import java.util.NoSuchElementException;
import java.util.Random;

public class Prob3Match {

    public static final int RED = 0;
    public static final int GREEN = 1;
    public static final int BLUE = 2;

    interface Bag {
        int draw();  // draw a single ball and remove from bag
        void reset();  // reset to original state
        int count();
    }

    private static class BagArray implements Bag {

        private final Random random;
        private final int[] balls;
        private int ballCount;

        public BagArray(int rCount, int gCount, int bCount) {
            random = new Random();
            ballCount = rCount + gCount + bCount;
            balls = new int[ballCount];
            for (int i = 0; i < rCount; i++) {
                balls[i] = RED;
            }
            for (int i = rCount; i < rCount + gCount; i++) {
                balls[i] = GREEN;
            }
            for (int i = rCount + gCount; i < ballCount; i++) {
                balls[i] = BLUE;
            }
        }

        @Override
        public int draw() {
            if (ballCount == 0) {
                throw new NoSuchElementException();
            }
            int randomIndex = random.nextInt(ballCount);
            int color = balls[randomIndex];
            // decrease the number of balls
            ballCount--;
            // swap with last index
            balls[randomIndex] = balls[ballCount];
            balls[ballCount] = color;
            return color;
        }

        @Override
        public void reset() {
            ballCount = balls.length;
        }

        @Override
        public int count() {
            return ballCount;
        }

    }

    private static class BagNoArray implements Bag {

        private final int rCountInit;
        private final int gCountInit;
        private final int bCountInit;

        private final Random random;

        private int rCount;
        private int gCount;
        private int bCount;
        private int ballCount;

        public BagNoArray(int rCount, int gCount, int bCount) {
            random = new Random();
            rCountInit = rCount;
            gCountInit = gCount;
            bCountInit = bCount;
            reset();
        }

        @Override
        public void reset() {
            rCount = rCountInit;
            gCount = gCountInit;
            bCount = bCountInit;
            ballCount = rCount + gCount + bCount;
        }

        @Override
        public int draw() {
            if (ballCount == 0) {
                throw new NoSuchElementException();
            }
            int randomIndex = random.nextInt(ballCount);
            ballCount--;
            if (randomIndex < rCount) {
                rCount--;
                return RED;
            } else if (randomIndex < rCount + gCount) {
                gCount--;
                return GREEN;
            } else {
                bCount--;
                return BLUE;
            }
        }

        @Override
        public int count() {
            return ballCount;
        }
    }

    public static float probability3rdDrawMatches(Bag bag, int trials) {
        assert bag.count() >= 6;  // since we will be drawing 6 balls

        int matchCount = 0;
        for (int i = 0; i < trials; i++) {
            // draw 4 balls and throw away
            for (int j = 0; j < 4; j++) {
                bag.draw();
            }
            // compare next two draws
            int ball5 = bag.draw();
            int ball6 = bag.draw();
            if (ball5 == ball6) {
                matchCount++;
            }
            // reset bag to original numbers for the next trial
            bag.reset();
        }
        return ((float) matchCount) / trials;
    }

    public static float probability3rdDrawMatches(Bag bag) {
        return probability3rdDrawMatches(bag, 1000000);
    }

    public static float probability3rdDrawMatchesMath(int rCount, int gCount, int bCount) {
        // Math solution for verification of results
        //
        // P(Total) = n! / (r! * g! * b!) -> [1]  - Total # of permutations, n = r + b + g
        //
        // P(5th=6th) = P(5th=r & 6th=r) + P(5th=g & 6th=g) + P(5th=b & 6th=b) -> [2]  - # of permutations where 5th=6th
        //
        // P(5th=r & 6th=r) = (n-2)! / [(r-2)! * g! * b!] -> [3a]
        // P(5th=g & 6th=g) = (n-2)! / [r! * (g-2)! * b!] -> [3b]
        // P(5th=g & 6th=g) = (n-2)! / [r! * g! * (b-2)!] -> [3c]
        //
        // from [3a] + [3b] + [3c], and applying [2] =>
        //
        // P(5th=6th) = (n-2)! / [(r-2)! * g! * b!] + (n-2)! / [r! * (g-2)! * b!] + (n-2)! / [r! * g! * (b-2)!]
        //
        // taking [(n-2)! / (r! * b! * c!)] common =>
        //
        // P(5th=6th) = [(n-2)! / (r! * b! * c!)] * [ r! / (r-2)! + b! / (b-2)! + g! / (g-2)! ]
        // P(5th=6th) = [(n-2)! / (r! * b! * c!)] * [ r(r-1) + b(b-1) + g(g-1) ] -> [4]
        //
        // Probability = P(5th=6th) / P(Total)
        //             = [(n-2)! / n!] * [ r(r-1) + b(b-1) + g(g-1) ]
        //             = [ r(r-1) + b(b-1) + g(g-1) ] / [n(n-1)]

        int n = rCount + gCount + bCount;
        int numerator = rCount * (rCount - 1) + bCount * (bCount - 1) + gCount * (gCount - 1);
        int denominator = n * (n - 1);
        return ((float) numerator) / denominator;
    }

    public static void printResultsBagArray(int rCount, int gCount, int bCount) {
        Bag bag = new BagArray(rCount, gCount, bCount);

        long start = System.nanoTime();
        float prob = probability3rdDrawMatches(bag);
        long end = System.nanoTime();
        System.out.println();
        System.out.println("BagArray");
        System.out.println("Probability: " + prob);
        System.out.println("Time: " + ((end - start)/1000000.0) + " ms");
    }

    public static void printResultsBagNoArray(int rCount, int gCount, int bCount) {
        Bag bag = new BagNoArray(rCount, gCount, bCount);

        long start = System.nanoTime();
        float prob = probability3rdDrawMatches(bag);
        long end = System.nanoTime();
        System.out.println();
        System.out.println("BagNoArray");
        System.out.println("Probability: " + prob);
        System.out.println("Time: " + ((end - start)/1000000.0) + " ms");
    }

    public static void printResultsMath(int rCount, int gCount, int bCount) {

        long start = System.nanoTime();
        float prob = probability3rdDrawMatchesMath(rCount, gCount, bCount);
        long end = System.nanoTime();
        System.out.println();
        System.out.println("Math");
        System.out.println("Probability: " + prob);
        System.out.println("Time: " + ((end - start)/1000000.0) + " ms");
    }

    public static void printResults(int rCount, int gCount, int bCount) {
        printResultsBagArray(rCount, gCount, bCount);
        printResultsBagNoArray(rCount, gCount, bCount);
        printResultsMath(rCount, gCount, bCount);
    }

    public static void main(String[] args) {
        // printResults(5,5,5);

        int rCount = Integer.parseInt(args[0]);
        int gCount = Integer.parseInt(args[1]);
        int bCount = Integer.parseInt(args[2]);
        printResults(rCount, gCount, bCount);
    }
}
