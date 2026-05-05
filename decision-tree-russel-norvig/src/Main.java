package src;

import java.util.Arrays;
import java.util.List;

/**
 * Entry point — runs DTL and prints full interactive state trace.
 */
public class Main {

    private static final String RESET = "\u001B[0m";
    private static final String BOLD  = "\u001B[1m";
    private static final String GREEN = "\u001B[32m";
    private static final String RED   = "\u001B[31m";
    private static final String CYAN  = "\u001B[36m";

    public static void main(String[] args) {
        printBanner();

        // ── Load dataset ──────────────────────────────────────────────────
        List<Example> examples = Dataset.load();

        List<Attribute> attributes = Arrays.asList(
                Attribute.ALTERNATE,
                Attribute.BAR,
                Attribute.FRI_SAT,
                Attribute.HUNGRY,
                Attribute.PATRONS,
                Attribute.PRICE,
                Attribute.RAINING,
                Attribute.RESERVATION,
                Attribute.TYPE,
                Attribute.WAIT_EST
        );

        printDatasetSummary(examples);

        // ── Run DTL ───────────────────────────────────────────────────────
        System.out.println(BOLD + CYAN + "\n══ DTL EXECUTION TRACE ══════════════════════" + RESET);
        DTL dtl = new DTL();
        TreeNode tree = dtl.learn(examples, attributes, examples, 0);

        // ── Print final tree ──────────────────────────────────────────────
        System.out.println(BOLD + CYAN + "\n══ LEARNED DECISION TREE ════════════════════" + RESET);
        System.out.println(tree.display(""));

        // ── Verify: classify all training examples ─────────────────────────
        System.out.println(BOLD + CYAN + "\n══ TRAINING ACCURACY ════════════════════════" + RESET);
        int correct = 0;
        for (Example e : examples) {
            boolean predicted = tree.classify(e);
            boolean actual    = e.isWillWait();
            boolean ok        = predicted == actual;
            if (ok) correct++;
            String mark = ok ? GREEN + "✓" : RED + "✗";
            System.out.printf("  %sE%-2d  predicted=%-3s  actual=%-3s%s%n",
                    mark, e.getId(),
                    predicted ? "YES" : "NO",
                    actual    ? "YES" : "NO",
                    RESET);
        }
        System.out.println(BOLD + "\n  Accuracy: " + correct + "/" + examples.size() + RESET);
    }

    private static void printBanner() {
        System.out.println(BOLD + CYAN);
        System.out.println("╔══════════════════════════════════════════════════╗");
        System.out.println("║   Decision Tree Learning — Russell & Norvig      ║");
        System.out.println("║   Restaurant Waiting Problem (Fig 18.3 / 18.6)   ║");
        System.out.println("╚══════════════════════════════════════════════════╝");
        System.out.println(RESET);
    }

    private static void printDatasetSummary(List<Example> examples) {
        long pos = examples.stream().filter(Example::isWillWait).count();
        System.out.println(BOLD + "Dataset:" + RESET
                + "  " + examples.size() + " examples  "
                + GREEN + "YES=" + pos + RESET + "  "
                + RED   + "NO=" + (examples.size() - pos) + RESET);
    }
}
